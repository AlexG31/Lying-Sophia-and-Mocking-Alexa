#!/bin/bash
git_root=$1
echo '========='
echo 'git root folder:', $git_root
echo '========='
python3 $git_root/bing/translateSentences.py \
    --sentence_folder $git_root/sentences \
    --output_folder $git_root/bing/translate-zh