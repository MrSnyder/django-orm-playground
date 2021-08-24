from django.urls import path

from .views import HomeView, PersonListView, PersonCreateView, PetListView, PetCreateView, PersonWithPetsCreateView, \
    PersonEditAllView

app_name = 'inline_forms'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('person/list', PersonListView.as_view(), name='person-list'),
    path('person/create', PersonCreateView.as_view(), name='person-create'),
    path('person/edit-all', PersonEditAllView.as_view(), name='person-edit-all'),
    path('person/create-with-pets', PersonWithPetsCreateView.as_view(), name='person-create-with-pets'),
    path('pet/list', PetListView.as_view(), name='pet-list'),
    path('pet/create', PetCreateView.as_view(), name='pet-create'),
]
