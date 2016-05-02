import json
import codecs

def parseJSON(filename,ID):
	data = []
	ignore = ['X-Parsed-By','Content-Type']

	with open(filename,'r+') as json_fp:
		for line in json_fp:
			data.append(json.loads(line))

	#data = data[23675:23678]
	instances = {}
	count  = 0

	for line in data:
		count += 1
		id_key = line['id']
		instances[id_key] = set()
		print count
		for key in line:
			if key in ignore:
				continue
			if isinstance(line[key],list):
				for item in line[key]:
					#item = item.decode('utf-8')
					instances[id_key].add(item)
			else:
				#item = line[key].decode('utf-8')
				item = line[key]
				instances[id_key].add(item)

	#print "instances:",instances
	'''
	fp = codecs.open(ID+'.txt','w+','utf8')
	for item in instances:
			fp.write(item + '\n')
	'''

	return instances


def writeJSON(data,ID):
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
	nltk_data_map = parseJSON('nltksample.json','nltk')
	onlp_data_map = parseJSON('opennlpsample.json','onlp')
	cnlp_data_map = parseJSON('corenlpsample.json','cnlp')

	uniques = {}

	for key in nltk_data_map:
		uniques[key] = set.intersection(nltk_data_map[key],onlp_data_map,cnlp_data_map[key])

	print uniques
	#uniques = set.intersection(nltk_data,cnlp_data)
	writeJSON(uniques,'final_intersected_id_sample')




getAgreement()
#parseJSON('corenlp_data_full.json','cnlp')