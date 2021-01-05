import pymysql
import json
import numpy as np
with open("data/gene_dict.json", 'r') as f:
    gene_dict = json.load(f)

# zero = 6.827949599114621e-05
# five = 0.3451084705628499

#humannet平滑得到相似度矩阵
def get_R():
     sum = 1061723.4732867337
     z = 0.001
     t = 100000/0.35#最大最小归一化系数
     # 查找基因对
     R = [[0.00019508427426041775] * 20071 for _ in range(20071)]
     for i in range(0,20071):
         R[i][i] = 1

     conn = pymysql.connect("******", "*******", "******", "******")
     # 获得Cursor
     cursor = conn.cursor()
     # 查找基因对
     count = cursor.execute('select gene1,gene2,similar from humannet')
     print(count)
     for i in range(count):
         g_g_s = cursor.fetchone()
         g1 = g_g_s[0]
         g2 = g_g_s[1]
         s = g_g_s[2]
         g1_num = gene_dict [g1]
         g2_num = gene_dict [g2]
         similar = (s+z*2) / (sum + 20071 * 20071 * z) *t
         print(g1,g1_num,g2,g2_num,similar)
         R[g1_num][g2_num] = similar
         R[g2_num][g1_num] = similar
     np.save('data/R.npy',R)
     conn.close()


get_R()
