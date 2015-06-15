#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
import tushare as ts
from tools import dbOper
# sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板
def getHistIndexData():
    df_sh= ts.get_hist_data('sh') 
#     df_sh = ts.get_h_data('000001', index=True,start='2006-01-01',end='2015-06-09')       
    df_sh['gap'] = (df_sh['high']-df_sh['low'])*100/df_sh['close']
    df_sh = df_sh.sort_index(ascending=False)
    df = df_sh.loc[:,['close','gap']]
    print df
    df.to_csv(r'D:\stock\index_02.csv')

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

def getHistIndexData1(startDate,endDate):
#     df_sh= ts.get_hist_data('sh',start =startDate,end = endDate )
#     df_sz= ts.get_hist_data('sz')
#     df_zxb= ts.get_hist_data('zxb')
#     df_cyb= ts.get_hist_data('cyb')

    df_trans = dbOper.getHistTran(startDate, endDate)
    df_trans['mkt'] = df_trans.code.apply(setStockMkt)
    df_trans['p_change_type'] = df_trans.p_change.apply(setPriceChangeType)
    df_index = df_trans.groupby(['tran_date','mkt','p_change_type']).size()
#     df_ix_sh = df_index[df_index['mkt'] == 'sh']
    print df_index

 
    

if __name__ == '__main__':
    getHistIndexData1('2015-05-29','2015-06-01')