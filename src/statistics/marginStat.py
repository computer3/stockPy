#coding=utf-8
'''
Created on 2015年7月3日

@author: Administrator
'''
import tushare as ts
startDate = '2015-06-01'
endDate = '2015-07-02'
df_sh = ts.sh_margins(start=startDate, end=endDate)
df_sh.to_csv(r'd:\stock\shMargin.csv',index = False)
df_sz = ts.sz_margins(start=startDate, end=endDate)
df_sz.to_csv(r'd:\stock\szMargin.csv',index = False)
print 'finished'