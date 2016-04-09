from caffe.proto import caffe_pb2
from google.protobuf.text_format import Merge
from google.protobuf import text_format
net = caffe_pb2.NetParameter()
Merge((open("new2.prototxt",'r').read()), net)
net.layers[5].bottom[0]="helloworld"
new_net=text_format.MessageToString(net)
with open('temp.prototxt', 'w') as f:
	f.write(new_net)


