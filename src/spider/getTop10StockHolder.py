#coding=utf-8
'''
Created on 2015年6月9日
爬取第一大股东数据
@author: Administrator
'''
import urllib2
import urllib
import re
import time
from bs4 import BeautifulSoup
import tushare as ts
from tools import dbOper

def getWebContent(headers, url):
    url=  url.encode('utf-8')
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response)
    content = str(soup)
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.replace('\r', '')
    return content

def getStockHolderInfok(stockCodeList):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'          
    cooke = 'pgv_pvi=8244609964; emstat_bc_emcount=164993042066668138; emstat_ss_emcount=15_1433872119_1146441478; pgv_info=ssi=s9950471570'    
    headers = { 'User-Agent' : user_agent,
                    'Cookie' : cooke,
                    'Connection':'keep-alive',
                    'Host':'hqdigi2.eastmoney.com',
                    'Referer':''}

    for stockCode in stockCodeList:
        try: 
            stockCode = stockCode.encode('utf-8')
            if stockCode[0] == '6':
                stockCodeStr = 'sh'+stockCode
            else:
                stockCodeStr = 'sz'+stockCode
            print str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),stockCode,' is started'   
            pageUrl = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code='+stockCodeStr
            headers['Referer'] = pageUrl
            content = getWebContent(headers, pageUrl)
            print content
            items = re.findall(re.compile('id="TTS_Table_Div".*?<table><tr>(.*?)</tr></table>',re.S)  ,content)
            if len(items) == 1:
                trStrs = re.findall(re.compile('<tr>(.*?)</tr>',re.S)  ,items[0])
                for tr in trStrs:
                    holder_postion = re.findall(re.compile('<th class="tips-dataL">(.*?)</th>',re.S),tr)[0]
                    
                    tdStrs = re.findall(re.compile('<td class="tips-dataL">(.*?)</td>',re.S)  ,tr)
                    if len(tdStrs) == 6:                        
                        holder_name = tdStrs[0].strip().replace("'","''").decode('utf-8')
                        stock_holder_type =tdStrs[1].strip().replace("'","''").decode('utf-8')
                        position_num = tdStrs[2].strip().replace("'","''").decode('utf-8')
                        position_rate = tdStrs[3].strip().replace("'","''").decode('utf-8')
                        change_num = tdStrs[4].strip().replace("'","''").decode('utf-8')
                        change_rate = tdStrs[5].strip().replace("'","''").decode('utf-8')
                        reportDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
                        sql = '''INSERT into  stock_holder_info (code,holder_postion,holder_name,stock_holder_type,position_num,position_rate,change_num,change_rate,report_date) 
                        VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s'
                        );''' % (stockCode,
                                 holder_postion,
                                 holder_name,
                                 stock_holder_type,
                                 position_num,
                                 position_rate,
                                 change_num,
                                 change_rate,
                                 reportDate
                                )
                        sql=  sql.encode('utf-8')
                        dbOper.insertIntoDb(sql);
                        print str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),stockCode,' is finished'   
        except BaseException, e:
            print str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))) , " Error: " ,stockCode, " : ", str(e)  
            continue
                     

if __name__ == '__main__':
    reportDate = str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
    stockCodeList = dbOper.getStockCodeListForStockHolder(reportDate)
    stockCodeList = ['600030']
    print len(stockCodeList),' need to load'
    getStockHolderInfok(stockCodeList)