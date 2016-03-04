import os.path
import scipy.io
import h5py
from precision import *
use_gpu = 1

# top K returned images
top_k = 30
feat_len = 48

result_folder = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/analysis'
# models
model_file = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/models/deepFashion_Jabong_48_iter_50000.caffemodel';
# model definition
model_def_file = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/modelDef/deepFashion_48_deploy.prototxt';

# train-test
test_file_list = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/test.txt.data';
test_label_file = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/test.txt.labels';
train_file_list = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/train.txt.data';
train_label_file = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/train.txt.labels';
# ----------- settings end here ----------------

 # outputs
feat_test_file = result_folder+'/feat-test.mat'
feat_train_file = result_folder+'/feat-train.mat'
binary_test_file = result_folder+'/binary-test.mat'
binary_train_file = result_folder+'/binary-train.mat'

# map and precision outputs
map_file = result_folder+'/map.txt'
precision_file = result_folder+'/precision-at-k.txt'

# feature extraction- test set
if os.path.isfile(binary_test_file)!=0:
	with h5py.File(binary_test_file, 'r') as f:
		binary_test = f['binary_test'][()]
else:
    print 'Load model using matlab or write a wrapper for it'
    
 # feature extraction- training set
if os.path.isfile(binary_train_file)!=0:
    	with h5py.File(binary_train_file, 'r') as f:
                binary_train = f['binary_train'][()]
else:
    print 'Load model using matlab or write a wrapper for it'

with open(train_label_file,'r') as f:
	trn_label=f.readlines()

with open(test_label_file,'r') as f:
        tst_label=f.readlines()

print type(binary_train)
mapRes, precision_at_k = precision( trn_label, binary_train, tst_label, binary_test, top_k, 1)
# fprintf('MAP = %f\n',map);
# save(map_file, 'map', '-ascii');
# P = [[1:1:top_k]' precision_at_k'];
# save(precision_file, 'P', '-ascii');



