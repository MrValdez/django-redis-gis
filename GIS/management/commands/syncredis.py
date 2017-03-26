from django.core.management.base import BaseCommand
from GIS.models import Location
from GIS.utils import save_location_to_redis


class Command(BaseCommand):
    help = 'Clones all the location in the database to Redis'

    def handle(self, *args, **options):
        self.stdout.write("Cloning to redis...")

        for location in Location.objects.all():
            self.stdout.write("Saving: {}".format(location))
            save_location_to_redis(location)

        self.stdout.write("...done")
