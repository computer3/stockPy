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
    sql ="select code from stock_holder_info t where date(t.report_date) = '"+reportDate+"';"
    df_exist =  psql.read_sql_query(sql, mysql_conn)
    df_result = df_ap[~df_ap.index.isin(df_exist.code)]
    mysql_conn.close() 
    return list(df_result.index)


if __name__ == '__main__':
    df =  getStockCodeListForStockHolder(str(time.strftime("%Y-%m-%d",time.localtime(time.time()))))
    
    sql = "INSERT into  stock_holder_info (code,holder_name,stock_holder_type,position_num,position_rate,change_num,change_rate,report_date) VALUES('002379','于荣强','流通A股','329,240,000','35.54%','不变','--','2015-06-09');"
    insertIntoDb(sql)
    
    