#!/bin/bash
git_root=$1
echo '========='
echo 'git root folder:', $git_root
echo '========='
python3 $git_root/bing/readSentences.py \
    --sentence_folder $git_root/sentences \
    --zh_folder $git_root/bing/translate-zh \
    --conversation_path $git_root/seed/conversation1.txt \
    --output_folder $git_root/bing/voice \
    --key_json $git_root/bing/speech-key.json