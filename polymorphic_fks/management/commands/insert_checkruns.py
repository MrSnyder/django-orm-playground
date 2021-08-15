import random
from itertools import islice

from django.core.management import BaseCommand

from polymorphic_fks.models import OgcService
from polymorphic_fks.models.checkruns import CheckrunUsingStandardFk


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

    def handle(self, *args, **options):
        services = OgcService.objects.all()

        self.stdout.write(f'Generating {Command.COUNT} CheckrunUsingStandardFk instances')
        checkruns = (self.checkrun_using_standard_fk(services) for i in range(1, Command.COUNT))
        self.insert_batch(checkruns, CheckrunUsingStandardFk, 1000)
        self.stdout.write(self.style.SUCCESS('Successfully generated and inserted checkruns'))
