#coding=utf-8
'''
Created on 2015年6月4日

@author: Administrator
'''
import tushare as ts
# 行业分类
ts.get_industry_classified()

# 概念分类
ts.get_concept_classified()

# 地域分类
ts.get_area_classified()

# 获取沪深300当前成份股及所占权重
ts.get_hs300s()

# 获取中小板股票数据，即查找所有002开头的股票
ts.get_sme_classified()

# 获取创业板股票数据，即查找所有300开头的股票
ts.get_gem_classified()

# 获取风险警示板股票数据，即查找所有st股票
ts.get_st_classified()

# 获取上证50成份股
ts.get_sz50s()

# 获取中证500成份股
ts.get_zz500s()