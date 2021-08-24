function addForm(prefix) {
    const templateForm = document.querySelector(`#id-${prefix}-form-template`);
    const html = templateForm.innerHTML;
    const formNum = document.querySelectorAll(`.${prefix}-form`).length;
    const newHtml = html.replace(RegExp(`${prefix}-\\d+-`, 'g'), `${prefix}-${formNum}-`);
    const newTemplateForm = templateForm.cloneNode();
    newTemplateForm.innerHTML = newHtml;
    templateForm.removeAttribute('id')
    templateForm.removeAttribute('style')
    templateForm.after(newTemplateForm);
    document.querySelector(`#id_${prefix}-TOTAL_FORMS`).value=formNum + 1;
}
