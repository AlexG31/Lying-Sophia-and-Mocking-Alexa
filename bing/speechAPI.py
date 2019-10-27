#encoding:utf8
import os, sys, re, pdb, codecs
import pickle
import requests
import time
import shutil, hashlib, argparse
import json
from translateAPI import loadSentence
# from translateAPI import TranslateChinese
#from GoogleTranslateAPI import TranslateChinese
bingurl = 'https://speech.platform.bing.com/synthesize'

def sha(text):
    m = hashlib.sha256()
    m.update(text.encode('utf8'))
    sha_key = m.hexdigest()
    return sha_key

class Text2SpeechConverter():
    def __init__(self, 
            tokenOutputPath = './text2speech.token.tmp',
            tokenEndpoint = 'https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken',
            private_key = '',
            synthesizeUrl = 'https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1'):
        self.synthesizeUrl = synthesizeUrl
        self.private_key = private_key
        self.tokenEndpoint = tokenEndpoint
        self.tokenOutputPath = tokenOutputPath
        self.name_list = [
            ['en-GB', 'Susan, Apollo'],
            ['en-GB', 'HazelRUS'],
            ['zh-CN', 'HuihuiRUS'],
            ['zh-TW', 'Yating, Apollo']
        ]
        self.name_index = 0

    def getToken(self):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'Ocp-Apim-Subscription-Key': self.private_key}
        print('POST:', self.tokenEndpoint)
        content = requests.post(self.tokenEndpoint, headers = headers)
        print('==== token ====')
        print(content.text)
        with open(self.tokenOutputPath, 'wb') as fout:
            pickle.dump(content.text, fout)

    def setNameIndex(self, index):
        assert index > 0
        index = index % len(self.name_list)
        self.name_index = index
        
    def loadToken(self):
        with open(self.tokenOutputPath, 'rb') as fin:
            token = pickle.load(fin)
        return token

    def convert(self, text, 
            outputPath = './tmp.mp3',
            isNeural = False
            ):
        language = self.name_list[self.name_index][0]
        speaker = self.name_list[self.name_index][1]
        token = self.loadToken()
        url = self.synthesizeUrl
        if isNeural:
            speaker = 'JessaNeural'
            url = 'https://southeastasia.tts.speech.microsoft.com/cognitiveservices/v1'
        # Add language parameters
        url = url + '?language={}'.format(language)

        requestData = u"<speak version='1.0' xml:lang='{0}'><voice xml:lang='{0}' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice ({0}, {2})'>{1}</voice></speak>".format(language,text, speaker)
        #print('request data:', requestData)

        headers = {'User-Agent': 'edream',
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'audio-16khz-64kbitrate-mono-mp3',
                'Authorization': 'Bearer {}'.format(token)}

        #print('url = ' + url)
        content = requests.post(url, headers = headers, data = requestData.encode('utf8'))

        if content.status_code != 200:
            print('Error code:', content.status_code)
            print(content.reason)
            return None

        with open(outputPath, 'wb') as fout:
            for chunk in content.iter_content(chunk_size=128):
                fout.write(chunk)
            #print(u'mp3 file output to ' + outputPath)
        
        return content

def getJsonId(path):
    pattern = re.compile(r'([a-z0-9\.-]+)\.json')
    return pattern.match(path).group(1)

def cmd():
    parser = argparse.ArgumentParser(
        description="Bing speech api"
    )

    parser.add_argument(
        '--input_sentence_json', help="input json sentence path", 
        default='./input-sentence.json')
    parser.add_argument(
        '--output_folder', default="./")
    parser.add_argument(
        '--key_json', default="./speech-key.json")

    args = parser.parse_args()
    return args

def loadKey(path):
    with open(path, 'r') as fin:
        data = json.load(fin)
    return data['key']
        
def main():
    args = cmd()
    private_key = loadKey(args.key_json)
    text2speech = Text2SpeechConverter(
        tokenEndpoint = 'https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken', 
        private_key = private_key,
        synthesizeUrl='https://southeastasia.tts.speech.microsoft.com/cognitiveservices/v1'
        )
    text2speech.getToken()

    sentence = loadSentence(args.input_sentence_json)
    print(sentence)
    print('- - -')
    output_path = os.path.join(args.output_folder, 'tmp.mp3')
    text2speech.convert(sentence, outputPath=output_path)

    print('done.')

if __name__ == '__main__':
    main()