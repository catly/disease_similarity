import numpy as np
import time
import matplotlib
import networkx as nx

matplotlib.use('agg')




def get_Graph():
    print('read')
    R_tab = np.load('data/GS_tab.npy')
    GS = np.load('data/GenSimR.npy')
    print('begin')
    node_n = {}
    z = float(0)
    # edge_distribution
    edge_distribution = list()
    # node_negative_distribution
    node_degree = list()
    # 点相互索引
    node_index = {}
    node_index_reversed = {}

    # node_顺序
    nodes_raw = list()
    # edges
    edges = list()

    for i in range(0, 19660):
        print(i)
        gene1 = str(R_tab[i])
        d = float(0)
        n = list()
        for j in range(0, 19660):
            gene2 = str(R_tab[j])
            if j == i:
                continue
            # 根据位置找基因
            s = GS[i][j]
            s = float(s)
            if (s == z):
                n.append(gene2)
                continue
            d = d + s
            if j > i:
                edge_distribution.append(s)
                edges.append((i, j))
        node_n[i] = n
        # 有边与该点相连
        if d == z:
            print("null node", i)
            continue
        node_index[gene1] = i
        node_index_reversed[i] = gene1
        nodes_raw.append(gene1)
        node_degree.append(d)
    print(len(node_index), len(nodes_raw), len(edge_distribution), len(edges), len(R_tab))
    return nodes_raw, edge_distribution, node_degree, node_index, node_index_reversed, edges,node_n


class DBLPDataLoader:
    def __init__(self):
        # 读取数据:
        self.nodes_raw, self.edge_distribution, \
        self.node_degree, self.node_index, self.node_index_reversed, \
        self.edges, self.node_n= get_Graph()

        t1 = time.time()
        self.num_of_nodes = len(self.node_index)
        self.num_of_edges = len(self.edges)
        
        # 读点
        # self.node_n_degree = {}
        # for key in self.node_n:
        #     nodes = self.node_n[key]
        #     degree = list()
        #     for i in nodes:
        #         degree.append(self.node_degree[self.node_index[i]])
        #     degree = np.array(degree)
        #     degree /= np.sum(degree)
        #     self.node_n_degree[key] = degree

        self.node_negative_distribution = np.power(np.array(self.node_degree), 0.75)
        self.node_negative_distribution /= np.sum(self.node_negative_distribution)
        
        self.edge_distribution /= np.sum(self.edge_distribution)
        t2 = time.time()
        print("%f distribution second:"% (t2 - t1))
        self.node_sampling = AliasSampling(prob=self.node_negative_distribution)
        self.edge_sampling = AliasSampling(prob=self.edge_distribution)
        t3 = time.time()
        print("%f sampling second:"% (t3 - t2))
        
        # self.edges = [(self.node_index[u], self.node_index[v]) for u, v, _ in self.edges_raw]

    def fetch_batch(self, batch_size=16, K=10, edge_sampling='atlas', node_sampling='atlas'):
        if edge_sampling == 'numpy':
            edge_batch_index = np.random.choice(self.num_of_edges, size=batch_size, p=self.edge_distribution)
        elif edge_sampling == 'atlas':
            edge_batch_index = self.edge_sampling.sampling(batch_size)
        elif edge_sampling == 'uniform':
            edge_batch_index = np.random.randint(0, self.num_of_edges, size=batch_size)
        u_i = []
        u_j = []
        label = []
        
        for edge_index in edge_batch_index:
            edge = self.edges[edge_index]
            # if self.g.__class__ == nx.Graph:
            if np.random.rand() > 0.5:      # important: second-order proximity is for directed edge
                edge = (edge[1], edge[0])
            u_i.append(edge[0])
            u_j.append(edge[1])
            label.append(1)
            nodes = self.node_n[edge[0]]
            for i in range(K):
                while True:
                    if node_sampling == 'numpy':
                        negative_node = np.random.choice(self.num_of_nodes, p=self.node_negative_distribution)
                    elif node_sampling == 'atlas':
                        negative_node = self.node_sampling.sampling()
                    elif node_sampling == 'uniform':
                        negative_node = np.random.randint(0, self.num_of_nodes)
                    if negative_node not in nodes:
                        break
                    # if not self.g.has_edge(self.node_index_reversed[negative_node], self.node_index_reversed[edge[0]]):
                    #     break
                u_i.append(edge[0])
                u_j.append(negative_node)
                label.append(-1)
                
        return u_i, u_j, label

    def embedding_mapping(self, embedding):
        # r = {node: embedding[self.node_index[node]] for node in self.nodes_raw}
        # print(len(r))
        # return r
        d = {}
        for node in self.nodes_raw:
            i = self.node_index[node]
            d[node] = embedding[i]
        return d


class AliasSampling:

    # Reference: https://en.wikipedia.org/wiki/Alias_method

    def __init__(self, prob):
        A1 = time.time()
        self.n = len(prob)
        self.U = np.array(prob) * self.n
        self.K = [i for i in range(len(prob))]
        overfull, underfull = [], []
        A2 = time.time()
        print("%f Alia_nUK second:"% (A2 - A1))
        for i, U_i in enumerate(self.U):
            if U_i > 1:
                overfull.append(i)
            elif U_i < 1:
                underfull.append(i)
        A3 = time.time()
        print("%f Alia_enumerate second:"% (A3 - A2))
        while len(overfull) and len(underfull):
            i, j = overfull.pop(), underfull.pop()
            self.K[j] = i
            self.U[i] = self.U[i] - (1 - self.U[j])
            if self.U[i] > 1:
                overfull.append(i)
            elif self.U[i] < 1:
                underfull.append(i)
        A4 = time.time()
        print("%f Alia_overfull and underfull second:"% (A4 - A3))
        
    def sampling(self, n=1):
        x = np.random.rand(n)
        i = np.floor(self.n * x)
        y = self.n * x - i
        i = i.astype(np.int32)
        res = [i[k] if y[k] < self.U[i[k]] else self.K[i[k]] for k in range(n)]

        
        if n == 1:
            return res[0]
        else:
            return res