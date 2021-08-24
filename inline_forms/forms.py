from django.forms import inlineformset_factory, formset_factory, ModelForm

from inline_forms.models import Pet, Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


PersonFormSet = formset_factory(PersonForm, extra=1)
PersonWithPetsFormSet = inlineformset_factory(Person, Pet, fields=('name', 'race',))
