from django.db import models


class ResourceManager(models.Manager):
    def filter_by_linked_resource(self, linked_resource):
        from polymorphic_fks.models import OgcService, Layer, FeatureType, DatasetMetadata, ServiceMetadata, \
            LayerMetadata, \
            FeatureTypeMetadata
        if isinstance(linked_resource, OgcService):
            return self.filter(ogc_service_id=linked_resource.id)
        elif isinstance(linked_resource, Layer):
            return self.filter(layer_id=linked_resource.id)
        elif isinstance(linked_resource, FeatureType):
            return self.filter(feature_type_id=linked_resource.id)
        elif isinstance(linked_resource, DatasetMetadata):
            return self.filter(dataset_metadata_id=linked_resource.id)
        elif isinstance(linked_resource, ServiceMetadata):
            return self.filter(service_metadata_id=linked_resource.id)
        elif isinstance(linked_resource, LayerMetadata):
            return self.filter(layer_metadata_id=linked_resource.id)
        elif isinstance(linked_resource, FeatureTypeMetadata):
            return self.filter(feature_type_metadata_id=linked_resource.id)
        else:
            raise ValueError(f"Unhandled resource class: {linked_resource.__class__.__name__}")
