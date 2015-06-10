#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
import tushare as ts
from numpy import mean


def add5DayChangeRate(df):
    #前5日平均涨跌量
    for i in range(5,len(df)):
        df.ix[i,'changeMa5'] = mean(df.ix[i-5:i,'price_change'])
        
if __name__ == '__main__':
    df_sh= ts.get_hist_data('sh') 
    df_sh = ts.get_h_data('000001', index=True,start='2006-01-01',end='2015-06-09')       
    df_sh['gap'] = (df_sh['high']-df_sh['low'])*100/df_sh['close']
    df_sh = df_sh.sort_index(ascending=False)
#     add5DayChangeRate(df_sh) 
    
    df = df_sh.loc[:,['close','gap']]
    print df
    df.to_csv(r'D:\stock\index_01.csv')