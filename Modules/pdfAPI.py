#Needed libraries
import os
from xmlrpc.client import DateTime
import tabula as tb
import numpy as np
import pandas as pd
import re  # regex
import json
import warnings
from datetime import datetime
from Classes.auditPDFdefault import pdftest

warnings.simplefilter(action='ignore', category=FutureWarning)

def readJsonRegex():
    # read json file "Regex.json" that holds the regex that are required
    try:
        with open("Regex.json", "r") as read_file:
            data2 = json.load(read_file)           #Import the regex entries to a dictionary
            return data2                           #Return the dictionary
    except:
        print("Something happenned reading Json file")

def conatDateTime(inDate, inHour):
    dateandTime= inDate + " " + inHour
    return dateandTime

def getNurse(value, reportType): #search nurse
    nameAux= re.search(regexlist[reportType]["getEmp"], str(value))   #Search a match on the value by using a regex to get the nurse name
    name= re.sub(r':\s', "", nameAux.group(0))            #Remove the blank space and the : from the name
    return name                                           #Return the nurse name

def writeDF(name, inDate,codeDep, payCode, specialCode, dateandTimeIn, dateandTimeOut, hour, code ): #write data in the excel
    global df
    info = {'NAME': name, 'DATE': inDate, 'GLCODE' : codeDep, 'PAYCODE': payCode, 'SPECIAL CODE' : specialCode, 'STARTDTM': dateandTimeIn, 'ENDDTM': dateandTimeOut, 'HOURS': hour, 'CODE' : code,  'DEPARTMENT' : codeDep }
    df= df.append(info, ignore_index= True)

def clear(): # clean the variables below
    global name, payCode, dateandTimeIn, dateandTimeOut, hour, code, inDate, outHour, codeDep, specialCode
    name = ""
    payCode = ""
    dateandTimeIn = ""
    dateandTimeOut = ""
    hour = ""
    code = ""
    inDate= ""
    outHour = ""
    codeDep = ""
    codeDep= ""
    specialCode = ""


regexlist= readJsonRegex()

#Create a empty DataFrame with the required columns
col=["EMPLID","NAME","DATE","AGENCY","GLCODE","PAYCODE","SPECIAL CODE","STARTDTM","ENDDTM","HOURLY RT","HOURS","WAGES","MULTIPLIER","ADDER","INVOICE ID","ApproveByAgency","ApproveByFacility","Pool","CODE","DEPARTMENT","Comments"] #Create a list with the dataframe headers
df= pd.DataFrame(columns=col)  #Create the empty dataframe


