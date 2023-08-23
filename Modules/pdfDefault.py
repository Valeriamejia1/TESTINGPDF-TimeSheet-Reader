#Needed libraries
import tabula as tb
import numpy as np
import pandas as pd
import re  # regex
import json
from datetime import datetime
from Classes.auditPDFdefault import pdftest
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os

def readJsonRegex():
    # read json file "Regex.json" that holds the regex that are required
    try:
        with open("Regex.json", "r") as read_file:
            data2 = json.load(read_file)           #Import the regex entries to a dictionary
            return data2                           #Return the dictionary
    except:
        print("Something happenned reading Json file")


def getNurse(value, reportType):
    nameAux= re.search(regexlist[reportType]["getEmp"], str(value))   #Search a match on the value by using a regex to get the nurse name
    #name= nameAux.group(0)                               #Get only the needed value from the match
    name= re.sub(r':\s', "", nameAux.group(0))            #Remove the blank space and the : from the name         
    return name                                           #Return the nurse name
    
    
def getGL(value, reportType):
    if re.search(regexlist[reportType]["getGLAux2"], str(value)):          #Search a match on the value by using a regex to get the GL codes: Matches format:   04/95221046530001/030/-/-/-/-
        glAux= re.search(regexlist[reportType]["getGLAux2"], value)        #Get the GL value by using a regex
        glCode= re.sub(r'/', "", glAux.group(0))               #Remove the "/" from the GL code by using a replacement from "/" to ""
    elif re.search(regexlist[reportType]["getGL"], str(value)):            #Search a match on the value by using a regex to get the GL codes: Matches format:   /1410/2600/3990/-/1410.2600.1815/34299
        glAux= re.search(regexlist[reportType]["getGL"], value)            #Get the GL value by using a regex
        glCode= re.sub(r'/', "", glAux.group(0))               #Remove the "/" from the GL code by using a replacement from "/" to ""
    elif re.search(regexlist[reportType]["getGL2"], str(value)):
        glAux= re.search(regexlist[reportType]["getGLAux3"], value)            #Get the GL value by using a regex
        glCode= glAux.group(0)
    else:
        glAux= re.search(regexlist[reportType]["getGLAux"], str(value))    #Search a match on the value by using a regex to get the GL codes: Matches format:   UH01/0197/PCSV/0/007317/0/CEDFAC
        glAux2= glAux.group(0)                                 #Get only the needed value from the match
        glAux3= glAux2.split("/")                              #split the value into a list of strings by the separator "/"
        if len(glAux3[4]) == 6:                                #verify if the GL code len is equal to 6
            glAux4= glAux3[4]                                  #Save into a variable the GL code
            glCode= glAux4[2:]                                 #Remove the two firt 0 of the GL code
        elif len(glAux3[4]) == 5:                              #verify if the GL code len is equal to 5
            glAux4= glAux3[4]                                  #Save into a variable the GL code
            glCode= glAux4[1:]                                 #Remove the first 0 from the GL code

        elif re.search(r'^\d+$', str(glAux3[4])):
            glCode= glAux3[4] 
        else:
            glAux= re.search(r'\/\d{4,6}\/', value)          
            glAux= glAux.group(0)
            glCode= re.sub(r'\/', "", glAux) 

        #else:
            #glCode= glAux3[4]                                  #If the GL code len is less tan 4 just save the code into a variable
    return glCode


