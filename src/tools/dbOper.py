#coding=utf-8
import pyodbc 
import pandas.io.sql as psql
import tushare as ts
import time
host = "localhost"
port = "3306"
database = "stock"
user = "root"
pwd = ""
conn_info = ('Driver={MySQL ODBC 5.3 ANSI Driver};Server=%s;Port=%s;Database=%s;User=%s; Password=%s;Option=3;'%(host, port, database, user, pwd)) 


def insertIntoDb(sql):
    mysql_conn  = pyodbc.connect(conn_info,charset='utf8')               
    mssql_cur = mysql_conn.cursor();              
    mssql_cur.execute(sql);
    mysql_conn.commit();
    mysql_conn.close()
    
def getStockCodeListForStockHolder(reportDate):
    df_ap = ts.get_stock_basics()    
    mysql_conn  = pyodbc.connect(conn_info,charset='utf8')
    sql ="select distinct code from stock_holder_info t where date(t.report_date) = '"+reportDate+"';"
    df_exist =  psql.read_sql_query(sql, mysql_conn)
    df_result = df_ap[~df_ap.index.isin(df_exist.code)]
    mysql_conn.close() 
    return list(df_result.index)

def getStockCodeListForHistTran():
    df_ap = ts.get_stock_basics()    
    mysql_conn  = pyodbc.connect(conn_info,charset='utf8')
    sql ="select distinct code from his_trans t ;"
    df_exist =  psql.read_sql_query(sql, mysql_conn)
    df_result = df_ap[~df_ap.index.isin(df_exist.code)]
    mysql_conn.close() 
    return list(df_result.index)

def getHistTran(startDate, endDate):
  
    mysql_conn  = pyodbc.connect(conn_info,charset='utf8')
    sql ="select * from his_trans t where t.tran_date >='"+startDate+"' and t.tran_date <= '"+endDate+"'"
    df =  psql.read_sql_query(sql, mysql_conn)
    return df

if __name__ == '__main__':
#     ls = getStockCodeListForHistTran()
#     print len(ls)
#     print ls
    df = getHistTran('2014-01-01','2015-06-01')
    print len(df)