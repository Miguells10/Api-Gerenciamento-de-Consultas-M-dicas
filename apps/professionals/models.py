"""
Professional model — represents a health professional entity.
UUID primary key prevents enumeration attacks.
"""

import uuid

from django.db import models

from apps.core.models import TimestampedModel


class Professional(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=50)

    class Meta:
        ordering = ["social_name"]
        verbose_name = "Professional"
        verbose_name_plural = "Professionals"

    def __str__(self) -> str:
        return f"{self.social_name} — {self.profession}"
