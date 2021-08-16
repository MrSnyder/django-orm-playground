# Create your views here.
from django.views.generic import TemplateView, DetailView
from django_tables2 import SingleTableView, RequestConfig

from polymorphic_fks.models import CheckrunWithGenericFk, CheckrunWithMultipleFks, \
    MultiTableBaseCheckrun, DjangoPolymorphicBaseCheckrun, OgcService, Layer, FeatureType, ServiceMetadata, \
    LayerMetadata, FeatureTypeMetadata, DatasetMetadata
from polymorphic_fks.tables import \
    CheckrunWithMultipleFksTable, MultiTableBaseCheckrunTable, DjangoPolymorphicBaseCheckrunTable, \
    CheckrunWithGenericFkTable


class HomeView(TemplateView):
    template_name = 'polymorphic_fks/home.html'


class OgcServiceDetailView(DetailView):
    model = OgcService


class LayerDetailView(DetailView):
    model = Layer


class FeatureTypeDetailView(DetailView):
    model = FeatureType


class DatasetMetadataDetailView(DetailView):
    model = DatasetMetadata


class ServiceMetadataDetailView(DetailView):
    model = ServiceMetadata


class LayerMetadataDetailView(DetailView):
    model = LayerMetadata


class FeatureTypeMetadataDetailView(DetailView):
    model = FeatureTypeMetadata


class CheckrunsWithGenericFk(SingleTableView):
    model = CheckrunWithGenericFk
    table_class = CheckrunWithGenericFkTable
    template_name = 'polymorphic_fks/checkruns.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('resource_type')

    def get_table(self, **kwargs):
        """
        Return a table object to use. The table has automatic support for
        sorting and pagination.
        """
        table_class = self.get_table_class()
        table = table_class(data=self.get_table_data(), **kwargs)
        table.exclude = tuple(self.request.GET.get('exclude', '').split(','))
        return RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(
            table
        )


class CheckrunsWithMultipleFks(SingleTableView):
    model = CheckrunWithMultipleFks
    table_class = CheckrunWithMultipleFksTable
    template_name = 'polymorphic_fks/checkruns.html'


class CheckrunsWithFksInChildTables(SingleTableView):
    model = MultiTableBaseCheckrun
    table_class = MultiTableBaseCheckrunTable
    template_name = 'polymorphic_fks/checkruns.html'


class CheckrunsWithDjangoPolymorphic(SingleTableView):
    model = DjangoPolymorphicBaseCheckrun
    table_class = DjangoPolymorphicBaseCheckrunTable
    template_name = 'polymorphic_fks/checkruns.html'
