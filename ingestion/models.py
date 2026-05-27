from django.db import models
from companies.models import Company
from django.contrib.auth.models import User


class DataSource(models.Model):

    SOURCE_TYPES = (
        ('SAP', 'SAP'),
        ('UTILITY', 'UTILITY'),
        ('TRAVEL', 'TRAVEL'),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPES
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    original_file = models.FileField(
        upload_to='uploads/'
    )

    def __str__(self):
        return f"{self.company.name} - {self.source_type}"


class RawRecord(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('FAILED', 'FAILED'),
        ('PROCESSED', 'PROCESSED'),
    )

    data_source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    raw_json = models.JSONField()

    ingestion_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)