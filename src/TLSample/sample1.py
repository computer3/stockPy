# -*- coding: utf-8 -*-
from dataapi import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('26a0fa114b621a5b9755507e17b04600f01da7b41b7dc950e19b357fbd721123')
#         url1='/api/macro/getChinaDataGDP.csv?field=&indicID=M010000002&indicName=&beginDate=&endDate='
#         code, result = client.getData(url1)
#         if code==200:
#             print result
#         else:
#             print code
#             print result
        url2='/api/subject/getSocialDataXQByDate.csv?field=&statisticsDate=20150630'
        code, result = client.getData(url2)
        if(code==200):
            print result
        else:
            print code
            print result

    except Exception, e:
        #traceback.print_exc()
        raise e