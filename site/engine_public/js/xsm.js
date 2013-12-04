function FilterFormAutoSubmit() {
    var form = $('#filter-form');
    controls = $(form).find('input');
    for (i in controls) {
        control = controls[i];
        console.log(control.id);

        $(control).change(function() {
            var form = $('#filter-form');
            form.submit();
        });
    }
}