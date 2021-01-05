import pymysql
import math
import numpy as np
import json
import networkx as nx
import matplotlib
matplotlib.use('agg')

#全部GO_term和GO中gene数量
GO = 18330
Gene_G = 19661
#Humannet中gene数量
Gene_H = 17929
#所有的基因量
Gene = 20071

SR = np.load('data/SR.npy')
R_tab = np.load('data/gene_tab.npy')
GO_tab = np.load('data/GO_tab.npy')

#GO_dict_tsm[GO_term] = [i,mean std]
with open("data/GO_dict_tms.json", 'r') as f:
    GO_dict_tsm = json.load(f)
with open("data/Gene2GO_dict.json", 'r') as f:
    Gene2GO_dict = json.load(f)
with open("data/GOs_z.json", 'r') as f:
    GOs_z = json.load(f)
print("begin:")




# 获得GO_term t 和  GO_terms T的相似度
def Sim(t,T):
    max1 = 0
    max2 = 0
    h = 0
    l = 0
    L= 0
    for j in T:
        gos = t + ',' + j
        try:
            z = GOs_z[gos]
        except KeyError:
            continue
        if z > 1.6:
            h = h+1
            if max1<z:
                max1 = z
                H = j
        if z < -1.6 :
            l = l+1
            if max2 > z :
                max2 = z
                L = j
        else:
            continue
    if h > l :
        i = GO_dict_tsm[t][0]
        j = GO_dict_tsm[H][0]
        Sim = SR[i][j]
    elif L == 0:
        return 0
    else:
        i = GO_dict_tsm[t][0]
        j = GO_dict_tsm[L][0]
        Sim = SR[i][j]
    return Sim


def GeneSim(g1,g2):
    try:
        T1 = Gene2GO_dict[g1]
    except KeyError:
        return 0
    try:
        T2 = Gene2GO_dict[g2]
    except KeyError:
        return 0
    x = 0
    y = 0
    for i in T1:
        x = x + Sim(i,T2)
    for j in T2:
        y = y + Sim(j,T1)

    z = len(T1) + len(T2)
    genesim = (x+y)/z

    return genesim


#得到Gene_S相似度矩阵
def get_GS():
    # 查找基因对
    G = [[0] * 20071 for _ in range(20071)]
    for i in range(0,20071):
        G[i][i] = 1
    for i in range(0,20071):
        for j in range(i+1,20071):
            #根据位置找基因
            gene1 = R_tab[i]
            gene2 = R_tab[j]
            s = GeneSim(gene1,gene2)
            G[i][j] = s
            G[j][i] = s
        print(i)
    np.save('data/GenSimR_.npy',G)

get_GS()


