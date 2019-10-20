import glob
import json
import os, sys
import sys, logging, time
import argparse
import random

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

def union(args):
    files = glob.glob(os.path.join(args.in_folder, '*.json'))

    resultDict = dict()
    lines = []
    for p in files:
        with open(p, 'r', encoding = 'utf8') as fin:
            data = json.load(fin)
        seed = data['seed']
        result = data['result']
        if seed not in resultDict:
            resultDict[seed] = list()
        resultDict[data['seed']].append(data['result'])

    # output to file
    seeds = loadSeedFile(args.seed_path)
    script = []
    for s in seeds:
        if s not in resultDict:
            break
        assert s in resultDict
        print('[{}] has ({}) results'.format(s, len(resultDict[s])))
        r = random.choice(resultDict[s])
        script.append(r)

    outputJsonFile(script, args.out_json_path)

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