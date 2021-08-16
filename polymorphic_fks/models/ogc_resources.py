from uuid import uuid4

from django.db import models
from django.urls import reverse

from polymorphic_fks.managers import ResourceManager


class OgcService(models.Model):
    class OgcServiceType(models.TextChoices):
        WMS = 'WMS',
        WFS = 'WFS',
        CSW = 'CSW'

    service_type = models.CharField(
        max_length=3,
        choices=OgcServiceType.choices
    )
    origin_url = models.URLField(max_length=4096)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('polymorphic_fks:ogcservice-detail', kwargs={'pk': self.pk})


class Layer(models.Model):
    service = models.ForeignKey(to=OgcService,
                                on_delete=models.CASCADE,
                                verbose_name="parent service",
                                help_text="the OGC Service (WMS) this layer belongs to")
    name = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('polymorphic_fks:layer-detail', kwargs={'pk': self.pk})


class FeatureType(models.Model):
    service = models.ForeignKey(to=OgcService,
                                on_delete=models.CASCADE,
                                verbose_name="parent service",
                                help_text="the OGC Service (WFS) this feature type belongs to")
    name = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('polymorphic_fks:featuretype-detail', kwargs={'pk': self.pk})


class DatasetMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    layers = models.ManyToManyField(Layer)
    feature_types = models.ManyToManyField(FeatureType)

    def __str__(self):
        return self.file_identifier

    def get_absolute_url(self):
        return reverse('polymorphic_fks:dataset-metadata-detail', kwargs={'pk': self.pk})


class ServiceMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    service = models.OneToOneField(OgcService, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_identifier

    def get_absolute_url(self):
        return reverse('polymorphic_fks:service-metadata-detail', kwargs={'pk': self.pk})


class LayerMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    layer = models.OneToOneField(Layer, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_identifier

    def get_absolute_url(self):
        return reverse('polymorphic_fks:layer-metadata-detail', kwargs={'pk': self.pk})


class FeatureTypeMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    feature_type = models.OneToOneField(FeatureType, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_identifier

    def get_absolute_url(self):
        return reverse('polymorphic_fks:featuretype-metadata-detail', kwargs={'pk': self.pk})


class Resource(models.Model):
    ogc_service = models.ForeignKey(to=OgcService, on_delete=models.CASCADE, null=True)
    layer = models.ForeignKey(to=Layer, on_delete=models.CASCADE, null=True)
    feature_type = models.ForeignKey(to=FeatureType, on_delete=models.CASCADE, null=True)
    dataset_metadata = models.ForeignKey(to=DatasetMetadata, on_delete=models.CASCADE, null=True)
    service_metadata = models.ForeignKey(to=ServiceMetadata, on_delete=models.CASCADE, null=True)
    layer_metadata = models.ForeignKey(to=LayerMetadata, on_delete=models.CASCADE, null=True)
    feature_type_metadata = models.ForeignKey(to=FeatureTypeMetadata, on_delete=models.CASCADE, null=True)
    objects = ResourceManager()

    @property
    def linked_resource_id(self):
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
    def linked_resource_url(self):
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

    @property
    def linked_resource_type(self):
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
    def linked_resource_name(self):
        if self.ogc_service_id:
            return self.ogc_service.name
        elif self.layer_id:
            return self.layer.name
        elif self.feature_type_id:
            return self.feature_type.name
        elif self.dataset_metadata_id:
            return 'Unnamed resource'
        elif self.service_metadata_id:
            return 'Unnamed resource'
        elif self.layer_metadata_id:
            return 'Unnamed resource'
        elif self.feature_type_metadata_id:
            return 'Unnamed resource'
        return None
