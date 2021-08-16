# Create your views here.
from django.views.generic import TemplateView, DetailView
from django_tables2 import SingleTableView, RequestConfig

from polymorphic_fks.models import CheckrunWithGenericFk, CheckrunWithMultipleFks, \
    MultiTableBaseCheckrun, DjangoPolymorphicBaseCheckrun, OgcService, Layer, FeatureType, ServiceMetadata, \
    LayerMetadata, FeatureTypeMetadata, DatasetMetadata, CheckrunWithFkLookupTable
from polymorphic_fks.tables import \
    CheckrunWithMultipleFksTable, MultiTableBaseCheckrunTable, DjangoPolymorphicBaseCheckrunTable, \
    CheckrunWithGenericFkTable, CheckrunWithFkLookupTableTable


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
        qs = super().get_queryset().order_by('pk')
        return qs.select_related('_resource_type')

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

    def get_queryset(self):
        qs = super().get_queryset().order_by('pk')
        return qs.select_related('ogc_service', 'layer', 'feature_type', 'dataset_metadata', 'service_metadata',
                                 'layer_metadata', 'feature_type_metadata')

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


class CheckrunsWithFkLookupTable(SingleTableView):
    model = CheckrunWithFkLookupTable
    table_class = CheckrunWithFkLookupTableTable
    template_name = 'polymorphic_fks/checkruns.html'

    def get_queryset(self):
        qs = super().get_queryset().order_by('pk')
        return qs.select_related('_resource__ogc_service', '_resource__layer', '_resource__feature_type',
                                 '_resource__dataset_metadata', '_resource__service_metadata',
                                 '_resource__layer_metadata', '_resource__feature_type_metadata')

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


class CheckrunsWithFksInChildTables(SingleTableView):
    model = MultiTableBaseCheckrun
    table_class = MultiTableBaseCheckrunTable
    template_name = 'polymorphic_fks/checkruns.html'

    def get_queryset(self):
        qs = super().get_queryset().order_by('pk')
        return qs.select_related('multitablecheckrunogcservice__resource', 'multitablecheckrunlayer__resource',
                                 'multitablecheckrunfeaturetype__resource',
                                 'multitablecheckrundatasetmetadata__resource',
                                 'multitablecheckrunservicemetadata__resource',
                                 'multitablecheckrunlayermetadata__resource',
                                 'multitablecheckrunfeaturetypemetadata__resource')

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


class CheckrunsWithDjangoPolymorphic(SingleTableView):
    model = DjangoPolymorphicBaseCheckrun
    table_class = DjangoPolymorphicBaseCheckrunTable
    template_name = 'polymorphic_fks/checkruns.html'

    def get_queryset(self):
        qs = super().get_queryset().order_by('pk')
        return qs
        # select_related on inherited models is not supported yet...
        # return qs.select_related('djangopolymorphiccheckrunogcservice', 'djangopolymorphiccheckrunlayer', ...)
        # see https://django-polymorphic.readthedocs.io/en/stable/advanced.html#combining-querysets
        # only works when one turns of the polymorphic mode:
        # return qs.non_polymorphic().select_related('djangopolymorphiccheckrunogcservice',
        #                                            'djangopolymorphiccheckrunlayer')

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
