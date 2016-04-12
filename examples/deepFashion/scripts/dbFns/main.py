# Django specific settings
import os
import json,yaml
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from db.models import *

def InsertData(data,mode):
	try:
		prod=products.objects.get(imageName=data['imageName'])
		if mode=="similar":
			prod.similarProducts=json.dumps(data['similarProducts'])
		if mode=="tags":
			prod.tags=json.dumps(data['tags'])
		if mode=="cross":
			prod.crossProducts=json.dumps(data['crossProducts'])
		prod.save()
	except:
		prod=products(imageName=data['imageName'],similarProducts=json.dumps(data['similarProducts']),tags=json.dumps(data['tags']),crossProducts=json.dumps(data['crossProducts']))
		prod.save()
	return True

def getData(imageName,mode):
	try:
		prod=products.objects.get(imageName=data['imageName'])
		result=prod.to_json()
		if mode=="similar" and len(result['similarProducts'])>0:
			return result
		if mode=="cross" and len(result['crossProducts'])>0:
			return result
		if mode=="tags" and len(result['tags'])>0:
			return result
		return None 
	except:
		return None

if __name__ == '__main__':
	# data=dict()
	# data['imageName']='h1'
	# data['similarProducts']=list()
	# entry=dict()
	# entry['h1']='h1'
	# data['similarProducts'].append(entry)

	# data['crossProducts']=list()
	# entry=dict()
	# entry['h1']='h1'
	# data['crossProducts'].append(entry)

	# data['tags']=list()
	# data['tags'].append('hello')


	# print InsertData(data)
	# print getData('h1')
	# print getData('h2')
	imageHash="myhasgh"
	getData(imageHash,"tags")
	InsertData({'imageName':imageHash,'similarProducts':[],'crossProducts':[],'tags':['t1','t2']},mode="tags")
	getData(imageHash,"similar")
	InsertData({'imageName':imageHash,'similarProducts':[{'h1':'h1'},{'h2':'h2'}],'crossProducts':[],'tags':[]},mode="similar")
	getData(imageHash,"tags")
	getData(imageHash,"similar")


	













