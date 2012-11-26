$(document).ready(
    function() {
        $('#editor-help').hide();
        $('#show-editor-help').click(
            function() {
                $('#editor-help').slideToggle(400);
                return false;
            });
    });