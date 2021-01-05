import numpy as np
import json


GO_tab = np.load('data/GO_tab.npy')
SR = np.load('data/SR.npy')
with open("data/GO_dict_tms.json", 'r') as f:
    GO_dict_tms = json.load(f)



#获得均值标准差
def GetMeanStd():
    GO_dict_tms = {}
    GO_t = list(GO_tab)
    for i in range(len(GO_t)):
        lis = SR[i]
        # 求均值
        lis_mean = np.mean(lis)
        # 求标准差
        lis_std = np.std(lis, ddof=1)
        GO_dict_tms[GO_t[i]] = [i, lis_mean, lis_std]
    with open('data/GO_dict_tms.json', 'w') as f:
        # # 设置不转换成ascii  json字符串首缩进
        f.write(json.dumps(GO_dict_tms, ensure_ascii=False, indent=2))
    f.close()
    return 0

#计算两个term的Z分数
def zSorce(t,t1):
    lis = GO_dict_tms[t]
    lis1 = GO_dict_tms[t1]
    i = lis[0]
    j = lis1[0]
    S = SR[i][j]
    x= lis[1]
    y = lis[2]
    z = (S - x)/y
    return z

#得到GO_S相似度矩阵
def get_SR():
    GetMeanStd()
    GOs_z = {}
    for i in range(0,18330):
        print(i)
        for j in range(i+1,18330):
            go1 = GO_tab[i]
            go2 = GO_tab[j]
            s = zSorce(go1,go2)
            if s > 1.6 or s < -1.6:
                goa = go1+','+go2
                gob = go2+','+go1
                GOs_z[goa] = s
                GOs_z[gob] = s
    with open('data/GOs_z.json', 'w') as f:
        # # 设置不转换成ascii  json字符串首缩进
        f.write(json.dumps(GOs_z, ensure_ascii=False, indent=2))

get_SR()