#!/bin/bash -x
echo '======== GPT-2 Model =========='
envPath=$1
modelFolder=$2
sentenceFolder=$3
outputPath=$4

generateScriptPath=$modelFolder/fix-prefix-gpt-2.py
utilScriptPath=$modelFolder/util.py
echo "env path: $envPath"
source $envPath/bin/activate

# GPT-2 Generation
gpt2lock="$modelFolder/gpt-2.lock"
dateFileName="`date -I`_`date +%H`"
sentenceFileName="$sentenceFolder/$dateFileName.json"
echo "generate sentence to $sentenceFileName" 

if mkdir $gpt2lock; then
    python3 $generateScriptPath \
        -output_json_folder $sentenceFolder

    deactivate
    # cp $generateStoryFile $exportStoryFile && \
    # sh /home/alexg/github/EdreamProject/bingAPI/run_api.sh &> \
    #     "/home/alexg/model/logs/bing-api-$dateFileName.log" && \
    # sh /home/alexg/github/EdreamProject/util/bin/send_json.sh 

    rm -rf $gpt2lock
else
    echo 'gpt-2 is already running'
    exit 1
fi