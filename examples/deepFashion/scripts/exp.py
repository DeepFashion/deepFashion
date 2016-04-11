#!/usr/bin/env python
'''
demostrate how to write a rpc server
'''
import json
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predictTags as predict
import getNear
import urllib
import random
import string

import sys, os, uuid, time
sys.path.append(os.path.abspath(".."))
import time
from haigha.connection import Connection
from haigha.message import Message


try:
    classifier = predict.CreateClassifier(self.settings_file)
    print "Creating caffe client"
except:
    print 'Some error'
    assert(False)

connection = Connection(
    user='vastrai', password='vastra1',
    vhost='/', host='52.86.70.177',
    heartbeat=None, debug=True
)
channel = connection.channel()
channel.queue.declare(queue='rpc_queue', auto_delete=False)


SETTINGS_FILE_EMBEDDING='/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json'
SETTINGS_FILE_TAGS='/home/ubuntu/caffe-cvprw15/examples/deepFashion/multimodal/SETTINGS.json'

def computeNN(imageURL):
    filename=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))+'.jpg'
    filename='/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/'+filename
    if os.path.isfile(filename):
        os.remove(filename) 
    urllib.urlretrieve(imageURL, filename)
    embedding=predict.InputImagePredict(filename,SETTINGS_FILE_EMBEDDING,"embedding",classifier)
    result=getNear.computeNN(SETTINGS_FILE_EMBEDDING, embedding)
    for i in range(len(result)):
        result[i]=result[i].strip()
        result[i]=result[i][8:]
        result[i]=result[i].replace("_", "/")
        result[i]=result[i].replace("catalog/s", "catalog_s")
    return result


def computeTags(imageURL):
    filename=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))+'.jpg'
    filename='/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/'+filename
    if os.path.isfile(filename):
        os.remove(filename) 
    urllib.urlretrieve(imageURL, filename)
    tags=predict.InputImagePredict(filename,SETTINGS_FILE_TAGS,"tags",classifier)
    return tags

def on_request(msg):
    imageURL = msg.body
    result=computeNN(imageURL)
    reply_to = msg.properties["reply_to"]
    correlation_id = msg.properties["correlation_id"]
    resp = Message(json.dumps(result), correlation_id=correlation_id)
    channel.basic.publish(resp,'',reply_to)
    delivery_info = msg.delivery_info
    channel.basic.ack(delivery_info["delivery_tag"])

channel.basic.qos(prefetch_count=2)
channel.basic.consume('rpc_queue', on_request, no_ack=False)

print " [x] Awaiting RPC requests"
while not channel.closed:
    connection.read_frames()
