from django.db import models

# Create your models here.
from django.utils import timezone


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    class Race(models.TextChoices):
        CAT = 'Cat',
        DOG = 'Dog',
        HAMSTER = 'Hamster'

    owner = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    race = models.CharField(
        max_length=20,
        choices=Race.choices,
        default=Race.CAT,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"{self.race} {self.name}"
