/**
 * Turns a container element into a dynamic jsTree control and binds it to a Django TreeFormSet.
 *
 * @param {string} treeContainerId - the id of the container element (must include '#')
 * @param {string} formPrefix - prefix of classes and ids of the formsets
 */
function initJsTreeFormset(treeContainerId, formPrefix) {
  function appendForm() {
    const forms = document.querySelectorAll(`.${formPrefix}-form`);
    const formNum = forms.length;
    // last form was the template form -> becomes the new form
    const form = forms[formNum - 1];
    const html = form.innerHTML;
    const templateHtml = html.replace(RegExp(`${formPrefix}-\\d+-`, 'g'), `${formPrefix}-${formNum}-`);
    const templateForm = form.cloneNode();
    templateForm.innerHTML = templateHtml;
    form.after(templateForm);
    form.removeAttribute('style')
    // update number of forms in management form
    // https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#understanding-the-managementform
    document.querySelector(`#id_${formPrefix}-TOTAL_FORMS`).value = formNum + 1;
  }
  function updateFormset() {
    // get the tree's nodes (in topological order, so a parent always precedes its children)
    let treeState = jsTree.get_json(undefined, {
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
    const forms = $(`.${formPrefix}-form`);
    const nodeIdToFormIdx = {};
    for (i in forms) {
      if (i < treeState.length) {
        const node = treeState[i];
        parentFormIdx = node.parent == '#' ? '' : nodeIdToFormIdx[node.parent];
        nodeIdToFormIdx[node.id] = i;
        $(`#id_${formPrefix}-${i}-name`).val(node.text);
        $(`#id_${formPrefix}-${i}-parent_form_idx`).val(parentFormIdx);
        $(`#id_${formPrefix}-${i}-DELETE`).prop('checked', false);
      } else {
        $(`#id_${formPrefix}-${i}-name`).val('');
        $(`#id_${formPrefix}-${i}-id`).val('');
        $(`#id_${formPrefix}-${i}-parent_form_idx`).val('');
        $(`#id_${formPrefix}-${i}-DELETE`).prop('checked', true);
      }
    }
  }
  $(treeContainerId).jstree({
    "core": {
      "check_callback": function (operation, node, nodeParent, nodePosition, more) {
        // operation can be 'create_node', 'rename_node', 'delete_node', 'move_node', 'copy_node' or 'edit'
        // in case of 'rename_node' node_position is filled with the new node name
        if (operation === 'move_node') {
          return typeof nodeParent.text !== 'undefined';
        }
        return true;
      },
      "data": function (obj, cb) {
        const nodes = [];
        const forms = $(`.${formPrefix}-form`);
        for (i = 0; i < forms.length - 1; i++) {
          nodes.push({
            id: $(`#id_${formPrefix}-${i}-id`).val(),
            parent: $(`#id_${formPrefix}-${i}-parent`).val() || "#",
            text: $(`#id_${formPrefix}-${i}-name`).val()
          });
        }
        if (nodes.length == 0) {
          appendForm();
          nodes.push({
            id: 0,
            parent: '#',
            text: '/',
          });
        }
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
    appendForm();
    updateFormset();
  }).on('rename_node.jstree', function (e, data) {
    updateFormset();
  }).on('delete_node.jstree', function (e, data) {
    updateFormset();
  }).on('move_node.jstree', function (e, data) {
    updateFormset();
  }).on('select_node.jstree', function (e, data) {
    // TODO switch visibility of form?
  });
  const jsTree = $(treeContainerId).jstree(true);
  $(treeContainerId).on('model.jstree', function (e, data) {
    data.nodes.forEach(nodeId => {
      let node = jsTree.get_node(nodeId);
      if (node.type === 'default') {
        jsTree.add_action(nodeId, {
          "id": "action_add_folder",
          "class": "fas fa-plus-circle pull-right",
          "title": "Add Folder",
          "after": true,
          "selector": "a",
          "event": "click",
          "callback": function (nodeId, node, action_id, action_el) {
            jsTree.create_node(node, {}, "last", function (newNode) {
              try {
                jsTree.edit(newNode);
              } catch (ex) {
                setTimeout(function () { inst.edit(newNode); }, 0);
              }
            });
          }
        });
        if (node.parent !== '#') {
          jsTree.add_action(nodeId, {
            "id": "action_remove",
            "class": "fas fa-minus-circle pull-right",
            "title": "Remove Child",
            "after": true,
            "selector": "a",
            "event": "click",
            "callback": function (nodeId, node) {
              jsTree.delete_node(node);
            }
          });
        }
        jsTree.add_action(nodeId, {
          "id": "action_edit",
          "class": "fas fa-edit pull-right",
          "title": "Edit",
          "after": true,
          "selector": "a",
          "event": "click",
          "callback": function (nodeId, node) {
            jsTree.edit(node.id);
          }
        });
      } else if (node.type === 'resource') {
        jsTree.add_action(nodeId, {
          "id": "action_remove",
          "class": "fas fa-minus-circle pull-right",
          "title": "Remove",
          "after": true,
          "selector": "a",
          "event": "click",
          "callback": function (nodeId, node) {
            jsTree.delete_node(node);
          }
        });
      }
    });
  });
  return jsTree;
}
