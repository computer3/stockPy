#coding=utf-8
'''
Created on 2015年6月3日
tushare接口数据存储
@author: Administrator



'''
from sqlalchemy import create_engine
import tushare as ts
from urllib2 import URLError
import time



#获取沪深上市公司基本情况
# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本
# totals,总股本(万)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# eps,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期
def loadStockBasicInfo():
    engine = create_engine('mysql://root:@127.0.0.1/stock?charset=utf8') 
    df = ts.get_stock_basics()
    df['code'] = df.index
    df.to_sql('stock_basics', engine,if_exists='replace', index=False)
    print 'Stock info is loaded successfully'


#获取沪深上市公司复权的历史数据
def loadHisTranDataFQ(startDate,endDate,codeList):    
    engine = create_engine('mysql://root:@127.0.0.1/stock?charset=utf8')
    while len(codeList) > 0:
        try:
            code = codeList[-1]
            print code, 'is started'
            df = ts.get_h_data(code, start=startDate, end=endDate)
            df['tran_date'] = df.index
            df['code'] = code
            df.to_sql('his_qfq_trans', engine,if_exists='append',index=False)
            print  code,'is finished'
            codeList.pop()
        except URLError as e:
            print 'Error', code, str(e)
            continue
        except BaseException as e:
            print 'Error', code, str(e)
            codeList.pop()
            continue
        
#获取沪深上市公司未复权的历史数据
def loadHisTranData(startDate,endDate,codeList):    
    engine = create_engine('mysql://root:@127.0.0.1/stock?charset=utf8')
    while len(codeList) > 0:
        try:
            code = codeList[-1]
            print code, 'is started'
            df = ts.get_hist_data(code, start=startDate, end=endDate)
            df['tran_date'] = df.index
            df['code'] = code
            df.to_sql('his_trans', engine,if_exists='append',index=False)
            print  code,'is finished'
            codeList.pop()
        except URLError as e:
            print 'Error', code, str(e)
            continue
        except BaseException as e:
            print 'Error', code, str(e)
            codeList.pop()
            continue
if __name__ == '__main__':
#     loadStockBasicInfo()
    startDate = '2013-01-01'
    endDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
    df = ts.get_stock_basics()
    codeList = list(df.index)
    loadHisTranData(startDate,endDate,codeList)

