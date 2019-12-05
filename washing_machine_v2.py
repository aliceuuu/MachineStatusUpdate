

import pymysql.cursors
import time
from datetime import datetime
from datetime import timedelta

#use UploadStatus to update machine status
def UploadStatus(address, status):
    sql = "INSERT INTO Washer.MachineStatus (version, address, status) VALUES ( 1.0," +str(address)+ "," +str(status)+")"
    cursor.execute(sql)
    connection.commit()
    
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

def IsRunning1():   
    #get data from DB
    #modify sql to select different data
    sql = "SELECT * FROM Washer.current_data WHERE address=1 ORDER BY id DESC  LIMIT 1;"
    cursor = connection.cursor() 
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.commit()
    
    global on1
    global last_peek1
    global start_time1
    output=0
    
    #STEP2: split data
    flag=1
    while flag:
        
        index=result[1]
        current=result[2]
        t=result[3]
        print(result)
        
     #STEP3: judge function 
        if on1==0 and current<6 and index==1:
            output=0
            break
########################################           
        if index==1 and current > 6 and on1==0 :  
            #記錄開始時間
            start_time1=t
            print("start_time1:", start_time1)
            output=1
            #在time interval 內直接輸出為1
            on1=1
########################################         
        #記錄開始時間
        end_time=t
        dis_time = (end_time-start_time1)
        #print(dis_time)
        hours, minutes, seconds = convert_timedelta(dis_time)
        #print("min:", minutes)
        if on1==1 and int(minutes)<36 and index==1:
            output=1
            break
        if on1==1 and int(minutes)>36 and index==1:
            if current>6:
                last_peek1=1
                output=1
            else:
                if last_peek1==0:
                    output=1
                else:
                    last_peek1=0
                    output=0
                    on1=0
########################################           

        flag=0
    return index, output

def IsRunning4():  
    #get data from DB
    #modify sql to select different data
    sql = "SELECT * FROM Washer.current_data WHERE address=4 ORDER BY id DESC  LIMIT 1;"
    cursor = connection.cursor() 
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.commit()
    
    global on4
    global last_peek4
    global start_time4
    output=0
    
    #STEP2: split data
    flag=1
    while flag:
        
        index=result[1]
        current=result[2]
        t=result[3]
        print(result)
########################################
        if on4==0 and current<6 and index==4:
            output=0
            break
########################################
        if index==4 and current > 6 and on4==0 :
            #記錄開始時間
            start_time4=t
            output=1
            print("start_time4:", start_time4)
            #在time interval 內直接輸出為1
            on4=1
######################################## 
        end_time=t
        dis_time = end_time-start_time4
        #print(dis_time)
        hours, minutes, seconds = convert_timedelta(dis_time)
        #print("min:", minutes)
        if on4==1 and int(minutes)<31 and index==4:
            output=1
            break
        if on4==1 and int(minutes)>31 and index==4:
            if current>6:
                last_peek4=1
                output=1
            else:
                if last_peek4==0:
                    output=1
                else:
                    last_peek4=0
                    output=0
                    on4=0

        
########################################           

        flag=0
    return index, output       

 

def IsRunning2():
    
    #get data from DB
    #modify sql to select different data
    sql = "SELECT * FROM Washer.current_data WHERE address=2 ORDER BY id DESC  LIMIT 1;"
    cursor = connection.cursor() 
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.commit()

    #STEP2: split data
    index=result[1]
    current=result[2]
    t=result[3]
    print(result)
        
    #STEP3: judge function            
    output=0
    if current > 6:
        output=1
    else:
        output=0
    return index, output

def IsRunning3():
    
    #get data from DB
    #modify sql to select different data
    sql = "SELECT * FROM Washer.current_data WHERE address=3 ORDER BY id DESC  LIMIT 1;"
    cursor = connection.cursor() 
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.commit()

    #STEP2: split data
    index=result[1]
    current=result[2]
    t=result[3]
    print(result)
        
    #STEP3: judge function            
    output=0
    if current > 6:
        output=1
    else:
        output=0
    return index, output

#connect to mysql on server
#upload to DB "Washer"
HOST = '140.114.216.118'
USER ='edorm'
PASSWORD  = 'edorm'
DB = 'Washer'
connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)

on1=0
on4=0
last_peek1=1
last_peek4=0
start_time1=datetime(2019, 12, 4, 22, 35, 2)
start_time4=datetime(2019, 12, 4, 22, 35, 2)




while True:
    #get data from DB
    #modify sql to select different data
    sql = "SELECT * FROM Washer.current_data ORDER BY id DESC LIMIT 1;"
    cursor = connection.cursor() 
    cursor.execute(sql)
    result = cursor.fetchone()
    
    connection.commit()
    #ID, status = IsRunning()
    ID, status=IsRunning1()
    print("ID:", ID, ", S:", status)
    #upload status
    UploadStatus(ID, status)
    time.sleep(1)
    
    ID, status=IsRunning2()
    print("ID:", ID, ", S:", status)
    #upload status
    UploadStatus(ID, status)
    time.sleep(1)

    ID, status=IsRunning3()
    print("ID:", ID, ", S:", status)
    #upload status
    UploadStatus(ID, status)
    time.sleep(1)
    
    ID, status=IsRunning4()
    print("ID:", ID, ", S:", status)
    #upload status
    UploadStatus(ID, status)
    time.sleep(30)
    

