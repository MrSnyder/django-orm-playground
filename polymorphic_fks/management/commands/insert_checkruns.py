import random
from itertools import islice, chain

from django.core.management import BaseCommand

from polymorphic_fks.models import OgcService, Layer, FeatureType, DatasetMetadata, ServiceMetadata, LayerMetadata, \
    FeatureTypeMetadata
from polymorphic_fks.models.checkruns import CheckrunWithGenericFk, CheckrunWithMultipleFks, \
    MultiTableCheckrunOgcService, MultiTableCheckrunLayer, MultiTableCheckrunFeatureType, \
    MultiTableCheckrunDatasetMetadata, MultiTableCheckrunServiceMetadata, MultiTableCheckrunLayerMetadata, \
    MultiTableCheckrunFeatureTypeMetadata, DjangoPolymorphicCheckrunOgcService, DjangoPolymorphicCheckrunLayer, \
    DjangoPolymorphicCheckrunFeatureType, DjangoPolymorphicCheckrunDatasetMetadata, \
    DjangoPolymorphicCheckrunServiceMetadata, DjangoPolymorphicCheckrunLayerMetadata, \
    DjangoPolymorphicCheckrunFeatureTypeMetadata


class Command(BaseCommand):
    COUNT = 100000
    help = 'Adds test data (checkruns for existing OGC resources)'

    def insert_batch(self, resources, resource_cls, batch_size):
        inserted_resources = []
        while True:
            batch = list(islice(resources, batch_size))
            if not batch:
                break
            inserted_resources.extend(resource_cls.objects.bulk_create(batch, batch_size))
        return inserted_resources

    @staticmethod
    def checkrun_with_generic_fk(resources):
        passed = bool(random.getrandbits(1))
        resource = random.choice(resources)
        return CheckrunWithGenericFk(passed=passed, resource=resource)

    @staticmethod
    def checkrun_with_multiple_fks(resources):
        passed = bool(random.getrandbits(1))
        resource = random.choice(resources)
        run = CheckrunWithMultipleFks(passed=passed)
        run.set_resource(resource)
        return run

    @staticmethod
    def checkrun_multi_table(resources):
        passed = bool(random.getrandbits(1))
        resource = random.choice(resources)
        if isinstance(resource, OgcService):
            return MultiTableCheckrunOgcService(passed=passed, resource=resource)
        elif isinstance(resource, Layer):
            return MultiTableCheckrunLayer(passed=passed, resource=resource)
        elif isinstance(resource, FeatureType):
            return MultiTableCheckrunFeatureType(passed=passed, resource=resource)
        elif isinstance(resource, DatasetMetadata):
            return MultiTableCheckrunDatasetMetadata(passed=passed, resource=resource)
        elif isinstance(resource, ServiceMetadata):
            return MultiTableCheckrunServiceMetadata(passed=passed, resource=resource)
        elif isinstance(resource, LayerMetadata):
            return MultiTableCheckrunLayerMetadata(passed=passed, resource=resource)
        elif isinstance(resource, FeatureTypeMetadata):
            return MultiTableCheckrunFeatureTypeMetadata(passed=passed, resource=resource)
        else:
            raise ValueError(f"Unhandled resource class: {resource.__class__.__name__}")

    @staticmethod
    def checkrun_django_polymorphic(resources):
        passed = bool(random.getrandbits(1))
        resource = random.choice(resources)
        if isinstance(resource, OgcService):
            return DjangoPolymorphicCheckrunOgcService(passed=passed, resource=resource)
        elif isinstance(resource, Layer):
            return DjangoPolymorphicCheckrunLayer(passed=passed, resource=resource)
        elif isinstance(resource, FeatureType):
            return DjangoPolymorphicCheckrunFeatureType(passed=passed, resource=resource)
        elif isinstance(resource, DatasetMetadata):
            return DjangoPolymorphicCheckrunDatasetMetadata(passed=passed, resource=resource)
        elif isinstance(resource, ServiceMetadata):
            return DjangoPolymorphicCheckrunServiceMetadata(passed=passed, resource=resource)
        elif isinstance(resource, LayerMetadata):
            return DjangoPolymorphicCheckrunLayerMetadata(passed=passed, resource=resource)
        elif isinstance(resource, FeatureTypeMetadata):
            return DjangoPolymorphicCheckrunFeatureTypeMetadata(passed=passed, resource=resource)
        else:
            raise ValueError(f"Unhandled resource class: {resource.__class__.__name__}")

    def handle(self, *args, **options):
        services = OgcService.objects.all()

        resources = list(chain(services, Layer.objects.all(), FeatureType.objects.all(), DatasetMetadata.objects.all(),
                               ServiceMetadata.objects.all(), LayerMetadata.objects.all(),
                               FeatureTypeMetadata.objects.all()))

        self.stdout.write(f'Generating {Command.COUNT} CheckrunWithGenericFk instances')
        checkruns = (self.checkrun_with_generic_fk(resources) for i in range(0, Command.COUNT))
        self.insert_batch(checkruns, CheckrunWithGenericFk, 1000)

        self.stdout.write(f'Generating {Command.COUNT} CheckrunWithMultipleFks instances')
        checkruns = (self.checkrun_with_multiple_fks(resources) for i in range(0, Command.COUNT))
        self.insert_batch(checkruns, CheckrunWithMultipleFks, 1000)

        self.stdout.write(f'Generating {Command.COUNT} MultiTableCheckrun instances')
        checkruns = [self.checkrun_multi_table(resources) for i in range(0, Command.COUNT)]
        filtered_checkruns = (run for run in checkruns)
        # self.stdout.write(f'Inserting {Command.COUNT} MultiTableBaseCheckrun instances')
        # self.insert_batch(filtered_checkruns, MultiTableBaseCheckrun, 1000)
        for cls in [MultiTableCheckrunOgcService, MultiTableCheckrunLayer,
                    MultiTableCheckrunFeatureType,
                    MultiTableCheckrunDatasetMetadata, MultiTableCheckrunServiceMetadata,
                    MultiTableCheckrunLayerMetadata,
                    MultiTableCheckrunFeatureTypeMetadata]:
            filtered_checkruns = [run for run in checkruns if isinstance(run, cls)]
            self.stdout.write(f'Inserting {len(filtered_checkruns)} {cls.__name__} instances')
            count = 1
            for run in filtered_checkruns:
                run.save()
                if count % 1000 == 0:
                    self.stdout.write(f'...{count}')
                count = count + 1

        self.stdout.write(f'Generating {Command.COUNT} DjangoPolymorphicCheckrun instances')
        checkruns = [self.checkrun_django_polymorphic(resources) for i in range(0, Command.COUNT)]
        for cls in [DjangoPolymorphicCheckrunOgcService, DjangoPolymorphicCheckrunLayer,
                    DjangoPolymorphicCheckrunFeatureType,
                    DjangoPolymorphicCheckrunDatasetMetadata, DjangoPolymorphicCheckrunServiceMetadata,
                    DjangoPolymorphicCheckrunLayerMetadata,
                    DjangoPolymorphicCheckrunFeatureTypeMetadata]:
            filtered_checkruns = [run for run in checkruns if isinstance(run, cls)]
            self.stdout.write(f'Inserting {len(filtered_checkruns)} {cls.__name__} instances')
            count = 1
            for run in filtered_checkruns:
                run.save()
                if count % 1000 == 0:
                    self.stdout.write(f'...{count}')
                count = count + 1

        self.stdout.write(self.style.SUCCESS('Successfully generated and inserted checkruns'))
