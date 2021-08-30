from django.urls import path
from django.views.generic import TemplateView

from cbv_trees.views import TreeNodeFormSetView, TreeNodeCreateView, TreeNodeListView

app_name = 'cbv_trees'
urlpatterns = [
    path('', TemplateView.as_view(template_name='cbv_trees/home.html'), name='home'),
    path('treenode/create', TreeNodeCreateView.as_view(), name='treenode-create'),
    path('treenode/lsit', TreeNodeListView.as_view(), name='treenode-list'),
    path('treenode/formset', TreeNodeFormSetView.as_view(), name='treenode-formset'),
]
