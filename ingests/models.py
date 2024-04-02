from django.db import models
from django.utils.translation import gettext_lazy as _

class Ingest(models.Model):
    class Status(models.TextChoices):
        UPLOADING = "uploading", _("Uploading")
        PROCESSING = "processing", _("Processing")
        COMPLETED = "completed", _("Completed")
        FAILED = "failed", _("Failed")

    name = models.CharField(max_length=256, unique=True)
    status = models.CharField(max_length=64, choices=Status, default=Status.UPLOADING)
    file = models.FileField(upload_to="uploads/")
    file_name = models.CharField(max_length=256, default="")
    process_time = models.FloatField(default=0)
    row_nums = models.BigIntegerField(default=0)
    processed_row_nums = models.BigIntegerField(default=0)

class Column(models.Model):
    ingest = models.ForeignKey(Ingest, on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    dtype = models.CharField(max_length=128)
    display_order = models.PositiveIntegerField(default=0)

class Record(models.Model):
    ingest = models.ForeignKey(Ingest, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)