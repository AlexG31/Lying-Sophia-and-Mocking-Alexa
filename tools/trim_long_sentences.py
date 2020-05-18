#encoding:utf8

import os, json, sys
import glob

def get_sentence_length(path):
    with open(path, 'r') as fin:
        data = json.load(fin)
        return len(data['result'])


def main():
    folder = sys.argv[1]
    # threshold can be 250
    threshold = int(sys.argv[2])
    output = 'tmp-rm-list.txt'
    json_list = glob.glob(os.path.join(folder, '*.json'))
    print('read {} sentences json from folder {}'.format(len(json_list), folder))
    with open(output, 'w') as fout:
        for j in json_list:
            l = get_sentence_length(j)
            if l > threshold:
                fout.write(j + '\n')

# python3 trim_long_sentences.py ../local_demo/resources/sentences/ 250
if __name__ == '__main__':
    main()