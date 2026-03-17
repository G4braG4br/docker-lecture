from typing import List, Self

from django.core.paginator import EmptyPage, Page, Paginator
from django.db.models import Exists, F, OuterRef, Q
from django.forms import CharField, IntegerField
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition.settings.restframework import REST_FRAMEWORK
from photition_models.models.photo.photo_model import Photo
from photition_models.models.photo.vote_model import Vote
from photition_models.models.user.photition_user_model import PhotitionUser


class PhotoListService(ServiceWithResult):
    search = CharField(required=False)
    order = CharField(required=False)
    page = IntegerField(required=False)
    per_page = IntegerField(required=False)
    user = ModelField(PhotitionUser, required=False)
    user_id = IntegerField(required=False)
    moderation_sort = CharField(required=False)

    def process(self) -> Self:
        if self.is_valid():
            self.result = self._paginated_addresses
        return self

    def get_photos(self) -> List[Photo]:
        queryset = Photo.objects.all().order_by("-id")

        if self._user_id is not None:
            if self.cleaned_data.get("moderation_sort") != "":
                queryset = queryset.filter(
                    state=self.cleaned_data.get("moderation_sort"),
                    author_id=self._user_id,
                    is_deleted=False,
                )
            else:
                queryset = queryset.filter(author_id=self._user_id, is_deleted=False)
        elif not self.is_staff():
            queryset = queryset.filter(is_deleted=False, is_allowed=True)
        else:
            if self.cleaned_data.get("moderation_sort") != "":
                queryset = queryset.filter(
                    state=self.cleaned_data.get("moderation_sort")
                )

        if self._search != "":
            queryset = queryset.filter(
                Q(title__icontains=self._search)
                | Q(description__icontains=self._search)
                | Q(author__username__icontains=self._search)
            )

        vote_sub_query = Vote.objects.filter(user=self._user, photo=OuterRef("pk"))

        queryset = (
            queryset.select_related("stat")
            .annotate(is_voted=Exists(vote_sub_query))
            .annotate(comment_count=F("stat__comment_count"))
            .annotate(vote_count=F("stat__vote_count"))
        )

        if self._order != "":
            queryset = queryset.order_by("-" + self._order)

        return queryset

    @property
    def _search(self) -> CharField | None:
        return self.cleaned_data.get("search")

    @property
    def _order(self) -> CharField | None:
        return self.cleaned_data.get("order")

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data.get("user")

    @property
    def _user_id(self) -> PhotitionUser:
        return self.cleaned_data.get("user_id")

    @property
    def _paginated_addresses(self) -> Page:
        try:
            return Paginator(
                Photo.objects.all().order_by("-id"),
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data["page"] or 1)
        except EmptyPage:
            return Paginator(
                None,
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)

    def is_staff(self) -> bool:
        if self._user is not None:
            return self._user.is_staff
        return False
