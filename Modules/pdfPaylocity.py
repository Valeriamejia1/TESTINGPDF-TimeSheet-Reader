#Needed Libraries
import PyPDF2
import pandas as pd
import re
import warnings
import numpy as np
from Classes.outputPaylocity import outputPaylocity
import os

#Remove warnings from the console logs
warnings.simplefilter(action='ignore', category=FutureWarning)   

global df
#Create a empty DataFrame with the required columns 
col=["EMPLID","NAME","DATE","AGENCY","GLCODE","PAYCODE","STARTDTM","ENDDTM","HOURLY RT","HOURS","WAGES","MULTIPLIER","ADDER","INVOICE ID","ApproveByAgency","ApproveByFacility","Pool","Comments"]
df= pd.DataFrame(columns=col)  #Create the empty dataframe  


def writeDF(name,date, inHour, outHour, hour, paytype, glCode): #write data in the excel
        global df
        info = {'NAME': name, 'DATE': date, 'STARTDTM' :date+ " " +inHour, 'ENDDTM':date+ " " +outHour, 'HOURS' : hour, 'PAYCODE' : paytype, "GLCODE": glCode}
        df= df.append(info, ignore_index= True)

def clear(): # Clear variables
    global inHour,outHour, hour, paytype, count, countAdjs
    inHour = ""
    outHour = ""
    hour = ""
    paytype = ""
    count = 0
    countAdjs = 0

