
import numpy as np
from openpyxl import load_workbook
import pickle


# 将数据整理为ROC可读的格式
def ROC_data():
    f1 = open('data/random2_similar.txt')
    f2= open('data/ROC_data.txt', 'a+', encoding='utf-8')
    i =128
    for line in f1.readlines():
        l = line.split(':')
        s = l[1].split('\n')
        f2.write(str(i))
        f2.write(',')
        f2.write(str(s[0]))
        f2.write(',')
        f2.write('0')
        f2.write('\n')
        i = i + 1
    f1.close()
    f2.close()



ROC_data()