import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predictTags as predict
import urllib
import time
import os


def compute(imageURL):
	urllib.urlretrieve(imageURL, '/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg')
	start_time = time.time()
	result=predict.InputImagePredict('/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/0001.jpg','/home/ubuntu/caffe-cvprw15/examples/deepFashion/multimodal/SETTINGS.json',"tags")
	end_time = time.time()
	print "Time for caffe = ", end_time-start_time
	return result


urlval="http://static2.jassets.com/p/Rider-Republic-Brown-Solid-Skirt-8202-3058971-1-catalog_s.jpg"
result=compute(urlval)
print result

