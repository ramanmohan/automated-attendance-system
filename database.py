#@author: Raman 
import pymysql.cursors
import json

class database:
    def __init__(self):
        self.con = pymysql.connect(host = 'localhost', user='root', 
                      password = 'ramanmohan', 
                      port = 3306, 
                      db = 'Attendace', 
                      cursorclass = pymysql.cursors.DictCursor)

    def createDataBase(self):
        try:
            with self.con.cursor() as cur:
                sqlQuery = 'CREATE DATABASE Attendance'        
                cur.execute(sqlQuery)
                self.con.commit()      
        finally:    
            self.con.close()
    
    def createTable(self):
        try:
            with self.con.cursor() as cur:
                sqlQuery = "CREATE TABLE employees(Serial_Number INT, Name VARCHAR(50) , Time_Stamp VARCHAR(100) , Attendance VARCHAR(10))"                
                cur.execute(sqlQuery)
                self.con.commit()      
        finally:    
            self.con.close()
            
    def loadFromDatabase(self):
         f = open('./database.txt','r')
         data_set = json.loads(f.read())
         count = 1
         for i in data_set.keys():
             try:
                 with self.con.cursor() as cur:
                     sqlQuery  = "INSERT INTO employees (`Serial_Number`,`Name`,`Time_Stamp`,`Attendance`) VALUES(%s,%s, %s,%s)"               
                     cur.execute(sqlQuery,(count,i,'NULL','NULL'))
                     self.con.commit()    
                     count = count + 1
             finally:    
                 pass
         self.con.close()
             

    def updateTable(self,timestamp,name):
        try:
            with self.con.cursor() as cur:
                sqlQuery = "UPDATE employees SET Time_Stamp = %s , Attendance = %s where Name = %s"               
                cur.execute(sqlQuery,(timestamp,'Present',name))
                self.con.commit()      
        finally:    
            pass
    
    def dropTable(self):
        try:
            with self.con.cursor() as cur:
                sqlQuery = "DROP TABLE employees"
                cur.execute(sqlQuery)
                self.con.commit()      
        finally:    
            self.con.close()
            
    def close_connection(self):
        self.con.close()

    def updateFullTable(self):
        try:
            with self.con.cursor() as cur:
                sqlQuery  = "UPDATE employees SET Time_Stamp = %s , Attendance = %s"               
                cur.execute(sqlQuery,('NULL','NULL'))
                self.con.commit()    
        finally:    
            self.con.close()
        
        
