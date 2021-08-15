from django_tables2 import tables

from polymorphic_fks.models import CheckrunUsingStandardFk


class CheckrunUsingStandardFkTable(tables.Table):

    checked_resource = tables.columns.Column(empty_values=())

    class Meta:
        model = CheckrunUsingStandardFk
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed',)

    def render_checked_resource(self):
        return 'OgcService'


class CheckrunWithGenericFkTable(tables.Table):

    class Meta:
        model = CheckrunUsingStandardFk
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'created_at', 'passed', 'resource_type')
