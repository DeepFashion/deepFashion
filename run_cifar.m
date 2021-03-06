close all;
clear;

% -- settings start here ---
% set 1 to use gpu, and 0 to use cpu
use_gpu = 1;

% top K returned images
top_k = 1000;
feat_len = 48;

% set result folder
result_folder = './analysis';

% models
model_file = './examples/cvprw15-cifar10/KevinNet_CIFAR10_48.caffemodel';
% model definition
model_def_file = './examples/cvprw15-cifar10/KevinNet_CIFAR10_48_deploy.prototxt';

% train-test
test_file_list = './examples/cvprw15-cifar10/dataset/test-file-list.txt';
test_label_file = './examples/cvprw15-cifar10/dataset/test-label.txt';
train_file_list = './examples/cvprw15-cifar10/dataset/train-file-list.txt';
train_label_file = './examples/cvprw15-cifar10/dataset/train-label.txt';
% --- settings end here ---

% outputs
feat_test_file = sprintf('%s/feat-test.mat', result_folder);
feat_train_file = sprintf('%s/feat-train.mat', result_folder);
binary_test_file = sprintf('%s/binary-test.mat', result_folder);
binary_train_file = sprintf('%s/binary-train.mat', result_folder);

file_name_test = sprintf('%s/file_name_test.mat', result_folder);
file_name_train = sprintf('%s/file_name_train.mat', result_folder);


% map and precision outputs
map_file = sprintf('%s/map.txt', result_folder);
precision_file = sprintf('%s/precision-at-k.txt', result_folder);

% feature extraction- test set
if exist(binary_test_file, 'file') ~= 0
    load(binary_test_file);
    load(file_name_test);
else
    [feat_test , list_im_test] = matcaffe_batch_feat(test_file_list, use_gpu, feat_len, model_def_file, model_file);
    save(feat_test_file, 'feat_test', '-v7.3');
    binary_test = (feat_test>0.5);
    save(binary_test_file,'binary_test','-v7.3');
    save(file_name_test,'list_im_test','-v7.3');
end
    
% feature extraction- training set
if exist(binary_train_file, 'file') ~= 0
    load(binary_train_file);
    load(file_name_train);
else
    [feat_train , list_im_train] = matcaffe_batch_feat(train_file_list, use_gpu, feat_len, model_def_file, model_file);
    save(feat_train_file, 'feat_train', '-v7.3');
    binary_train = (feat_train>0.5);
    save(binary_train_file,'binary_train','-v7.3');
    save(file_name_train,'list_im_train','-v7.3');

end

trn_label = load(train_label_file);
tst_label = load(test_label_file);

[mapping] = precisionMod( trn_label, binary_train, tst_label, binary_test, top_k, 1, list_im_test, list_im_train);

for i = 1:size(mapping,1)
	for j = 1:size(mapping,2)
		fprintf('%s\t',mapping{i,j}{1});
	end
	fprintf('\n');
end

