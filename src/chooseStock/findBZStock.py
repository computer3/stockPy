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


def getStockInfoFQ(startDate, endDate,  stockCode,specialDate):
    if startDate > specialDate:
        print "startDate should be before the specialDate"
        return None
    stock = {}
    df_tran = ts.get_h_data(stockCode, start=startDate, end=endDate,pause=5)
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
    stock['prePx'] = float(df_tran[-1:].close)
    stock['prePXMa5'] = mean(df_tran[-5:].close)
    stock['preVolMa5'] = mean(df_tran[-5:].volume)
    stock['preAmtMa5'] = mean(df_tran[-5:].amount)
    return stock

def getStockInfo(startDate, endDate,  stockCode,specialDate):
    if startDate > specialDate:
        print "startDate should be before the specialDate"
        return None
    stock = {}
    df_tran = ts.get_hist_data(stockCode, start=startDate, end=endDate,pause=5)
    df_tran['close'] = df_tran['close'].convert_objects(convert_numeric=True)
    df_tran['volume'] = df_tran['volume'].convert_objects(convert_numeric=True)
    
    
    #按日期由远及近进行排序
    df_tran = df_tran.sort_index()

    stock['maxPxSpecialDate'] = max(df_tran[specialDate:].close)
    stock['minPxSpecialDate'] = min(df_tran[specialDate:].close)
    stock['maxPxAll']  = max(df_tran.close)
    stock['minPxAll'] = min(df_tran.close)
    stock['maxVol20']  = max(df_tran[-20:].volume)
    stock['maxGrowthRate'] = (stock['maxPxAll'] - stock['minPxAll'])/stock['minPxAll']  
    stock['prePx'] = float(df_tran[-1:].close)
    stock['prePXMa5'] = float(df_tran[-1:].ma5)
    stock['preVolMa5'] = float(df_tran[-1:].v_ma5)
    stock['preAmtMa5'] = float(df_tran[-1:].ma5) * float(df_tran[-1:].v_ma5)*100
    return stock

def chooseBZStock(startDate, endDate,specialDate,stockList,fileName):
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(r'C:\log\stock.log')
    logger.addHandler(fh)
    with open(fileName, 'w') as f:
        strResult = ','.join(['代码','收盘价指标','最高涨幅指标','最大成交量指标','5日成交金额指标'])
        f.write(strResult)
        f.write('\n') 
    while len(stockList) > 0:   
        try:
            stockCode = stockList[-1]
            if float(ts.get_realtime_quotes(stockCode).price) == 0:
                continue;
            print str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),stockCode,'is starting'
            stock = getStockInfo(startDate, endDate, stockCode,specialDate)
    
            strResult = stockCode
            #最新收盘价在2015年最高价的0.8-0.9之间
            if  stock['prePx']<= stock['maxPxSpecialDate']*0.9 and stock['prePx'] >=stock['maxPxSpecialDate'] * 0.8:  
                strResult+=',' + '1'
            else:
                strResult+=',' + '0'
            #从20140101到当前最高涨幅在200%以下                  
            if (stock['maxPxAll'] - stock['minPxAll'])/stock['minPxAll'] <2:
                strResult+=',' + '1'
            else:
                strResult+=',' + '0'
            #当前5日成交量为20日内最高成交量的0.3-0.5之间                             
            if stock['preVolMa5'] <= stock['maxVol20']*0.5 and stock['preVolMa5'] >= stock['maxVol20']*0.3:
                strResult+=',' + '1'
            else:
                strResult+=',' + '0'
            #5日内日成交金额在5亿以下
            if stock['preAmtMa5'] < 500000000:
                strResult+=',' + '1'
            else:
                strResult+=',' + '0'
            
            print strResult
            with open(fileName, 'a') as f:
                f.write(strResult)
                f.write('\n') 
            
            print  str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),stockCode,'is finished'        
            stockList.pop()  
        except URLError,e:
            print 'Error',stockCode,str(e)
            stockList.pop()
            continue         
        except BaseException, e:
            print stockCode,str(e)
            logger.error('Code: '+stockCode+ ' : '+str(e))     
            stockList.pop()  
            continue                  

    
    

    
    
if __name__ == '__main__':
    fileName = r'd:\stock\stockBZChoose.csv'
    startDate = '2014-01-01'
    endDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
    specialDate = '2015-01-01'
#     stockCode = '600030'
#     print getStockInfo(startDate, endDate, stockCode,'2015-01-01')   
   
    df = ts.get_hs300s()
    stockCodeList = list(df.code)
    chooseBZStock(startDate, endDate,specialDate,stockCodeList,fileName)
