#!/usr/bin/env bash

styler_path=""

function get_path()
{
    styler_path="$1/codestyle-checker"
    [ -d $styler_path ]
}

get_path "../" || get_path "../../" || ( echo "Sorry, no codestyle checker found" && exit 1 )
$SHELL ${styler_path}/check_code_style.sh "$@"
