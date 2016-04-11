# Django specific settings
import os
import json,yaml
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from db.models import *

def InsertData(data):
	try:
		prod=products.objects.get(imageName=data['imageName'])
		prod.similarProducts=json.dumps(data['similarProducts'])
		prod.tags=json.dumps(data['tags'])
		prod.crossProducts=json.dumps(data['crossProducts'])
		prod.save()
	except:
		prod=products(imageName=data['imageName'],similarProducts=json.dumps(data['similarProducts']),tags=json.dumps(data['tags']),crossProducts=json.dumps(data['crossProducts']))
		prod.save()
	return True

def getData(imageName):
	try:
		prod=products.objects.get(imageName=data['imageName'])
		return prod.to_json()
	except:
		return None

if __name__ == '__main__':
	data=dict()
	data['imageName']='h1'
	data['similarProducts']=list()
	entry=dict()
	entry['h1']='h1'
	data['similarProducts'].append(entry)

	data['crossProducts']=list()
	entry=dict()
	entry['h1']='h1'
	data['crossProducts'].append(entry)

	data['tags']=list()
	data['tags'].append('hello')


	print InsertData(data)
	print getData('h1')
	print getData('h2')
	













