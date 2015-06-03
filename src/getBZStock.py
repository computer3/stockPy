#coding=utf-8
'''
补涨股选取
1.最新收盘价在2015年最高价的0.8-0.9之间
2.从20140101到当前最高涨幅在200%以下
3.当前5日成交量为20日内最高成交量的0.3-0.5之间
4.有效换手率在5%以下。有效换手率=日成交股数/（总流通股本-第一大流通股东流通股数量）
5.5日内日成交金额在5亿以下
'''
import tushare as ts
import time
import logging  
from pandas import DataFrame
from numpy import mean
from urllib2 import URLError


def getStockInfo(startDate, endDate,  stockCode,specialDate):
    if startDate > specialDate:
        print "startDate should be before the specialDate"
        return None
    stock = {}
    df_tran = ts.get_h_data(stockCode, start=startDate, end=endDate)
    df_tran['close'] = df_tran['close'].convert_objects(convert_numeric=True)
    df_tran['volume'] = df_tran['volume'].convert_objects(convert_numeric=True)
    df_tran['amount'] = df_tran['amount'].convert_objects(convert_numeric=True)
    
    #按日期由远及近进行排序
    df_tran = df_tran.sort_index()

    stock['maxPxSpecialDate'] = max(df_tran[specialDate:].close)
    stock['minPxSpecialDate'] = min(df_tran[specialDate:].close)
    stock['maxPxAll']  = max(df_tran.close)
    stock['minPxAll'] = min(df_tran.close)
    stock['maxVol20']  = max(df_tran[-20:].volume)
    stock['maxGrowthRate'] = (stock['maxPxAll'] - stock['minPxAll'])/stock['minPxAll']  
    stock['prePx'] = df_tran[-1:].close
    stock['prePXMa5'] = mean(df_tran[-5:].close)
    stock['preVolMa5'] = mean(df_tran[-5:].volume)
    stock['preAmtMa5'] = mean(df_tran[-5:].amount)
    return stock

def chooseBZStock(startDate, endDate):
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(r'C:\log\stock.log')
    logger.addHandler(fh)

    result = {}
    df_all_stock = ts.get_stock_basics()
    for i in range(len(df_all_stock)):    
        try:
            stockCode = df_all_stock.index[i]
    #         stockCode = df_all_stock[i]
            if float(ts.get_realtime_quotes(stockCode).price) == 0:
                continue;
            print stockCode,'is starting'
            stock = getStockInfo(startDate, endDate, stockCode,'2015-01-01')
    
            if  stock['prePx']<= stock['maxPxSpecialDate']*0.9 and stock['prePx'] >=stock['maxPxSpecialDate'] * 0.8:                     
                if (stock['maxPxAll'] - stock['minPxAll'])/stock['minPxAll'] <2:                                
                    if stock['preVolMa5'] <= stock['maxVol20']*0.5 and stock['preVolMa5'] >= stock['maxVol20']*0.3:                     
                        if stock['preAmtMa5'] < 500000000:
                            result[stockCode] = stock   
            print  stockCode,'is finished'               
        except BaseException, e:
            print stockCode,str(e)
            logger.error('Code: '+stockCode+ ' : '+str(e))       
            continue                  
    df = DataFrame(result).T
    print df
    
    
def getLowestGrowth(startDate, endDate):
    result = {}
    df_all_stock = ts.get_stock_basics()
    stockCodeList = list(df_all_stock.index)
    szStockList = [code for code in stockCodeList if code[0] == '0' or code[0] == '3']

    while len(szStockList) > 0:
        try:
            stockCode = szStockList[-1]
            print  stockCode,'is started'
            if float(ts.get_realtime_quotes(stockCode).price) > 0 and df_all_stock.ix[stockCode]['timeToMarket'] < 20140101:  
                stock = getStockInfo(startDate, endDate, stockCode,'2015-01-01')                
                result[stockCode] = stock       
                print  stockCode,'is finished'
                szStockList.pop()
            else:
                szStockList.pop()     
        except URLError,e:
            print 'Error',stockCode,str(e)
            continue  
        except BaseException, e:
            print 'Error',stockCode,str(e)
            szStockList.pop()
            continue       
 
                 
    df = DataFrame(result).T   
    df = df.sort(columns = 'maxGrowthRate')
    return df[:10]

    
    
if __name__ == '__main__':
    startDate = '2014-01-01'
    endDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
    stockCode = '600583'

#     print getStockInfo(startDate, endDate, stockCode,'2015-01-01')   
    df = getLowestGrowth(startDate, endDate)
    print df.loc[:,['maxGrowthRate','minPxAll','maxPxAll']]
