from django.contrib import admin

# Register your models here.
from polymorphic_fks.models import Layer, FeatureType, DatasetMetadata, ServiceMetadata, LayerMetadata, \
    FeatureTypeMetadata, OgcService
from polymorphic_fks.models.checkruns import CheckrunWithGenericFk

admin.site.register(OgcService)
admin.site.register(Layer)
admin.site.register(FeatureType)
admin.site.register(DatasetMetadata)
admin.site.register(ServiceMetadata)
admin.site.register(LayerMetadata)
admin.site.register(FeatureTypeMetadata)

admin.site.register(CheckrunWithGenericFk)
