from django.urls import path

from .views import HomeView, CheckrunUsingStandardFkListView, CheckrunsWithGenericFk, CheckrunsWithMultipleFks, \
    CheckrunsWithFksInChildTables

app_name = 'polymorphic_fks'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkruns-with-standard_fk/', CheckrunUsingStandardFkListView.as_view(), name='checkruns-using-standard-fk'),
    path('checkruns-with-generic-fk/', CheckrunsWithGenericFk.as_view(), name='checkruns-with-generic-fk'),
    path('checkruns-with-multiple-fks/', CheckrunsWithMultipleFks.as_view(), name='checkruns-with-multiple-fks'),
    path('checkruns-with-fks-in-child-tables/', CheckrunsWithFksInChildTables.as_view(), name='checkruns-with-fks-in-child-table'),
]
