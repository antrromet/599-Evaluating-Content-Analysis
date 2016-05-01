from nltk.tag import RegexpTagger
from nltk.tokenize import RegexpTokenizer
from tika import parser, detector
import re
import argparse
import os
import fnmatch
import json


def get_measurement_range_map(measurements):
    measuretags = set([x[1] for x in measurements])
    measuretag_values = dict([(x, []) for x in measuretags])
    pattern = r'-?[0-9]+([\.0-9]+)?'
    [measuretag_values[x[1]].append(float(re.match(pattern, x[0]).group())) for x in measurements]
    return map(lambda measuretag, values: {'title': measuretag, 'measures': [min(values), max(values)]},
               measuretag_values.keys(), measuretag_values.values())


def get_measurements(filename):
    parser_obj = parser.from_file(filename)
    if 'content' in parser_obj and parser_obj['content']:
        return [x for x in regextagger.tag(tokenizer.tokenize(parser_obj['content'])) if x[1] != 'OTHER']


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-dir', '--rootdir', required=True, help='Please enter a rootdir')
    args = args_parser.parse_args()

    regextagger = RegexpTagger([
        # (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(kmph|km/hr|kms/hr|kilometers/hr|kilometer/hr)$)','KMPH'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(cm|cms|centimeter|centimeters|centimetre|centimetres)$)', 'CM'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(km|kms|kilometer|kilometers|kilometre|kilometres)$)', 'KM'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(mm|mms|millimeter|millimeters|millimetre|millimetres)$)', 'MM'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(m|meter|meters|metre|metres)$)', 'METER'),
        (r"(?i)(^[0-9]+(.[0-9]+)?\s*(ft|feet|foot|\')$)", 'FEET'),
        # (r'(?i)(^[0-9]+(.[0-9]+)?\s*(inch|inches|\")$)','INCH'),
        # (r'(?i)(^[0-9]+(.[0-9]+)?\s*(yard|yards|yd|yds)$)','YARD'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(mile|miles)$)', 'MILE'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(second|seconds|s|sec|secs)$)', 'SEC'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(minute|minutes|mins|min)$)', 'MIN'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(hour|hours|hr|hrs)$)', 'HOUR'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(day|days)$)', 'DAY'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(year|years|yr|yrs)$)', 'YEAR'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(month|months)$)', 'MONTH'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(week|weeks|wk|wks)$)', 'WEEK'),
        (r'(?i)(^[0-9]+(.[0-9]+)?\s*(gram|gramme|gm|gms|g|grams|grammes|gs)$)', 'GRAM'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(kilogram|kilogramme|kg|kilograms|kilogrammes|kgs)$)', 'KG'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(milligram|milligramme|mg|milligrams|milligrammes|mgs)$)', 'MG'),
        # (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(ton|tons|tonne|tonnes)$)','TON'),
        # (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(pounds|pound|lb|lbs)$)','POUND'),
        # (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(pounds|pound|lb|lbs)$)','LITRE'),
        # \(r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(pounds|pound|lb|lbs)$)','GALLON'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(celcius|c|deg.celcius|deg.c)$)', 'CELCIUS'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(farenheit|f|deg.farenheit|deg.f|degree|deg)$)', 'FARENHEIT'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(kelvin|k|deg.kelvin|deg.k)$)', 'KELVIN'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(volt|volts|V)$)', 'VOLTS'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(ampere|amperes|A|amps|amp)$)', 'AMPS'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(watt|watts|W)$)', 'WATT'),
        (r'(?i)(^-?[0-9]+(.[0-9]+)?\s*(kilowatt|kilowatts|kW)$)', 'kW'),
        (r'.*', 'OTHER')])

    tokenizer = RegexpTokenizer('-?[0-9]+(\.[0-9]+)?\s*(\w|/)+')

    filenames = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(args.rootdir) for f in
                 fnmatch.filter(files, '*')]
    measurements = [y for x in filter(lambda content: content, map(get_measurements, filenames)) for y in x]
    with open('ner_spectrum.json', 'w') as f:
        json.dump(get_measurement_range_map(measurements), f)
