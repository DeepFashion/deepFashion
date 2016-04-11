import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predictTags as predict
import getNear
import urllib
import time
import os

# os.environ['GLOG_minloglevel'] = '3'

def compute(imageURL):
	urllib.urlretrieve(imageURL, '/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg')
	start_time = time.time()
	embedding=predict.InputImagePredict('/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg','/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json',"embedding")
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

