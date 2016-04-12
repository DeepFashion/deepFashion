# Django specific settings
import os
import json,yaml
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from db.models import *
from db.serializer import *
import numpy as np
def insertNLPFeedback(data):
	serializer = nlpFeedbackSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		return serializer.data
	return serializer.errors

def insertPlanitFeedback(data):
	feedId=data['feedId']
	dataToInsert=dict()
	dataToInsert['init']=json.dumps((data['init']).tolist())
	dataToInsert['final']=json.dumps((data['final']).tolist())
	dataToInsert['trajInfo']=data['trajInfo']
	e2eFeed=e2eFeedback.objects.get(id=feedId)
	e2eFeed.planitFeedback.append(dataToInsert)
	e2eFeed.save()
	return dataToInsert

def exclusivePlanitFeedback(data):
	dataToInsert=dict()
	dataToInsert['init']=json.dumps((data['init']).tolist())
	dataToInsert['final']=json.dumps((data['final']).tolist())
	dataToInsert['trajInfo']=data['trajInfo']
	dataToInsert['envName']=data['envName']
	insertData=dict()
	insertData['planitFeedback']=dataToInsert
	serializer = planitFeedbackSerializer(data=insertData)
	if serializer.is_valid():
		serializer.save()
		return serializer.data
	return serializer.errors




def inserte2eFeedback(data):
	serializer = FeedBackSerializer(data=data)
	if serializer.is_valid():
		# feedback=e2eFeedback()
		# objList=feedback.__class__.objects.all().filter(feedId=data['feedId'])
		# print objList
		# if (len(objList)>0):
		# 	objList[0].tellmedaveOutput.append(data['tellmedaveOutput'][0])
		# 	objList[0].save()
		# else:
		# 	serializer.save()
		try:
			feedback=e2eFeedback.objects.get(envName=data['envName'],actualInput=data['actualInput'])
			feedback.tellmedaveOutput.append(data['tellmedaveOutput'][0])
			feedback.save()
		except:
			serializer.save()

		return serializer.data
	return serializer.errors

def insertTrajectory(data):
	serializer = trajectorySerializer(data=data)
	if serializer.is_valid():
		try:
			trajectory=trajectoryDatabase.objects.get(envName=data['envName'],objectFrom=data['objectFrom'],objectTo=data['objectTo'])
			trajectory.trajectory.append(data['trajectory'][0])
			trajectory.save()
			print 'here'
		except:
			serializer.save()
		
		return serializer.data
	return serializer.errors

def insertBestTrajectory(data):
	serializer = bestTrajectorySerializer(data=data)
	if serializer.is_valid():
		try:
			trajectory=bestTrajectoryDatabase.objects.get(envName=data['envName'],objectFrom=data['objectFrom'],objectTo=data['objectTo'])
			trajectory.bestTrajectory=data['bestTrajectory']
			trajectory.save()
		except:
			serializer.save()
		return serializer.data
	return serializer.errors

def insertObjects(data):
	serializer = objectSerializer(data=data)
	if serializer.is_valid():
		try:
			objectList=objectDatabase.objects.get(envName=data['envName'])
			objectList.objectsList=data['objectsList']
			objectList.save()
		except:
			serializer.save()
		return serializer.data
	return serializer.errors

def insertPlanitLog(data):
	serializer = planitLogSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		return serializer.data
	return serializer.errors

def insertObjectPosition(data):
	data['objectPosition']=json.dumps((data['objectPosition']).tolist())
	serializer = objectPositionSerializer(data=data)
	if serializer.is_valid():
		try:
			objectPos=objectPositionDatabase.objects.get(envName=data['envName'],objectName=data['objectName'])
			objectPos.objectPosition=data['objectPosition']
			objectPos.save()
		except:
			serializer.save()
		return serializer.data
	return serializer.errors

def getObjectPosition(data):
	try:
		objectPos=objectPositionDatabase.objects.get(envName=data['envName'],objectName=data['objectName'])
		result=yaml.safe_load(json.dumps(objectPos.to_json()))
		result['objectPosition']=np.asarray(json.loads(result['objectPosition']))
		return result
	except:
		return None


def gete2eFeedback(data):
	try:
		feedback=e2eFeedback.objects.get(envName=data['envName'],actualInput=data['actualInput'])
		return yaml.safe_load(json.dumps(feedback.to_json()))
	except:
		return None

