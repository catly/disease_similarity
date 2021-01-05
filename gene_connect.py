import pickle
import numpy as np
import re
# f1 = open('order_data_ave/1/gene_150.pkl', "r", encoding ='utf - 8')
# f2 = open('order_data_ave/2/gene_150.pkl', "r", encoding ='utf - 8')

def load_obj(name):
    with open(name+'.pkl', 'rb') as f:
        return pickle.load(f)
f1 = load_obj('dim_data_ave/400/gene_first')
f2 = load_obj('dim_data_ave/400/gene_second')

def save_obj(obj,name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def main():
    third = {}
    for key in f1:
        fe1 = f1[key]
        fe2 = f2[key]
        third[key] = np.hstack([fe1,fe2])

    save_obj(third, "dim_data_ave/400/gene_third")
    return 0

main()

