from uuid import uuid4

from django.db import models
from django.urls import reverse


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
