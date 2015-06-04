#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
from sqlalchemy import create_engine
import tushare as ts
from urllib2 import URLError
import time
from numpy import mean

# 添加变化量和变化率
# 默认时间按降序排
def addChangRate(df):
    for i in range(len(df) - 1):
        df.ix[i,'change'] = df.ix[i,'close'] - df.ix[i+1,'close']
        df.ix[i,'changeRate'] = df.ix[i,'change']/df.ix[i+1,'close']

# 默认时间按降序排

def add5DayChangeRate(df):
    #前5日平均涨跌量
    for i in range(5,len(df) - 5):
        print df.ix[i-5:i+5,'change']
        df.ix[i,'changeMa5'] = mean(df.ix[i-5:i+5,'change'])




if __name__ == '__main__':
    df_sh = ts.get_h_data('000001',index=True)
#     df_sz = ts.get_h_data('399001',index=True)
#     df_hs300 = ts.get_h_data('000300',index=True)
        
    df_sh['gap'] = df_sh['high']-df_sh['low']
    addChangRate(df_sh)
    add5DayChangeRate(df_sh)
    
    
    df = df_sh.loc[:,['close','gap','change','changeMa5']]
    print df
    df.to_csv(r'D:\stock\index.csv')