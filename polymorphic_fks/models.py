from django.db import models


class Item1(models.Model):
    name = models.TextField(blank=True, null=True)

