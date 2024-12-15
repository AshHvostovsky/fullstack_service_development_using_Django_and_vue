from django.core.management.base import BaseCommand

from faker import Faker

from missions.models import Mission


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(10):
            Mission.objects.create(
                name=fake.company(),
                launch_date=fake.date_this_century(),
                outcome=fake.postcode()
                description=fake.paragraph(nb_sentences=3),
                space_program=fake.postcode()
                mission_type=fake.postcode()
                user=fake.postcode()
            )


