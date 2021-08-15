from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from polymorphic_fks.models import OgcService


class CheckrunUsingStandardFk(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()
    resource = models.ForeignKey(to=OgcService,
                                 on_delete=models.CASCADE)


class CheckrunWithGenericFk(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()
    resource_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(app_label='polymorphic_fks', model='ogcservice') |
                         Q(app_label='polymorphic_fks', model='layer') |
                         Q(app_label='polymorphic_fks', model='featuretype') |
                         Q(app_label='polymorphic_fks', model='datasetmetadata') |
                         Q(app_label='polymorphic_fks', model='servicemetadata') |
                         Q(app_label='polymorphic_fks', model='layermetadata') |
                         Q(app_label='polymorphic_fks', model='featuretypemetadata')
    )
    resource_id = models.PositiveIntegerField()
    resource = GenericForeignKey('resource_type', 'resource_id')
