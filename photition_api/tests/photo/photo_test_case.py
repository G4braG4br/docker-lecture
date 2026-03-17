from django.db import connection
from rest_framework.test import APITestCase


class PhotoAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._create_photostats_view()

    @classmethod
    def _create_photostats_view(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DROP MATERIALIZED VIEW IF EXISTS photition_models_photostats CASCADE;
                """
            )

            cursor.execute(
                """
                    CREATE MATERIALIZED VIEW photition_models_photostats AS
                    SELECT
                        photo.id as photo_id,
                        COALESCE(COUNT(DISTINCT vote.id), 0) as vote_count,
                        COALESCE(COUNT(DISTINCT CASE WHEN comment.is_deleted = FALSE THEN comment.id END), 0) as
                        comment_count
                    FROM photition_models_photo AS photo
                    LEFT JOIN photition_models_vote AS vote ON photo.id = vote.photo_id
                    LEFT JOIN photition_models_comment AS comment ON photo.id = comment.photo_id
                    GROUP BY photo.id;
                """
            )
            cursor.execute(
                """CREATE UNIQUE INDEX photition_models_photostats_pkey ON photition_models_photostats (photo_id);"""
            )
