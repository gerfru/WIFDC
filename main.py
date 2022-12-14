#Import Faker into a Python Program
from faker import Faker
import pandas as pd
import pymssql
import random
from datetime import datetime
from datetime import date
import re


def connectDB(strServer, strDatabase):
    # ---------------------------------------------------------------------------------
    # Connect to a database, when the name and server is provided
    
    # @Args:
    #       - strServername:    DNS Name of the server, where the Database is located.
    #       - strDatabase:      Name of the Database
    # @Returns:
    #       - conn:             connection object
    #       - cur:              database cursor object
    # ---------------------------------------------------------------------------------
    conn = pymssql.connect (server = strServer, database = strDatabase)
    cur = conn.cursor()
    #cur.execute('select * from hce.series.series_test')
    return conn, cur


def getDataFormat(conn, strTable):
    # ---------------------------------------------------------------------------------
    # load format of a database table into a dataframe
    
    # @Args:
    #       - conn:             connection object.
    #       - cur:              database cursor object
    # @Returns:
    #       - df:               dataframe containing table format
    # ---------------------------------------------------------------------------------
    strQuery = """SELECT frs.name, frs.system_type_name FROM sys.dm_exec_describe_first_result_set('select top 10 * from {}',NULL,NULL) frs""".format(strTable)
    df = pd.read_sql(strQuery, conn)
    return df


def createDataFrame (dfFormat):
    df = pd.DataFrame(columns= dfFormat['name'])
    print(dfFormat.name)
    #print(dfFormat['system_type_name'].iloc[0])

    fake = Faker()
    Faker.seed(0)

    print('Dataframe Size: '+ str(len(dfFormat.system_type_name)))
    for length in range(0, len(dfFormat.system_type_name)):
        print ('Length: ' + str(length) + ' ' + 'Column: ' + str(dfFormat.system_type_name.iloc[length]))
        if str(dfFormat.system_type_name.iloc[length]).find('varchar') != -1:
            result = re.search('varchar(.*)', str(dfFormat.system_type_name.iloc[length]))
            strLength = result.group(1)
            strLength = strLength.replace('(', '')
            strLength = strLength.replace(')','')
            strFakeText = '?' * int(strLength)
            for _ in range (10):
                #print(fake.bothify(text = strFakeText))
                pass





def fake_run():
     #Intiaize Faker
    fake = Faker()
    df = pd.DataFrame()
    for val in range(3):
        df.loc[val, 'series_name'] = 'Test_Gerald'
        df.loc[val, 'object_name'] = 'Test_Object'
        df.loc[val, 'value'] = random.randrange(200, 400)
        df.loc[val, 'date'] = fake.date_between_dates(date_start=datetime(2020,1,1), date_end=datetime(2023,1,1))
        df.loc[val, 'object_type'] = 'CUBE'
        df.loc[val, 'load_type'] = 'QUEUE'
        df.loc[val, 'data_source'] = 'CUBE'
        df.loc[val, 'info'] = date.today()

    return df

def pushToDB (conn, cur, df):
    
    for index, row in df.iterrows():
        #cur.execute(strQuery.format(strSeriesName=row.series_name,  strObjectName=row.object_name, strValue = row.value, strDate = row.date, strObjectType = row.object_type,  strLoadType = row.load_type, strDataSource = row.data_source, strInfo = str(row.info)) )
        # https://stackoverflow.com/questions/1136437/inserting-a-python-datetime-datetime-object-into-mysql
        #print (''' INSERT INTO hce.series.series_test ([series_name], [object_name] , [value], [date], [object_type], [load_type], [data_source], [info]) VALUES( %s, %s, %s, '%s', %s, %s, %s, '%s'  )''' , (row.series_name, row.object_name, row.value, row.date, row.object_type, row.load_type, row.data_source, row.info))
        #cur.execute(''' INSERT INTO hce.series.series_test ([series_name], [object_name] , [value], [date], [object_type], [load_type], [data_source], [info]) VALUES( %s, %s, %s, '%s', %s, %s, %s, '%s'  )''' , (row.series_name, row.object_name, row.value, row.date, row.object_type, row.load_type, row.data_source, row.info))
        strQuery = ''' INSERT INTO hce.series.series_test ([series_name], [object_name] , [value], [date], [object_type], [load_type], [data_source], [info]) VALUES( ' {strSeriesName} ', '{strObjectName}', '{strValue}', {strDate}, '{strObjectType}', '{strLoadType}', '{strDataSource}', {strInfo} )'''
        #print(strQuery.format(strSeriesName=row.series_name, strObjectName=row.object_name, strValue=row.value, strDate=row.date, strObjectType=row.object_type, strLoadType=row.load_type, strDataSource=row.data_source, strInfo=row.info))
        strDateInsert = (row.date)
        strInfoInsert = (row.info)
        # https://bobbyhadz.com/blog/python-attributeerror-str-object-has-no-attribute-strftime
        cur.execute(strQuery.format(strSeriesName=row.series_name, strObjectName=row.object_name, strValue=row.value, strDate=strDateInsert.strftime("%d/%m/%Y %H:%M:%S"), strObjectType=row.object_type, strLoadType=row.load_type, strDataSource=row.data_source, strInfo=strInfoInsert.strftime("%d/%m/%Y %H:%M:%S")))
    conn.commit()
    cur.close()



def main():
    # ------ Get Connected ----- # 
    conn, cur = connectDB('localhost', 'HCE')
    # ----- Get the datatypes from a table ----- # 
    dfFormat = getDataFormat(conn, 'hce.dbo.ALL_BEW_AMPEL')
    createDataFrame(dfFormat)
    

if __name__ == '__main__':
    main()