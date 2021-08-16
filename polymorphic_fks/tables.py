from django_tables2 import tables

from polymorphic_fks.models import CheckrunWithMultipleFks, MultiTableBaseCheckrun, \
    DjangoPolymorphicBaseCheckrun, CheckrunWithGenericFk

VALUE_ABSOLUTE_LINK = """
{% if value.get_absolute_url%}
<a href="{{value.get_absolute_url}}">{{value}}</a>
{% else %}
{{value}}
{% endif %}
"""


class CheckrunWithGenericFkTable(tables.Table):
    linked_resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id }}</a>')

    class Meta:
        model = CheckrunWithGenericFk
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed')


class CheckrunWithMultipleFksTable(tables.Table):
    resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id }}</a>')

    class Meta:
        model = CheckrunWithMultipleFks
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed')


class MultiTableBaseCheckrunTable(tables.Table):
    resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id_poly }}</a>')

    class Meta:
        model = MultiTableBaseCheckrun
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed',)


class DjangoPolymorphicBaseCheckrunTable(tables.Table):
    resource = tables.columns.TemplateColumn(
        '<a href="{{ record.resource_url }}">{{ record.resource_type }} #{{ record.resource_id }}</a>')

    class Meta:
        model = DjangoPolymorphicBaseCheckrun
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed',)
