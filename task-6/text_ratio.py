from __future__ import division

import json
import math
import sys
from datetime import datetime

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


def calculate_size():
    print('Calculating size')
    merged_file_path = 'merged_features.json'
    temp_size = open('temp_size.json', 'w+')
    i = 0
    max_size = {}
    with open(merged_file_path) as lines:
        for line in lines:
            i += 1
            json_line = json.loads(line.strip())
            if 'content' in json_line:
                content_size = sys.getsizeof(json_line['content'])
            else:
                content_size = 0
            content_type = json_line['Content-Type'].split(';')[0]
            new_json = {'id': json_line['id'], 'Content-Type': content_type}
            if 'X-Parsed-By' in json_line:
                new_json['X-Parsed-By'] = json_line['X-Parsed-By']
            if 'normalized_file_size' in json_line:
                new_json['normalized_file_size'] = json_line['normalized_file_size']
            if content_type in max_size:
                if content_size > max_size[content_type]:
                    max_size[content_type] = content_size
            else:
                max_size[content_type] = content_size
            new_json['content_size'] = content_size
            json.dump(new_json, temp_size)
            temp_size.write('\n')
    print('Calculated size for ' + str(i) + ' files')
    return max_size


def normalize_size(max_size):
    print('Normalizing size')
    temp_ratio = 'temp_size.json'
    ratio_file = open('size.json', 'w+')
    i = 0
    with open(temp_ratio) as lines:
        for line in lines:
            i += 1
            json_line = json.loads(line.strip())
            content_type = json_line['Content-Type']
            new_json = {'id': json_line['id'], 'Content-Type': content_type,
                        'normalized_file_size': json_line['normalized_file_size']}
            if 'X-Parsed-By' in json_line:
                new_json['X-Parsed-By'] = json_line['X-Parsed-By']
            try:
                normalized_size = json_line['content_size'] / max_size[content_type]
            except ZeroDivisionError:
                # Because no content was obtained for octet-stream files
                normalized_size = 0
            normalized_size = math.sqrt(normalized_size)
            new_json['normalized_content_size'] = normalized_size
            json.dump(new_json, ratio_file)
            ratio_file.write('\n')
    print('Normalized size for ' + str(i) + ' files')


def main():
    start_time = datetime.now()

    max_size = calculate_size()
    normalize_size(max_size)

    end_time = datetime.now()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