def main(response, file, reportType):
        
    regexlist = outputPaylocity.readJsonRegex()

    currentTime = outputPaylocity.date_time()
    #Line to run the script for users
    #path = regexlist[reportType]["output_file"] + reportType + " output " + currentTime + ".xlsx"

    #Line to change file name
    pdf_file_name = os.path.splitext(os.path.basename(file))[0]
    # Modify the path variable to use the base name of the PDF file for the name of the Excel file.
    path = "Output/" + pdf_file_name + currentTime + ".xlsx"


    global df, inHour,outHour, hour, paytype, count, countAdjs
    clear()
    flag = ""
    glCode = ""
    flagGL = False
    flagGetGL = False

    #desired_pages = list(range(1, 3))

    with open(file, 'rb') as pdf_file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(pdf_file)

        # Iterate over the pages
        #for page_num in desired_pages:
        for page_num in range(len(reader.pages)): #read all pages
            # Check if the page number is within the valid range
            if page_num >= 0 and page_num < len(reader.pages):
                page = reader.pages[page_num]# Extract the text from the page
                text = page.extract_text()
                lines = text.split('\n')# Split the text into lines
                for line in lines:# Iterate over the lines
                    if line.strip():  # Check if the line is not empty or composed only of whitespace
                        #print(line)
                        
                        # If a name is found, set the flag to extract it
                        if re.search(regexlist[reportType]["searchName"], str(line)):
                            glCode = ""             # Reset glCode
                            flag = "GetName"        # Set the flag to extract the name
                            flagGL = True           # Set flagGL to True

                        # If the name is found, extract it and set the flag to search for the date next
                        elif re.search(regexlist[reportType]["getName"], str(line)) and flag == "GetName":
                                name= outputPaylocity.getName(line, reportType) # Extract the name
                                #print(name)
                                flag = "searchDate"

                        # If a date is found, set the flag to extract it
                        elif re.search(regexlist[reportType]["searchDate"], str(line)) and flag == "searchDate":
                                flag = "getDate" # Set the flag to get the date

                        # If the date is found, extract it and set the flag to search for inHour next
                        elif re.search(regexlist[reportType]["getDate"], str(line)) and (flag == "getDate" or flag =="DateORinHour"):
                            date = outputPaylocity.getDate(line, reportType)  # Extract the date
                            #print(date)
                            flag = "getInHour"  # Set the flag to get "inHour"

                        # If the regex pattern to get the "inHour" matches the line and the flag is "getInHour" or "DateORinHour"
                        elif re.search(regexlist[reportType]["getInHour"], str(line)) and (flag == "getInHour" or flag =="DateORinHour"):
                                inHour = outputPaylocity.getInHour(line, reportType) # Extract the "inHour"
                                #print(inHour)
                                flag = "getOutHourOrTotalHours" # Set the flag to get "outHour" or "TotalHours"

                        # If the regex pattern to get the "inHour" matches the line and the flag is "getOutHourOrTotalHours"
                        elif re.search(regexlist[reportType]["getInHour"], str(line)) and flag == "getOutHourOrTotalHours":
                                outHour = outputPaylocity.getInHour(line, reportType) # Extract the "outHour"
                                #print(outHour)
                                flag= "TotalHours"  # Set the flag to get the total hours

                        # If the regex pattern to get the hours matches the line and the flag is "getOutHourOrTotalHours" or "TotalHours"
                        elif re.search(regexlist[reportType]["getHours"], str(line)) and (flag == "getOutHourOrTotalHours" or flag == "TotalHours"):
                            hourAux = outputPaylocity.getHours(line, reportType) # Extract the hours
                            count+=1
                            if count == 4:
                                hour = hourAux  # Store the hours
                                flag = "paytype" # Set the flag to get the pay type next
                                #print(hour)

                        # If the regex pattern to search for "searchGL" matches the line and the flagGL is True
                        elif re.search(regexlist[reportType]["searchGL"], str(line)) and flagGL == True:
                             flagGL = False   # Set flagGL to False to avoid re-searching "searchGL"
                             flagGetGL = True  # Set flagGetGL to True to get the GL code

                        # If the regex pattern to get the GL code matches the line and flagGetGL is True
                        elif re.search(regexlist[reportType]["getGL"], str(line)) and flagGetGL == True:
                            glCode= outputPaylocity.getGLCode(line, reportType) # Extract the GL code
                            #print(glCode)
                            df.loc[df['NAME'] == name, 'GLCODE'] = glCode  # Update GL code in DataFrame
                            flagGetGL = False # Set flagGetGL to False to avoid re-extracting GL code

                        # If the regex pattern to search for "searchPayType" matches the line and the flag is "paytype"
                        elif re.search(regexlist[reportType]["searchPayType"], str(line)) and flag == "paytype":
                            paytype = outputPaylocity.getPayType(line, reportType) # Extract the paytype
                            #print(paytype)
                            writeDF(name,date, inHour, outHour, hour, paytype, glCode)  # Write data to DataFrame
                            flag = "DateORinHour"  # Set flag to "DateORinHour" to continue searching for date or inHour
                            clear() # Clear variables

                        # Search Pay Adjustments word
                        elif re.search(regexlist[reportType]["searchPayAdjs"], str(line)):
                            flag= "searchDateAdjs"
                        
                        elif re.search(regexlist[reportType]["searchDate"], str(line)) and flag == "searchDateAdjs":
                             flag = "GetDateAdjs"
                             
                        # If the date is found, extract it and set the flag to search for inHour next
                        elif re.search(regexlist[reportType]["getDate"], str(line)) and flag == "GetDateAdjs":
                            date = outputPaylocity.getDate(line, reportType)  # Extract the date
                            #print(date)
                            flag = "paytypeAdjs"

                         # If the regex pattern to search for "searchPayTypeAdjs" matches the line and the flag is "paytypeAdjs"
                        elif re.search(regexlist[reportType]["searchPayType"], str(line)) and flag == "paytypeAdjs":
                            paytype = outputPaylocity.getPayType(line, reportType) # Extract the paytype
                            #print(paytype)
                            flag = "getHoursAdjus"
                        
                        # If the regex pattern to get the hours matches the line and the flag is "getHoursAdjus"
                        elif re.search(regexlist[reportType]["getHours"], str(line)) and flag == "getHoursAdjus":
                            hourAux = outputPaylocity.getHours(line, reportType) # Extract the hours
                            countAdjs+=1
                            if countAdjs == 2:
                                hour = hourAux  # Store the hours
                                #print(hour)
                                writeDF(name,date, inHour, outHour, hour, paytype, glCode)  # Write data to DataFrame
                                flag = "GetDateAdjs"  # Set flag to "GetDateAdjs" to continue searching for date or inHour
                                clear() # Clear variables
                        
                        #Search Ozarks word
                        elif re.search(regexlist[reportType]["searchNxtNurse"], str(line)):
                            flag= "GetNxtName"

                                     
                        
    writer = pd.ExcelWriter(path)
    #line to save the file with the new name
    df.to_excel(writer, sheet_name='Sheet1',index = None, header=True)  # Save df in a sheet named 'RawData' 
    writer.save()  # Save the changes to the Excel file

    df1= df.copy(deep=True)
    df.drop(df.index,inplace=True)
    df.drop(df.index,inplace=True)
    return not (df1.empty)
                                

                        


                                 

                            

                            
                                 
                                 