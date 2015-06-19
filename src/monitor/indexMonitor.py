#coding=utf-8
'''
Created on 2015年6月17日

@author: Administrator
'''
import tushare as ts
def getRealTimeInfor(stockCode):
    df = ts.get_today_ticks(stockCode)    
    print df.groupby('type')['volume','amount'].sum()
    df = ts.get_realtime_quotes(stockCode)
    print df.loc[:,['price','pre_close','open','high','low']]


if __name__ == '__main__':
    stockCode = '600030'
    getRealTimeInfor(stockCode)