% ------------------------------------------------------------------------
function images = prepare_batch_autoencoder(image_files,batch_size)
% ------------------------------------------------------------------------

num_images = length(image_files);

CROPPED_DIM = 50;

num_images = length(image_files);
images = zeros(CROPPED_DIM,CROPPED_DIM,3,batch_size,'single');

parfor i=1:num_images
    % read file
    fprintf('%c Preparing %s\n',13,image_files{i});
    try
        im = imread(image_files{i});
        % resize to fixed input size
        im = single(im);
        im = imresize(im, [CROPPED_DIM CROPPED_DIM], 'bilinear');
        % Transform GRAY to RGB
        if size(im,3) == 1
            im = cat(3,im,im,im);
        end
        % Crop the center of the image
	    im = im(:,:,[3 2 1])
        images(:,:,:,i) = permute(im,[2 1 3]);
    catch
        warning('Problems with file',image_files{i});
    end
end
