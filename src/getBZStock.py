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

def getStockInfo(startDate, endDate,  stockCode):
    stock = {}
    df_tran = ts.get_hist_data(stockCode, start=startDate, end=endDate)
    df_tran_2015 = df_tran['2015-01-01':]
    stock['maxPx2015'] = max(df_tran_2015.close)
    stock['minPx2015'] = min(df_tran_2015.close)
    stock['maxPxAll']  = max(df_tran.close)
    stock['minPxAll'] = min(df_tran.close)
    stock['maxVol20']  = max(df_tran[-20:].volume)*1000
    stock['maxGrowthRate'] = (stock['maxPxAll'] - stock['minPxAll'])/stock['minPxAll']
    df_pre_tran = df_tran[-1:]    
    stock['prePx'] = float(df_pre_tran.close)
    stock['prePXMa5'] = float(df_pre_tran.ma5)
    stock['preVolMa5'] = float(df_pre_tran.v_ma5)*1000
    stock['preAmtMa5'] = stock['prePXMa5'] * stock['preVolMa5']
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
            stock = getStockInfo(startDate, endDate, stockCode)
    
            if  stock['prePx']<= stock['maxPx2015']*0.9 and stock['prePx'] >=stock['maxPx2015'] * 0.8:                     
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
    for i in range(len(df_all_stock)):    
            try:
                stockCode = df_all_stock.index[i]
                if stockCode[0] == '0' or  stockCode[0] == '3':
                    if not float(ts.get_realtime_quotes(stockCode).price) == 0:
                        t = ts.get_hist_data(stockCode,start='2014-01-01',end='2014-01-02')
                        if float(t.close) > 0:
                            stock = getStockInfo(startDate, endDate, stockCode)                
                            result[stockCode] = stock       
                            print  stockCode,'is finished'                     
            except BaseException, e:
                print 'Error',stockCode,str(e)
                continue                  
    df = DataFrame(result).T   
    df = df.sort(columns = 'maxGrowthRate')
    return df[:30]

    
    
if __name__ == '__main__':
    startDate = '2014-01-01'
    endDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
    df = getLowestGrowth(startDate, endDate)
    print df['maxGrowthRate']