def getTrajectory(data):
	try:
		trajectory=trajectoryDatabase.objects.get(envName=data['envName'],objectFrom=data['objectFrom'],objectTo=data['objectTo'])
		return yaml.safe_load(json.dumps(trajectory.to_json()))
	except:
		return None
def getBestTrajectory(data):
	try:
		trajectory=bestTrajectoryDatabase.objects.get(envName=data['envName'],objectFrom=data['objectFrom'],objectTo=data['objectTo'])
		return yaml.safe_load(json.dumps(trajectory.to_json()))
	except:
		return None
def getObjects(data):
	try:
		objectList=objectDatabase.objects.get(envName=data['envName'])
		return yaml.safe_load(json.dumps(objectList.to_json()))
	except:
		return None

def getPlanitFeedBack():
	feedback=planitFeedbackModel.objects.all()
	result=list()
	for feed in feedback:
		feed=yaml.safe_load(json.dumps(feed.to_json()))['planitFeedback']
		feed['init']=np.asarray(json.loads(feed['init']))
		feed['final']=np.asarray(json.loads(feed['final']))
		result.append(feed)
	return result

def deleteFeeds():
	feedback=planitFeedbackModel.objects.all()
	for feed in feedback

if __name__ == '__main__':
	# data={'NLPInstruction':'Hello World','envName':1}
	# print insertNLPFeedback(data)
	# print 

	# data={'envName':'env_1','actualInput':'HelloWorld','tellmedaveOutput':[['I1','I2','I3']],'videoPath':'randomVideoPath','feedId':'f1'}
	# print inserte2eFeedback(data)
	# print 

	# data={'envName':'env_1','actualInput':'HelloWorld','tellmedaveOutput':[['I1','I2','I3']],'videoPath':'randomVideoPath','feedId':'f2'}
	# print inserte2eFeedback(data)
	# print 

	# data={'envName':'env_1','actualInput':'HelloWorld','tellmedaveOutput':[['I4','I5','I6']],'videoPath':'randomVideoPath','feedId':'f2'}
	# print inserte2eFeedback(data)
	# print 

	# data={'envName':'env_1','objectFrom':'o1','objectTo':'o2','trajectory':['t3']}
	# print insertTrajectory(data)
	# print 

	# data={'envName':'env_1','objectFrom':'o1','objectTo':'o2','trajectory':['t4']}
	# print insertTrajectory(data)
	# print 

	# data={'envName':'env_1','objectFrom':'o1','objectTo':'o3','trajectory':['t4']}
	# print insertTrajectory(data)
	# print 


	# data={'envName':'env_1','objectFrom':'o1','objectTo':'o2','bestTrajectory':'t3'}
	# print insertBestTrajectory(data)
	# print 

	# data={'envName':'env_1','objectFrom':'o1','objectTo':'o2','bestTrajectory':'t4'}
	# print insertBestTrajectory(data)
	# print 

	# data={'envName':'env_1','objectFrom':'o1','objectTo':'o3','bestTrajectory':'t4'}
	# print insertBestTrajectory(data)
	# print 


	# data={'envName':'env_1','objectsList':['o1','o2']}
	# print insertObjects(data)
	# print 

	# data={'envName':'env_1','objectsList':['o3','o4']}
	# print insertObjects(data)
	# print 

	# data={'envName':'env_1','objectsList':['o3','o4']}
	# print insertObjects(data)
	# print 

	# data={'initialWeight':{'a':'1'},'feedback':{'a':'1'},'finalWeight':{'a':'1'}}
	# print insertPlanitLog(data)
	# print 

	# data={'initialWeight':{'a':'1'},'feedback':{'a':'1'},'finalWeight':{'a':'1'}}
	# print insertPlanitLog(data)
	# print 

	# print gete2eFeedback({'envName':'env_1','actualInput':'HelloWorld'})
	# print getTrajectory({'envName':'env_1','objectFrom':'o1','objectTo':'o2'})
	# print getBestTrajectory({'envName':'env_1','objectFrom':'o1','objectTo':'o2'})
	# print getObjects({'envName':'env_1'})

	# data={'envName':'env_1','objectName':'HelloWorld','objectPosition':np.array([2,3,1,0])}
	# print insertObjectPosition(data)

	# print getObjectPosition({'envName':'env_1','objectName':'HelloWorld'})

	# print exclusivePlanitFeedback({'envName':'env_1','trajInfo':'HelloWorld','init':np.array([2,3,1,0]),'final':np.array([2,3,1,0])})


	print getPlanitFeedBack()





