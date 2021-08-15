from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from polymorphic.models import PolymorphicModel

from polymorphic_fks.models import OgcService, Layer, FeatureType, DatasetMetadata, ServiceMetadata, LayerMetadata, \
    FeatureTypeMetadata


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


class CheckrunWithMultipleFks(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()
    ogc_service = models.ForeignKey(to=OgcService, on_delete=models.CASCADE, null=True)
    layer = models.ForeignKey(to=Layer, on_delete=models.CASCADE, null=True)
    feature_type = models.ForeignKey(to=FeatureType, on_delete=models.CASCADE, null=True)
    dataset_metadata = models.ForeignKey(to=DatasetMetadata, on_delete=models.CASCADE, null=True)
    service_metadata = models.ForeignKey(to=ServiceMetadata, on_delete=models.CASCADE, null=True)
    layer_metadata = models.ForeignKey(to=LayerMetadata, on_delete=models.CASCADE, null=True)
    feature_type_metadata = models.ForeignKey(to=FeatureTypeMetadata, on_delete=models.CASCADE, null=True)

    def set_resource(self, resource):
        if isinstance(resource, OgcService):
            self.ogc_service = resource
        elif isinstance(resource, Layer):
            self.layer = resource
        elif isinstance(resource, FeatureType):
            self.feature_type = resource
        elif isinstance(resource, DatasetMetadata):
            self.dataset_metadata = resource
        elif isinstance(resource, ServiceMetadata):
            self.service_metadata = resource
        elif isinstance(resource, LayerMetadata):
            self.layer_metadata = resource
        elif isinstance(resource, FeatureTypeMetadata):
            self.feature_type_metadata = resource
        else:
            raise ValueError(f"Unhandled resource class: {resource.__class__.__name__}")

    @property
    def resource_type(self):
        if self.ogc_service_id:
            return OgcService
        elif self.layer_id:
            return Layer
        elif self.feature_type_id:
            return FeatureType
        elif self.dataset_metadata_id:
            return DatasetMetadata
        elif self.service_metadata_id:
            return ServiceMetadata
        elif self.layer_metadata_id:
            return LayerMetadata
        elif self.feature_type_metadata_id:
            return FeatureTypeMetadata
        return None


class MultiTableBaseCheckrun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()


class MultiTableCheckrunOgcService(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=OgcService, on_delete=models.CASCADE)


class MultiTableCheckrunLayer(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=Layer, on_delete=models.CASCADE)


class MultiTableCheckrunFeatureType(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=FeatureType, on_delete=models.CASCADE)


class MultiTableCheckrunDatasetMetadata(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=DatasetMetadata, on_delete=models.CASCADE)


class MultiTableCheckrunServiceMetadata(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=ServiceMetadata, on_delete=models.CASCADE)


class MultiTableCheckrunLayerMetadata(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=LayerMetadata, on_delete=models.CASCADE)


class MultiTableCheckrunFeatureTypeMetadata(MultiTableBaseCheckrun):
    resource = models.ForeignKey(to=FeatureTypeMetadata, on_delete=models.CASCADE)


class DjangoPolymorphicBaseCheckrun(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()


class DjangoPolymorphicCheckrunOgcService(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=OgcService, on_delete=models.CASCADE)


class DjangoPolymorphicCheckrunLayer(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=Layer, on_delete=models.CASCADE)


class DjangoPolymorphicCheckrunFeatureType(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=FeatureType, on_delete=models.CASCADE)


class DjangoPolymorphicCheckrunDatasetMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=DatasetMetadata, on_delete=models.CASCADE)


class DjangoPolymorphicCheckrunServiceMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=ServiceMetadata, on_delete=models.CASCADE)


class DjangoPolymorphicCheckrunLayerMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=LayerMetadata, on_delete=models.CASCADE)


class DjangoPolymorphicCheckrunFeatureTypeMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=FeatureTypeMetadata, on_delete=models.CASCADE)
