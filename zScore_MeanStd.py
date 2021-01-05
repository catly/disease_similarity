import numpy as np
import json

GO_tab = np.load('data/GO_tab.npy')
SR = np.load('data/SR.npy')

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
    return 0

GetMeanStd()