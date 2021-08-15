from itertools import islice

from django.core.management import BaseCommand

from polymorphic_fks.models import Apple, Banana, Grapes, Kiwifruit, Lemon, Pineapple, Watermelon


class Command(BaseCommand):
    help = 'Adds test data (fruits)'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def insert_batch(self, cls, objs, batch_size):
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            cls.objects.bulk_create(batch, batch_size)

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(f'Generating {count} fruits (for each type)')
        apples = (Apple.random() for i in range(0, count))
        bananas = (Banana.random() for i in range(0, count))
        grapes = (Grapes.random() for i in range(0, count))
        kiwifruits = (Kiwifruit.random() for i in range(0, count))
        lemons = (Lemon.random() for i in range(0, count))
        pineapples = (Pineapple.random() for i in range(0, count))
        watermelons = (Watermelon.random() for i in range(0, count))
        self.stdout.write(f'Generating apples')
        self.insert_batch(Apple, apples, 1000)
        self.stdout.write(f'Generating bananas')
        self.insert_batch(Banana, bananas, 1000)
        self.stdout.write(f'Generating grapes')
        self.insert_batch(Grapes, grapes, 1000)
        self.stdout.write(f'Generating kiwi fruits')
        self.insert_batch(Kiwifruit, kiwifruits, 1000)
        self.stdout.write(f'Generating lemons')
        self.insert_batch(Lemon, lemons, 1000)
        self.stdout.write(f'Generating pineapples')
        self.insert_batch(Pineapple, pineapples, 1000)
        self.stdout.write(f'Generating watermelons')
        self.insert_batch(Watermelon, watermelons, 1000)
        self.stdout.write(self.style.SUCCESS('Successfully generated fruits'))
