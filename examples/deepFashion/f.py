import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predictTags as predict
import getNear
import urllib
import time
import os
import caffeClientManager as cCM


SETTINGS_FILE='/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json'
numThreads=1
threadPoolObj=cCM.caffeThreadManager(numThreads,SETTINGS_FILE)


def compute(imageURL):
	urllib.urlretrieve(imageURL, '/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg')
	start_time = time.time()
	
	classifier=threadPoolObj.getThread()
	if not classifier:
		print 'Unable to contact the weaver server'
		assert False
	print 'Recieved a Thread'

	embedding=predict.InputImagePredict('/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg',SETTINGS_FILE,"embedding",classifier)
	
	threadPoolObj.returnThread(classifier)
	print 'Returned a Thread'

	mid_time = time.time()
	nn=getNear.computeNN('/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json', embedding)
	end_time = time.time()
	print "Time for caffe = ", mid_time-start_time
	print "Time for nn = ", end_time-mid_time
	return nn


urlval="http://static2.jassets.com/p/Rider-Republic-Brown-Solid-Skirt-8202-3058971-1-catalog_s.jpg"
result=compute(urlval)


for i in range(len(result)):
	result[i]=result[i].strip()
	result[i]=result[i][8:]
	result[i]=result[i].replace("_", "/")
	result[i]=result[i].replace("catalog/s", "catalog_s")

print result

