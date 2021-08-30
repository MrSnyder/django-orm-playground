$(function () {
  const prefix = 'layer';
    function appendForm() {
        const forms = document.querySelectorAll(`.${prefix}-form`);
        const formNum = forms.length;
        // last form was the spare form -> becomes the new form now
        const form = forms [formNum - 1];
        const html = form.innerHTML;
        const spareHtml = html.replace(RegExp(`${prefix}-\\d+-`, 'g'), `${prefix}-${formNum}-`);
        const spareForm = form.cloneNode();
        spareForm.innerHTML = spareHtml;
        form.after(spareForm);
        form.removeAttribute('style')
        document.querySelector(`#id_${prefix}-TOTAL_FORMS`).value=formNum + 1;
    }
  function update_formset() {
    let tree = $('#mapcontext_tree').jstree(true);
    let tree_state = tree.get_json(undefined, {
      flat: true,
      no_a_attr: true,
      no_li_attr: true,
      no_state: true
    }).map(node => ({
      id: node.id,
      text: node.text,
      type: node.type,
      parent: node.parent,
      data: node.data
    }));
    const layerForms = $('.layer-form');
    const nodeIdToLayerIdx = {};
    for (i in layerForms) {
        if (i < tree_state.length) {
            const node = tree_state[i];
            parentLayerIdx = node.parent == '#' ? '' : nodeIdToLayerIdx[node.parent];
            nodeIdToLayerIdx[node.id] = i;
            layerForms[i].setAttribute('data-jstree-node-id', node.id);
            $(`#id_layer-${i}-name`).val(node.text);
//            $(`#id_layer-${i}-id`).val(node.id);
            $(`#id_layer-${i}-parent_form_idx`).val(parentLayerIdx);
            $(`#id_layer-${i}-DELETE`).prop('checked', false);
        } else {
            $(`#id_layer-${i}-name`).val('');
            $(`#id_layer-${i}-id`).val('');
            $(`#id_layer-${i}-parent_form_idx`).val('');
            if ($(`#id_layer-${i}-id`).val()) {
                $(`#id_layer-${i}-DELETE`).prop('checked', true);
            }
        }
    }
  }
  $('#mapcontext_tree').jstree({
    "core": {
      "check_callback": function (operation, node, node_parent, node_position, more) {
        // operation can be 'create_node', 'rename_node', 'delete_node', 'move_node', 'copy_node' or 'edit'
        // in case of 'rename_node' node_position is filled with the new node name
        if (operation === 'move_node') {
          return typeof node_parent.text !== 'undefined';
        }
        return true;
      },
      "data": function (obj, cb) {
        const nodes = [];
        // TODO configurable
        const layerForms = $('.layer-form');
        for (i = 0; i < layerForms.length - 1; i++) {
            layerForm = layerForms.get(i);
            console.log(layerForms.get(i));
            nodes.push ({
                // TODO configurable
                id : $(`#id_layer-${i}-id`).val(),
                parent : $(`#id_layer-${i}-parent`).val() || "#",
                text : $(`#id_layer-${i}-name`).val(),
            });
        }
        if (nodes.length == 0) {
            appendForm();
            nodes.push ({
                id : 0,
                parent : '#',
                text : '/',
            });
        }
        console.log(nodes);
        cb.call(this, nodes);
      }
    },
    "plugins": ["dnd", "types", "unique", "rename", "actions"],
    "dnd": {
      "copy": false,
    },
    "types": {
      "root": {
        "icon": "fas fa-folder",
        "valid_children": ["default", "resource"]
      },
      "default": {
        "icon": "fas fa-folder",
        "valid_children": ["default", "resource"]
      },
      "resource": {
        "icon": "fas fa-map",
        "valid_children": []
      }
    }
  }).on('create_node.jstree', function (e, data) {
    console.log("*** create_node");
    appendForm(data.node.id);
    update_formset();
  }).on('rename_node.jstree', function (e, data) {
    console.log("*** rename_node");
    update_formset();
  }).on('delete_node.jstree', function (e, data) {
    console.log("*** delete_node");
    update_formset();
  }).on('move_node.jstree', function (e, data) {
    console.log("*** move_node");
    update_formset();
  }).on('select_node.jstree', function (e, data) {
    console.log("*** select_node");
    // TODO switch visibility of form?
  });
  let layerTree = $('#mapcontext_tree').jstree(true);
  $('#mapcontext_tree').on('model.jstree', function (e, data) {
    data.nodes.forEach(node_id => {
      let node = layerTree.get_node(node_id);
      if (node.type === 'default') {
        layerTree.add_action(node_id, {
          "id": "action_add_folder",
          "class": "fas fa-plus-circle pull-right",
          "title": "Add Folder",
          "after": true,
          "selector": "a",
          "event": "click",
          "callback": function (node_id, node, action_id, action_el) {
            let jstree = $('#mapcontext_tree').jstree(true);
            jstree.create_node(node, {}, "last", function (new_node) {
              try {
                jstree.edit(new_node);
              } catch (ex) {
                setTimeout(function () { inst.edit(new_node); }, 0);
              }
            });
          }
        });
        if (node.parent !== '#') {
          layerTree.add_action(node_id, {
            "id": "action_remove",
            "class": "fas fa-minus-circle pull-right",
            "title": "Remove Child",
            "after": true,
            "selector": "a",
            "event": "click",
            "callback": function (node_id, node, action_id, action_el) {
              let jstree = $('#mapcontext_tree').jstree(true);
              jstree.delete_node(node);
            }
          });
        }
        layerTree.add_action(node_id, {
          "id": "action_edit",
          "class": "fas fa-edit pull-right",
          "title": "Edit",
          "after": true,
          "selector": "a",
          "event": "click",
          "callback": function (node_id, node, action_id, action_el) {
            let jstree = $('#mapcontext_tree').jstree(true);
            jstree.edit(node.id);
          }
        });
      } else if (node.type === 'resource') {
        layerTree.add_action(node_id, {
          "id": "action_remove",
          "class": "fas fa-minus-circle pull-right",
          "title": "Remove",
          "after": true,
          "selector": "a",
          "event": "click",
          "callback": function (node_id, node, action_id, action_el) {
            let jstree = $('#mapcontext_tree').jstree(true);
            jstree.delete_node(node);
          }
        });
      }
    });
  });
});
