#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs

jsonData="`cat $1`"
TRAIN_FILE=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["ALT_TRAIN_FILE"]'`
TEST_FILE=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["ALT_TEST_FILE"]'`
DB_TRAIN=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["ALT_DBNAME_TRAIN"]'`
DB_TEST=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["ALT_DBNAME_TEST"]'`
DB_TYPE=`echo $jsonData | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["DBTYPE"]'`
TOOLS=../../build/tools


echo "Creating train $DB_TYPE..."

GLOG_logtostderr=1 $TOOLS/convert_vector \
    --backend="$DB_TYPE" \
    $TRAIN_FILE \
    $DB_TRAIN

echo "Creating val $DB_TYPE..."

GLOG_logtostderr=1 $TOOLS/convert_vector \
    --backend="$DB_TYPE" \
    $TEST_FILE \
    $DB_TEST

echo "Done."
