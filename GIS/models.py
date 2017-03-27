from django.db import models
from .utils import save_location_to_redis, delete_redis_location


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Category")
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.long, self.lat)

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)
        save_location_to_redis(self)

    def delete(self, *args, **kwargs):
        delete_redis_location(self)
        super(Location, self).delete(*args, **kwargs)