<?php

/**
  * Checks whether page alias is valid
  * @return true if alias is valid, false otherwise
  **/
function xcms_check_page_alias($alias)
{
    // everything should be replaced if OK
    $bad = preg_replace("#[a-z/A-Z.0-9_-]+#i", "", $alias);
    return xu_empty($bad);
}

?>