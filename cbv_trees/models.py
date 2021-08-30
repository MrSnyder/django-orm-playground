from django.db import models

# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class TreeNode(MPTTModel):
    parent = TreeForeignKey("TreeNode", on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="child_nodes")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
