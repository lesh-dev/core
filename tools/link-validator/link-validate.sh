#!/usr/bin/env bash

# (c) fizlesh.ru dev team
# maintainer: vdm (vdm-photo@ya.ru)

if ! [ "$1" ]; then
	echo "This script validates specified site and checks link integrity."
	echo "Syntax: $0 <url-to-validate>"
	exit 1
fi

URL="$1"
LOG="validate.log"
BROKEN="broken.log"
wget --exclude-directories="/forum" --no-verbose --spider -r $URL -o "$LOG"

if grep -B2 "broken link!" "$LOG" > "$BROKEN"; then
	echo "ERROR! Broken links detected! See files '$BROKEN' and '$LOG' for details."
	exit 1
else
	echo "No broken links found"
	rm -f "$BROKEN"
	exit 0
fi
