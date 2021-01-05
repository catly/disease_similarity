#f+h->S
import json
import time
import numpy as np
import math
from goatools import obo_parser
GO = 18330
Gene = 20071
with open("data/GO2gene_dict.json", 'r') as f:
    GO2gene_dict = json.load(f)
with open("data/gene_dict.json", 'r') as f:
    gene_dict = json.load(f)

GO_tab = np.load('data/GO_tab.npy')
DR = np.load('data/DR.npy')
go_obo = obo_parser.GODag('data/go-basic.obo',optional_attrs={'part_of'})


with open("data/GO_dict_tc.json", 'r') as f:
    GO_dict_tc = json.load(f)



#取公共父节点
def GetCommonparent(t1,t2):
    goids = []
    goids.append(t1)
    goids.append(t2)
    rec = go_obo[goids[0]]
    candidates = rec.get_all_parents()
    candidates.update({rec.item_id})
    # Find intersection with second to nth GO ID
    for goid in goids[1:]:
        rec = go_obo[goid]
        parents = rec.get_all_parents()
        parents.update({rec.item_id})
        # Find the intersection with the candidates, and update.
        candidates.intersection_update(parents)
        if len(candidates) == 0:
            root = rec.namespace
            switch = {'molecular_function': "GO:0003674",  # 注意此处不要加括号
                      'biological_process': "GO:0008150",  # 注意此处不要加括号
                      'cellular_component': "GO:0005575",  # 注意此处不要加括号
                      }
            choice = root  # 获取选择
            s = switch.get(choice)
            return s
        s = max(candidates, key=lambda t: go_obo[t].depth)
    return s

def GetChild(p):
    term1 = go_obo.query_term(p)
    child = term1.get_all_children()
    child = list(child)
    return child



def GOSimilar_f(d,g1,g2,gp):
    u = len(set(gp).union(set(g1).union(set(g2))))
    G1 = len(g1)
    G2 = len(g2)
    f = d*d*u+(1-d*d)*((G1*G2)**0.5)
    return f


#计算GO_term相似度h
def GOSimilar_h(d,G1,G2):
    ma = max(G1,G2)
    h = d*d*GO+(1-d*d)*ma
    return h


#计算GO_term相似度S
def GOSimilar_S(t1,t2):
    p = GetCommonparent(t1,t2)
    if p == 0:
        return 0
    try:
        i = GO_dict_tc[p][1]
    except KeyError:
        gp = []    
    else:
        gp = i  
    g1 = GO_dict_tc[t1][1]
    g2 = GO_dict_tc[t2][1]
    G1 = len(g1)
    G2 = len(g2)
    Gp = len(gp)
    i = GO_dict_tc[t1][0]
    j = GO_dict_tc[t2][0]
    d = DR[i][j]
    f = GOSimilar_f(d,g1,g2,gp)
    h = GOSimilar_h(d,G1,G2)
    S = (2*math.log(Gene)-2*math.log(f))/(2*math.log(Gene)-math.log(G1)-math.log(G2))*(1-h*Gp/(Gene*Gene))
    return S



#得到GO_S相似度矩阵
def get_SR():
    # 查找基因对
    G = [[0] * 18330 for _ in range(18330)]
    for i in range(0,18330):
        G[i][i] = 1
    for i in range(0,18330):
        for j in range(i+1,18330):
            go1 = GO_tab[i]
            go2 = GO_tab[j]
            s = GOSimilar_S(go1,go2)
            G[i][j] = s
            G[j][i] = s
        print(i)
    np.save('data/SR.npy',G)


get_SR()

