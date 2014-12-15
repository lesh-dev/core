$(document).ready(function() {

    $('#member_person_id-selector').change(function() {
        var id = $('#member_person_id-selector').val();
        jQuery.get('/xsm/api/person/' + id.toString(), function(data) {
            $('#department_id-selector').val(data.object.department_id);
            $('#is_teacher-checkbox').prop('checked', data.object.is_teacher.length > 0);
            $('#is_student-checkbox').prop('checked', data.object.is_student.length > 0);
        });
    });

});
