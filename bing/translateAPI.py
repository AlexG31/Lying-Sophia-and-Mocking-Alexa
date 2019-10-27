#encoding:utf8
import os, sys, re, pdb, codecs
import pickle
import requests
import pdb, glob
import time
import shutil, hashlib
import json, argparse

import os, requests, uuid, json

# This simple app uses the '/translate' resource to translate text from
# one language to another.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

# Checks to see if the Translator Text subscription key is available
# as an environment variable. If you are setting your subscription key as a
# string, then comment these lines out.

def translateV3(text, subscriptionKey):
    # If you want to set your subscription key as a string, uncomment the next line.
    #subscriptionKey = 'put_your_key_here'

    # If you encounter any issues with the base_url or path, make sure
    # that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=zh-Hans'
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    # You can pass more than one object in body.
    body = [{
        u'text' : text
    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
    return response[0]["translations"][0]["text"]

def cmd():
    parser = argparse.ArgumentParser(
        description="Bing translate api"
    )

    parser.add_argument(
        '--input_sentence_json', help="input json sentence path", 
        default='./input-sentence.json')
    parser.add_argument(
        '--output_json', default="./output-zh.json")

    args = parser.parse_args()
    return args


def loadSentence(path):
    with open(path, 'r', encoding='utf8') as fin:
        data = json.load(fin)
    sentence = data['result']
    return sentence

def writeJsonData(data, path):
    with open(path, 'w', encoding='utf8') as fout:
        json.dump(data, fout, indent=4, ensure_ascii=False)

def isTranslated(name, output_folder):
    translate_name = 'zh-{}'.format(name)
    return os.path.exists(os.path.join(output_folder, translate_name))

def getFileName(path):
    return os.path.split(path)[-1]

def translateSentences(sentence_folder, output_folder, subscriptionKey, delay = 1):
    files = glob.glob(os.path.join(sentence_folder, '*.json'))
    for sentence_file in files:
        sentence_file_name = getFileName(sentence_file)
        output_file_name = 'zh-{}'.format(sentence_file_name)
        print('translating {}'.format(sentence_file_name))
        if isTranslated(sentence_file_name, output_folder):
            print('skipped ...')
            continue
        sentence = loadSentence(sentence_file)
        time.sleep(delay)
        print('- - -')
        print(sentence)
        zh = translateV3(sentence, subscriptionKey)
        print(zh)
        data = dict(text = sentence, zh = zh)
        output_path = os.path.join(output_folder, output_file_name)
        writeJsonData(data, output_path)
        

def main():
    args = cmd()
    sentence = loadSentence(args.input_sentence_json)
    print(sentence)
    print('- - -')
    key = ''
    zh = translateV3(sentence, key)
    print(zh)
    data = dict(text = sentence, zh = zh)
    writeJsonData(data, args.output_json)
    print('done.')

if __name__ == '__main__':
    main()
