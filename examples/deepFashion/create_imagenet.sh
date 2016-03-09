#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs

jsonData="`cat $1`"
RESIZE_VAL=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["RESIZE"]'`
TRAIN_FILE=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["TRAIN_FILE"]'`
TEST_FILE=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["TEST_FILE"]'`
DB_TRAIN=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["DB_TRAIN"]'`
DB_TEST=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["DB_TEST"]'`
DB_TYPE=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["DB_TYPE"]'`
DATASET_ROOT=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["DATASET_ROOT"]'`
TOOLS=../../build/tools


# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=$RESIZE_VAL
  RESIZE_WIDTH=$RESIZE_VAL
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

echo "Creating train $DB_TYPE..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    --backend="$DB_TYPE" \
    $DATASET_ROOT \
    $TRAIN_FILE \
    $DB_TRAIN

echo "Creating val $DB_TYPE..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    --backend="$DB_TYPE" \
    $DATASET_ROOT \
    $TEST_FILE \
    $DB_TEST

echo "Done."
