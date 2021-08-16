from django_tables2 import tables

from polymorphic_fks.models import CheckrunWithMultipleFks, MultiTableBaseCheckrun, \
    DjangoPolymorphicBaseCheckrun, CheckrunWithGenericFk


class CheckrunWithGenericFkTable(tables.Table):
    linked_resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id }}</a>')

    class Meta:
        model = CheckrunWithGenericFk
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed', 'resource_name')


class CheckrunWithMultipleFksTable(tables.Table):
    resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id }}</a>')

    class Meta:
        model = CheckrunWithMultipleFks
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed', 'resource_name')


class MultiTableBaseCheckrunTable(tables.Table):
    resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id_poly }}</a>')

    class Meta:
        model = MultiTableBaseCheckrun
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed', 'resource_name')


class DjangoPolymorphicBaseCheckrunTable(tables.Table):
    resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id }}</a>')

    class Meta:
        model = DjangoPolymorphicBaseCheckrun
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed', 'resource_name')
