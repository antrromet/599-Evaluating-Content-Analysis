from __future__ import division

import json

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


def main():
    orig_data = open('language_diversity.data', 'r')
    new_data_file = open('fixed_data.json', 'w+')

    languages = ['be', 'ca', 'da', 'de', 'en', 'eo', 'es', 'et', 'fa', 'fi', 'fr', 'gl', 'hu', 'is', 'it', 'lt', 'nl',
                 'no', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sv', 'th', 'uk']

    orig_data = json.load(orig_data)
    new_data = []
    for item in orig_data:
        new_item = {'ContentType': item['ContentType'], 'Languages': {}}
        for lan in languages:
            val = 0
            if lan in item['Languages']:
                val = item['Languages'][lan]
            new_item['Languages'][lan] = val
        new_data.append(new_item)

    print json.dumps(new_data, indent=4)
    json.dumps(new_data, new_data_file)


if __name__ == '__main__':
    main()
