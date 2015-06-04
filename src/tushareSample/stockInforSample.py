#coding=utf-8
import tushare as ts

# 获取沪深上市公司基本情况
df = ts.get_stock_basics()
date = df.ix['600848']['timeToMarket']#上市日期YYYYMMDD

#获取2014年第3季度的业绩报表数据
ts.get_report_data(2014,3)

#获取2014年第3季度的盈利能力数据
ts.get_profit_data(2014,3)


#获取2014年第3季度的营运能力数据
ts.get_operation_data(2014,3)


#获取2014年第3季度的成长能力数据
ts.get_growth_data(2014,3)

#获取2014年第3季度的偿债能力数据
ts.get_debtpaying_data(2014,3)

#获取2014年第3季度的现金流量数据
ts.get_cashflow_data(2014,3)