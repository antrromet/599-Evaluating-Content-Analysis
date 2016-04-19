from __future__ import division
import json
import math
import os
from datetime import datetime

import sys

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


def calculate_ratio():
    print('Calculating ratios')
    merged_file_path = '../../data-files/merged_features.json'
    temp_ratio = open('temp_ratio.json', 'w+')
    i = 0
    max_ratio = {}
    with open(merged_file_path) as lines:
        for line in lines:
            i += 1
            solr_index_size = sys.getsizeof(line)
            json_line = json.loads(line.strip())
            content_type = json_line['Content-Type']
            content_type = content_type.split(';')[0]
            new_json = {'id': json_line['id'], 'Content-Type': content_type}
            file_size = json_line['file_size']
            ratio = solr_index_size / file_size
            if content_type in max_ratio:
                if ratio > max_ratio[content_type]:
                    max_ratio[content_type] = ratio
            else:
                max_ratio[content_type] = ratio
            new_json['ratio'] = ratio
            json.dump(new_json, temp_ratio)
            temp_ratio.write('\n')
    print('Calculated ratio for ' + str(i) + ' files')
    return max_ratio


def normalize_ratio(max_ratio):
    print('Normalizing ratios')
    temp_ratio = 'temp_ratio.json'
    ratio_file = open('ratio.json', 'w+')
    i = 0
    with open(temp_ratio) as lines:
        for line in lines:
            i += 1
            json_line = json.loads(line.strip())
            content_type = json_line['Content-Type']
            new_json = {'id': json_line['id'], 'Content-Type': content_type}
            ratio = json_line['ratio']
            ratio = ratio / max_ratio[content_type]
            ratio = math.sqrt(ratio)
            new_json['ratio'] = ratio
            json.dump(new_json, ratio_file)
            ratio_file.write('\n')
    print('Normalized ratio for ' + str(i) + ' files')


def prepare_d3_data():
    print('Preparing D3 data')
    bar_chart_data = [
        {"name": "text/plain", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/xhtml+xml", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/msword", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0,
         "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "video/quicktime", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "audio/mpeg", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "image/jpeg", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/fits", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/mp4", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/xml", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "image/gif", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "video/mp4", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/pdf", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/x-netcdf", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/rss+xml", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "image/png", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "application/octet-stream", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0},
        {"name": "text/html", "0-0.05": 0, "0.05-0.1": 0, "0.1-0.15": 0, "0.15-0.2": 0, "0.2-0.25": 0,
         "0.25-0.3": 0, "0.3-0.35": 0, "0.35-0.4": 0, "0.4-0.45": 0, "0.45-0.5": 0, "0.5-0.55": 0, "0.55-0.6": 0,
         "0.6-0.65": 0, "0.65-0.7": 0, "0.7-0.75": 0, "0.75-0.8": 0, "0.8-0.85": 0, "0.85-0.9": 0, "0.9-0.95": 0,
         "0.95-1": 0}]

    with open('ratio.json') as lines:
        for line in lines:
            json_line = json.loads(line.strip())
            content_type = json_line['Content-Type']
            for child in bar_chart_data:
                if child['name'] == content_type:
                    ratio = json_line['ratio']
                    rang = ''
                    if ratio <= 0.05:
                        rang = "0-0.05"
                    elif ratio <= 0.1:
                        rang = "0.05-0.1"
                    elif ratio <= 0.15:
                        rang = "0.1-0.15"
                    elif ratio <= 0.2:
                        rang = "0.15-0.2"
                    elif ratio <= 0.25:
                        rang = "0.2-0.25"
                    elif ratio <= 0.3:
                        rang = "0.25-0.3"
                    elif ratio <= 0.35:
                        rang = "0.3-0.35"
                    elif ratio <= 0.4:
                        rang = "0.35-0.4"
                    elif ratio <= 0.45:
                        rang = "0.4-0.45"
                    elif ratio <= 0.5:
                        rang = "0.45-0.5"
                    elif ratio <= 0.55:
                        rang = "0.5-0.55"
                    elif ratio <= 0.6:
                        rang = "0.55-0.6"
                    elif ratio <= 0.65:
                        rang = "0.6-0.65"
                    elif ratio <= 0.7:
                        rang = "0.65-0.7"
                    elif ratio <= 0.75:
                        rang = "0.7-0.75"
                    elif ratio <= 0.8:
                        rang = "0.75-0.8"
                    elif ratio <= 0.85:
                        rang = "0.8-0.85"
                    elif ratio <= 0.9:
                        rang = "0.85-0.9"
                    elif ratio <= 0.95:
                        rang = "0.9-0.95"
                    elif ratio <= 1:
                        rang = "0.95-1"
                    child[rang] += 1
    print('Writing D3 data files')
    write_bar_chart_files(bar_chart_data)


def write_bar_chart_files(bar_chart_data):
    for child in bar_chart_data:
        name = child['name']
        name = name.replace('/', '_')
        if not os.path.exists('bar_chart_data'):
            os.makedirs('bar_chart_data')
        with open('bar_chart_data/' + name + '_data.tsv', 'w+') as data_file:
            data_file.write('Range\tFrequency\n')
            data_file.write("0-0.05" + '\t' + str(child["0-0.05"]) + '\n')
            data_file.write("0.05-0.1" + '\t' + str(child["0.05-0.1"]) + '\n')
            data_file.write("0.1-0.15" + '\t' + str(child["0.1-0.15"]) + '\n')
            data_file.write("0.15-0.2" + '\t' + str(child["0.15-0.2"]) + '\n')
            data_file.write("0.2-0.25" + '\t' + str(child["0.2-0.25"]) + '\n')
            data_file.write("0.25-0.3" + '\t' + str(child["0.25-0.3"]) + '\n')
            data_file.write("0.3-0.35" + '\t' + str(child["0.3-0.35"]) + '\n')
            data_file.write("0.35-0.4" + '\t' + str(child["0.35-0.4"]) + '\n')
            data_file.write("0.4-0.45" + '\t' + str(child["0.4-0.45"]) + '\n')
            data_file.write("0.45-0.5" + '\t' + str(child["0.45-0.5"]) + '\n')
            data_file.write("0.5-0.55" + '\t' + str(child["0.5-0.55"]) + '\n')
            data_file.write("0.55-0.6" + '\t' + str(child["0.55-0.6"]) + '\n')
            data_file.write("0.6-0.65" + '\t' + str(child["0.6-0.65"]) + '\n')
            data_file.write("0.65-0.7" + '\t' + str(child["0.65-0.7"]) + '\n')
            data_file.write("0.7-0.75" + '\t' + str(child["0.7-0.75"]) + '\n')
            data_file.write("0.75-0.8" + '\t' + str(child["0.75-0.8"]) + '\n')
            data_file.write("0.8-0.85" + '\t' + str(child["0.8-0.85"]) + '\n')
            data_file.write("0.85-0.9" + '\t' + str(child["0.85-0.9"]) + '\n')
            data_file.write("0.9-0.95" + '\t' + str(child["0.9-0.95"]) + '\n')
            data_file.write("0.95-1" + '\t' + str(child["0.95-1"]) + '\n')


def main():
    start_time = datetime.now()

    max_ratio = calculate_ratio()
    normalize_ratio(max_ratio)
    prepare_d3_data()

    end_time = datetime.now()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
