#!/bin/bash
#
# Convert diff output to colorized HTML.

cat <<EOF
<pre>
EOF

echo -n '<span style="color: gray">'

first=1
diffseen=0
lastonly=0

OIFS=$IFS
IFS='
'

# The -r option keeps the backslash from being an escape char.
read -r s

while [[ $? -eq 0 ]]
do
    # Get beginning of line to determine what type
    # of diff line it is.
    t1=${s:0:1}
    t2=${s:0:2}
    t3=${s:0:3}
    t4=${s:0:4}
    t7=${s:0:7}

    # Determine HTML class to use.
    if [[ "$t7" == 'Only in' ]]; then
        cls='color: purple;' # only
        if [[ $diffseen -eq 0 ]]; then
            diffseen=1
            echo -n '</span>'
        else
            if [[ $lastonly -eq 0 ]]; then
                echo "</div>"
            fi
        fi
        if [[ $lastonly -eq 0 ]]; then
            echo "<div style=''>" # diff-div
        fi
        lastonly=1
    elif [[ "$t4" == 'diff' ]]; then
        cls='color: #8a2be2; display: none;' # diff
        if [[ $diffseen -eq 0 ]]; then
            diffseen=1
            echo -n '</span>'
        else
            echo "</div>"
        fi
        echo "<div style=''>" # diff-div
        lastonly=0
    elif [[ "$t3" == '+++' ]]; then
        cls='color: maroon;' # plus3
        lastonly=0
    elif [[ "$t3" == '---' ]]; then
        cls='color: blue;' # minus3
        lastonly=0
    elif [[ "$t2" == '@@' ]]; then
        cls='color: lime;' # at2
        lastonly=0
    elif [[ "$t1" == '+' ]]; then
        cls='color: green;' # plus
        lastonly=0
    elif [[ "$t1" == '-' ]]; then
        cls='color: red;' # minus
        lastonly=0
    else
        cls=
        lastonly=0
    fi

    # Convert &, <, > to HTML entities.
    s=$(sed -e 's/\&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' <<<"$s")
    if [[ $first -eq 1 ]]; then
        first=0
    else
        echo
    fi

    # Output the line.
    if [[ "$cls" ]]; then
        echo -n '<span style="'${cls}'">'${s}'</span>'
    else
        echo -n ${s}
    fi
    read -r s
done
IFS=$OIFS

if [[ $diffseen -eq 0 && $onlyseen -eq 0 ]]; then
    echo -n '</span>'
else
    echo "</div>"
fi
echo

cat <<EOF
</pre>
EOF