def main(response, file, reportType, delete_sched):
    """
    Main code for PDF to Excel. Receives response whether or no convert hours and file to process.
    """
    import Classes.outputAPI as outputAPI
    global name, payCode, dateandTimeIn, dateandTimeOut, hour, code, inDate, outHour, codeDep, df, modified_df, specialCode
    current = datetime.now()
    currentTimeAux = str(current.strftime("%Y-%m-%d %H:%M:%S"))
    currentTime= currentTimeAux.replace(":", "")
    path = regexlist[reportType]["output_file"] + reportType +" output " + currentTime + ".xlsx"

    for filenames in file:

        #Read the PDF file and create a list of dataframes with the PDF pages
        table= tb.read_pdf(filenames, pages='all', stream= True, lattice=False, silent=False, guess=False, multiple_tables=True, pandas_options={'header': None}, java_options="-Dfile.encoding=UTF8")

        
        flag= "Code"
        dictIn= {}
        dictOut= {}
        DepAux = False
        arrayPaycode = []
        arrayHours= []
        flag2 = ""
        flag3 = ""
        codeDep = ""
        flagPaycodesAux=False

        #Loop over the data
        for item in table:                              #Iterate on the list of DataFrames
            for index, row in item.iterrows():          #Iterate on the DataFrame rows
                row = row.fillna('')                    #Replace the NaN values to blank spaces in the row
                for index, value in row.items():        #Iterate on the row values
                    if value != '':                     #Evaluate value is not empty (to skip the black values)
                        #print(value)
                        if re.search(regexlist[reportType]["searchCode"], str(value)) and flag == "Code": # search codes
                            codeAux= re.search(regexlist[reportType]["getCode"], str(value))
                            code= codeAux.group(0)
                            #print (code)
                            flag= "Emp"

                        if re.search(regexlist[reportType]["searchEmp"], str(value)) and flag == "Emp": #search name of the employee
                            name= getNurse(value, reportType)
                            flag= "Departament"
                            #print(name)

                        elif re.search(regexlist[reportType]["startGLDepartment"], str(value)) and flag == "Departament": #search key words about department
                            if re.search(regexlist[reportType]["searchDepartment"], str(value)): # search GL codes in the same iteration
                                codeDepAux= re.search(regexlist[reportType]["getDepartment"], str(value))
                                codeDep= codeDepAux.group(0)
                                if codeDep == "TRAVELERS INPT":
                                    DepAux = True
                                else:
                                    flag= "Check"
                            else:
                                flag= "SearchDep"

                        elif re.search(regexlist[reportType]["searchDepartment"], str(value)) and flag == "SearchDep": # search GL codes in the next iteration
                            codeDepAux= re.search(regexlist[reportType]["getDepartment"], str(value))
                            codeDep= codeDepAux.group(0)

                            if codeDep == "TRAVELERS INPT":
                                DepAux = True

                            else:
                                flag= "Check"

                        elif re.search(regexlist[reportType]["searchDepartment"], str(value)) and DepAux == True: # valid if exist other GL code other than TRAVELERS INPT
                            codeDepAux= re.search(regexlist[reportType]["getDepartment"], str(value))
                            codeDep= codeDepAux.group(0)
                            flag= "Check"

                        elif codeDep == "TRAVELERS INPT" and DepAux == True:
                            codeDep = ""
                            flag= "Check"

                        elif re.search(r'Clocking(\/Calendar)?', str(value)) and (flag == "Check" or "Stop"):
                            if re.search(regexlist[reportType]["startDate"], str(value)): #search first times
                                flag= "DateIn"
                            elif re.search(regexlist[reportType]["startClocking"], str(value)): #search first GL Codes
                                if len(arrayPaycode) > 0:
                                    if len(arrayPaycode) == len(arrayHours):
                                        for i in range(len(arrayPaycode)):
                                            payCode = arrayPaycode[i]
                                            hour = arrayHours[i]
                                            writeDF(name, inDate, codeDep, payCode, specialCode, dateandTimeIn, dateandTimeOut, hour, code)
                                arrayPaycode.clear()
                                arrayHours.clear()
                                flag2 = ""
                                flag3= ""
                                flag4 = ""
                                payCode = ""
                                hour = ""
                                flag= "Stop"

                        elif re.search(regexlist[reportType]["searchDate"], str(value)) and (flag == "DateIn" or flag =="HoursIn"): #obtain firts dat
                            dateAux= re.search(regexlist[reportType]["getDate"], str(value))
                            dateAux1= re.sub(r',', "", dateAux.group(0))
                            dateAux2= datetime.strptime(dateAux1, "%B %d %Y").strftime('%m-%d-%Y')
                            inDate= re.sub(r'-', "/", str(dateAux2))
                            flag= "HoursIn"
                            flagPaycodesAux=False
                            #print(inDate)

                        elif re.search(regexlist[reportType]["searchTimeIn"], str(value)) and flag == "HoursIn": #obtain in time
                            if re.search(regexlist[reportType]["getTimeIn"], str(value)):
                                inHourAux= re.search(regexlist[reportType]["getTimeIn2"], str(value))
                                inHour= inHourAux.group(0)
                                #print(inHour)
                                dateandTimeIn = conatDateTime(inDate, inHour)
                                specialCode = ""
                                if re.search(regexlist[reportType]["getSpecialCode"], str(value)):
                                    specialCodeAux = re.search(regexlist[reportType]["getSpecialCode"], str(value))
                                    specialCode = specialCodeAux.group(0)

                                if re.search(regexlist[reportType]["GethPayCodeRow"], str(value)): #obtain paycode in the same iteration
                                    payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                                    payCode =payCodeAux.group(0)
                                    #dateandTimeOut = inDate + " -"
                                    dateandTimeOut = ""
                                    flag= "GetHours"
                                    flagPaycodesAux=True
                                else:
                                    flag= "HoursOutAux"
                            else:
                                flag= "InHour"

                        elif re.search(regexlist[reportType]["searchSepTimeIn"], str(value)) and flag == "InHour": #obtain in time in the next iteration
                            inHourAux= re.search(regexlist[reportType]["getSepTimeIn"], str(value))
                            inHour= inHourAux.group(0)
                            #print(inHour)
                            dateandTimeIn = conatDateTime(inDate, inHour)
                            specialCode = ""
                            if re.search(regexlist[reportType]["getSpecialCode"], str(value)):
                                    specialCodeAux = re.search(regexlist[reportType]["getSpecialCode"], str(value))
                                    specialCode = specialCodeAux.group(0)
                            if re.search(regexlist[reportType]["GethPayCodeRow"], str(value)): #obtain paycode in the same iteration
                                payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                                payCode =payCodeAux.group(0)
                                #dateandTimeOut = inDate + " -"
                                dateandTimeOut = ""
                                flag= "GetHours"
                                flagPaycodesAux=True
                            else:
                                flag= "HoursOutAux"

                        elif re.search(regexlist[reportType]["GethPayCodeRow"], str(value)) and flag == "HoursOutAux": #obtain paycode in case does not have out time
                            payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                            payCode =payCodeAux.group(0)
                            #dateandTimeOut = inDate + " -"
                            dateandTimeOut = ""
                            flag= "GetHours"
                            flagPaycodesAux=True

                        elif (re.search(regexlist[reportType]["searchDate"], str(value))) and flag == "HoursOutAux": #obtain date in case does not have out time and paycode
                            #dateandTimeOut = inDate + " -"
                            dateandTimeOut = ""
                            flagPaycodesAux=False
                            if re.search(regexlist[reportType]["getDate"], str(value)):
                                dateAux= re.search(regexlist[reportType]["getDate"], str(value))
                                dateAux1= re.sub(r',', "", dateAux.group(0))
                                dateAux2= datetime.strptime(dateAux1, "%B %d %Y").strftime('%m-%d-%Y')
                                inDate= re.sub(r'-', "/", str(dateAux2))
                                flag = "HoursIn"

                            else:
                                flag = "Stop"

                        elif re.search(regexlist[reportType]["searchTimeOut"], str(value)) and flag == "HoursOutAux": #obtaion out time
                            if re.search(regexlist[reportType]["getTimeOut"], str(value)):
                                outHourAux= re.search(regexlist[reportType]["getTimeOut"], str(value))
                                outHour= outHourAux.group(0)
                                #print(inHour)
                                #dateandTimeOut= conatDateTime(inDate, outHour)
                                dateandTimeOut= outHour
                                flag = "otherHoursOut"
                                
                            else:
                                flag= "OutHour"
                                flagPaycodesAux=True

                        elif re.search(regexlist[reportType]["searchSepTimeOut"], str(value)) and flag == "OutHour": #obtain out time in the next iteration
                            if re.search(regexlist[reportType]["getSepTimeOut"], str(value)):
                                outHourAux= re.search(regexlist[reportType]["getSepTimeOut"], str(value))
                                outHour= outHourAux.group(0)
                                #print(inHour)
                                flag= "otherHoursOut"   
                                flagPaycodesAux=True

                        elif re.search(regexlist[reportType]["searchTimeOut"], str(value)) and flag == "otherHoursOut": #valid if exit another out time
                            if re.search(regexlist[reportType]["getTimeOut"], str(value)):
                                outHourAux= re.search(regexlist[reportType]["getTimeOut"], str(value))
                                outHour= outHourAux.group(0)
                                if re.search(regexlist[reportType]["getSpecialCode"], str(value)):
                                    specialCodeAux = re.search(regexlist[reportType]["getSpecialCode"], str(value))
                                    specialCode2 = specialCodeAux.group(0)
                                    if specialCode == "":
                                       specialCode = specialCode2
                                #dateandTimeOut= conatDateTime(inDate, outHour)
                                dateandTimeOut= outHour
                                flag= "otherHoursOut"
                                arrayPaycode.clear()
                                arrayHours.clear()
                                flag2= ""
                                flagPaycodesAux=True
                            else:
                                flag = "OtherOutHour"
                                
                            

                        elif re.search(regexlist[reportType]["searchSepTimeOut"], str(value)) and flag == "OtherOutHour" : #valid if exit another out time in the next iteration
                            if re.search(regexlist[reportType]["getSepTimeOut"], str(value)):
                                outHourAux= re.search(regexlist[reportType]["getSepTimeOut"], str(value))
                                outHour= outHourAux.group(0)
                                if re.search(regexlist[reportType]["getSpecialCode"], str(value)):
                                    specialCodeAux = re.search(regexlist[reportType]["getSpecialCode"], str(value))
                                    specialCode2 = specialCodeAux.group(0)
                                    if specialCode == "":
                                       specialCode = specialCode2     
                                #print(inHour)
                                #dateandTimeOut= conatDateTime(inDate, outHour)
                            dateandTimeOut= outHour
                            flag= "otherHoursOut"
                            arrayPaycode.clear()
                            arrayHours.clear()
                            flag2=""

                        elif re.search(regexlist[reportType]["SearchPayCodeRow"], str(value)) and flag == "otherHoursOut" : #search paycode in row
                            if re.search(regexlist[reportType]["GethPayCodeRow"], str(value)):
                                payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                                payCode =payCodeAux.group(0)
                                #dateandTimeOut= conatDateTime(inDate, outHour)
                                dateandTimeOut= outHour
                                flag= "GetHours"
                                flagPaycodesAux=True
                            else:
                                flag = "SearchPayCode"

                        elif re.search(regexlist[reportType]["GethPayCodeRow"], str(value)) and flag == "SearchPayCode" : #search paycode in row in the next iteration
                                payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                                payCode =payCodeAux.group(0)
                                #dateandTimeOut= conatDateTime(inDate, outHour)
                                dateandTimeOut= outHour
                                flagPaycodesAux=True
                                if re.search(regexlist[reportType]["getHours2"], str(value)): #obtain hours in row
                                    hourAux = re.search(regexlist[reportType]["getHours2"], str(value))
                                    hour = hourAux.group(0)
                                    writeDF(name, inDate,codeDep, payCode,specialCode, dateandTimeIn, dateandTimeOut, hour, code)
                                    payCode = ""
                                    hour = ""
                                    flag= "GetPaycodeAux"
                                    flag4= "nextpaycoderow"
                                else:
                                    flag= "GetHours"

                        elif re.search(regexlist[reportType]["GethPayCodeRow"], str(value)) and (flag == "GetPaycodeAux" and flagPaycodesAux==True): #valid if exit another paycode in the next iteration
                            if re.search(regexlist[reportType]["GethPayCodeRow"], str(value)):
                                payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                                payCode =payCodeAux.group(0)
                                flag= "GetHours"
                            else:
                                flag = "SearchPayCode"

                        elif re.search(regexlist[reportType]["GethPayCodeRow"], str(value)) and flag == "GetPayCodeAux" and flag4 == "nextpaycoderow": #valid if exit another paycode in the next Cell
                            if re.search(regexlist[reportType]["GethPayCodeRow"], str(value)):
                                payCodeAux= re.search(regexlist[reportType]["GethPayCodeRow"], str(value))
                                payCode =payCodeAux.group(0)
                                flag= "GetHours"
                            else:
                                flag = "SearchPayCode"

                        elif re.search(regexlist[reportType]["GetPayCodeColumn"], str(value)) and (flag == "otherHoursOut" or flag == "GetPaycodeAux"): #obtain paycode in column
                            if re.search(regexlist[reportType]["GetPayCodeColumn"], str(value)):
                                paycodeAux= str(value)
                                flag = "otherHoursOut"
                                flag2 = "column"
                                paycodeAux1 = paycodeAux.split()  #divide words if they have more than one paycode in the same iteration
                                if len(paycodeAux1) > 1:
                                    for paycodeAux3 in paycodeAux1:
                                        arrayPaycode.append(paycodeAux3)
                                else:
                                    arrayPaycode.append(paycodeAux)

                        elif re.search(regexlist[reportType]["getHours2"], str(value)) and flag == "otherHoursOut" and flag2 == "column": #obtain hours in column
                            if re.search(regexlist[reportType]["getHours2"], str(value)):
                                hourColumn= str(value)
                                flag = "otherHoursOut"
                                flag3 = "Printcolumns"
                                hourColumn1 = hourColumn.split()  #divide words if they have more than one paycode in the same iteration
                                if len(hourColumn1) > 1:
                                    for hourColumn2 in hourColumn1:
                                        arrayHours.append(hourColumn2)
                                else:
                                    arrayHours.append(hourColumn)


                        elif re.search(regexlist[reportType]["getHours2"], str(value)) and flag == "GetHours": #obtain hours in row
                            hourAux = re.search(regexlist[reportType]["getHours2"], str(value))
                            hour = hourAux.group(0)
                            writeDF(name, inDate,codeDep, payCode, specialCode, dateandTimeIn, dateandTimeOut, hour, code)
                            payCode = ""
                            hour = ""
                            flag= "GetPaycodeAux"
                            flag4= "nextpaycoderow"

                        elif (re.search(regexlist[reportType]["searchDate"], str(value))) and (flag == "GetPaycodeAux"): #obtain next date
                            flagPaycodesAux=False
                            if re.search(regexlist[reportType]["getDate"], str(value)):
                                dateAux= re.search(regexlist[reportType]["getDate"], str(value))
                                dateAux1= re.sub(r',', "", dateAux.group(0))
                                dateAux2= datetime.strptime(dateAux1, "%B %d %Y").strftime('%m-%d-%Y')
                                inDate= re.sub(r'-', "/", str(dateAux2))
                                flag = "HoursIn"
                            else:
                                flag = "Stop"

                        elif (re.search(regexlist[reportType]["searchDate"], str(value))) and (flag == "otherHoursOut" and flag3 == "Printcolumns"): #obtaion next date and print arrays
                            flagPaycodesAux=False
                            if re.search(regexlist[reportType]["getDate"], str(value)):
                                if len(arrayPaycode) > 0:
                                    if len(arrayPaycode) == len(arrayHours):
                                        for i in range(len(arrayPaycode)):
                                            payCode = arrayPaycode[i]
                                            hour = arrayHours[i]
                                            writeDF(name, inDate, codeDep, payCode, specialCode, dateandTimeIn, dateandTimeOut, hour, code)
                                arrayPaycode.clear()
                                arrayHours.clear()
                                flag2 = ""
                                flag3= ""
                                flag4 = ""
                                payCode = ""
                                hour = ""
                                dateAux= re.search(regexlist[reportType]["getDate"], str(value))
                                dateAux1= re.sub(r',', "", dateAux.group(0))
                                dateAux2= datetime.strptime(dateAux1, "%B %d %Y").strftime('%m-%d-%Y')
                                inDate= re.sub(r'-', "/", str(dateAux2))
                                flag = "HoursIn"
                            else:
                                flag = "Stop"

                        elif (re.search(regexlist[reportType]["searchDate"], str(value))) and (flag == "otherHoursOut"): #obtain next dates is they does not have paycodes
                            flagPaycodesAux=False
                            if re.search(regexlist[reportType]["getDate"], str(value)):
                                writeDF(name, inDate,codeDep, payCode, specialCode, dateandTimeIn, dateandTimeOut, hour, code)
                                payCode = ""
                                dateAux= re.search(regexlist[reportType]["getDate"], str(value))
                                dateAux1= re.sub(r',', "", dateAux.group(0))
                                dateAux2= datetime.strptime(dateAux1, "%B %d %Y").strftime('%m-%d-%Y')
                                inDate= re.sub(r'-', "/", str(dateAux2))
                                flag = "HoursIn"
                            else:
                                flag = "Stop"

                        elif re.search(regexlist[reportType]["brakeLoop"], str(value)) :     #Here the loop is broken, in case there are more nurses, the variables are cleaned.
                            clear()
                            dictIn.clear()
                            dictOut.clear()
                            arrayPaycode.clear()
                            arrayHours.clear()
                            flag2 = ""
                            flag3 = ""
                            DepAux = False
                            if re.search(regexlist[reportType]["serchTimeCardReport"], str(value)):
                                flag= "Code"
                            else:
                                flag= "Start"

                        elif re.search(regexlist[reportType]["startPage"], str(value)) and flag == "Start":
                            flag= "Code"

    output = outputAPI.outputAPI(df,delete_sched) #outputAPi class
    modified_df = output.modifyDataPaycodes() #df modified
    modified_df = output.iterateDF()
    modified_df = output.RemoveDuplicates()


    writer = pd.ExcelWriter(path)
    modified_df.to_excel(writer, sheet_name='OutputData', index = None, header=True)  # Save modified_df in another sheet named 'OutputData'
    df.to_excel(writer, sheet_name='RawData',index = None, header=True)  # Save df in a sheet named 'RawData' 
    writer.save()  # Save the changes to the Excel file

    df1= modified_df.copy(deep=True)
    modified_df.drop(modified_df.index,inplace=True)
    df.drop(df.index,inplace=True)

    if df1.empty:
        return False
    else:
        return True