import gpt_2_simple as gpt2
import tensorflow as tf
import glob
import json
import os, sys
from tensorflow.core.protobuf import rewriter_config_pb2
import sys, logging, time

log_path = sys.argv[1]
logging.basicConfig(filename=log_path, filemode='w', level = logging.INFO)
logger = logging.getLogger('train_model')

outputFile = './gen-result.json'
rawOutputFile = './raw-output.txt'
seed_folder = '../seed/'
model_name = "774M"
def generate(sess, prefix, turn = 100, length = 1023):
    # results = gpt2.generate(sess,
    #     length=length,
    #     nsamples=20,
    #     temperature=0.7,
    #     prefix=cur,
    #     return_as_list=True)
    results = gpt2.generate(sess,
        temperature=0.7,
        prefix = prefix,
        model_name=model_name,
        return_as_list = True)
    return results

def loadSeedFile(path):
    seeds = []
    with open(path, 'r', encoding='utf8') as fin:
        for line in fin:
            seeds.append(line.strip('\r\n'))
    return seeds
            
def loadSeeds(index = 0):
    files = glob.glob(os.path.join(seed_folder, '*.txt'))
    assert(len(files) > 0)
    return loadSeedFile(files[0])

def rawOutput(path, seed, result):
    with open(path, 'w', encoding = 'utf8') as fout:
        fout.write(u'seed: {}\n'.format(seed))
        fout.write(u'----------\n')
        for line in result:
            fout.write(u'{}\n'.format(line))

def outputJsonFile(data, path):
    with open(path, 'w', encoding='utf8') as fout:
        json.dump(data, fout, indent = 4, ensure_ascii = False)

if __name__ == '__main__':
    start_time = time.time()
    logger.info('start training at {}'.format(start_time))
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, model_name=model_name)

    print('-----generate-----')
    seeds = loadSeeds()
    generationResults = dict()
    for ind, s in enumerate(seeds):
        print(u"[{}]using seed {}".format(ind, s))
        result = generate(sess, s)
        print(u'result size {}'.format(len(result)))
        rawOutput(rawOutputFile, s, result)
        generationResults[s] = result

    logger.info('time cost {}s'.format(time.time() - start_time))
    print('done.')