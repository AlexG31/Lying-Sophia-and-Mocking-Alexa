import glob
import json
import os, sys, re
import sys, logging, time
import argparse
import random

current_file_path = os.path.abspath(__file__)
git_root = os.path.dirname(
            os.path.dirname(
             os.path.dirname(current_file_path)
           ))
print('git_root path:', git_root)
def getDataByIndex(pid, name):
    seed_path = os.path.join(git_root, 'seed', 'conversation1.txt')
    seeds = loadSeedFile(seed_path)
    assert len(seeds) > 0
    s = seeds[pid % len(seeds)]

    # get candidates
    sentence_folder = os.path.join(git_root, 'sentences')
    candidates = getCandidates(sentence_folder)
    candidates = list(filter(lambda x: hasResource(x, name), candidates[s]))
    if len(candidates) == 0:
        return None
    c = random.choice(candidates)
    c = appendVoiceFullPath(c, name)
    c['status'] = 'ok'
    return json.dumps(c)

def appendVoiceFullPath(data, name):
    voice_en = '/voice/{}-{}'.format(name.lower(), data['voice-en'])
    data['voice-en'] = voice_en

    voice_zh = '/voice/{}-{}'.format(name.lower(), data['voice-zh'])
    data['voice-zh'] = voice_zh
    return data

def hasResource(data, name):
    print(data, name)
    voice_en = '/voice/{}-{}'.format(name.lower(), data['voice-en'])
    if not resourceExists(voice_en):
        print('⭕️en voice')
        return False
    voice_zh = '/voice/{}-{}'.format(name.lower(), data['voice-zh'])
    if not resourceExists(voice_zh):
        print('⭕️zh voice')
        return False
    if not resourceExists(data['zh']):
        print('⭕️zh translate')
        return False
    return True
    

def loadText(path):
    results = []
    with open(path, 'r', encoding='utf8') as fin:
        for line in fin:
            results.append(line.strip('\r\n'))
    return results
            
def outputJsonFile(data, path):
    with open(path, 'w', encoding='utf8') as fout:
        json.dump(data, fout, indent = 4, ensure_ascii = False)

def loadSeedFile(path):
    seeds = []
    with open(path, 'r', encoding='utf8') as fin:
        for line in fin:
            seeds.append(line.strip('\r\n'))
    return seeds

def getJsonId(path):
    pattern = re.compile(r'([a-z0-9\.-]+)\.json')
    return pattern.match(path).group(1)

resultDict = dict()
updateResultDictCountDown = 201
def getCandidates(sentence_folder, updateCount = 200):
    global resultDict
    global updateResultDictCountDown
    updateResultDictCountDown += 1
    if updateResultDictCountDown <= updateCount:
        return resultDict
    updateResultDictCountDown = 0
    resultDict = dict()

    files = glob.glob(os.path.join(sentence_folder, '*.json'))
    for p in files:
        print('loading file {}'.format(p))
        sid = getJsonId(os.path.split(p)[-1])
        with open(p, 'r', encoding = 'utf8') as fin:
            data = json.load(fin)
        seed = data['seed']
        if seed not in resultDict:
            resultDict[seed] = list()
        data['voice-en'] = 'en-{}.mp3'.format(sid)
        data['voice-zh'] = 'zh-{}.mp3'.format(sid)
        data['zh'] = '/translate-zh/zh-{}.json'.format(sid)
        resultDict[data['seed']].append(data)
    return resultDict

def union(args):
    files = glob.glob(os.path.join(args.in_folder, '*.json'))

    resultDict = dict()
    lines = []
    for p in files:
        sid = getJsonId(os.path.split(p)[-1])
        with open(p, 'r', encoding = 'utf8') as fin:
            data = json.load(fin)
        seed = data['seed']
        result = data['result']
        if seed not in resultDict:
            resultDict[seed] = list()
        data['voice-en'] = 'en-{}.mp3'.format(sid)
        data['voice-zh'] = 'zh-{}.mp3'.format(sid)
        data['zh'] = '/translate-zh/zh-{}.json'.format(sid)
        resultDict[data['seed']].append(data)

    # output to file
    seeds = loadSeedFile(args.seed_path)
    script = []
    for ind, s in enumerate(seeds):
        name = 'alexa' if ind % 2 == 0 else 'sophia'
        if s not in resultDict:
            break
        assert s in resultDict
        print('[{}] has ({}) results'.format(s, len(resultDict[s])))
        r = random.choice(resultDict[s])
        r['voice-en'] = '/voice/{}-{}'.format(name, r['voice-en'])
        r['voice-zh'] = '/voice/{}-{}'.format(name, r['voice-zh'])
        script.append(r)

    outputJsonFile(script, args.out_json_path)

def resourceExists(path):
    abs_path = git_root + '/bing' + path
    return os.path.exists(abs_path)

def cmd():
    parser = argparse.ArgumentParser(
        description="Easily retrain OpenAI's GPT-2 text-generating model on new texts. (https://github.com/minimaxir/gpt-2-simple)"
    )

    parser.add_argument(
        '--cmd', help="command ", default='union')
    parser.add_argument(
        '--seed_path', help="seed file path")
    parser.add_argument(
        '--in_folder', help="input folder", default='union')
    parser.add_argument(
        '--out_json_path', help="output path", default='./util-output.json')
    

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = cmd()
    if args.cmd == 'union':
        union(args)

    print('done.')