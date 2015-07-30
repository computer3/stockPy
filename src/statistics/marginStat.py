#coding=utf-8
'''
Created on 2015年7月3日

@author: Administrator
'''
import tushare as ts
import pandas as pd

startDate = '2015-06-01'
endDate = '2015-07-30'
df_sh = ts.sh_margins(start=startDate, end=endDate)

df_sz = ts.sz_margins(start=startDate, end=endDate)
df_all=pd.merge(df_sh,df_sz,on="opDate")
df_all['rzye'] = df_all['rzye_x']+df_all['rzye_y']
df_all['rzmre'] = df_all['rzmre_x']+df_all['rzmre_y']
df_all = df_all.loc[:,['opDate','rzye','rzmre']]
fileName = r'D:\stock\stockMargin' +startDate+'_' + endDate + '.csv'
df_all.to_csv(fileName,index = False)
print '\nfinished'