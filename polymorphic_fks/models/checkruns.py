from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.urls import reverse
from polymorphic.models import PolymorphicModel

from polymorphic_fks.models import OgcService, Layer, FeatureType, DatasetMetadata, ServiceMetadata, LayerMetadata, \
    FeatureTypeMetadata


def getmodelattr(model, attr, default=None):
    try:
        return getattr(model, attr)
    except model.DoesNotExist:
        return default


class CheckrunWithGenericFk(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()
    _resource_type = models.ForeignKey(
        ContentType,
        db_column='resource_type_id',
        on_delete=models.CASCADE,
        limit_choices_to=Q(app_label='polymorphic_fks', model='ogcservice') |
                         Q(app_label='polymorphic_fks', model='layer') |
                         Q(app_label='polymorphic_fks', model='featuretype') |
                         Q(app_label='polymorphic_fks', model='datasetmetadata') |
                         Q(app_label='polymorphic_fks', model='servicemetadata') |
                         Q(app_label='polymorphic_fks', model='layermetadata') |
                         Q(app_label='polymorphic_fks', model='featuretypemetadata')
    )
    _resource_id = models.PositiveIntegerField(db_column='resource_id', )
    resource = GenericForeignKey('_resource_type', '_resource_id')

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def resource_type(self):
        if self._resource_type.model == 'ogcservice':
            return OgcService.__name__
        elif self._resource_type.model == 'layer':
            return Layer.__name__
        elif self._resource_type.model == 'featuretype':
            return FeatureType.__name__
        elif self._resource_type.model == 'datasetmetadata':
            return DatasetMetadata.__name__
        elif self._resource_type.model == 'servicemetadata':
            return ServiceMetadata.__name__
        elif self._resource_type.model == 'layermetadata':
            return LayerMetadata.__name__
        elif self._resource_type.model == 'featuretypemetadata':
            return FeatureTypeMetadata.__name__
        return None

    @property
    def resource_url(self):
        if self._resource_type.model == 'ogcservice':
            return reverse('polymorphic_fks:ogcservice-detail', kwargs={'pk': self._resource_id})
        elif self._resource_type.model == 'layer':
            return reverse('polymorphic_fks:layer-detail', kwargs={'pk': self._resource_id})
        elif self._resource_type.model == 'featuretype':
            return reverse('polymorphic_fks:featuretype-detail', kwargs={'pk': self._resource_id})
        elif self._resource_type.model == 'datasetmetadata':
            return reverse('polymorphic_fks:dataset-metadata-detail', kwargs={'pk': self._resource_id})
        elif self._resource_type.model == 'servicemetadata':
            return reverse('polymorphic_fks:service-metadata-detail', kwargs={'pk': self._resource_id})
        elif self._resource_type.model == 'layermetadata':
            return reverse('polymorphic_fks:layer-metadata-detail', kwargs={'pk': self._resource_id})
        elif self._resource_type.model == 'featuretypemetadata':
            return reverse('polymorphic_fks:featuretype-metadata-detail', kwargs={'pk': self._resource_id})
        return None


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
    def resource_id(self):
        if self.ogc_service_id:
            return self.ogc_service_id
        elif self.layer_id:
            return self.layer_id
        elif self.feature_type_id:
            return self.feature_type_id
        elif self.dataset_metadata_id:
            return self.dataset_metadata_id
        elif self.service_metadata_id:
            return self.service_metadata_id
        elif self.layer_metadata_id:
            return self.layer_metadata_id
        elif self.feature_type_metadata_id:
            return self.feature_type_metadata_id
        return None

    @property
    def resource_type(self):
        if self.ogc_service_id:
            return OgcService.__name__
        elif self.layer_id:
            return Layer.__name__
        elif self.feature_type_id:
            return FeatureType.__name__
        elif self.dataset_metadata_id:
            return DatasetMetadata.__name__
        elif self.service_metadata_id:
            return ServiceMetadata.__name__
        elif self.layer_metadata_id:
            return LayerMetadata.__name__
        elif self.feature_type_metadata_id:
            return FeatureTypeMetadata.__name__
        return None

    @property
    def resource_url(self):
        if self.ogc_service_id:
            return reverse('polymorphic_fks:ogcservice-detail', kwargs={'pk': self.ogc_service_id})
        elif self.layer_id:
            return reverse('polymorphic_fks:layer-detail', kwargs={'pk': self.layer_id})
        elif self.feature_type_id:
            return reverse('polymorphic_fks:featuretype-detail', kwargs={'pk': self.feature_type_id})
        elif self.dataset_metadata_id:
            return reverse('polymorphic_fks:dataset-metadata-detail', kwargs={'pk': self.dataset_metadata_id})
        elif self.service_metadata_id:
            return reverse('polymorphic_fks:service-metadata-detail', kwargs={'pk': self.service_metadata_id})
        elif self.layer_metadata_id:
            return reverse('polymorphic_fks:layer-metadata-detail', kwargs={'pk': self.layer_metadata_id})
        elif self.feature_type_metadata_id:
            return reverse('polymorphic_fks:featuretype-metadata-detail', kwargs={'pk': self.feature_type_metadata_id})
        return None


class MultiTableBaseCheckrun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()

    @property
    def resource_id_poly(self):
        return (getmodelattr(self, 'multitablecheckrunogcservice') \
                or getmodelattr(self, 'multitablecheckrunlayer') \
                or getmodelattr(self, 'multitablecheckrunfeaturetype') \
                or getmodelattr(self, 'multitablecheckrundatasetmetadata') \
                or getmodelattr(self, 'multitablecheckrunservicemetadata') \
                or getmodelattr(self, 'multitablecheckrunlayermetadata') \
                or getmodelattr(self, 'multitablecheckrunfeaturetypemetadata')).id

    @property
    def resource_type(self):
        if getmodelattr(self, 'multitablecheckrunogcservice'):
            return OgcService.__name__
        elif getmodelattr(self, 'multitablecheckrunlayer'):
            return Layer.__name__
        elif getmodelattr(self, 'multitablecheckrunfeaturetype'):
            return FeatureType.__name__
        elif getmodelattr(self, 'multitablecheckrundatasetmetadata'):
            return DatasetMetadata.__name__
        elif getmodelattr(self, 'multitablecheckrunservicemetadata'):
            return ServiceMetadata.__name__
        elif getmodelattr(self, 'multitablecheckrunlayermetadata'):
            return LayerMetadata.__name__
        elif getmodelattr(self, 'multitablecheckrunfeaturetypemetadata'):
            return FeatureTypeMetadata.__name__
        return None

    @property
    def resource_url(self):
        if getmodelattr(self, 'multitablecheckrunogcservice'):
            return reverse('polymorphic_fks:ogcservice-detail', kwargs={'pk': self.multitablecheckrunogcservice.id})
        elif getmodelattr(self, 'multitablecheckrunlayer'):
            return reverse('polymorphic_fks:layer-detail', kwargs={'pk': self.layer.multitablecheckrunlayer.id})
        elif getmodelattr(self, 'multitablecheckrunfeaturetype'):
            return reverse('polymorphic_fks:featuretype-detail', kwargs={'pk': self.multitablecheckrunfeaturetype.id})
        elif getmodelattr(self, 'multitablecheckrundatasetmetadata'):
            return reverse('polymorphic_fks:dataset-metadata-detail',
                           kwargs={'pk': self.multitablecheckrundatasetmetadata.id})
        elif getmodelattr(self, 'multitablecheckrunservicemetadata'):
            return reverse('polymorphic_fks:service-metadata-detail',
                           kwargs={'pk': self.multitablecheckrunservicemetadata.id})
        elif getmodelattr(self, 'multitablecheckrunlayermetadata'):
            return reverse('polymorphic_fks:layer-metadata-detail',
                           kwargs={'pk': self.multitablecheckrunlayermetadata.id})
        elif getmodelattr(self, 'multitablecheckrunfeaturetypemetadata'):
            return reverse('polymorphic_fks:featuretype-metadata-detail',
                           kwargs={'pk': self.multitablecheckrunfeaturetypemetadata.id})
        return None


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

    @property
    def resource_type(self):
        return OgcService.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:ogcservice-detail', kwargs={'pk': self.resource.id})


class DjangoPolymorphicCheckrunLayer(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=Layer, on_delete=models.CASCADE)

    @property
    def resource_type(self):
        return Layer.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:layer-detail', kwargs={'pk': self.resource.id})


class DjangoPolymorphicCheckrunFeatureType(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=FeatureType, on_delete=models.CASCADE)

    @property
    def resource_type(self):
        return FeatureType.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:featuretype-detail', kwargs={'pk': self.resource.id})


class DjangoPolymorphicCheckrunDatasetMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=DatasetMetadata, on_delete=models.CASCADE)

    @property
    def resource_type(self):
        return DatasetMetadata.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:dataset-metadata-detail', kwargs={'pk': self.resource.id})


class DjangoPolymorphicCheckrunServiceMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=ServiceMetadata, on_delete=models.CASCADE)

    @property
    def resource_type(self):
        return ServiceMetadata.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:service-metadata-detail', kwargs={'pk': self.resource.id})


class DjangoPolymorphicCheckrunLayerMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=LayerMetadata, on_delete=models.CASCADE)

    @property
    def resource_type(self):
        return LayerMetadata.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:layer-metadata-detail', kwargs={'pk': self.resource.id})


class DjangoPolymorphicCheckrunFeatureTypeMetadata(DjangoPolymorphicBaseCheckrun):
    resource = models.ForeignKey(to=FeatureTypeMetadata, on_delete=models.CASCADE)

    @property
    def resource_type(self):
        return FeatureTypeMetadata.__name__

    @property
    def resource_url(self):
        return reverse('polymorphic_fks:featuretype-metadata-detail', kwargs={'pk': self.resource.id})
