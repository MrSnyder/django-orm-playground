# Create your views here.
from django.forms import modelformset_factory, BaseModelFormSet
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from extra_views import ModelFormSetView

from cbv_trees.forms import TreeNodeForm, BaseModelTreeFormSet
from cbv_trees.models import TreeNode


class TreeNodeCreateView(CreateView):
    model = TreeNode
    # FormMixin requires either 'fields' or 'form_class', but not both
    form_class = TreeNodeForm
    success_url = reverse_lazy('cbv_trees:treenode-list')


class TreeNodeListView(ListView):
    model = TreeNode


class TreeNodeFormSetView(ModelFormSetView):
    model = TreeNode
    form_class = TreeNodeForm
    template_name = 'cbv_trees/treenode_formset.html'
    prefix = 'treenode'
    factory_kwargs = {'extra': 1, 'can_delete': True, 'formset': BaseModelTreeFormSet}
