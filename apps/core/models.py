"""
Abstract base model that adds audit timestamp fields to any model.
Following DRY: avoids repeating created_at/updated_at across every model.
"""

from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
