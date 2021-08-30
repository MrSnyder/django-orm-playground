from django.db import models

# Create your models here.
from extra_views import InlineFormSetFactory
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class TreeNode(MPTTModel):
    parent = TreeForeignKey("TreeNode", on_delete=models.CASCADE, null=True, blank=True,
                            related_name="child_nodes")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Map(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Layer(MPTTModel):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, blank=False, null=False)
    parent = TreeForeignKey("Layer", on_delete=models.CASCADE, null=True, blank=True,
                            related_name="child_layers")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
