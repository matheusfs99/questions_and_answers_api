import uuid
from django.db import models
from django.contrib.auth.models import User


class UUIDPrimaryKeyField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs["primary_key"] = True
        kwargs["editable"] = False
        kwargs["default"] = uuid.uuid4
        super().__init__(*args, **kwargs)


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    id = UUIDPrimaryKeyField()


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseModel(UUIDModel, TimestampedModel):
    class Meta:
        abstract = True

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
