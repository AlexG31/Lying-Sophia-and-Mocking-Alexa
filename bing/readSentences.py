#encoding:utf8
import os, sys, re, pdb, codecs
import pickle
import requests
import time, glob
import shutil, hashlib, argparse
import json
from translateAPI import loadSentence
import speechAPI

def cmd():
    parser = argparse.ArgumentParser(
        description="Bing speech api"
    )

    parser.add_argument(
        '--sentence_folder', help="input json sentence path", 
        default='./input-sentence.json')
    parser.add_argument(
        '--zh_folder', help="input translate chinese folder", 
        default='./translate-zh')
    parser.add_argument(
        '--conversation_path', help="input conversation path", 
        default='../seed/conversation1.txt')
    parser.add_argument(
        '--output_folder', default="./voice")
    parser.add_argument(
        '--key_json', default="./speech-key.json")
    parser.add_argument(
        '--delay', type=int, default=3)

    args = parser.parse_args()
    return args

def produceVoice(sentence, converter, output_file_name, args):
    output_path = os.path.join(args.output_folder, output_file_name)
    if os.path.exists(output_path):
        print('skipped ...')
        return None
    time.sleep(args.delay)
    converter.convert(sentence, outputPath = output_path)
    return True

def loadZh(path):
    with open(path, 'r', encoding = 'utf8') as fin:
        data = json.load(fin)
    return data['zh']

def readByName(name, sentence_file, converter, args, en_index = 0, zh_index = 2):
    sentence_id = speechAPI.getJsonId(os.path.split(sentence_file)[-1])
    sentence = loadSentence(sentence_file)
    output_file_name = '{}-en-{}.mp3'.format(name, sentence_id)

    print('{}: {}'.format(name, sentence_file))
    print(u'🇬🇧🔜 {}'.format(output_file_name))
    print(sentence)

    converter.setNameIndex(en_index)
    produceVoice(sentence, converter, output_file_name, args)

    # produce chinese
    zh_file = 'zh-{}.json'.format(sentence_id)
    zh_path = os.path.join(args.zh_folder, zh_file)
    print(u'zh file path: {}'.format(zh_path))
    assert os.path.exists(zh_path)
    zh = loadZh(zh_path)
    print(zh)

    converter.setNameIndex(zh_index)
    output_file_name = '{}-zh-{}.mp3'.format(name, sentence_id)
    print(u'🇨🇳🔜 {}'.format(output_file_name))
    produceVoice(zh, converter, output_file_name, args)
        
def isAlexa(path, conversation_path):
    with open(path, 'r', encoding='utf8') as fin:
        data = json.load(fin)
    seed = data['seed']
    with open(conversation_path, 'r', encoding = 'utf8') as fin:
        line_index = 0
        for line in fin:
            c = line.strip(' \r\n')
            if c == seed.strip(' \r\n'):
                return line_index % 2 == 0
            line_index += 1

    assert False

def read(converter, args):
    files = glob.glob(os.path.join(args.sentence_folder, '*.json'))
    for sentence_file in files:
        print(u'🌵 {}'.format(sentence_file))
        if isAlexa(sentence_file, args.conversation_path):
            readByName('alexa', sentence_file, converter, args, en_index=0, zh_index=2)
        else:
            readByName('sophia', sentence_file, converter, args, en_index=1, zh_index=3)

def main():
    args = cmd()
    private_key = speechAPI.loadKey(args.key_json)
    text2speech = speechAPI.Text2SpeechConverter(
        tokenEndpoint = 'https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken', 
        private_key = private_key,
        synthesizeUrl='https://southeastasia.tts.speech.microsoft.com/cognitiveservices/v1'
        )
    text2speech.getToken()

    read(text2speech, args)
    print('done.')

if __name__ == '__main__':
    main()