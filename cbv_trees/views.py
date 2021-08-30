# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from extra_views import ModelFormSetView, CreateWithInlinesView, UpdateWithInlinesView

from cbv_trees.forms import TreeNodeForm, BaseModelTreeFormSet, LayerInline
from cbv_trees.models import TreeNode, Map


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


class MapCreateWithLayersInlineView(CreateWithInlinesView):
    model = Map
    fields = "__all__"
    inlines = [LayerInline]
    template_name = 'cbv_trees/map_form_inline.html'
    success_url = reverse_lazy('cbv_trees:map-list')


class MapUpdateWithLayersInlineView(UpdateWithInlinesView):
    model = Map
    fields = "__all__"
    inlines = [LayerInline]
    template_name = 'cbv_trees/map_form_inline.html'
    success_url = reverse_lazy('cbv_trees:map-list')

    def get_initial(self):
        initial = super().get_initial()
        return initial
