#!/usr/bin/env bash
set -e
VALIDATOR="python site-validate.py -v"

BASE="http://fizlesh.ru"

function validate()
{
    $VALIDATOR "${BASE}$1"
    sleep 10
}

validate ""
validate "/?page=z01News"
validate "/?page=z024Official"
validate "/?page=z025AboutUs"
validate "/?page=z026Life"
validate "/?page=z03Education"
validate "/?page=z03Education/2006"
validate "/?page=z03Education/2007"
validate "/?page=z03Education/2008"
validate "/?page=z03Education/2009"
validate "/?page=z03Education/2010"
validate "/?page=z03Education/lectures2011"
validate "/?page=z03Education/lesh-practicum"
validate "/?page=z027Equipment"
validate "/?page=z027Equipment/cloth"
validate "/?page=z027Equipment/docs"
validate "/?page=z027Equipment/equip"
validate "/?page=z027Equipment/stuff"
validate "/?page=z027Equipment/stuff"
validate "/?page=z04Science"
validate "/?page=z060JoinUs"
validate "/?page=z065Photoalbum"
validate "/?page=z066Humor"
validate "/?page=z07Links"
validate "/?page=z08Contact"
