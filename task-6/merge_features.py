from itertools import izip
import json
from datetime import datetime

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


def merge(merged_json, key, value):
    if key == 'X-Parsed-By':
        if key in merged_json:
            merged_json[key] = list(merged_json[key]) + list(set(value) - set(merged_json[key]))
        else:
            merged_json[key] = value
    else:
        merged_json[key] = value
    return merged_json


def main():
    start_time = datetime.now()
    # Paths to all the parsers data
    data_files_paths = [
        '../../data-files/tika_content.json',
        '../../data-files/file_size_data.json',
        '../../data-files/tika_data.json'
    ]

    error_file = open('errors.txt', 'w+')
    merged_features_file = open('merged_features.json', 'w+')
    x = 0
    # Reading all line by line and merging them into a single file
    with open(data_files_paths[0]) as tika_data, open(data_files_paths[1]) as file_size_data, open(
            data_files_paths[2]) as tika_content_data:
        for a, b, c in izip(tika_data, file_size_data, tika_content_data):
            a = json.loads(a.strip())
            b = json.loads(b.strip())
            c = json.loads(c.strip())
            x += 1
            if a['id'] == b['id']:
                merged_json = {}
                for key, value in a.iteritems():
                    merged_json[key] = value
                for key, value in b.iteritems():
                    merged_json[key] = value
                for key, value in c.iteritems():
                    merged_json[key] = value
                json.dump(merged_json, merged_features_file)
                merged_features_file.write('\n')
            else:
                error_file.write('Error in line ' + str(x) + ':\n')
                error_file.write(
                    'tika_data[id]: ' + a['id'] + '  - tika_data[Content-Type]:' + a['Content-Type'] + '\n')
                error_file.write(
                    'file_size_data[id]: ' + b['id'] + '  - file_size_data[Content-Type]:' + b['Content-Type'] + '\n')
                error_file.write(
                    'Content[id]: ' + c['id'] + '  - Content[Content-Type]:' + c['Content-Type'] + '\n')
                break

    error_file.close()
    end_time = datetime.now()
    print(end_time - start_time)
    print('Merged ' + str(x) + ' files')


if __name__ == '__main__':
    main()
