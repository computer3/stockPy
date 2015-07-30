#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
import tushare as ts
import pandas as pd
from tools import dbOper
import time
from pandas import DataFrame
# sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板

def setStockMkt(stockCode):
    if stockCode[0] == '6':
        return  'sh'
    elif stockCode[0:3] == '002':
        return 'zxb'
    elif stockCode[0:3] == '300':
        return 'cyb'
    else:
        return 'sz'
def setPriceChangeType(price):
    if price > 0:
        return 'up'
    elif price < 0:
        return 'down'
    else:
        return 'nochange'

def getHistIndexData(startDate,endDate):
    df_sh= ts.get_hist_data('sh',start =startDate,end = endDate ).reset_index()
    df_sz= ts.get_hist_data('sz',start =startDate,end = endDate ).reset_index()
    df_zxb= ts.get_hist_data('zxb',start =startDate,end = endDate ).reset_index()
    df_cyb= ts.get_hist_data('cyb',start =startDate,end = endDate ).reset_index()

    df_trans = dbOper.getHistTran(startDate, endDate)
    df_trans['mkt'] = df_trans.code.apply(setStockMkt)
    df_trans['p_change_type'] = df_trans.p_change.apply(setPriceChangeType)
    df_index = df_trans.groupby(['tran_date','mkt','p_change_type']).size()

    df_index = df_index.unstack(2)
    df_index = df_index.reset_index()
  
    df_index_sh = df_index[df_index['mkt']== 'sh']
    df_sh = pd.merge(df_sh,df_index_sh,left_on='date',right_on='tran_date')
    
    df_index_sz = df_index[df_index['mkt']== 'sz']
    df_sz = pd.merge(df_sz,df_index_sz,left_on='date',right_on='tran_date')
    
    df_index_zxb = df_index[df_index['mkt']== 'zxb']
    df_zxb = pd.merge(df_zxb,df_index_zxb,left_on='date',right_on='tran_date')
    
    df_index_cyb = df_index[df_index['mkt']== 'cyb']
    df_cyb = pd.merge(df_cyb,df_index_cyb,left_on='date',right_on='tran_date')
    
    df_result = df_sh.append(df_sz)
    df_result = df_result.append(df_zxb)
    df_result = df_result.append(df_cyb)
    df_result['gap'] = df_result.high - df_result.low

    df_result = df_result.loc[:,['date','mkt','close','price_change','gap','up','down','nochange']]

    
    fileName = r'D:\stock\index_stat_' +startDate+'_' + endDate + '.csv'
    df_result.to_csv(fileName,index = False)

def getIndexChangeRate(startDate,endDate):    
    df_result = DataFrame()
    df = ts.get_hist_data('sh',start =startDate,end = endDate ).reset_index()
    df['gap'] = df['high'] - df['low']
    df['gap_rate'] = df['gap']/df['close']*100
    df['mkt'] = 'sh'
    df_result = df_result.append(df)
    
    df = ts.get_hist_data('sz',start =startDate,end = endDate ).reset_index()
    df['gap'] = df['high'] - df['low']
    df['gap_rate'] = df['gap']/df['close']*100
    df['mkt'] = 'sz'
    df_result = df_result.append(df)
    
    df = ts.get_hist_data('zxb',start =startDate,end = endDate ).reset_index()
    df['gap'] = df['high'] - df['low']
    df['gap_rate'] = df['gap']/df['close']*100
    df['mkt'] = 'zxb'
    df_result = df_result.append(df)
    
    df = ts.get_hist_data('cyb',start =startDate,end = endDate ).reset_index()
    df['gap'] = df['high'] - df['low']
    df['gap_rate'] = df['gap']/df['close']*100
    df['mkt'] = 'cyb'
    df_result = df_result.append(df)
    
    fileName = r'D:\stock\index_changeRate_' +startDate+'_' + endDate + '.csv'
    df_result = df_result.loc[:,['date','mkt','close','volume','price_change','p_change','gap','gap_rate']]
    df_result = df_result.sort_index(by='date',ascending=False)
    df_result.to_csv(fileName,index = False)

if __name__ == '__main__':
    print str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),'start'
    getIndexChangeRate('2015-06-01','2015-07-30')
#     getHistIndexData()
    print str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),'finished'