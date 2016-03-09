import os
import shutil
from os import listdir
from os.path import isfile, join
import json
import re

def findAndReplace(filename,find,replace):
	with open(filename, 'r') as content_file:
		contents = content_file.readlines()
	res=""
	for line in contents:
		line = re.sub(find,replace, line.rstrip())
		res+=line
	# saveFilename=".".join(filename.split('.')[:-1])
	with open(filename,'w+') as f:
		f.write(res)

def configureJson(ROOT,PROJECT,DB,settingFileName):
	PATH=ROOT+"/"+PROJECT+"/"
	DBPATH=DB+PROJECT+"/"
	settings=dict()
	settings["RESIZE"] = 256
	settings["TOP_K"] = 30
	settings["FEATURE_LEN"] = 48
	settings["DBTYPE"] = "leveldb"
	settings["TRAIN_FILE"] = PATH+"train.txt"
	settings["TEST_FILE"] = PATH+"test.txt"
	settings["DBNAME_TRAIN"] = DBPATH+PROJECT+"_TRAIN"
	settings["DBNAME_TEST"] = DBPATH+PROJECT+"_test"
	settings["DATASET_ROOT"] = DBPATH
	settings["RESULT_FOLDER"] = PATH+"analysis"
	settings["MODEL_FILE"] = DBPATH+"snapshot/"+PROJECT+"_iter_50000.caffemodel"
	settings["MODEL_DEF_FILE"] = PATH+"deepFashion_48_deploy.prototxt"
	settings["TEST_FILE_DATA"] = PATH+"test.txt.data"
	settings["TEST_FILE_LABEL"] = PATH+"test.txt.labels"
	settings["TRAIN_FILE_DATA"] = PATH+"train.txt.data"
	settings["TRAIN_FILE_LABEL"] = PATH+"train.txt.labels"
	settings["SNAPSHOT_LOC"] = DBPATH+"snapshot/"+PROJECT
	with open(PROJECT+'/'+settingFileName, 'w+') as fp:
		json.dump(settings, fp, indent=4, sort_keys=True)


def protxtFiles(PROJECT):
	with open(PROJECT+'/SETTINGS.json', 'r') as content_file:
		settings = json.load(content_file)
	print settings
	trainDb=settings["DBNAME_TRAIN"]
	testDb=settings["DBNAME_TEST"]
	snapshot=settings["SNAPSHOT_LOC"]

	findAndReplace(PROJECT+'/train_fashion_48.prototxt',r'source: \".+\"','source: "'+trainDb+'"')
	findAndReplace(PROJECT+'/test_fashion_48.prototxt',r'source: \".+\"','source: "'+testDb+'"')
	findAndReplace(PROJECT+'/solver_fashion_48.prototxt',r'snapshot_prefix: \".+\"','snapshot_prefix: "'+snapshot+'"')



def main():
	PROJECT_ROOT="/home/ubuntu/caffe-cvprw15/examples/deepFashion"
	LOCAL_PROJECT_ROOT="/home/siddhantmanocha/Projects/neural/deepFashion/examples/deepFashion"
	PROJECT_NAME="Test"
	DBDIR="/data/deepfashion/"

	if (os.path.isdir(PROJECT_NAME)):
		print "Project with same name exists"
		return

	os.mkdir(PROJECT_NAME+"/")
	os.mkdir(PROJECT_NAME+"/analysis")
	os.mkdir(DBDIR+PROJECT_NAME)
	os.mkdir(DBDIR+PROJECT_NAME+'/snapshot')
	
	templateDir="modelTemplate/"
	onlyfiles = [f for f in listdir(templateDir) if isfile(join(templateDir, f))]
	for filename in onlyfiles:
		shutil.copy(templateDir+filename, PROJECT_NAME+"/"+filename)

	configureJson(PROJECT_ROOT,PROJECT_NAME,DBDIR,'SETTINGS.json')
	configureJson(LOCAL_PROJECT_ROOT,PROJECT_NAME,DBDIR,'SETTINGS.json.local')
	protxtFiles(PROJECT_NAME)

main()





