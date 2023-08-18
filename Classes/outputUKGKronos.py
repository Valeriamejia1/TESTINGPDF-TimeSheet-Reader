import json
import re
from datetime import datetime

class UKGKronos:

    global regexlist

    def readJsonRegex():
        try:
            with open("Regex.json", "r") as read_file:
                data = json.load(read_file)
                return data
        except:
            print("Something happenned reading Json file")

    regexlist= readJsonRegex()

    def date_time():
        current = datetime.now()
        currentTimeAux = str(current.strftime("%Y-%m-%d %H:%M:%S"))
        currentTime= currentTimeAux.replace(":", "")
        return currentTime
    
    def getNurse(value, reportType,name):                                #Method to get the nurse name
        nameAux= re.search(regexlist[reportType]["getName"], str(value)) #Search a match on the value by using a regex to get the name
        nameAux= nameAux.group(0)
        nameAux2 = re.sub(r'\sID', "", nameAux)
        name = name + nameAux2                                           #contatenate the name
        return name
    
    def getPrimaryJob(value, reportType):                                               #Method to get the Primary Job
        PrimaryJobAux= re.search(regexlist[reportType]["GetPrimary"], str(value))       #Search a match on the value by using a regex to get the Primary Job
        PrimaryJobAux= PrimaryJobAux.group(0)
        return PrimaryJobAux
    
    def getDate(value, reportType):
        lineAux= re.search(regexlist[reportType]["getDate"], str(value)) #Search a match on the value by using a regex to get the date
        dateAux = lineAux.group(0)  #Get only the needed value from the match
        dateAux = datetime.strptime(dateAux, "%m/%d/%y").strftime('%m/%d/%Y') #Change the date format in year
        return dateAux
    
    def getPaycode(value, reportType,paycode):
        paycodeAux = re.search(regexlist[reportType]["searchPaycode"], str(value)) #Search a match on the value by using a regex to get the paycode
        paycodeAux = paycodeAux.group(0)  #Get only the needed value from the match
        paycode = paycode + " " +paycodeAux
        return paycode

    def getInHour(value, reportType, date):
        lineAux = re.search(regexlist[reportType]["getInhour"], str(value)) #Search a match on the value by using a regex to get the time in
        inHourAux = lineAux.group(0)  #Get only the needed value from the match
        inHour = datetime.strptime(inHourAux, "%I:%M%p").strftime("%H:%M") #change hour format to 24H
        inHour = date + " " + inHour #concatenate 
        return inHour
    
    def getOutHour(value, reportType, date):
        OutHour=""
        lineAux = re.findall(regexlist[reportType]["getInhour"], str(value)) #Search a match on the value by using a regex to get the time in
        if len(lineAux) >= 2: #Validate the length of the list
            OutHourAux = lineAux[1]  #Get only the needed value from the match
            if re.findall(regexlist[reportType]["getInhour"], str(OutHourAux)): # Using find all to get the out hour as list
                OutHour = datetime.strptime(OutHourAux, "%I:%M%p").strftime("%H:%M") #change hour format to 24H
                OutHour = date + " " + OutHour #concatenate 
            else:
                OutHour=""
        else:
            OutHour=""                  
        return OutHour

    def getHours(value, reportType):
        hoursAux = re.search(regexlist[reportType]["getHours"], str(value)) #Search a match on the value by using a regex to get the hours
        hours = hoursAux.group(0) #Get only the needed value from the match
        return hours
    
    def getComments(value,reportType, comment):
        commentAux =  re.search(regexlist[reportType]["getcomment"], str(value)) #Search a match on the value by using a regex to get comments
        commentAux= commentAux.group(0)
        comment= comment + " " + commentAux  #concatenate
        return comment