def getDateTime(value, reportType):
    value2= re.sub(r'-', " ", value)              #Remove the "-" values that are next to the date
    value3= re.sub('\s\+', ' ', value2)
    value4= " ".join(value3.split())
    dt= value4.split(" ", 3)                       #split the value into a list of strings by the separator " ", this is to separete the date time
    if re.search(r'UPO|UPS', str(dt)):             #Check if there is UPO or UPS entries in the list
        data= False                                #Set a false to don't add this row
        return data                                #Return the false
    else:
        dataDT=[]                                                              #Create a blank list
        date= dt[0]                                                             #save the date to a variable
        if re.search(r'^([AMP])?\d{1,2}([AMP])?\/M\d{1,2}\/\d{4}', date) :
            date=re.sub(r'[AMP]', "",date)  
        dataDT.append(date)                                                    #Append the date to the list
        flagCom= False
        comment1= ""
        if len(dt) > 1:
            if re.search(r'\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2}', dt[1]):
                timeAux= str(dt[1].strip()+" "+dt[2].strip())                      #Check if the "dt" list len is more than 1, this to identify if is just a date or date and time

                if re.search(regexlist[reportType]["extraComment"], timeAux):
                    flagCom= True

                time= convertHours(timeAux, reportType)
                dataDT.append(time)                                                #Append the time to the list
            else:
                time="No time"
                comment1= dt[1]
                if len(dt) > 2:
                    comment1= comment1 + " | " + dt[2] 
                dataDT.append(time)
                 
        if len(dt) > 3:                                                        #Check if the "dt" list len is more than 1, this to identify if there is comments next to the date and time
            if re.search(regexlist[reportType]["getcomment"], dt[3]):                      #Search a match on the value by using a regex to get comments: Matches format:   Any letters from A to Z excluding AM or PM conbinations Example: 5/10/2022 12:00 AM HCL
                comment1= comment1 + " | " + dt[3]                                                 #Save the comments located on the position 3 on the list to a variable
                dataDT.append(comment1)                                        #Append the comments to the list
        elif comment1 != "":
            dataDT.append(comment1)
        return dataDT, flagCom                                                 #Return the list                                              #Return the list

    
def getHours(value,response, reportType):                                                  
    hourAux= re.search(regexlist[reportType]["getHours"], value)                           #Get a match on the value by using a regex to get the hours: Matches format:   10.25
    hourAux= hourAux.group(0)                                                  #Get only the needed value from the match
    hourAux= re.sub(r':', '.', hourAux)
    if response == True:                                                       #This evaluate if if needed the rounding on the minutes, the "response" variable has the user response. True=Rounding, False= No rounding
        hourAux= hourAux.split('.', 2)                                         #Split the total hours to a list, to separate the minutes from the hours
        hourAux2= "{:.2f}".format(int(hourAux[1])/60)                          #Convert the minutoes to seconds, formula: minutes/60
        hourAux2= hourAux2.split('.', 2)                                       #Split the result to a list
        hour= hourAux[0]+"."+str(hourAux2[1])                                  #Get only the seconds value after the point
        return hour                                                            #Return the hour
    else:                      
        hour= hourAux                                                          #Save the hour without the rounding, this appli for response= False
        return hour                                                            #Return the hour
    

def checkComments(value, reportType):
    #Get GL
    size= (len(df.index))-1                                                    #Get the dataframe last row number, to override any extra GL, comment or Pay Code
    if re.search(regexlist[reportType]["getEntrieMP"], str(value)):                        #Search a match on the value by using a regex to get values "MP" on the comments. The time of this values must be changed to "No Time"
        changeTime= df.at[size, 'STARTDTM']                                    #Get the current value on the row and column "STARTDMT"
        x = re.sub(r'\d{1,2}:\d{2}', "No time", changeTime)                    #Replace the time to "No time"
        df.at[size, 'STARTDTM']= x                                             #Write on the dataframe the new value
    if re.search(regexlist[reportType]["extraGL"], str(value)):
        glAuxExtra= re.search(regexlist[reportType]["extraGL"], value)
        if re.search(r'\/\d{4}\/\d{4}\/', glAuxExtra.group(0)):
            glAuxExtra2= re.sub(r'^\/|\/$', "", glAuxExtra.group(0))
            df.at[size, 'GLCODE']= glAuxExtra2
        #elif re.search(regexlist[reportType]["getGL3"], str(value)):
        #    glAuxExtraAux2= re.search(regexlist[reportType]["getGLAux3"], value)            #Get the GL value by using a regex
        #    glAuxExtra2= glAuxExtraAux2.group(0)
        #    df.at[size, 'GLCODE']= glAuxExtra2   
        elif re.search(r'\/\d{4}(\-|\.)\d{4}(\-|\.)\d{4,5}', glAuxExtra.group(0)):     #Get the GL with "-" in output 
            glAuxExtra2= re.sub(r'/', " ", glAuxExtra.group(0))
            glAuxExtra2= glAuxExtra2.strip()
            df.at[size, 'GLCODE']= glAuxExtra2
        else:
            glAuxExtra2= re.sub(r'/|-', " ", glAuxExtra.group(0))                       #Get the GL without "-"
            glAuxExtra2= glAuxExtra2.strip()
            df.at[size, 'GLCODE']= glAuxExtra2
    #Get PayCode 
    elif re.search(regexlist[reportType]["getExtraPayCode"], str(value)):      #Search a match on the value by using a regex to get Pay Codes on the comments. Matches format:    06-Hourly Precept or 06-Hourly Training
        df.at[size, 'PAYCODE']= value                                          #Write on the dataframe the new Pay Rule



