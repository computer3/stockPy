#coding=utf-8
import tushare as ts
df = ts.get_realtime_quotes('000721')
print df