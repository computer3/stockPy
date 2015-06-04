#coding=utf-8
import tushare as ts
import pyodbc 
import pandas.io.sql as psql
df = ts.get_tick_data('600848', date='2014-12-22')
print df

host = "localhost"
port = "3306"
database = "stock"
user = "root"
pwd = ""
conn_info = ('Driver={MySQL ODBC 5.3 ANSI Driver};Server=%s;Port=%s;Database=%s;User=%s; Password=%s;Option=3;'%(host, port, database, user, pwd)) 
mysql_conn  = pyodbc.connect(conn_info,charset='utf8')

df.to_sql(df, mysql_conn)