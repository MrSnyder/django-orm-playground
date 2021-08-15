# Create your views here.
from django.views.generic import ListView, TemplateView

from polymorphic_fks.models import CheckrunUsingStandardFk


class HomeView(TemplateView):
    template_name = 'polymorphic_fks/home.html'


class CheckrunUsingStandardFkListView(ListView):
    model = CheckrunUsingStandardFk
    template_name = 'polymorphic_fks/checkrun_using_standard_fk.html'
