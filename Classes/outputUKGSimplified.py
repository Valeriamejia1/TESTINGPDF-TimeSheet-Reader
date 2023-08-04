import json
import re
import PyPDF2
import pandas as pd
from datetime import datetime

class UKGSimplified:

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

    def writeDF(name,gl,date):
        global df
        infoAux = {'NAME': name, 'GLCODE': gl, 'DATE':date }
        df= df.append(infoAux, ignore_index= True)

    def convertDate(value):
        time = datetime.strptime(value, "%b %d, %Y").strftime('%m/%d/%Y')
        return time

    def getNurse(value, reportType):              
        nameAux= re.search(regexlist[reportType]["getName"], str(value))
        nameAux= nameAux.group(0)
        name = re.sub(r'\s\(', "", nameAux)
        return name

    def getGL(value, reportType):              
        glAux = re.search(regexlist[reportType]["getGL"], str(value))
        gl = re.sub(r'\(|\)', "", glAux.group(0))
        return gl
    
    def getDate(value, reportType):              
        dateAux = re.search(regexlist[reportType]["searchDate"], str(value))
        date = UKGSimplified.convertDate(dateAux.group(0))
        return date
    
    def getHours(line, reportType):
        hoursAux = re.search(regexlist[reportType]["getHours"], str(line)) #Search a match on the value by using a regex to get the hours
        hours = hoursAux.group(0) #Get only the needed value from the match
        hours = re.sub(r'[a-zA-Z\s]', "", hours)
        return hours

    def getInHour(line, reportType, date):
        lineAux = re.search(regexlist[reportType]["getInhour"], str(line)) #Search a match on the value by using a regex to get the time in
        inHourAux = lineAux.group(0)  #Get only the needed value from the match
        InHour = datetime.strptime(inHourAux, "%I:%M %p").strftime("%H:%M") #change hour format to 24H
        InHour = date + " " + InHour #concatenate 
        return InHour
    
    def getPaycodes(line, reportType, paycode):
        paycodeAux = re.search(regexlist[reportType]["searchPaycode"], str(line))
        paycodeAux2 = paycodeAux.group(0)
        if re.search(r'\d{4}(?!\-)', paycodeAux2):
            paycodeFinal = paycode + " " + re.sub(r'\d{4}(?!\-)', "", paycodeAux2)
        else:
            if re.search(r'\d{3}', paycodeAux2):
                paycodeFinal = paycode + " " + re.sub(r'\d{3}', "", paycodeAux2)
            else:
                paycodeFinal = paycode + " " + paycodeAux2
                
        return paycodeFinal

    def toExcel(df, reportType):
        currentTime = UKGSimplified.date_time()
        path = regexlist[reportType]["output_file"] + reportType + " output " + currentTime + ".xlsx"
        writer = pd.ExcelWriter(path)
        df.to_excel(writer, sheet_name='Sheet1',index = None, header=True)  # Save df in a sheet named 'RawData' 
        writer.save()  # Save the changes to the Excel file

        
        df1= df.copy(deep=True)
        df.drop(df.index,inplace=True)
        df.drop(df.index,inplace=True)
        return not (df1.empty)
    
    

    

        