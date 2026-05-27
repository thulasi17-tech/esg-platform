from django.db import models
from django.contrib.auth.models import User
from emissions.models import NormalizedEmissionRecord


class AuditLog(models.Model):

    record = models.ForeignKey(
        NormalizedEmissionRecord,
        on_delete=models.CASCADE
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    old_value = models.JSONField()

    new_value = models.JSONField()

    changed_at = models.DateTimeField(auto_now_add=True)