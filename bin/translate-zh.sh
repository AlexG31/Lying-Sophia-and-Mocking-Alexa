#!/bin/bash -x
gitFolder=$1
sentenceFolder=$2
outputPath=$3

seed_path=$gitFolder/seed/conversation1.txt
# translate sentences to chinese
python3 $gitFolder/model/ 