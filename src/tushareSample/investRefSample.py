#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
import tushare as ts

# 分配预案
#每到季报、年报公布的时段，就经常会有上市公司利润分配预案发布，而一些高送转高分红的股票往往会成为市场炒作的热点。
df = ts.profit_data(top=60)
df.sort('shares',ascending=False)
df[df.shares>=10]#选择每10股送转在10以上的

# 业绩预告
ts.forecast_data(2014,2)#获取2014年中报的业绩预告数据

# 限售股解禁
# 以月的形式返回限售股解禁情况，通过了解解禁股本的大小，判断股票上行的压力。可通过设定年份和月份参数获取不同时段的数据。
ts.xsg_data()

# 新股数据
ts.new_stocks()

# 融资融券
ts.sh_margins(start='2015-01-01', end='2015-04-19')
ts.sz_margins(start='2015-01-01', end='2015-04-19')
#如果不设symbol参数或者开始和结束日期时段设置过长，数据获取可能会比较慢，建议分段分步获取，比如一年为一个周期
ts.sh_margin_details(start='2015-01-01', end='2015-04-19', symbol='601989')
ts.sz_margin_details('2015-04-20')
