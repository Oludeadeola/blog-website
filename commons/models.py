import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class AbstractCommonModel(models.Model):

    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, unique=True, db_index=True, editable=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

