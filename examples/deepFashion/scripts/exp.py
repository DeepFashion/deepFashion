#!/usr/bin/env python
'''
demostrate how to write a rpc server
'''
import json
import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/examples/deepFashion/scripts')
import predictTags as predict
import getNear
import urllib
import random
import string

import  os, uuid, time
sys.path.append(os.path.abspath(".."))
import time
from haigha.connection import Connection
from haigha.message import Message

# from dbFns import main as db
from dbFns import reddis as redisDb

SETTINGS_FILE_EMBEDDING='/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json'
SETTINGS_FILE_TAGS='/home/ubuntu/caffe-cvprw15/examples/deepFashion/multimodal/SETTINGS.json'

def githash(filename):
    with open(filename,'r') as f:
        data=f.readlines()
    data="".join(data)
    s = sha1()
    s.update("blob %u\0" % len(data))
    s.update(data)
    return s.hexdigest()

classifierTags = predict.CreateClassifier(SETTINGS_FILE_TAGS)
classifierNN = predict.CreateClassifier(SETTINGS_FILE_EMBEDDING)
print "Creating caffe client"

connection = Connection(
    user='vastrai', password='vastra1',
    vhost='/', host='52.86.70.177',
    heartbeat=None, debug=True
)
channel = connection.channel()
channel.queue.declare(queue='rpc_queue', auto_delete=False)



def computeNN(imageURL):
    filename=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))+'.jpg'
    filename='/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/'+filename
    if os.path.isfile(filename):
        os.remove(filename) 
    urllib.urlretrieve(imageURL, filename)
    
    imageHash=githash(filename)
    
    dbRes=redisDb.fetchKey(imageHash+"_similar")
    if dbRes:
        return {'imageURL':imageURL,'result': dbRes}

    embedding=predict.InputImagePredict(filename,SETTINGS_FILE_EMBEDDING,"embedding",classifierNN)
    
    result=getNear.computeNN(SETTINGS_FILE_EMBEDDING, embedding)
    for i in range(len(result)):
        result[i]=result[i].strip()
        result[i]=result[i][8:]
        result[i]=result[i].replace("_", "/")
        result[i]=result[i].replace("catalog/s", "catalog_s")
    resList=list()
    for val in result:
        resList.append({'imageURL':val,'productURL':'https://www.youtube.com/watch?v=IFUjwj_RB5o&nohtml5=False'})
    
    # db.InsertData({'imageName':imageHash,'similarProducts':resList,'crossProducts':[],'tags':[]},mode="similar")
    redisDb.insertKey(imageHash+"_similar",resList)
    return {'imageURL':imageURL,'result':resList}


def computeTags(imageURL):
    filename=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))+'.jpg'
    filename='/home/ubuntu/caffe-cvprw15/examples/deepFashion/tmp/'+filename
    if os.path.isfile(filename):
        os.remove(filename) 
    urllib.urlretrieve(imageURL, filename)

    imageHash=githash(filename)

    dbRes=redisDb.fetchKey(imageHash+"_tags")
    if dbRes:
        return {'imageURL':imageURL,'result': dbRes}
    # dbRes=db.getData(imageHash,"tags")
    # if dbRes:
    #     return {'imageURL':imageURL,'result': dbRes['tags']}


    tags=predict.InputImagePredict(filename,SETTINGS_FILE_TAGS,"tags",classifierTags)

    redisDb.insertKey(imageHash+"_tags",tags)
    # db.InsertData({'imageName':imageHash,'similarProducts':[],'crossProducts':[],'tags':tags},mode="tags")
    
    return {'imageURL':imageURL,'result':tags}

def on_request(msg):
    val = json.loads(str(msg.body))
    print val
    imageURL=val['url']
    if val['type']=="similar":
	result=computeNN(imageURL)
    else:
	result=computeTags(imageURL)
    print result
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
