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
hl2json.py <HeroLab File>
```
