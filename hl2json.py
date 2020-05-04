#!/usr/bin/env python3

import xmltodict
import json
import sys
import zipfile
import os
import argparse

def main():
    ap = argparse.ArgumentParser(description='Extract Pathfinder characters from HeroLab files and store them locally in various formats')
    ap.add_argument('file', help='HeroLab *.por file', nargs='+')
    ap.add_argument('-j', '--json', help='Extract JSON (Default if nothing else is selected)', action='store_true')
    ap.add_argument('-x', '--xml', help='Extract XML Statblock', action='store_true')
    ap.add_argument(      '--html', help='Extract HTML Statblock', action='store_true')
    ap.add_argument('-t', '--text', help='Extract text statblock', action='store_true')
    ap.add_argument('-d', '--debug', help='Debug output', action='store_true')
    args = ap.parse_args()

    # set json output as default if no other output flags were set
    if not args.xml and not args.html and not args.text:
        args.json = True

    for hl_filename in args.file:
        hl_basename = os.path.splitext(hl_filename)[0]

        assert zipfile.is_zipfile(hl_filename)
        with zipfile.ZipFile(hl_filename, 'r') as zip:
            num_chars = get_number_of_chars(zip) # not yet used

            infolist = zip.infolist()
            for entry in infolist:
                if args.debug:
                    print(str(entry))

                if not entry.filename.startswith('statblocks_'):
                    continue

                char_name = get_char_name(entry.filename)
                if hl_basename != char_name:
                    base_output_filename = '{} - {}'.format(hl_basename, char_name)
                else:
                    base_output_filename = hl_basename

                if args.html and entry.filename.startswith('statblocks_html'):
                    extract_into_file(zip, entry.filename, base_output_filename, 'html')

                if args.text and entry.filename.startswith('statblocks_text'):
                    extract_into_file(zip, entry.filename, base_output_filename, 'txt')

                if args.xml and entry.filename.startswith('statblocks_xml'):
                    extract_into_file(zip, entry.filename, base_output_filename, 'xml')

                if args.json and entry.filename.startswith('statblocks_xml'):
                    data = zip.read(entry.filename)

                    json_filename = '{}.json'.format(base_output_filename)
                    with open(json_filename, 'w') as json_file:
                        data_dict = xmltodict.parse(data, attr_prefix='_', postprocessor=(
                            lambda _, key, value: (key if key else "", value if value else ""))
                        )
                        json_file.write(json.dumps(data_dict, indent='\t'))

def extract_into_file(zip, zip_filename, output_basename, output_extension):
    output_filename = '{}.{}'.format(output_basename, output_extension)
    with open(output_filename, 'wb') as file:
        data = zip.read(zip_filename)
        file.write(data)

def get_char_name(full_filename):
    filename = os.path.basename(full_filename)
    base_filename = os.path.splitext(filename)[0]

    # Char filenames in HeroLab have pattern '<index>_<char>.<ext>'
    # If the char name contains spaces, they are replace by underscores

    prefix_endpos = base_filename.find('_')
    assert prefix_endpos != -1
    return base_filename[prefix_endpos+1:].replace('_', ' ')

def get_number_of_chars(zip):
    count = 0
    for entry in zip.infolist():
        if entry.filename.startswith('statblocks_xml'):
            count+=1
    return count

if __name__=="__main__":
    main()
