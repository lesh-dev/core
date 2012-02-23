#!/bin/bash
set -e 
VALIDATOR="python site-validate.py"

BASE="http://fizlesh.ru"
$VALIDATOR "$BASE"
$VALIDATOR "$BASE/?page=z03Education"
$VALIDATOR "$BASE/?page=z01News"
$VALIDATOR "$BASE/?page=z025AboutUs"
$VALIDATOR "$BASE/?page=z026Life"
$VALIDATOR "$BASE/?page=z027Equipment"
$VALIDATOR "$BASE/?page=z027Equipment/cloth"
$VALIDATOR "$BASE/?page=z027Equipment/docs"
$VALIDATOR "$BASE/?page=z027Equipment/equip"
$VALIDATOR "$BASE/?page=z027Equipment/stuff"