def writeDF(nurse,gl,payRule,date,time,timeOut, hour,comment,entireGL):
    global df                                                                 #Global variable, it is the dataframe
    infoAux = {'NAME': nurse, 'GLCODE': gl, 'PAYCODE': payRule, 'DATE': date, 'STARTDTM': date+" "+time, 'ENDDTM' : date+ " " +timeOut, 'HOURS': hour, 'Comments': comment, 'EntireGLCode' : entireGL}  #Create a dict with the got data associated with their columns names
    df= df.append(infoAux, ignore_index= True)                                #Append a new row to the data fram by using the got data

def convertHours(time24, reportType):
    dt= time24.split(" ", 3)
    dtAux= dt[0] + " " + dt[1]
    if re.search(regexlist[reportType]["getTime"], dtAux):
        time24Aux= datetime.strptime(dtAux, "%I:%M:%S %p")              #Convert the time in time format
        time48= datetime.strftime(time24Aux, "%H:%M")                   #Convert the time in 48 hrs format
    elif re.search(regexlist[reportType]["getTime2"], dtAux):
        try:
    # Tratar de convertir a formato 24 horas ("%H:%M") utilizando el formato "%I:%M %p"
            time24Aux = datetime.strptime(dtAux, "%I:%M %p")
            time48 = datetime.strftime(time24Aux, "%H:%M")
        except ValueError:
    # Si ocurre un error (ValueError), es porque el formato no coincide con "%I:%M %p"
    # Realizar la acción alternativa aquí
            time48 = re.search(regexlist[reportType]["getTime2"], dtAux)
            time48=time48.group(0) 
    
    return time48
    
#Read a json file with the regex values and import them to a dictionary    
regexlist= readJsonRegex()

#Create a empty DataFrame with the required columns 
col=["EMPLID","NAME","DATE","AGENCY","GLCODE","PAYCODE","STARTDTM","ENDDTM","HOURLY RT","HOURS","WAGES","MULTIPLIER","ADDER","INVOICE ID","ApproveByAgency","ApproveByFacility","Pool","Comments","EntireGLCode"] #Create a list with the dataframe headers
df= pd.DataFrame(columns=col)  #Create the empty dataframe


