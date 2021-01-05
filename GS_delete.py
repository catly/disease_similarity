import numpy as np

def get_Graph_():
    print('read')
    R_tab = np.load('data/gene_tab.npy')
    GS = np.load('data/GenSimR.npy')
    print('begin')
    D = list()
    T = list()
    z = float(1)
    o = float(0)

    for i in range(0, 20070):
        gene1 = str(R_tab[i])
        print(i)
        if i  == 0:
            D = GS[:,i]
            continue
        sum = np.sum(GS[:,i])
        if sum == z or sum == o:
            print("sum:",sum)
            continue
        T.append(gene1)
        D = np.c_[D,GS[:,i]]
    print(len(D[1]))
    np.save('data/GenSimR.npy',D)
    np.save('data/GS_tab.npy',T)

get_Graph_()