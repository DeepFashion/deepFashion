import os.path
import scipy.io
import h5py
from precision import *
import argparse
import json

def computeNN(settings_file, query_binary):
	with open(settings_file, 'r') as content_file:
		settings = json.load(content_file)
	mode=1
	# top K returned images
	top_k = settings['TOP_K']
	feat_len = settings['FEATURE_LEN']

	# result_folder = '/home/ubuntu/caffe-cvprw15/examples/deepFashion/analysis'
	result_folder = settings['RESULT_FOLDER']
	# models
	model_file = settings['MODEL_FILE']
	# model definition
	model_def_file = settings['MODEL_DEF_FILE']

	# train-test
	test_file_list = settings['TEST_FILE_DATA']
	test_label_file = settings['TEST_FILE_LABEL']
	train_file_list = settings['TRAIN_FILE_DATA']
	train_label_file = settings['TRAIN_FILE_LABEL']
	# ----------- settings end here ----------------

	 # outputs
	feat_test_file = result_folder+'/feat-test.mat'
	feat_train_file = result_folder+'/feat-train.mat'
	binary_test_file = result_folder+'/binary-test.mat'
	binary_train_file = result_folder+'/binary-train.mat'

		
	 # feature extraction- training set
	if os.path.isfile(binary_train_file)!=0:
		with h5py.File(binary_train_file, 'r') as f:
				binary_train = f['binary_train'][()]
	else:
		print 'Load model using matlab or write a wrapper for it'


	with open(train_file_list,'r') as f:
		fileTrain=f.readlines()

	K = top_k;
	result=list()
		# query_binary = np.array([tst_binary[i,:]]
	if mode==1:
		similarity = distance.cdist(trn_binary,query_binary,'hamming')
	elif mode ==2:
		similarity = distance.cdist(trn_binary,query_binary,'euclidean')

	y2=np.argsort(similarity[:,0]);

	for j in range(K):
		result.append(fileTrain[y2[j]])

	return result