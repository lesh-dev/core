function xjs_add_slider(el_id, show_el_id) {
    $(document).ready(
        function() {
            el_id = '#' + el_id;
            show_el_id = '#' + show_el_id;
            $(el_id).hide();
            $(show_el_id).click(
                function() {
                    $(el_id).slideToggle(400);
                    return false;
                });
        });
}
