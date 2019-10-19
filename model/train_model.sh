#!/bin/bash -x
echo '========GPT-2 Model Training=========='
modelHome="/home/alexg/model"
cd $modelHome
source /home/alexg/model/cpu/bin/activate

echo "=====Let's Collect News!====="
trainingFile="/home/alexg/model/training-news.txt"
spiderWorkFolder="/home/alexg/spider/work/"
python3 /home/alexg/github/EdreamProject/util/merge_data_util.py \
$spiderWorkFolder \
$trainingFile

# Train GPT-2 Model
logpath="/home/alexg/model/training_logs/`date -I`_`date +%H%M`.txt"
if mkdir ./gpt-2.lock; then
    python3 helloworld.py $logpath
    rm -rf ./gpt-2.lock
else
    echo 'gpt-2 is running'
    exit 1
fi

