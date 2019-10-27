#!/bin/bash -x
echo '======== GPT-2 Model =========='
gitFolder=$1
outputPath=$2

seed_path=$gitFolder/seed/conversation1.txt
# union sentences according to script order
python3 $gitFolder/model/util.py --cmd union \
    --seed_path $seed_path \
    --in_folder $gitFolder/sentences \
    --out_json_path $outputPath