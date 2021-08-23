# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from inline_forms.models import Person, Pet


class HomeView(TemplateView):
    template_name = 'inline_forms/home.html'


class PersonListView(ListView):
    model = Person


class PersonCreateView(CreateView):
    model = Person
    fields = "__all__"
    success_url = reverse_lazy('inline_forms:person-list')


class PetListView(ListView):
    model = Pet


class PetCreateView(CreateView):
    model = Pet
    fields = "__all__"
    success_url = reverse_lazy('inline_forms:pet-list')
