#!/bin/bash -x
echo '======== GPT-2 Model =========='
envPath=$1
gitFolder=$2

generateScriptPath=$gitFolder/model/fix-prefix-gpt-2.py
utilScriptPath=$gitFolder/model/util.py
echo "env path: $envPath"
source $envPath/bin/activate

# GPT-2 Generation
sentenceFolder="$gitFolder/sentences/"
gpt2lock="$gitFolder/model/gpt-2.lock"
dateFileName="`date -I`_`date +%H`"
echo "generate sentence to $sentenceFolder" 

if mkdir $gpt2lock; then
    python3 $generateScriptPath \
        --output_json_folder $sentenceFolder \
        --model_name 774M \
        --seed_cap 5 \
        --seed_folder $gitFolder/seed/

    deactivate
    bash $gitFolder/bing/run_translate.sh $gitFolder
    bash $gitFolder/bing/run_speech.sh $gitFolder
    bash $gitFolder/bing/run_speech.sh $gitFolder

    rm -rf $gpt2lock
else
    echo 'gpt-2 is already running'
    exit 1
fi