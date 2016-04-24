from __future__ import division

import json
import os
from datetime import datetime

from tika import language

__author__ = "Antrromet"
__email__ = "antrromet@gmail.com"


def main():
    start_time = datetime.now()
    # Read the data from the following path
    data_files = '/Users/Antrromet/Documents/USC/Spring2016/CDA_CSCI599/Assignment_2/data/'

    dashboard_data = []
    # Write the response in the following file
    i = 0
    for path, dirs, files in os.walk(data_files):
        dirs.sort()
        path_spl = path.split('/')
        content_type = path_spl[len(path_spl) - 1].replace('_', '/')

        for f in sorted(files):
            if f not in '.DS_Store':
                if i >= 0:
                    i += 1
                    print(str(i) + '. ' + content_type + ' - ' + str(f))
                    lang = language.from_file(path + '/' + f)
                    added_lan = False
                    found_content = False
                    for item in dashboard_data:
                        if item['ContentType'] == content_type:
                            found_content = True
                            for lan in item['Languages']:
                                if lan == lang:
                                    added_lan = True
                                    val = item['Languages'][lang]
                                    item['Languages'][lang] = val + 1
                                    break
                            if not added_lan:
                                item['Languages'][lang] = 1
                    if not found_content:
                        dashboard_data.append({'ContentType': content_type, 'Languages': {lang: 1}})
                else:
                    i += 1

                if i % 1000 == 0:
                    print 'Parsed ' + str(i) + ' files'

    print json.dumps(dashboard_data, indent=4)
    end_time = datetime.now()
    print(end_time - start_time)
    output_file = open('language_diversity.data', 'w+')
    json.dump(dashboard_data, output_file)


if __name__ == '__main__':
    main()
