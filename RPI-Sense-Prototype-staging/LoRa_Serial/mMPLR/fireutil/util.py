from datetime import datetime

def getDate():
    dateTimeObj = datetime.now()
    if(dateTimeObj.day < 10):
        day = '0'+ str(dateTimeObj.day)
    else:
        day = str(dateTimeObj.day)
    if(dateTimeObj.month < 10):
        month = '0'+ str(dateTimeObj.month)
    else:
        month = str(dateTimeObj.month)    
    date = str(dateTimeObj.year)+ "-" + str(month) + "-" + str(day) 
    #print(date)
    return date

def getTime():
    dateTimeObj = datetime.now()
    if(dateTimeObj.second < 10):
        second = '0'+ str(dateTimeObj.second)
    else:
        second = str(dateTimeObj.second)
    if(dateTimeObj.minute < 10):
        minute = '0'+ str(dateTimeObj.minute)
    else:
        minute = str(dateTimeObj.minute)
    if(dateTimeObj.hour < 10):
        hour = '0'+ str(dateTimeObj.hour)
    else:
        hour = str(dateTimeObj.hour)    
    time = str(hour) +':'+ str(minute) +':' + str(second) 
    #print(time)
    return time
