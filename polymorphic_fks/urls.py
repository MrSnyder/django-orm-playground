from django.urls import path

from .views import HomeView, CheckrunsWithGenericFk, CheckrunsWithMultipleFks, \
    CheckrunsWithFksInChildTables, CheckrunsWithDjangoPolymorphic

app_name = 'polymorphic_fks'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkruns-with-generic-fk/', CheckrunsWithGenericFk.as_view(), name='checkruns-with-generic-fk'),
    path('checkruns-with-multiple-fks/', CheckrunsWithMultipleFks.as_view(), name='checkruns-with-multiple-fks'),
    path('checkruns-with-fks-in-child-tables/', CheckrunsWithFksInChildTables.as_view(),
         name='checkruns-with-fks-in-child-table'),
    path('checkruns-with-django-polymorphic/', CheckrunsWithDjangoPolymorphic.as_view(),
         name='checkruns-with-django-polymorphic'),
]
