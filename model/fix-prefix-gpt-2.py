import gpt_2_simple as gpt2
import tensorflow as tf
import glob
import json,argparse
import os, sys
from tensorflow.core.protobuf import rewriter_config_pb2
import sys, logging, time
from util import loadSeedFile, outputJsonFile

logger = logging.getLogger('train_model')

outputFile = './gen-result.json'
rawOutputFile = './raw-output.txt'
seed_folder = '../seed/'
def generate(sess, prefix, model_name, turn = 100, length = 1023):
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

def simpleCut(result):
    line = result[0]
    return line.split('\n')[0]

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

def cmd():
    parser = argparse.ArgumentParser(
        description="Easily retrain OpenAI's GPT-2 text-generating model on new texts. (https://github.com/minimaxir/gpt-2-simple)"
    )

    parser.add_argument(
        '--output_json_folder', help="output json sentence path", default='./')
    parser.add_argument(
        '--log_path', help="log path", default='./gpt2-generate-log.txt')
    parser.add_argument(
        '--model_name', help="124M, 774M", default='774M')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = cmd()

    model_name = args.model_name
    log_path = args.log_path
    logging.basicConfig(filename=log_path, filemode='w', level = logging.INFO)
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, model_name=model_name)

    print('-----generate-----')
    seeds = loadSeeds()
    for ind, s in enumerate(seeds):
        start_time = time.time()
        outputPath = os.path.join(args.output_json_folder, 
            'sentence-{}.json'.format(start_time))
        logger.info('start training at {}'.format(start_time))
        print(u"[{}]using seed {}".format(ind, s))
        result = generate(sess, s, model_name)
        line = simpleCut(result)
        print('[line]{}'.format(line))
        print(u'result size {}'.format(len(result)))
        outputJsonFile(dict(seed=s, result = line), outputPath)

        print('time cost {}s'.format(time.time() - start_time))
        logger.info('time cost {}s'.format(time.time() - start_time))
    print('done.')