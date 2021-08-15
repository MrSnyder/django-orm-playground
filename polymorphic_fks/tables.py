from django_tables2 import tables

from polymorphic_fks.models import CheckrunWithMultipleFks, MultiTableBaseCheckrun, \
    DjangoPolymorphicBaseCheckrun, CheckrunWithGenericFk


class CheckrunWithGenericFkTable(tables.Table):
    class Meta:
        model = CheckrunWithGenericFk
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed', 'resource_type')


class CheckrunWithMultipleFksTable(tables.Table):
    resource_type = tables.columns.Column(empty_values=())

    class Meta:
        model = CheckrunWithMultipleFks
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed')

    def render_resource_type(self, record):
        return record.resource_type.__name__


class MultiTableBaseCheckrunTable(tables.Table):
    resource_type = tables.columns.Column(empty_values=())

    class Meta:
        model = MultiTableBaseCheckrun
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed',)

    def render_resource_type(self):
        return 'Unknown'


class DjangoPolymorphicBaseCheckrunTable(tables.Table):
    resource_type = tables.columns.Column(empty_values=())

    class Meta:
        model = DjangoPolymorphicBaseCheckrun
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed',)

    def render_resource_type(self, record):
        return record.__class__.__name__
