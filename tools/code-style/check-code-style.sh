#!/bin/bash
# We should not ignore any errors, it's better to fail
# Please do not remove the following line
set -e

# Runs python-based code style checker

# ignore list (contrib files whose code style
# we don't want to verify
ignore_list_files="class.phpmailer.php"
ignore_list_dirs="/forum/"

# some settings that you don't need to touch
path="."
my_base="$(dirname "$(readlink -f "$0")")"
tmp="/tmp"

print_usage()
{
    cat - <<EOF
Usage: `basename $0` <options>
    -h  --help                  Show this help
    -n  --names-only            Print only failed file names-only
    -f  --file <file-name>      Check only given file
    -c  --commit                Check all modified files in GIT repo
                                You must be inside GIT repo to use it
EOF
    exit 1

}

# print error message, then print help and exit
error_exit()
{
    local need_help="$1"
    local message="$2"
    echo "Error: $message"
    echo
    if [ "$need_help" == "help" ] ; then
        print_usage
    fi
    exit 1
}

while [ -n "$1" ] ; do
    if [ "$1" == "-h" ] || [ "$1" == "--help" ] ; then
        print_usage
        shift
        continue
    fi
    if [ "$1" == "-n" ] || [ "$1" == "--names-only" ] ; then
        names_only="yes"
        shift
        continue
    fi
    if [ "$1" == "-c" ] || [ "$1" == "--commit" ] ; then
        commit_only="yes"
        shift
        continue
    fi
    if [ "$1" == "-f" ] || [ "$1" == "--file" ] ; then
        shift
        check_file_name="$1"
        if [ -z "$check_file_name" ] ; then
            error_exit "help" "File name is not given for 'file' parameter"
        fi
        shift
        continue
    fi
    # invalid args, print usage and bail out
    print_usage
done

# flush global failure flag
fail=

check_file()
{
    fn="$1"
    if $my_base/check.py "$fn" > $tmp/check-result ; then
        return
    fi

    if [ "$names_only" == "yes" ] ; then
        echo $fn
    else
        echo "*** Checking '$fn' failed:"
        cat $tmp/check-result
        echo
        echo
    fi
    fail="yes"
}

check_style()
{
    for i in `find $path -type f -name "$1"`; do
        local ignore=""
        # skip ignored files
        ib="`basename $i`"
        for b in $ignore_list_files ; do
            if [ "$ib" == "$b" ] ; then
                ignore="yes"
                ignore_reason="whitelisted file"
                break
            fi
        done
        for d in $ignore_list_dirs ; do
            if echo "$i" | grep -q "$d" ; then
                ignore="yes"
                ignore_reason="whitelisted directory"
                break
            fi
        done

        if [ "$ignore" == "yes" ] ; then
            #echo "IGNORED: $i by $ignore_reason"
            continue
        fi
        # check files
        check_file "$i"
    done
    return 0
}

if [ -n "$check_file_name" ] ; then
    check_file "$check_file_name"
elif [ -n "$commit_only" ] ; then
    # detect .git root directory
    my_dir="$(pwd)"
    while ! [ -d .git ] ; do
        cd ..
        if [ $(pwd) == "/" ] ; then
            cd "$my_dir"
            error_exit "help" "You are not inside the git repo"
        fi
    done
    # obtain files list
    files_to_check="$(git status --porcelain | grep '^ [MA]' | cut -c4-)"
    for fn in $files_to_check; do
        check_file "$fn"
    done
    cd $my_dir
else
    check_style '*.xcms'
    check_style '*.php'
    check_style '*.code'
    check_style '*.sh'
fi

if [ "$fail" == "yes" ] ; then
    echo "Code style checking failed, see the output for details"
    exit 1
fi