from django.contrib import admin

# Register your models here.
from inline_forms.models import Person, Pet

admin.site.register(Person)
admin.site.register(Pet)
