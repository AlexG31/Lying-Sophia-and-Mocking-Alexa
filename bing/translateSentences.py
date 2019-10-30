#encoding:utf8
import os, sys, re, pdb, codecs
import pickle
import requests
import pdb, glob
import time
import shutil, hashlib
import json, argparse
from translateAPI import translateSentences

import os, requests, uuid, json

def cmd():
    parser = argparse.ArgumentParser(
        description="translate sentences"
    )

    parser.add_argument(
        '--sentence_folder', help="input json sentence path", 
        default='./')
    parser.add_argument(
        '--output_folder', default="./translate-zh.json")
    parser.add_argument(
        '--key_json', default="./translate-key.json")

    args = parser.parse_args()
    return args

def loadKey(path):
    with open(path, 'r', encoding = 'utf8') as fin:
        data = json.load(fin)
    key = data['key']
    return key

def main():
    args = cmd()
    key = loadKey(args.key)
    translateSentences(args.sentence_folder, args.output_folder, key)

if __name__ == '__main__':
    main()
