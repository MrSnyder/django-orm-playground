function addForm(prefix) {
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
