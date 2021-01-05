import tensorflow as tf


class LINEModel:
    def __init__(self, args):
        self.u_i = tf.placeholder(name='u_i', dtype=tf.int32, shape=[args.batch_size * (args.K + 1)])
        print("LINEModel.u_i")
        self.u_j = tf.placeholder(name='u_j', dtype=tf.int32, shape=[args.batch_size * (args.K + 1)])
        print("LINEModel.u_j")
        self.label = tf.placeholder(name='label', dtype=tf.float32, shape=[args.batch_size * (args.K + 1)])
        print("LINEModel.labe")

        #初始化向量
        self.embedding = tf.get_variable('target_embedding', [args.num_of_nodes, args.embedding_dim],
                                         initializer=tf.random_uniform_initializer(minval=-1., maxval=1.))
        print("LINEModel.embedding")

        self.u_i_embedding = tf.matmul(tf.one_hot(self.u_i, depth=args.num_of_nodes), self.embedding)
        print("LINEModel.u_i_embedding")
        if args.proximity == 'first-order':
            self.u_j_embedding = tf.matmul(tf.one_hot(self.u_j, depth=args.num_of_nodes), self.embedding)
            print("LINEModel.u_j_embedding")
        elif args.proximity == 'second-order':
            self.context_embedding = tf.get_variable('context_embedding', [args.num_of_nodes, args.embedding_dim],
                                                     initializer=tf.random_uniform_initializer(minval=-1., maxval=1.))
            print("LINEModel.context_embedding")
            self.u_j_embedding = tf.matmul(tf.one_hot(self.u_j, depth=args.num_of_nodes), self.context_embedding)
            print("LINEModel.u_j_embedding")


        self.inner_product = tf.reduce_sum(self.u_i_embedding * self.u_j_embedding, axis=1)
        print("LINEModel.inner_product")

        self.loss = -tf.reduce_mean(tf.log_sigmoid(self.label * self.inner_product))
        print("LINEModel.loss")
        self.learning_rate = tf.placeholder(name='learning_rate', dtype=tf.float32)
        print("LINEModel.learning_rate")
        # self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate)
        self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate)
        print("LINEModel.optimizer")
        self.train_op = self.optimizer.minimize(self.loss)
        print("LINEModel.train_op")


