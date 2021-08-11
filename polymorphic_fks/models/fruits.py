import random
from random import randint

from django.db import models


class Apple(models.Model):
    class AppleColor(models.TextChoices):
        RED = 'red',
        GOLDEN = 'golden',
        GREEN = 'green',
        YELLOW = 'yellow'

    color = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'an apple: color={self.color}'

    @staticmethod
    def random():
        return Apple(color=random.choice(list(Apple.AppleColor)))


class Banana(models.Model):
    length_cm = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'a banana: length={self.length_cm} cm'

    @staticmethod
    def random():
        return Banana(length_cm=random.random() * 25 + 5)


class Grapes(models.Model):
    count = models.IntegerField()

    def __str__(self):
        return f'some grapes: count={self.count}'

    @staticmethod
    def random():
        return Grapes(count=randint(5, 50))


class Kiwifruit(models.Model):
    weight_g = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'a kiwi fruit: weight={self.weight_g}g'

    @staticmethod
    def random():
        return Kiwifruit(weight_g=random.random() * 190 + 10)


class Lemon(models.Model):
    circumference_mm = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'a lemon: circumference_mm={self.circumference_mm}mm'

    @staticmethod
    def random():
        return Lemon(circumference_mm=random.random() * 150 + 50)


class Pineapple(models.Model):
    height_cm = models.DecimalField(max_digits=4, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self):
        return f'a pineapple: height_cm={self.height_cm}, weight_kg={self.weight_kg}'

    @staticmethod
    def random():
        return Pineapple(height_cm=random.random() * 30 + 10, weight_kg=random.random() * 2.5 + 0.5)


class Watermelon(models.Model):
    circumference_cm = models.DecimalField(max_digits=4, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return f'a watermelon: circumference_cm={self.circumference_cm}, weight_kg={self.weight_kg}'

    @staticmethod
    def random():
        return Watermelon(circumference_cm=random.random() * 40 + 20, weight_kg=random.random() * 14 + 1)
