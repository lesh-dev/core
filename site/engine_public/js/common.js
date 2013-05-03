function AddSlider(elId, showElId) {
    $(document).ready(
        function() {
            elId = '#' + elId;
            showElId = '#' + showElId;
            $(elId).hide();
            $(showElId).click(
                function() {
                    $(elId).slideToggle(400);
                    return false;
                });
        });
}
