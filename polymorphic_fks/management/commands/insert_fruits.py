from django.core.management import BaseCommand

from polymorphic_fks.models import Apple, Banana, Grapes, Kiwifruit, Lemon, Pineapple, Watermelon


class Command(BaseCommand):
    help = 'Adds test data (fruits)'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(f'Generating {count} fruits (for each type)')
        for i in range(1, count):
            print(Apple.random())
            print(Banana.random())
            print(Grapes.random())
            print(Kiwifruit.random())
            print(Lemon.random())
            print(Pineapple.random())
            print(Watermelon.random())

        # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
