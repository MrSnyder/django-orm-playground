from django.db import models

from polymorphic_fks.models import OgcService


class CheckrunUsingStandardFk(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()
    resource = models.ForeignKey(to=OgcService,
                                 on_delete=models.CASCADE)
