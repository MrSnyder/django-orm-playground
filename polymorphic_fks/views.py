# Create your views here.
from django.views.generic import ListView, TemplateView
from django_tables2 import SingleTableView

from polymorphic_fks.models import CheckrunUsingStandardFk, CheckrunWithGenericFk, CheckrunWithMultipleFks, \
    MultiTableBaseCheckrun
from polymorphic_fks.tables import CheckrunUsingStandardFkTable, CheckrunWithGenericFkTable, \
    CheckrunWithMultipleFksTable, MultiTableBaseCheckrunTable


class HomeView(TemplateView):
    template_name = 'polymorphic_fks/home.html'


class CheckrunUsingStandardFkListView(SingleTableView):
    model = CheckrunUsingStandardFk
    table_class = CheckrunUsingStandardFkTable
    template_name = 'polymorphic_fks/checkruns.html'


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
