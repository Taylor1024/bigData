#!/usr/bin/python
#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import math 
from snownlp import SnowNLP

#整个文本对象
text = pd.read_csv('data.csv')

# att 情感分析行
contents_column = text.iloc[:,6]
  #   print contents_column
senti = [ SnowNLP(i).sentiments for i in contents_column ]
  #   print senti 这是矩阵中的行
att = []
for i in senti:
    if (i>0.3):
        att.append(1)
    else:
        att.append(-1)
  #print att 得到判定正负一的行，存储在 att 中



# sco 用户评价分数
  #这是个列
sco = text.iloc[:,3]


# vote 用户被支持数量
vote = text.iloc[:,4]

#情感倾向
tend = np.dot(att,vote)
  #print tend
if tend > 0:
    print 'positive'
else:
    print 'negetive'

#贡献分数
tribute = np.dot(att,sco)
print tribute

b = tribute * (-1)
E = math.e
f = 1/ ( 1 + pow( E,b) )
print f
