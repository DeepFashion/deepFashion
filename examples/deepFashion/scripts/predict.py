#!/usr/bin/env python
"""
By default it configures and runs based on SETTING.json file
"""
import json
import numpy as np
import os
import sys
import argparse
import glob
import time
import sys
sys.path.append('/home/ubuntu/caffe-cvprw15/python/')
import caffe

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def parseArgs():
    parser = argparse.ArgumentParser()
    # Required arguments: input and settings file
    parser.add_argument(
        "input_file",
        help="Input image, directory, or npy."
    )

    parser.add_argument(
        "settings_file",
        help="Settings file for prediction"
    )
    # # Optional arguments.
    parser.add_argument(
        "--output_file",
        default='result.npy',
        help="Output npy filename."
    )

    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--center_only",
        action='store_true',
        help="Switch for prediction from center crop alone instead of " +
             "averaging predictions across crops (default)."
    )
    parser.add_argument(
        "--images_dim",
        default='256,256',
        help="Canonical 'height,width' dimensions of input images."
    )
    parser.add_argument(
        "--mean_file",
        default="/home/ubuntu/caffe-cvprw15/python/caffe/imagenet/ilsvrc_2012_mean.npy",
        help="Data set image mean of H x W x K dimensions (numpy array). " +
             "Set to '' for no mean subtraction."
    )
    parser.add_argument(
        "--input_scale",
        type=float,
        help="Multiply input features by this scale to finish preprocessing."
    )
    parser.add_argument(
        "--raw_scale",
        type=float,
        default=255.0,
        help="Multiply raw input by this scale before preprocessing."
    )
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    parser.add_argument(
        "--ext",
        default='jpg',
        help="Image file extension to take as input when a directory " +
             "is given as the input file."
    )
    args = parser.parse_args()
    with open(args.settings_file, 'r') as content_file:
        settings = json.load(content_file)

    args.model_def=settings['MODEL_DEF_FILE']
    args.pretrained_model=settings['MODEL_FILE']

    return args


def InputImagePredictAux(args):
    image_dims = [int(s) for s in args.images_dim.split(',')]

    mean, channel_swap = None, None
    if args.mean_file:
        mean = np.load(args.mean_file)
    if args.channel_swap:
        channel_swap = [int(s) for s in args.channel_swap.split(',')]
    # Make classifier.
    start = time.time()
    classifier = caffe.Classifier((args.model_def).encode('ascii','ignore'), (args.pretrained_model).encode('ascii','ignore'),
            image_dims=image_dims, gpu=args.gpu, mean=mean,
            input_scale=args.input_scale, raw_scale=args.raw_scale,
            channel_swap=channel_swap)
    print "Caffe model loaded in ", time.time()-start
    if args.gpu:
        print 'GPU mode'

    # Load numpy array (.npy), directory glob (*.jpg), or image file.
    args.input_file = os.path.expanduser(args.input_file)
    if args.input_file.endswith('npy'):
        inputs = np.load(args.input_file)
    elif os.path.isdir(args.input_file):
        inputs =[caffe.io.load_image(im_f)
                 for im_f in glob.glob(args.input_file + '/*.' + args.ext)]
    else:
        inputs = [caffe.io.load_image(args.input_file)]

    print "Classifying %d inputs." % len(inputs)

    # Classify.
    start = time.time()
    predictions = classifier.predict(inputs,False)
    for i in range(predictions.shape[0]):
	predictions[i:]=(predictions[i:]>0.5).astype(int)
    print "Prediction done in %.2f s." % (time.time() - start)
    # Save
    np.save(args.output_file, predictions)
    #return
    return predictions
    
    
def InputImagePredict(input_file,settings_file):
    defaultData={
    'center_only':False, 'channel_swap':'2,1,0', 'ext':'jpg', 'gpu':False, 
    'images_dim':'256,256','input_scale':None, 
    'mean_file':'/home/ubuntu/caffe-cvprw15/python/caffe/imagenet/ilsvrc_2012_mean.npy', 
    'output_file':'result.npy', 
    'raw_scale':255.0
    } 
    with open(settings_file, 'r') as content_file:
        settings = json.load(content_file)
    defaultData['settings_file']=settings_file
    defaultData['input_file']=input_file
    defaultData['model_def']=settings['MODEL_DEF_FILE']
    defaultData['pretrained_model']=settings['MODEL_FILE']

    return InputImagePredictAux(dotdict(defaultData))


if __name__ == '__main__':
    print InputImagePredictAux(parseArgs())
    #print InputImagePredict('f1','../hello/SETTINGS.json')
