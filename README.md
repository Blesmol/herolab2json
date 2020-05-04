# herolab2json #

Python3 script to convert HeroLab Pathfinder characters to JSON to import into roll20

## Description ##

This script takes a HeroLab ``*.por`` file for Pathfinder 1st Edition and creates for each included character a JSON file that can be used on roll20 with the Pathfinder Community Character Sheet. Existing files with the same name will be overwritten.

## Requirements  ##

* Python 3
* Python 3 module ``xmltodict``
  ```
  pip3 install xmltodict
  ```

## Usage ##

```
hl2json.py [-h] [-j] [-x] [--html] [-t] [-d] file [file ...]

Extract Pathfinder characters from HeroLab files and store them locally in
various formats

positional arguments:
  file         HeroLab *.por file

optional arguments:
  -h, --help   show this help message and exit
  -j, --json   Extract JSON (Default if nothing else is selected)
  -x, --xml    Extract XML Statblock
  --html       Extract HTML Statblock
  -t, --text   Extract text statblock
  -d, --debug  Debug output
```
