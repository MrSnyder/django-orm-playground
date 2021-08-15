# Create your views here.
from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from polymorphic_fks.models import CheckrunWithGenericFk, CheckrunWithMultipleFks, \
    MultiTableBaseCheckrun, DjangoPolymorphicBaseCheckrun
from polymorphic_fks.tables import \
    CheckrunWithMultipleFksTable, MultiTableBaseCheckrunTable, DjangoPolymorphicBaseCheckrunTable, \
    CheckrunWithGenericFkTable


class HomeView(TemplateView):
    template_name = 'polymorphic_fks/home.html'


class CheckrunsWithGenericFk(SingleTableView):
    model = CheckrunWithGenericFk
    table_class = CheckrunWithGenericFkTable
    template_name = 'polymorphic_fks/checkruns.html'


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
