# Create your views here.
from django.db import transaction
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView

from inline_forms.forms import PersonWithPetsFormSet, PersonForm
from inline_forms.models import Person, Pet


class HomeView(TemplateView):
    template_name = 'inline_forms/home.html'


class PersonListView(ListView):
    model = Person


class PersonCreateView(CreateView):
    model = Person
    # FormMixin requires either 'fields' or 'form_class', but not both
    form_class = PersonForm
    success_url = reverse_lazy('inline_forms:person-list')


# for FormSets, CreateView (or UpdateView) do not really seem to fit, as they are bound to a single object
# so, let's use FormView
class PersonEditAllView(FormView):
    form_class = modelformset_factory(Person, fields='__all__', extra=3, can_delete=True)
    success_url = reverse_lazy('inline_forms:person-list')
    template_name = 'inline_forms/person_set_form.html'

    # FormMixin: Redirects to get_success_url()
    def form_valid(self, form):
        # Changed, deleted, updated instances are bound to the formset automatically
        form.save()
        print(f"Changed: {len(form.changed_objects)}")
        print(f"Deleted: {len(form.deleted_objects)}")
        print(f"Updated: {len(form.new_objects)}")
        # for person_dict in form.cleaned_data:
        #     if person_dict:
        #         # 'id' attribute actually *is* the Person for pre-existing entities
        #         person = person_dict.get('id', None)
        #         del person_dict['id']
        #         if person:
        #             for key in person_dict:
        #                 setattr(person, key, person_dict[key])
        #         else:
        #             person = Person(**person_dict)
        #         person.save()
        return super().form_valid(form)


class PersonWithPetsCreateView(CreateView):
    model = Person
    fields = "__all__"
    success_url = reverse_lazy('inline_forms:pet-list')

    def get_context_data(self, **kwargs):
        data = super(PersonWithPetsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pets'] = PersonWithPetsFormSet(self.request.POST)
        else:
            data['pets'] = PersonWithPetsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pets = context['pets']
        with transaction.atomic():
            self.object = form.save()
            if pets.is_valid():
                pets.instance = self.object
                pets.save()
        return super(PersonWithPetsCreateView, self).form_valid(form)


class PetListView(ListView):
    model = Pet


class PetCreateView(CreateView):
    model = Pet
    fields = "__all__"
    success_url = reverse_lazy('inline_forms:pet-list')
