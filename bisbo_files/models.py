from django.db import models
from accounts.models import User
from model_utils.models import TimeStampedModel


class BisboFiles(TimeStampedModel):
    PNG = "png"
    JPG = "jpg"

    file_types = [
        (PNG, "png"),
        (JPG, "jpg")
    ]
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=100, choices=file_types, default="png")
    file_tag = models.CharField(max_length=1000, db_index=True)
    upload_file = models.FileField(max_length=500, null=True)
    upload_video = models.FileField(max_length=500, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="files_created_by")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="files_modified_by")

    class Meta:
        db_table = "bisbo_files"

    def __str__(self):
        return self.file_name
