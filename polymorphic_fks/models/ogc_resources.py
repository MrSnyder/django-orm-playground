from uuid import uuid4

from django.db import models


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


class Layer(models.Model):
    service = models.ForeignKey(to=OgcService,
                                on_delete=models.CASCADE,
                                verbose_name="parent service",
                                help_text="the OGC Service (WMS) this layer belongs to")
    name = models.TextField()

    def __str__(self):
        return self.name


class FeatureType(models.Model):
    service = models.ForeignKey(to=OgcService,
                                on_delete=models.CASCADE,
                                verbose_name="parent service",
                                help_text="the OGC Service (WFS) this feature type belongs to")
    name = models.TextField()

    def __str__(self):
        return self.name


class DatasetMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    layers = models.ManyToManyField(Layer)
    feature_types = models.ManyToManyField(FeatureType)

    def __str__(self):
        return self.file_identifier


class ServiceMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    service = models.OneToOneField(OgcService, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_identifier


class LayerMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    layer = models.OneToOneField(Layer, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_identifier


class FeatureTypeMetadata(models.Model):
    file_identifier = models.TextField(default=uuid4)
    feature_type = models.OneToOneField(FeatureType, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_identifier
