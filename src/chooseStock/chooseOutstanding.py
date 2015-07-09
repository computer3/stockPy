#coding=utf-8
'''
Created on 2015年7月9日

@author: Administrator
'''
import tushare as ts
import pandas as pd
def getOutStandingStock():
    df_stk = ts.get_stock_basics().reset_index()

    df_trans = ts.get_today_all()
    df_result = pd.merge(df_stk,df_trans,on = 'code')
    df_result = df_result.loc[:,['code','name_x','industry','outstanding','trade']]
    df_result['outstanding_amt'] =  df_result['outstanding'] * df_result['trade'] * 10000    
    df_result = df_result[df_result.outstanding_amt < 1500000000]
    return df_result
    
def getStockList():
    startDate = '2014-06-20'
    endDate = '2015-07-08'
    df_stock = getOutStandingStock();
    fileName = r'd:\stock\outStandingChoose.csv'
    with open(fileName, 'w') as f:
        strResult = ','.join(['code','trade','high','low','lastYear'])
        f.write(strResult)
        f.write('\n') 
    for stockCode in df_stock['code']:
        try:
            df_tran = ts.get_h_data(stockCode, startDate, endDate)
            trade = float(df_tran.ix[endDate]['close'])
            high =  max(df_tran.close)
            low =  min(df_tran.close)
            lastYear = float(df_tran.ix[startDate]['close'])
            strResult = ','.join([stockCode,str(trade),str(high),str(low),str(lastYear)])
            with open(fileName, 'a') as f:
                f.write(strResult)
                f.write('\n') 
                print stockCode,'is finished'
        except BaseException, e:
            print stockCode,str(e)
            continue
if __name__ == '__main__':
    getStockList()