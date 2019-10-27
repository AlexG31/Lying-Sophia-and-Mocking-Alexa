#!/bin/bash
# sync zh/voice data between local and remote server

git_root=$1
#dest_root=$2
dest_root='l2:/home/alexg/github/Lying-Sophia-and-Mocking-Alexa/'
echo '========='
echo 'git root folder:', $git_root
echo '➡️', $dest_root
echo '========='

rsync -r $git_root/bing/translate-zh $dest_root/bing/
rsync -r $git_root/bing/voice $dest_root/bing/

