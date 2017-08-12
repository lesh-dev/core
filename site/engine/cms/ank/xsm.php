<?php

function xsm_valid_aparam($aparam)
{
    return (
        substr($aparam, 0, 5) == "list-" ||
        substr($aparam, 0, 5) == "view-" ||
        substr($aparam, 0, 5) == "edit-" ||
        substr($aparam, 0, 4) == "add-" ||
        false
    );
}
