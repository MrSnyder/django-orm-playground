import random
from itertools import islice, chain

from django.core.management import BaseCommand

from polymorphic_fks.models import OgcService, Layer, FeatureType, DatasetMetadata, ServiceMetadata, LayerMetadata, \
    FeatureTypeMetadata
from polymorphic_fks.models.checkruns import CheckrunUsingStandardFk, CheckrunWithGenericFk, CheckrunWithMultipleFks


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
    def checkrun_using_standard_fk(services):
        passed = bool(random.getrandbits(1))
        resource = random.choice(services)
        return CheckrunUsingStandardFk(passed=passed, resource=resource)

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

    def handle(self, *args, **options):
        services = OgcService.objects.all()

        resources = list(chain(services, Layer.objects.all(), FeatureType.objects.all(), DatasetMetadata.objects.all(),
                          ServiceMetadata.objects.all(), LayerMetadata.objects.all(), FeatureTypeMetadata.objects.all()))


        # self.stdout.write(f'Generating {Command.COUNT} CheckrunUsingStandardFk instances')
        # checkruns = (self.checkrun_using_standard_fk(services) for i in range(1, Command.COUNT))
        # self.insert_batch(checkruns, CheckrunUsingStandardFk, 1000)
        #
        # self.stdout.write(f'Generating {Command.COUNT} CheckrunWithGenericFk instances')
        # checkruns = (self.checkrun_with_generic_fk(resources) for i in range(1, Command.COUNT))
        # self.insert_batch(checkruns, CheckrunWithGenericFk, 1000)

        self.stdout.write(f'Generating {Command.COUNT} CheckrunWithMultipleFks instances')
        checkruns = (self.checkrun_with_multiple_fks(resources) for i in range(1, Command.COUNT))
        self.insert_batch(checkruns, CheckrunWithMultipleFks, 1000)


        # self.stdout.write(self.style.SUCCESS('Successfully generated and inserted checkruns'))
