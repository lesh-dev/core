function xsm_set_selected_person_data()
{
    var id = $('#member_person_id-selector').val();
    jQuery.get('/xsm/api/get/person/' + id.toString(), function(data) {
        $('#department_id-selector').val(data.object.department_id);
        $('#is_teacher-checkbox').prop('checked', data.object.is_teacher.length > 0);
        $('#is_student-checkbox').prop('checked', data.object.is_student.length > 0);
    });

}

$(document).ready(function() {
    // set initial values
    xsm_set_selected_person_data();
    // handle changes
    $('#member_person_id-selector').change(xsm_set_selected_person_data);
});
