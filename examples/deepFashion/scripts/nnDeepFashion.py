import os.path
import scipy.io
import h5py
from precision import *
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    # Required arguments: input and settings file
    parser.add_argument(
        "settings_file",
        help="Input image, directory, or npy."
    )


def main(settings_file):
	with open(settings_file, 'r') as content_file:
		settings = json.load(content_file)

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

	mapRes, precision_at_k = precision( trn_label, binary_train, tst_label, binary_test, top_k, 1)
	return mapRes,precision_at_k

if __name__ == '__main__':
	args=parseArgs()
	mapRes, precision_at_k = main(args.settings_file)
