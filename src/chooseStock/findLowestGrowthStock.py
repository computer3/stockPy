#coding=utf-8
'''
Created on 2015年6月8日
寻找某一时间段内涨幅最低的股票
@author: Administrator
'''
import tushare as ts
from pandas import DataFrame
from urllib2 import URLError
import time


def getLowestGrowth(startDate, endDate,stockList):
    result = {}
    while len(stockList) > 0:
        try:
            stockCode = stockList[-1]
            print  stockCode,'is started'
            #取当天有交易的股票
            if float(ts.get_realtime_quotes(stockCode).price) > 0:
                df_tran = ts.get_h_data(stockCode, start=startDate, end=endDate) 
                #将收盘价转化为数值
                df_tran['close'] = df_tran['close'].convert_objects(convert_numeric=True)
                #按日期由远及近进行排序
                df_tran = df_tran.sort_index()
                stock = {}
               
                stock['maxPxAll']  = max(df_tran.close)
                stock['minPxAll'] = min(df_tran.close)
                stock['maxGrowthRate'] = (stock['maxPxAll'] - stock['minPxAll'])/stock['minPxAll']      
                result[stockCode] = stock       
                print  stockCode,'is finished'
                stockList.pop()
            else:
                stockList.pop()
     
        except URLError,e:
            print 'Error',stockCode,str(e)
            continue  
        except BaseException, e:
            print 'Error',stockCode,str(e)
            stockList.pop()
            continue     
                 
    df = DataFrame(result).T   
    df = df.sort(columns = 'maxGrowthRate')
    return df

    
if __name__ == '__main__':
    startDate = '2015-04-01'
    endDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
#     df_all_stock = ts.get_stock_basics()
#     #获取深市所有在20140101前上市的股票
#     df_all_stock = ts.get_stock_basics()
#     stockCodeList = list(df_all_stock.index)
#     stockCodeList = [code for code in stockCodeList if (code[0] == '0' or code[0] == '3') and df_all_stock.ix[code]['timeToMarket'] < 20140101]
#     
#     #获取金融行业的股票列表
#     df = ts.get_industry_classified()
#     stockCodeList = list(df[df.c_name == u'金融行业']['code'])
#     #获取证券的股票列表
#     df = df_all_stock[df_all_stock.name.str.contains(u'证券')]
#     stockCodeList = list(df.index)
    
    #获得沪深300的股票
    df = ts.get_hs300s()
    stockCodeList = list(df['code'])
    print 'Total stock number is ', len(stockCodeList)
    df = getLowestGrowth(startDate, endDate,stockCodeList)
    fileName = r'D:\stock\ stock_growth_' +startDate+'_' + endDate + '.csv'
    df.to_csv(fileName)