def main(response, file, reportType,  from_convert_pdf_Default= False):
    """
    Main code for PDF to Excel. Receives response whether or no convert hours and file to process.
    """
  

    current = datetime.now()
    currentTimeAux = str(current.strftime("%Y-%m-%d %H:%M:%S"))
    currentTime= currentTimeAux.replace(":", "")
    pdf_file_name = os.path.splitext(os.path.basename(file))[0]

    if from_convert_pdf_Default:
        
        if response == True:
            path = "QA/Output Files/OUTPUT Default/" + pdf_file_name + " minutes" + ".xlsx"
        else:
            path = "QA/Output Files/OUTPUT Default/" + pdf_file_name + ".xlsx"
    else:
        path = regexlist[reportType]["output_file"] + "output " + currentTime + ".xlsx"
        audit = pdftest(file, reportType, regexlist)
        audit.audit_report()
    
    #Read the PDF file and create a list of dataframes with the PDF pages
    table= tb.read_pdf(file, pages='all', stream= True, lattice=False, silent=False, guess=False, multiple_tables=True, pandas_options={'header': None}, java_options="-Dfile.encoding=UTF8")
    

    #Flags to control the execution
    flag="Emp"                                  #To search the nurse name
    flagExtra=False                             #To search comments or any extra gl code
    nameVerif= ""                                   #This variable is used to verify if the next page is the same nurse
    flagComment= False
    nurse = ""
    timeOut = "" 
    flagOutOux= ""
    flagGLextra= False
    gl=""
    entireGL=""
    #Loop over the data
    for item in table:                              #Iterate on the list of DataFrames 
        for index, row in item.iterrows():          #Iterate on the DataFrame rows
            row = row.fillna('')                    #Replace the NaN values to blank spaces in the row
            for index, value in row.items():        #Iterate on the row values
                if value != '':                     #Evaluate value is not empty (to skip the black values)
                    #print(value)
                    #print(flag)
                    #Get the nurse name
                    if re.search(regexlist[reportType]["searchEmp"], str(value)) and flag == "Emp":
                        name= getNurse(value, reportType)      #Call the function to get the nurse name and save it to an variable
                        if name != nurse:
                            #if nameVerif != name:      #Verify if the last nurse is the same current
                            nurse= name            #Save the nurse name
                            payRule= "Regular"
                            flag= "GL"             #Change to flag to GL to search the GL code
                            flagEmpAux = True 
                            flagGLextra= True
                            #print(nurse)
                        else:
                            flag="Emp"
                    elif re.search(regexlist[reportType]["searchEmp"], str(value)) and flagEmpAux == True:     #This statement verify if exist any other nurse name
                        nameAux= getNurse(value, reportType)                                                   #Get the nurse name
                        if nameAux != nurse:                                                       #Veify if the nurse name is different of the new one
                            nurse= nameAux                                                         #Save the new name on the variable replacing the old one
                            flag= "GL" 
                            flagGLextra= True                                                            #Change the flag to seach a new GL
 
                    #Get the GL code        
                    elif re.search(regexlist[reportType]["searchGL"], str(value)) and flag == "GL":
                        entireGL= re.search(regexlist[reportType]["searchEntireGL"], value)   #The regular expression is applied to extract the entire GL code
                        entireGL= entireGL.group(0)                   
                        entireGL= str(entireGL).strip()               #Blank spaces are deleted
                        gl= getGL(value, reportType)           #Call the function to get the GL code and save it to an variable
                        flag= "DatesAux"
                        #print(allgl)
                        #print(gl)

                    elif re.search(regexlist[reportType]["startDateTime"], str(value)) and (flag == "GL" and flagGLextra== True):
                        flag="Date"
                        flagGLextra=False
                        flagEmpAux= False 
                        gl=""
                        entireGL=""
                    #Get Dates and time
                    elif re.search(regexlist[reportType]["startDateTime"], str(value)) and flag == "DatesAux":
                        flag= "Date"                             #Change to flag to Date to search the Dates
                        flagEmpAux= False                        #Stop searching a possible nurse name
                    elif re.search(regexlist[reportType]["searchDateTime"], str(value)) and flag == "Date":
                        comment= ""                                                         #Intialize the comments variable, we can get comments from here when the date time format is:   5/3/2022 12:00 AM Missed Break WA
                        datetimeAux1= getDateTime(value, reportType)          #Call the function to get the Date, Time and any comment, and save them into a list
                        if datetimeAux1 != False:
                            comAux= True
                            datetimeAux= datetimeAux1[0]
                            flagComment= datetimeAux1[1]
                            date= datetimeAux[0]                 #Save the date, it always is on the position 0 on the list
                            #print(date)
                            if len(datetimeAux) == 1:            #If the list lenght is equal to 1 only got the date
                                flag="Time"                      #Change the flag to "Time", this is to use another function to get the time
                            else:   
                                time= datetimeAux[1]             #Save the time, it is located on the position 1 on the list
                                #print(time)
                                flag= "HourDaily" 
                                if re.search(regexlist[reportType]["searchSepTimeOut2"], str(value)) :  
                                    timeOutAux = re.search(regexlist[reportType]["searchSepTimeOut2"], str(value))
                                    timeOutAux = timeOutAux.group(0)
                                    if re.search(regexlist[reportType]["searchSepTimeOut"], str(timeOutAux)):
                                        timeOutAux2= re.search(regexlist[reportType]["searchSepTimeOut"], str(timeOutAux))
                                        timeOutAux2 = timeOutAux2.group(0)
                                        timeOut = convertHours(timeOutAux2, reportType)
                                else:
                                    flagOutOux = "OutAux"        

                                if len(datetimeAux) >= 3:        #if the list len is 3 it means that has comments
                                    comment= datetimeAux[2]      #Save the comments, they are located on the position 2 on the list
                                    if comment != "":
                                        payRule= comment             #Add the comment as PayRule too
                                else:
                                    comment=""
                        else:
                            comAux= False                   

                    #Get the separated time
                    elif re.search(regexlist[reportType]["searchSepTime"], str(value)) and flag == "Time":    #This statement get the time when the time value is not next to the date          
                        time= convertHours(value, reportType)
                        if re.search(regexlist[reportType]["searchSepTimeOut"], str(value)):
                            timeOutAux = re.search(regexlist[reportType]["searchSepTimeOut"], str(value)) #obtain timeout
                            timeOutAux2 = timeOutAux.group(0)
                            timeOut = convertHours(timeOutAux2, reportType)
                            flag= "HourDaily"                                                               #Change to flag to HourDaily to search the total hours
                        else:    
                            flag= "DateAuxOut"  
                                                                                   
                    elif re.search(regexlist[reportType]["searchExpData"],str(value)) and (flagOutOux == "OutAux"):   
                        flagOutOux = "False"                                                                    #Ignore the word "Data", Leaving the "OutOux" flag set to "false".

                    elif re.search(regexlist[reportType]["searchSepTimeOut"], str(value)) and ( flag== "DateAuxOut" or flagOutOux== "OutAux"):
                        timeOutAux = re.search(regexlist[reportType]["searchSepTimeOut"], str(value)) #obtain timeout
                        timeOutAux2 = timeOutAux.group(0)
                        timeOut = convertHours(timeOutAux2, reportType)
                        flag= "HourDaily"


                    elif re.search(regexlist[reportType]["searchComments"], str(value)) and flagComment== True:
                        comment= comment + " | " + value
                        payRule = value
                        flagComment= False
                    
                    #Get hours    
                    elif re.search(regexlist[reportType]["searchHours"], str(value)) and flag == "HourDaily": #This statement get the time hours
                            hour= getHours(value, response, reportType)                                        #Call the function to get the hours, if the response value is True, a kind of rounding will be applied on the minutes
                            flag= "Date"                                                          #Change to flag to Date to search the next date
                            #print(hour)
                            writeDF(nurse,gl,payRule,date,time,timeOut,hour,comment,entireGL)                      #Call the a funtion to append all the get values on the dataframe
                            payRule= "Regular"
                            timeOut = ""
                            flagComment= False                                                    #Return the pay code to the default value "Regular"
                            flagExtra= True                                                       #This flag is used to identify comments on the next values

                    elif re.search(regexlist[reportType]["nextPage"], str(value)) and flag == "Date":         #This is to identify were the page ends
                        flag= "DatesAux"                                                          #This flag is to search data for the same nurse on a next page

                    #Next nurse  
                    elif re.search(regexlist[reportType]["brakeLoop"], str(value)):                           #This statement brake identify where the page ends 
                        #flag= "NoMore"                                                            #The flag change to avoid get more data, this until reach the next nurse
                        flag="Emp" 
                        flagExtra= False
                        #nameVerif= name
                        payRule= ""
                        gl= ""
                        date= ""
                        time= ""
                        hour= ""
                        comment= ""
                        entireGL = ""
                        timeOut = ""
                        flagOutOux =""
                    elif re.search(regexlist[reportType]["searchComments"], str(value)) and flag == "Date" and flagExtra== True and comAux== True: #This statement is used to get the comments
                        comment= comment + " | " + value                                                             #Concatenate the comments nad separete them by using a pipe
                        size= (len(df.index))-1                                                                      #Get the dataframe last row number, to override the comments
                        df.at[size, 'Comments']= comment                                                             #Write on the dataframe the Comments
                        checkComments(value, reportType)                                                                         #This functions identify useful or needed datd from the comments
    
    writer = pd.ExcelWriter(path)                                                                                    #The following commands send the dataframe to an Excel file and save it on the path
    df.to_excel(writer, index = None, header=True)
    writer.save()

    
    df1= df.copy(deep=True)
    df.drop(df.index,inplace=True)

    if df1.empty:
        return False
    else:
        return True
        