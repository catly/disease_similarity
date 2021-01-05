import numpy as np
import json

with open("data/gene_dict.json", 'r') as f:
    gene_dict = json.load(f)
with open("GO2gene_dict.json", 'r') as f:
    GO2gene_dict = json.load(f)
GO_tab = np.load('data/GO_tab.npy')
R = np.load('data/R.npy')


#累乘，求和(term对应基因集list)
def Sum_Multipy_G(list1,list2):
    W = list()
    for x in list1:
        l = list()
        for y in list2:
            i = gene_dict[x]
            j = gene_dict[y]
            d = R[i][j]
            l.append(d)
        W.append(l)
    W = np.array(W)
    c1 = np.prod(W,axis=1)  #列乘
    c2 = np.prod(W,axis=0)  #行乘
    r1 = np.sum(c1)
    r2 = np.sum(c2)
    return r1,r2


def get_D(t1,t2):
    G1 = GO2gene_dict[t1]
    G2 = GO2gene_dict[t2]
    x ,y = Sum_Multipy_G(G1, G2)
    G = list(set(G1).union(set(G2)))
    z = len(G)
    D = (x + y) / (2 * z - x - y)
    return D


#得到GO_D相似度矩阵
def get_DR():
    # 查找基因对
    G = [[0] * 18330 for _ in range(18330)]
    for i in range(0,18330):
        G[i][i] = 1
    for i in range(0,18330):
        for j in range(i+1,18330):
            go1 = GO_tab[i]
            go2 = GO_tab[j]
            s = get_D(go1,go2)
            G[i][j] = s
            G[j][i] = s
        print(i)
    np.save('data/DR.npy',G)

get_DR()
