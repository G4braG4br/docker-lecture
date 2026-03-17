from photition_api.serializers.notice.serializer import NoticeSerializer
from photition_models.models import Notice, PhotitionUser, Photo, PhotoStats
from photition_models.models.notice.notice_status_model import NoticeStatus


def get_initiator_action(request):
    initiator = request.data.get("initiator")
    if initiator is not None:
        return PhotitionUser.objects.get(pk=initiator)
    return None


def get_recipient_action(request):
    recipient = request.data.get("recipient")
    if recipient is not None:
        return PhotitionUser.objects.get(pk=recipient)
    return None


def get_photo_action(request):
    photo = request.data.get("photo")
    if photo is not None:
        return Photo.objects.get(pk=photo)
    return None


def create_notice_action(
    event=None,
    initiator=None,
    photo=None,
    recipient=None,
    message=None,
):
    numeric_data = None
    if photo is not None:
        if "VOTE" in event:
            numeric_data = PhotoStats.objects.get(photo_id=photo.id).vote_count
        elif "COMMENT" in event:
            numeric_data = PhotoStats.objects.get(photo_id=photo.id).comment_count
    notice = Notice.objects.create(
        event=event,
        initiator=initiator,
        photo=photo,
        recipient=recipient,
        message=message,
        numeric_data=numeric_data,
    )

    if recipient is None:
        users = PhotitionUser.objects.all()
        NoticeStatus.objects.bulk_create(
            [NoticeStatus(user=user, notice=notice) for user in users]
        )
    else:
        NoticeStatus.objects.create(user=recipient, notice=notice)
    return NoticeSerializer(notice).data
