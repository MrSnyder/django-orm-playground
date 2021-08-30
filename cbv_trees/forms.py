from django import forms
from django.forms import ModelForm, BaseModelFormSet, BaseInlineFormSet
from extra_views import InlineFormSetFactory

from cbv_trees.models import TreeNode, Layer


class TreeNodeForm(ModelForm):
    parent_form_id = forms.CharField(max_length=20, required=False)

    class Meta:
        model = TreeNode
        fields = ['id', 'parent', 'name']


class BaseModelTreeFormSet(BaseModelFormSet):

    def save(self, commit=True):
        """
        Save model instances for every form, adding and changing instances
        as necessary, and return the list of instances.
        """

        # delete all forms that existed before
        for form in self.forms:
            existing_object = form.cleaned_data.get('id', None)
            if existing_object:
                print(f"Deleting... {existing_object}")
                existing_object.delete()

        # save all forms not marked for deletion
        new_objects = []

        # ignore the last form (this is the template form)
        total_forms = self.management_form.cleaned_data['TOTAL_FORMS'] - 1
        for i in range(0, total_forms):
            form = self.forms[i]
            print(f"Saving form {i}: {form}")
            if form.cleaned_data.get('DELETE', None):
                continue
            parent_form_id = form.cleaned_data.get("parent_form_id", None)
            if parent_form_id:
                parent = new_objects[int(parent_form_id)]
                form.instance.parent = parent
            else:
                form.instance.parent = None
            form.cleaned_data['id'] = None

            model_instance = form.save(commit=False)
            # ensure that there are no left-over values for MPTT-specific fields (lft, rght, tree_id, level)
            clean_model_instance = TreeNode(name=model_instance.name, parent=model_instance.parent)
            clean_model_instance.save()
            new_objects.append(clean_model_instance)
            print(f"Saved {clean_model_instance}")
        return new_objects


class LayerForm(ModelForm):
    parent_form_idx = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Layer
        fields = ['id', 'parent', 'parent_form_idx', 'name']


class LayerTreeInlineFormSet(BaseInlineFormSet):

    def save(self, commit=True):
        """
        Save model instances for every form, adding and changing instances
        as necessary, and return the list of instances.
        """

        # delete all forms that existed before
        # TODO better delete all objects related to the "instance"?
        for form in self.forms:
            existing_object = form.cleaned_data.get('id', None)
            if existing_object:
                print(f"Deleting... {existing_object}")
                existing_object.delete()

        new_objects = []
        # ignore the last form (this is the template form)
        total_forms = self.management_form.cleaned_data['TOTAL_FORMS'] - 1
        for i in range(0, total_forms):
            form = self.forms[i]
            if form.cleaned_data.get('DELETE', None):
                continue
            parent_form_idx = form.cleaned_data.get("parent_form_idx", None)
            if parent_form_idx:
                parent = new_objects[int(parent_form_idx)]
                form.instance.parent = parent
            else:
                form.instance.parent = None
            model_instance = form.save(commit=False)
            # ensure that there are no left-over values for MPTT-specific fields (lft, rght, tree_id, level)
            clean_model_instance = Layer(name=model_instance.name, map=model_instance.map, parent=model_instance.parent)
            clean_model_instance.save()
            new_objects.append(clean_model_instance)
            print(f"Saved {clean_model_instance}")
        return new_objects


class LayerInline(InlineFormSetFactory):
    model = Layer
    #fields = '__all__'
    form_class = LayerForm
    prefix = 'layer'
    factory_kwargs = {'extra': 1, 'can_delete': True, 'formset': LayerTreeInlineFormSet}
