#!/usr/bin/env python3
# Date: 2020/01/05
# Author: Armit

# 主成分分析PCA基本思想：特征值、特征向量
# 构建所有特征的协方差矩阵，求该矩阵的特征值最大的几个方向的特征向量、即主成分
# 第一主成分总是和第二主成分正交、其余同理，最后张开的子空间也是"方的"

import random
import numpy as np
import matplotlib.pyplot as plt

def get_data(N=100, begin=0, end=10):
  fx = lambda x: 1.7 * x + 0.4
  data = np.array([np.array([x, fx(x) + random.random() * random.randrange(4)])
          for x in np.linspace(begin, end, N)
          for _ in range(random.randrange(6))])
  return data

def pca(data, top_n_feat=100):  # data = [(ft1, ft2, ..., ftm), ...]
  # 去平均值/中心化
  data_mean = np.mean(data, axis=0)   # mean by column
  data -= data_mean
  
  # 协方差矩阵特征分解 Cov(X,Y) = E(XY) - E(X)E(Y); Cov(X,X) = D(X)
  cov = np.cov(data, rowvar=False)    # rowvar=False: each column is a variable
  eig_vals, eig_vecs = np.linalg.eig(np.mat(cov))
  eig_vals_idxs = np.argsort(eig_vals)[:-(top_n_feat+1):-1]
  red_eig_vecs = eig_vecs[:, eig_vals_idxs]  # 选择所有行，取指定列
  
  # 还原低维空间数据点
  red_data = data * red_eig_vecs      # 降维后的矩阵
  recon_data = (red_data * red_eig_vecs.T) + data_mean
  return red_data, recon_data

if __name__ == "__main__":
  data = get_data()
  plt.scatter(data[:,0], data[:,1])
  plt.show()
  red_data, recon_data = pca(data)
  plt.scatter(recon_data[:,0], recon_data[:,1])
  plt.show()
