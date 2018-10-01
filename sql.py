#@author: Raman
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import pymysql.cursors
import time
import json

import datetime
 
con = pymysql.connect(host = 'localhost', user='root', 
                      password = 'ramanmohan', 
                      port = 3306,
                      db = 'Attendace' ,
                      cursorclass = pymysql.cursors.DictCursor)

f = open('./database.txt','r')
data_set = json.loads(f.read())
count = 1
for i in data_set.keys():
    try:
        with con.cursor() as cur:
            sqlQuery  = "INSERT INTO employees (`Serial_Number`,`Name`,`Time_Stamp`,`Attendance`) VALUES(%s,%s, %s,%s)"               
            cur.execute(sqlQuery,(count,i,'NULL','NULL'))
            con.commit()    
            count = count + 1
    finally:
        pass    
        #con.close()

'''

try:
    with con.cursor() as cur:
        ts=time.time()
        mydate = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
        #sqlQuery = 'CREATE DATABASE Attendace'
        sqlQuery = "CREATE TABLE employees(Serial_Number INT, Name VARCHAR(50) , Time_Stamp VARCHAR(100) , Attendance VARCHAR(10))"
        #sqlQuery = "CREATE TABLE IF NOT EXISTS employees(Serial_Number INT, Name VARCHAR(10) , Time_Stamp VARCHAR(10))"
        #sqlQuery = "DROP TABLE employees"
        #sqlQuery = "SELECT * from employees"
        #sqlQuery = "INSERT INTO employees (`Serial_Number`,`Name`,`Time_Stamp`) VALUES(%s,%s, %s)"
        #sqlQuery = "sqlQuery, (INT 0, str("
        #sqlQuery = "UPDATE employees SET Time_Stamp = %s where Name = 'Rajesh'"
        cur.execute(sqlQuery)
        #cur.execute(sqlQuery,(mydate))
        #sqlQuery = ('SELECT * from employees')
        #cur.execute(sqlQuery)
        #result = cur.fetchall()
        #print(result)
        con.commit()      
finally:    
        con.close()
'''





