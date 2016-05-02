import json
import codecs

def parseJSON(filename,ID):
	data = []
	ignore = ['X-Parsed-By','id','Content-Type']

	with open(filename,'r+') as json_fp:
		for line in json_fp:
			data.append(json.loads(line))

	#data = data[23675:23678]
	instances = set()
	count  = 0

	for line in data:
		count += 1
		print count
		for key in line:
			if key in ignore:
				continue
			if isinstance(line[key],list):
				for item in line[key]:
					#item = item.decode('utf-8')
					instances.add(item)
			else:
				#item = line[key].decode('utf-8')
				item = line[key]
				instances.add(item)

	#print "instances:",instances
	'''
	fp = codecs.open(ID+'.txt','w+','utf8')
	for item in instances:
			fp.write(item + '\n')
	'''

	return instances


def writeSets(data,ID):
	fp = codecs.open(ID+'.txt','w+','utf8')
	for item in data:
			fp.write(item + '\n')

def readTemp(filename):
	data = set()
	with open(filename,'r') as fp:
		for item in fp:
			data.add(item)

	return data


def getAgreement():
	nltk_data = parseJSON('nltk_data_full.json','nltk')
	onlp_data = parseJSON('opennlp_data_full.json','onlp')
	cnlp_data = parseJSON('corenlp_data_full.json','cnlp')

	uniques = set()

	uniques = set.intersection(nltk_data,onlp_data,cnlp_data)
	writeSets(nltk_data, 'nltk_data_file')
	writeSets(cnlp_data, 'corenlp_data_file')
	writeSets(onlp_data, 'opennlp_data_file')
	writeSets(uniques,'final_intersected')




getAgreement()
