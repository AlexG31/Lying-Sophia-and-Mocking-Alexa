import gpt_2_simple as gpt2
import tensorflow as tf
from tensorflow.core.protobuf import rewriter_config_pb2
import sys, logging, time

#model_name = "124M"
model_name = "774M"
log_path = sys.argv[1]
logging.basicConfig(filename=log_path, filemode='w', level = logging.INFO)
logger = logging.getLogger('train_model')
logger.info('start training at {}'.format(time.time()))
gpt2.download_gpt2('./models', model_name)

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, model_name=model_name)

print('-----generate-----')
gpt2.generate(sess,
    temperature=0.7,
    model_name=model_name)
