from django.urls import path

from .views import HomeView, CheckrunUsingStandardFkListView

app_name = 'polymorphic_fks'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkrun_using_standard_fk/', CheckrunUsingStandardFkListView.as_view(), name='checkruns-using-standard-fk'),
]
