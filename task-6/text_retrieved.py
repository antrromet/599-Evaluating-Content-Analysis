from __future__ import division

import json
from datetime import datetime

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


# Return the range in words depending upon the size. The range is spread out into 20 categories from 0-1
def get_range(size):
    rang = ''
    if size <= 0.05:
        rang = "0-0.05"
    elif size <= 0.1:
        rang = "0.05-0.1"
    elif size <= 0.15:
        rang = "0.1-0.15"
    elif size <= 0.2:
        rang = "0.15-0.2"
    elif size <= 0.25:
        rang = "0.2-0.25"
    elif size <= 0.3:
        rang = "0.25-0.3"
    elif size <= 0.35:
        rang = "0.3-0.35"
    elif size <= 0.4:
        rang = "0.35-0.4"
    elif size <= 0.45:
        rang = "0.4-0.45"
    elif size <= 0.5:
        rang = "0.45-0.5"
    elif size <= 0.55:
        rang = "0.5-0.55"
    elif size <= 0.6:
        rang = "0.55-0.6"
    elif size <= 0.65:
        rang = "0.6-0.65"
    elif size <= 0.7:
        rang = "0.65-0.7"
    elif size <= 0.75:
        rang = "0.7-0.75"
    elif size <= 0.8:
        rang = "0.75-0.8"
    elif size <= 0.85:
        rang = "0.8-0.85"
    elif size <= 0.9:
        rang = "0.85-0.9"
    elif size <= 0.95:
        rang = "0.9-0.95"
    elif size <= 1:
        rang = "0.95-1"
    return rang


# Generate D3 data
def generate_d3_data():
    merged_file_path = 'size.json'
    output_file = open('text_retrieved.json', 'w+')
    flare = {'name': 'flare', 'description': 'Parser call chain vs amount of text retrieved', 'children': []}
    with open(merged_file_path) as lines:
        for line in lines:
            json_line = json.loads(line.strip())
            if 'X-Parsed-By' in json_line:
                x_parsed_by = json_line['X-Parsed-By']
                rang = get_range(json_line['normalized_file_size'])
                if 'normalized_content_size' in json_line:
                    text_range = get_range(json_line['normalized_content_size'])
                else:
                    text_range = 0
                mime_type = json_line['Content-Type'].split(';')[0]
                x_parsed_by = json.dumps(x_parsed_by)
                parser_added = False
                for child in flare['children']:
                    if child['name'] == x_parsed_by:
                        size_child_added = False
                        size_children = child['children']
                        for size_child in size_children:
                            if size_child['name'] == rang:
                                mimetype_added = False
                                mimetype_children = size_child['children']
                                for mimetype_child in mimetype_children:
                                    if mimetype_child['name'] == mime_type:
                                        metadata_added = False
                                        metadata_children = mimetype_child['children']
                                        for metadata_child in metadata_children:
                                            if metadata_child['name'] == text_range:
                                                metadata_added = True
                                                val = metadata_child['size']
                                                metadata_child['size'] = val + 1
                                                break
                                        if not metadata_added:
                                            metadata_children.append(
                                                {'name': text_range, 'description': 'Amount of Text retrieved',
                                                 'size': 1})

                                        mimetype_added = True
                                        break
                                if not mimetype_added:
                                    mimetype_children.append(
                                        {'name': mime_type, 'description': 'MIME Type', 'children': [
                                            {'name': text_range, 'description': 'Amount of Text retrieved',
                                             'size': 1}]})

                                size_child_added = True
                                break
                        if not size_child_added:
                            size_children.append({'name': rang, 'description': 'Normalized File Size', 'children': [
                                {'name': mime_type, 'description': 'MIME Type',
                                 'children': [{'name': text_range, 'description': 'Amount of Text retrieved',
                                               'size': 1}]}]})
                        parser_added = True
                        break
                if not parser_added:
                    flare['children'].append({'name': x_parsed_by, 'description': 'Parser Call Chain', 'children': [
                        {'name': rang, 'description': 'Normalized File Size',
                         'children': [{'name': mime_type, 'description': 'MIME Type', 'children': [
                             {'name': text_range, 'description': 'Amount of Text retrieved', 'size': 1}]}]}]})
    json.dump(flare, output_file)


def main():
    start_time = datetime.now()

    generate_d3_data()

    end_time = datetime.now()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
