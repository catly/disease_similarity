import tensorflow as tf
import numpy as np
import argparse
from model import LINEModel
from utils import DBLPDataLoader
import pickle
import time


def main():
    # 处理命令行
    # 创建解析对象
    parser = argparse.ArgumentParser()
    # 添加命令行 设置参数
    parser.add_argument('--embedding_dim', default=200)  # 嵌入维度
    parser.add_argument('--batch_size', default=128)  # 每次batch采样个数
    parser.add_argument('--K', default=5)  # 负采样个数
    parser.add_argument('--proximity', default='second-order', help='first-order or second-order')
    parser.add_argument('--learning_rate', default=0.01)  # 初始学习率
    parser.add_argument('--mode', default='train')
    parser.add_argument('--num_batches', default=50000)  # batch次数
    parser.add_argument('--total_graph', default=True)
    args = parser.parse_args()
    if args.mode == 'train':
        train(args)
    elif args.mode == 'test':
        test(args)


def train(args):
    data_loader = DBLPDataLoader()
    suffix = args.proximity
    args.num_of_nodes = data_loader.num_of_nodes
    model = LINEModel(args)
    with tf.Session() as sess:
        print(args)
        print('batches\tloss\tsampling time\ttraining_time\tdatetime')
        tf.global_variables_initializer().run()
        initial_embedding = sess.run(model.embedding)
        learning_rate = args.learning_rate
        sampling_time, training_time = 0, 0
        for b in range(args.num_batches):
            t1 = time.time()
            u_i, u_j, label = data_loader.fetch_batch(batch_size=args.batch_size, K=args.K)
            feed_dict = {model.u_i: u_i, model.u_j: u_j, model.label: label, model.learning_rate: learning_rate}
            t2 = time.time()
            sampling_time += t2 - t1

            if b % 100 != 0:
                sess.run(model.train_op, feed_dict=feed_dict)
                training_time += time.time() - t2
                # learn_rate = tf.train.natural_exp_decay(
                #     learning_rate=args.learning_rate, global_step=args.num_batch, decay_steps=100, decay_rate=0.9, staircase=False)

                if learning_rate > args.learning_rate * 0.0001:
                    learning_rate = args.learning_rate * (1 - b / args.num_batches)
                else:
                    learning_rate = args.learning_rate * 0.0001

            else:
                loss = sess.run(model.loss, feed_dict=feed_dict)
                print("learning_rate:",learning_rate)
                print('%d\t%f\t%0.2f\t%0.2f\t%s' % (b, loss, sampling_time, training_time,
                                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                sampling_time, training_time = 0, 0
            if b % 1000 == 0 or b == (args.num_batches - 1):
                embedding = sess.run(model.embedding)
                normalized_embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
                pickle.dump(data_loader.embedding_mapping(normalized_embedding),
                            open('data/gene_embedding.pkl', 'wb'))


def test(args):
    pass

if __name__ == '__main__':
    main()