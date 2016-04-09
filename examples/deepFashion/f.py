from scripts import predict
embedding=predict.InputImagePredict('/home/ubuntu/caffe-cvprw15/examples/deepFashion/dataset/http:__static2.jassets.com_p_King-26-I-Mustard-Yellow-Solid-Short-1248-1335051-1-catalog_s.jpg','/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json')
nn=predict.getNN('/home/ubuntu/caffe-cvprw15/examples/deepFashion/label_jabong/SETTINGS.json', embedding)
print nn