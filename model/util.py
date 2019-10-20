import glob
import json
import os, sys
import sys, logging, time

def loadText(path):
    results = []
    with open(path, 'r', encoding='utf8') as fin:
        for line in fin:
            results.append(line.strip('\r\n'))
    return results
            

if __name__ == '__main__':
    pass