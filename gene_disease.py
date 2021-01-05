import json
import  re
import numpy as np
import pickle
np.set_printoptions(linewidth=1000)

with open("D2Gene_dict.json", 'r') as f:
    GO2gene_dict = json.load(f)

def load_obj(name):
    with open(name+'.pkl', 'rb') as f:
        return pickle.load(f)



def save_obj(obj,name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def sum(a,b):
    c = []
    for i in range(0,150):
        c.append(a[i]+b[i])
    return c

# def max_pooling(a,b):
#     for i in range(0,50):
#         if(a[i]<b[i]):
#             a[i]=b[i]
#     return a


fpkl = load_obj('first/gene_150')



def main():
    le = len(GO2gene_dict)
    third = {}
    for i in GO2gene_dict.keys():
        le = le-1
        print(le,i)
        s = GO2gene_dict[i]
        y = float(0)
        b = []
        for j in range(0, 150):
            b.append(y)


        #######
        num = 0
        ######
        for x in s:
            #####
            num = num + 1
            #####
            print(x)
            try:
                k = fpkl[x]
            except:
                ######
                num = num - 1
                ######
                print(x,"x")
                continue
            #######
            b = sum(b,k)
            #######
            # b = max_pooling(b, k)
        ######
        if num != 0:
        ######
            c = np.array(b)
            result = c/num
            third[i] = result
        # third[i] = c

    save_obj(third, "first/disease_150")





main()