#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
import tushare as ts
# sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板

# 1.历史行情
# 只能获取近三年的历史数据，未进行复权，速度很快
ts.get_hist_data('600848') 
ts.get_hist_data('600848',start='2015-01-05',end='2015-01-09')
ts.get_hist_data('600848',ktype='W') #获取周k线数据
ts.get_hist_data('600848',ktype='M') #获取月k线数据
ts.get_hist_data('600848',ktype='5') #获取5分钟k线数据
ts.get_hist_data('600848',ktype='15') #获取15分钟k线数据
ts.get_hist_data('600848',ktype='30') #获取30分钟k线数据
ts.get_hist_data('600848',ktype='60') #获取60分钟k线数据
ts.get_hist_data('sh')#获取上证指数k线数据，其它参数与个股一致，下同
ts.get_hist_data('sz')#获取深圳成指k线数据
ts.get_hist_data('hs300')#获取沪深300指数k线数据
ts.get_hist_data('sz50')#获取上证50指数k线数据
ts.get_hist_data('zxb')#获取中小板指数k线数据
ts.get_hist_data('cyb')#获取创业板指数k线数据

# 2.历史复权数据
# 可提供股票上市以来所有历史数据，默认为前复权
ts.get_h_data('002337') #前复权
ts.get_h_data('002337',autype='hfq') #后复权
ts.get_h_data('002337',autype=None) #不复权
ts.get_h_data('002337',start='2015-01-01',end='2015-03-16') #两个日期之间的前复权数据
ts.get_h_data('399106', index=True) #深圳综合指数

# 3.一次性获取当前交易所有股票的行情数据，如果是节假日，即为上一交易日
ts.get_today_all()

# 4.实时交易数据
ts.get_realtime_quotes('sh')
ts.get_realtime_quotes('000581')

# 5.当日分笔
df = ts.get_today_ticks('601333')

# 6.历史分笔
df = ts.get_tick_data('600848',date='2014-01-09')

# 7.获取所有指数实时行情列表
df = ts.get_index()