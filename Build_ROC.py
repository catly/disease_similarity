#使用ROC_data文件数据建立ROC图
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import codecs



def data():
    f = codecs.open('data/ROC_400.txt', mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
    line = f.readline()  # 以行的形式进行读取文件
    list1 = []
    list2 = []
    while line:
        a = line.split(',')
        b = a[1:2]  # 这是选取需要读取的位数
        c = a[2:3]
        list1 += b  # 将其添加在列表之中
        list2 += c
        line = f.readline()
    f.close()
    list1 = map(float, list1)
    list2 = map(float, list2)
    list1 = list(list1)
    list2 = list(list2)
    X = np.array(list1)
    y = np.array(list2)
    return X,y



scores,y = data()
fpr, tpr, thresholds = metrics.roc_curve(y, scores)
print(fpr)
print(tpr)
print(thresholds)
auc = metrics.auc(fpr, tpr)
print(auc)
#############画图##################
plt.title('ROC')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.plot(fpr, tpr, '--*b', label="tuli")
plt.legend()
plt.show()