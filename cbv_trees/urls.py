from django.urls import path
from django.views.generic import TemplateView, ListView

from cbv_trees.models import Map
from cbv_trees.views import TreeNodeFormSetView, TreeNodeCreateView, TreeNodeListView, MapCreateWithLayersInlineView
from inline_forms.views import PersonCreateWithPetsInlineView

app_name = 'cbv_trees'
urlpatterns = [
    path('', TemplateView.as_view(template_name='cbv_trees/home.html'), name='home'),
    path('treenode/create', TreeNodeCreateView.as_view(), name='treenode-create'),
    path('treenode/lsit', TreeNodeListView.as_view(), name='treenode-list'),
    path('treenode/formset', TreeNodeFormSetView.as_view(), name='treenode-formset'),

    path('map/list', ListView.as_view(model=Map), name='map-list'),
    path('map/create-with-layers-inline', MapCreateWithLayersInlineView.as_view(),
         name='map-create-with-layers-inline'),
]
