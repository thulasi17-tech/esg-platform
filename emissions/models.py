from django.db import models
from companies.models import Company
from ingestion.models import DataSource


class NormalizedEmissionRecord(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('FLAGGED', 'FLAGGED'),
        ('APPROVED', 'APPROVED'),
        ('LOCKED', 'LOCKED'),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    data_source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    scope = models.CharField(max_length=20)

    category = models.CharField(max_length=100)

    activity_date = models.DateField()

    normalized_value = models.FloatField()

    normalized_unit = models.CharField(max_length=50)

    emission_factor = models.FloatField()

    co2e = models.FloatField()

    STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('FLAGGED', 'Flagged'),
]

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='PENDING'
    )

    is_flagged = models.BooleanField(default=False)

    flag_reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)