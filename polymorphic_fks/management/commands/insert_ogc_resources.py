import random
from itertools import islice
from uuid import uuid4

from django.core.management import BaseCommand

from polymorphic_fks.models.ogc_resources import OgcService, Layer, FeatureType, ServiceMetadata, LayerMetadata, \
    FeatureTypeMetadata, DatasetMetadata, Resource


class Command(BaseCommand):
    help = 'Adds test data (OGC resources)'

    WMS_COUNT = 10000
    WFS_COUNT = 10000
    CSW_COUNT = 10000

    LAYER_COUNT = 100000
    FEATURE_TYPE_COUNT = 100000
    DATASET_COUNT = 20000

    def insert_batch(self, resources, resource_cls, batch_size):
        inserted_resources = []
        while True:
            batch = list(islice(resources, batch_size))
            if not batch:
                break
            inserted_resources.extend(resource_cls.objects.bulk_create(batch, batch_size))
        return inserted_resources

    @staticmethod
    def random_ogc_service(service_type):
        attribute = random.choice(('marvelous', 'beautiful', 'wonderful', 'incredible',))
        return OgcService(service_type=service_type,
                          origin_url=f'http://www.some-gdi.com/services/{uuid4()}',
                          name=f'Another {attribute} {service_type}')

    @staticmethod
    def random_layer(wms_resources):
        attribute = random.choice(('nice', 'useful', 'reasonable', 'yellow',))
        service = random.choice(wms_resources)
        return Layer(service=service,
                     name=f'Another {attribute} WMS layer')

    @staticmethod
    def random_feature_type(wfs_resources):
        attribute = random.choice(('nice', 'useful', 'reasonable', 'cool',))
        service = random.choice(wfs_resources)
        return FeatureType(service=service,
                           name=f'Another {attribute} WFS feature type')

    @staticmethod
    def random_dataset(layers, feature_types):
        # linked_layers = []
        # linked_feature_types = []
        # for i in range(1, random.randint(1, 10)):
        #     linked_layers.append(random.choice(layers))
        # for i in range(1, random.randint(1, 10)):
        #     linked_feature_types.append(random.choice(feature_types))
        return DatasetMetadata()

    def insert_base_resources(self, resources, resource_cls):
        if resource_cls == OgcService:
            base_resources = (Resource(ogc_service=resource) for resource in resources)
        if resource_cls == Layer:
            base_resources = (Resource(layer=resource) for resource in resources)
        if resource_cls == FeatureType:
            base_resources = (Resource(feature_type=resource) for resource in resources)
        if resource_cls == DatasetMetadata:
            base_resources = (Resource(dataset_metadata=resource) for resource in resources)
        if resource_cls == ServiceMetadata:
            base_resources = (Resource(service_metadata=resource) for resource in resources)
        if resource_cls == LayerMetadata:
            base_resources = (Resource(layer_metadata=resource) for resource in resources)
        if resource_cls == FeatureTypeMetadata:
            base_resources = (Resource(feature_type_metadata=resource) for resource in resources)
        self.insert_batch(base_resources, Resource, 1000)

    def handle(self, *args, **options):

        # Services
        self.stdout.write(f'Generating {Command.WMS_COUNT} WMS resources')
        wms_resources = (Command.random_ogc_service(OgcService.OgcServiceType.WMS) for i in range(0, Command.WMS_COUNT))
        wms_resources = self.insert_batch(wms_resources, OgcService, 1000)
        self.insert_base_resources(wms_resources, OgcService)
        self.stdout.write(f'Generating {Command.WFS_COUNT} WFS resources')
        wfs_resources = (Command.random_ogc_service(OgcService.OgcServiceType.WFS) for i in range(0, Command.WFS_COUNT))
        wfs_resources = self.insert_batch(wfs_resources, OgcService, 1000)
        self.insert_base_resources(wfs_resources, OgcService)
        self.stdout.write(f'Generating {Command.WFS_COUNT} CSW resources')
        csw_resources = (Command.random_ogc_service(OgcService.OgcServiceType.CSW) for i in range(0, Command.CSW_COUNT))
        csw_resources = self.insert_batch(csw_resources, OgcService, 1000)
        self.insert_base_resources(csw_resources, OgcService)
        service_metadata = (ServiceMetadata(service=ogc_service) for ogc_service in
                            (wms_resources + wfs_resources + csw_resources))
        service_metadata = self.insert_batch(service_metadata, ServiceMetadata, 1000)
        self.insert_base_resources(service_metadata, ServiceMetadata)

        # Layers
        self.stdout.write(f'Generating {Command.LAYER_COUNT} layer resources')
        layers = (Command.random_layer(wms_resources) for i in range(0, Command.LAYER_COUNT))
        layers = self.insert_batch(layers, Layer, 1000)
        self.insert_base_resources(layers, Layer)
        layer_metadata = (LayerMetadata(layer=layer) for layer in layers)
        layer_metadata = self.insert_batch(layer_metadata, LayerMetadata, 1000)
        self.insert_base_resources(layer_metadata, LayerMetadata)

        # FeatureType
        self.stdout.write(f'Generating {Command.FEATURE_TYPE_COUNT} feature type resources')
        feature_types = (Command.random_feature_type(wfs_resources) for i in range(0, Command.FEATURE_TYPE_COUNT))
        feature_types = self.insert_batch(feature_types, FeatureType, 1000)
        self.insert_base_resources(feature_types, FeatureType)
        feature_type_metadata = (FeatureTypeMetadata(feature_type=feature_type) for feature_type in feature_types)
        feature_type_metadata = self.insert_batch(feature_type_metadata, FeatureTypeMetadata, 1000)
        self.insert_base_resources(feature_type_metadata, FeatureTypeMetadata)

        # Datasets
        self.stdout.write(f'Generating {Command.DATASET_COUNT} dataset metadata records')
        dataset_metadata = (Command.random_dataset(layers, feature_types) for i in range(0, Command.DATASET_COUNT))
        dataset_metadata = self.insert_batch(dataset_metadata, DatasetMetadata, 1000)
        self.insert_base_resources(dataset_metadata, DatasetMetadata)

        self.stdout.write(f'Linking dataset metadata records to layers / feature types', ending='')
        counter = 1
        for record in dataset_metadata:
            linked_layers = []
            linked_feature_types = []
            for i in range(1, random.randint(1, 5)):
                linked_layers.append(random.choice(layers))
            for i in range(1, random.randint(1, 5)):
                linked_feature_types.append(random.choice(feature_types))
            record.layers.set(linked_layers)
            record.feature_types.set(linked_feature_types)
            if counter % 1000 == 0:
                self.stdout.write(f'...{counter}', ending='')
            counter = counter + 1
        self.stdout.write()

        self.stdout.write(self.style.SUCCESS('Successfully generated and inserted OGC resources'))
