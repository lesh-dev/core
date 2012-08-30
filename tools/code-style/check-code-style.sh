#!/bin/bash

# Checks that no tabs uses in code
# set -xe

editor=$EDITOR
if [ $editor. == . ]; then
    editor=vi
fi
path="."
use_ui=false

while [ true ]; do
    command=$1
    shift 
    if [ $command. == "--ui." ]; then
        use_ui=true
    fi
    if [ $command. == "--editor." ]; then
        use_ui=true
        editor=$1
        shift
    fi
    if [ $command. == "--path." ]; then
        path=$1
        shift
    fi
    if [ $command. == . ]; then
      break;
    fi
done

function get_bool()
{
    while [ true ]; do
      read -p "$1" ans
      if [ $ans. == "n." ]; then echo 0; return 0; fi
      if [ $ans. == "N." ]; then echo 0; return 0; fi
      if [ $ans. == "no." ]; then echo 0;  return 0; fi
      if [ $ans. == "y." ]; then echo 1; return 1; fi
      if [ $ans. == "Y." ]; then echo 1; return 1; fi
      if [ $ans. == "yes." ]; then echo 1; return 1; fi
    done
}

check_tabs()
{
    greep()
    {
        find $path -type f -name $1 | xargs grep $'\t'
    }
    
    if greep $1 ; then
        echo "*** ERROR *** There was tabs."
    fi
    for i in $(greep | sed s/":.*"//g | sort  | uniq ); do
        echo "  Tabs was found in file: $i"
        if [ $use_ui == true ]; then
            ans=$(get_bool "Do You want to open editor? [y/n] ")
            if [ $ans == 1 ]; then
                $editor $(echo $i | sed s/":.*"//g)
            fi
        fi
    done
    
    return 0
}
check_shorttag()
{
    greep() # Ох нифига ж себе! Вложенные функции на баше! А замыкания тут есть?
    {
	grep -RI '<[?][^px]' $path || grep -RI '<[?]$' ../../site
    }
    if greep ; then
	echo " *** ERROR *** There was short tags found"
    fi
    failed_tags=$(greep | sed s/":.*"//g | sort  | uniq )
    for i in $failed_tags; do
        echo "  Short tags was found in file: $i"
        if [ $use_ui == true ]; then
            ans=$(get_bool "Do You want to open editor? [y/n] ")
            if [ $ans == 1 ]; then
                $editor $(echo $i | sed s/":.*"//g)
            fi
        fi
    done
    return 0
}

# TODO: check cr/lf symbols in code

echo "Path: $path"
check_shorttag
check_tabs '*.xcms'
check_tabs '*.php'
check_tabs '*.code'
check_tabs '*.sh'
