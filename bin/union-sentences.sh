#!/bin/bash -x
echo '======== GPT-2 Model =========='
gitFolder=$1
sentenceFolder=$2
outputPath=$3

seed_path=$gitFolder/seed/conversation1.txt
# union sentences according to script order
python3 $gitFolder/model/util.py --cmd union --seed_path $seed_path \
    --in_folder $sentenceFolder \
    --out_json_path $outputPath