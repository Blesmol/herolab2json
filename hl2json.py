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
    ap.add_argument('-x', '--xml', help='Extract XML', action='store_true')
    args = ap.parse_args()

    # set json output as default
    if not args.xml:
        args.json = True

    for hl_filename in args.file:
        hl_basename = os.path.splitext(hl_filename)[0]

        assert zipfile.is_zipfile(hl_filename)
        with zipfile.ZipFile(hl_filename, 'r') as zip:
            infolist = zip.infolist()
            for entry in infolist:
                if entry.filename.startswith('statblocks_xml'):
                    data = zip.read(entry.filename)
                    base_source_filename = os.path.splitext(os.path.basename(entry.filename))[0]

                    prefix_endpos = base_source_filename.find('_')
                    assert prefix_endpos != -1
                    char_name = base_source_filename[prefix_endpos+1:]

                    base_output_filename = '{} - {}'.format(hl_basename, char_name)

                    if args.xml:
                        xml_filename = '{}.xml'.format(base_output_filename)
                        with open(xml_filename, 'wb') as xml_file:
                            xml_file.write(data)

                    if args.json:
                        json_filename = '{}.json'.format(base_output_filename)
                        with open(json_filename, 'w') as json_file:
                            data_dict = xmltodict.parse(data, attr_prefix='_', postprocessor=(
                                lambda _, key, value: (key if key else "", value if value else ""))
                            )
                            json_file.write(json.dumps(data_dict, indent='\t'))


if __name__=="__main__":
    main()
