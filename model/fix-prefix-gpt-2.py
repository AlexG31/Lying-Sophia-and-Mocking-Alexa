import gpt_2_simple as gpt2
import tensorflow as tf
import glob
import json,argparse
import os, sys, re
from tensorflow.core.protobuf import rewriter_config_pb2
import sys, logging, time
from util import loadSeedFile, outputJsonFile

logger = logging.getLogger('train_model')

outputFile = './gen-result.json'
rawOutputFile = './raw-output.txt'
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
    line = line.split('\n')[0]
    line = re.sub(r'[_<>\|]+', ' ', line)
    return line

def loadSeeds(args, index = 0):
    files = glob.glob(os.path.join(args.seed_folder, '*.txt'))
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
    parser.add_argument(
        '--model_dir', help="models dir", default='models')
    parser.add_argument(
        '--start_index', help="seed start index", type=int, default=0)
    parser.add_argument(
        '--seed_cap', help="max number of seeds to run in a session", type=int, default=3)
    parser.add_argument(
        '--seed_folder', help="seed file folder", type=str, default='../seed/')

    args = parser.parse_args()
    return args

def validLength(line):
    words = line.split(' ')
    return len(line) < 3000 and len(words) < 200

def generateWithGarentee(sess, seed, model_name, repeatCap = 10):
    line = seed
    for r in range(repeatCap):
        print('[repeat {}]'.format(r))
        result = generate(sess, seed, model_name)
        print(u'result size {}'.format(len(result)))
        line = simpleCut(result)
        if validLength(line) and len(line) - len(seed) > 2:
            break
    return line

def runSeeds(seeds, args):
    tf.reset_default_graph()
    model_name = args.model_name
    with gpt2.start_tf_sess() as sess:
        gpt2.load_gpt2(sess, model_name=model_name, model_dir=args.model_dir)
        for ind, s in enumerate(seeds):
            if ind < args.start_index:
                continue
            start_time = time.time()
            outputPath = os.path.join(args.output_json_folder, 
                'sentence-{}.json'.format(start_time))
            logger.info('start training at {}'.format(start_time))
            print(u"[{}]using seed {}".format(ind, s))
            line = generateWithGarentee(sess, s, model_name)

            print('[line]{}'.format(line))
            outputJsonFile(dict(seed=s, result = line), outputPath)

            print('time cost {}s'.format(time.time() - start_time))
            logger.info('time cost {}s'.format(time.time() - start_time))

if __name__ == '__main__':
    args = cmd()

    log_path = args.log_path
    logging.basicConfig(filename=log_path, filemode='w', level = logging.INFO)

    print('-----generate-----')
    seeds = loadSeeds(args)
    for ind in range(0, len(seeds), args.seed_cap):
        print('seed range[{}:{}]'.format(ind, ind + args.seed_cap))
        sub_seeds = seeds[ind:ind + args.seed_cap]
        runSeeds(sub_seeds, args)
    

    print('done.')
