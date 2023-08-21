#Needed libraries
import PyPDF2
import pandas as pd
import re  # regex
from Classes.outputUKGcommon import logUKGcommon
from datetime import datetime
import os

class pdfUKGcommon:
    
    global df
    #Create a empty DataFrame with the required columns 
    col=["EMPLID","NAME","DATE","AGENCY","GLCODE","PAYCODE","STARTDTM","ENDDTM","HOURLY RT","HOURS","WAGES","MULTIPLIER","ADDER","INVOICE ID","ApproveByAgency","ApproveByFacility","Pool","Comments", "PrimaryJob"] #Create a list with the dataframe headers
    df= pd.DataFrame(columns=col)  #Create the empty dataframe
    
    def clear(): #clear data
        global date, paycode, inHour, hours, paycode2, comment
        date = ""
        paycode = ""
        inHour = ""
        hours = ""
        paycode2=""
        comment = ""
        
        
    def writeDF(nurse, date, paycode, inHour, hours, comment, primaryJob): #write data in the excel
        global df
        info = {'NAME': nurse, 'DATE': date, 'PAYCODE' : paycode, 'STARTDTM' : inHour, 'HOURS': hours, 'Comments': comment, 'PrimaryJob' : primaryJob}
        df= df.append(info, ignore_index= True)
        
    def main(response, file, reportType, from_convert_pdf_UKGC=False):
        
        #Read a json file with the regex values and import them to a dictionary
        regexlist= logUKGcommon.readJsonRegex()

        pdf_file_name = os.path.splitext(os.path.basename(file))[0]

        if from_convert_pdf_UKGC:
            path = "Output/OUTPUT UKGCommon/" + pdf_file_name + ".xlsx"
        else:
            path = regexlist[reportType]["output_file"] + reportType + " output " + currentTime + ".xlsx"

        global nurse, date, paycode, inHour, hours, flag, paycode2, comment, primaryJob, df

        arrayGLword =[]
        arrayCodeGL = []

        current = datetime.now()
        currentTimeAux = str(current.strftime("%Y-%m-%d %H:%M:%S"))
        currentTime= currentTimeAux.replace(":", "")
        path = regexlist[reportType]["output_file"] + reportType +" output " + currentTime + ".xlsx"

        #desired_pages = list(range(91,93))  # Desired pages (range)

        primaryJob = ""
        flag = "Emp"
        flagComment = False
        flagExtra = True
        flagGL = False
        pdfUKGcommon.clear()

        with open(file, 'rb') as pdf_file:   # Open the PDF file
            reader = PyPDF2.PdfReader(pdf_file)   # Create a PDF reader object
            
            #for page_num in desired_pages: # Iterate over the pages
            for page_num in range(len(reader.pages)): #lee todas las paginas
                if page_num >= 0 and page_num < len(reader.pages):  # Check if the page number is within the valid range
                    page = reader.pages[page_num]  # Extract the text from the page
                    text = page.extract_text()
                    lines = text.split('\n')    # Split the text into lines
                    for line in lines:   # Iterate over the lines
                        if line.strip():  # Check if the line is not empty or composed only of whitespace
                            #print(line)
                            if re.search(regexlist[reportType]["searchEMPL"], str(line)) and flag == "Emp": #Search with the keyword to find the name of nurse 
                                nurse= logUKGcommon.getNurse(line, reportType)
                                #print(nurse)
                                flag= "getPrimaryJob"

                            elif re.search(regexlist[reportType]["searchPrimeryJob"], str(line)) and flag == "getPrimaryJob": #Search with keyword to find the primary job
                                flag = "searchDateORprimaryJob"
                                flagGL = True

                            elif re.search(regexlist[reportType]["getPrimaryJob"], str(line)) and "searchDateORprimaryJob" and flagGL == True:  #Obtain the primary job 
                                primaryJob = logUKGcommon.getPrimaryJob(line, reportType, primaryJob)
                                #flag= "searchDateORprimaryJob"

                            elif re.search(regexlist[reportType]["searchDate"], str(line)) and flag == "searchDateORprimaryJob": #Search with keyword to find the date 
                                flagGL = False
                                flag= "date"

                            elif re.search(regexlist[reportType]["getDate"], str(line)) and (flag =="date" or flag == "inHourORdate" or flag == "HoursORdate" or flag == "PaycodeORdateORinHour"): #Get the date 
                                if (flag == "inHourORdate" or flag== "HoursORdate" or flag == "PaycodeORdateORinHour") and flagExtra == True: #in case the flag indacates that information is missing 
                                    pdfUKGcommon.writeDF(nurse, date, paycode, inHour,hours, comment, primaryJob)       #call the fuction to write the information 
                                pdfUKGcommon.clear()
                                flagExtra= True
                                date = logUKGcommon.getDate(line, reportType)  # Obtain the date 

                                #print(date)
                                if re.search(regexlist[reportType]["searchPaycode"], str(line)): #Search the paycode with the keyword 
                                    paycode = logUKGcommon.getPaycode(line, reportType)     #Obtain the paycode 
                                    flag= "PaycodeORdateORinHour"
                                    #print(paycode)
                                else:
                                    paycode = "Regular"      # in case that PDF have not information in paycode change as "Regular" 
                                if re.search(regexlist[reportType]["getInhour"], str(line)):  #Search the time in 
                                    inHour = logUKGcommon.getInHour(line, reportType, date)  # Obtain the time in 
                                    #print(inHour)
                                    if re.search(regexlist[reportType]["getHours"], str(line)): #Search the hours 
                                        hours = logUKGcommon.getHours(line, reportType) #Obtain the hours 
                                        #print(hours)
                                        flag = "date"
                                        pdfUKGcommon.writeDF(nurse, date, paycode, inHour,hours, comment, primaryJob) #Write the information obtained 
                                        flagComment = True        
                                    else:
                                        flag = "HoursORdate"
                                      
                                

                            elif re.search(regexlist[reportType]["searchPaycode"], str(line)) and flag == "PaycodeORdateORinHour": #Serch a second paycode 
                                paycode2 = logUKGcommon.getPaycode(line, reportType) # obtain the second paycode 
                                paycode = paycode + " / " + paycode2    # concatenate the 2 paycodes in case that was found 
                                #print(paycode2)
                                if re.search(regexlist[reportType]["getInhour"], str(line)):  #Search Time in 
                                    inHour = logUKGcommon.getInHour(line, reportType, date) #Get Time in 
                                    #print(inHour)
                                    if re.search(regexlist[reportType]["getHours"], str(line)): #Search Hours
                                        hours = logUKGcommon.getHours(line, reportType) #Get hours
                                        #print(hours)
                                        flag = "date"
                                        pdfUKGcommon.writeDF(nurse, date, paycode, inHour,hours, comment, primaryJob) #call the function to wirte the information 
                                        flagComment = True
                                else: 
                                    flag = "inHourORdate"
                                
                                
                            elif re.search(regexlist[reportType]["getInhour"], str(line)) and (flag == "inHourORdate" or flag == "PaycodeORdateORinHour"): #Search the time in 
                                inHour = logUKGcommon.getInHour(line, reportType, date) #Get the time in 
                                #print(inHour)
                                if re.search(regexlist[reportType]["getHours"], str(line)):  #Search the Hours 
                                    hours = logUKGcommon.getHours(line, reportType)          #get the Hours
                                    #print(hours)
                                    flag = "date"
                                    pdfUKGcommon.writeDF(nurse, date, paycode, inHour,hours, comment, primaryJob) #Call the fuction to write the information 
                                    flagComment = True
                                else:
                                    flag = "HoursORdate"

                            elif re.search(regexlist[reportType]["getHours"], str(line)) and flag == "HoursORdate"  :   #Search the Hours 
                                    hours = logUKGcommon.getHours(line, reportType)                                     #get the hours 
                                    #print(hours)
                                    flag = "date"
                                    pdfUKGcommon.writeDF(nurse, date, paycode, inHour,hours, comment, primaryJob)       #call the fuction to write the information 
                                    flagComment = True

                            elif re.search(regexlist[reportType]["getComment2"], str(line)) and (flag =="date" or flag == "inHourORdate" or flag == "HoursORdate" or flag == "PaycodeORdateORinHour") and flagComment == True: #This statement is used to get the comments
                                if (flag == "inHourORdate" or flag== "HoursORdate" or flag == "PaycodeORdateORinHour"):
                                    pdfUKGcommon.writeDF(nurse, date, paycode, inHour,hours, comment, primaryJob)
                                    flagExtra = False
                                    flag = "date"
                                comment= logUKGcommon.getComments(line, comment, reportType)                                                         #Obtain the comment 
                                size= (len(df.index))-1                                                                      #Get the dataframe last row number, to override the comments
                                df.at[size, 'Comments']= comment  
                                

                            elif re.search(regexlist[reportType]["searchGL"], str(line)) and (flag =="date" or flag == "inHourORdate" or flag == "HoursORdate" or flag == "PaycodeORdateORinHour"):  #Search with keyword the GL
                                flag = "getGL"

                            elif re.search(regexlist[reportType]["getComment"], str(line)) and (flag =="getGL"):  #Search with "Getcomment" as keyword to find a GL
                                glWordAux = re.search(regexlist[reportType]["getComment"], str(line))  #set a GL auxiliar and search with keyboard 
                                glWordAux2 = glWordAux.group(0)
                                glWord = logUKGcommon.getGLword(glWordAux2)                             #Obtain the GL 
                                if re.search(regexlist[reportType]["getGL"], str(line)):              #Search the numbers in GL 
                                    codeGLAux = re.search(regexlist[reportType]["getGL"], str(line)) 
                                    codeGLAux2 = codeGLAux.group(0)                               
                                    codeGL = logUKGcommon.getCodeGL(codeGLAux2)                       #Obtain the GL
                                    arrayGLword.append(glWord)                                  #add to array 
                                    arrayCodeGL.append(codeGL)                                  #add to array 


                            elif re.search(regexlist[reportType]["breakLoop"], str(line)):  #Stop by keyword to no get more information 
                                outputUKGcommon = logUKGcommon(df,arrayCodeGL, arrayGLword, nurse)  #the variables that we need to use 
                                df = outputUKGcommon.getComparationGl()                              #call the fuction to comparate the GL 
                                flag = "startPage"
                                pdfUKGcommon.clear()
                                nurse = ""
                                primaryJob = ""
                                arrayGLword.clear
                                arrayCodeGL.clear
                                flagExtra=True

                            elif re.search(regexlist[reportType]["startPage"], str(line)) and flag == "startPage": #when start to search a new nurse 
                                flag = "Emp"

        

        writer = pd.ExcelWriter(path)
        df.to_excel(writer, sheet_name='Sheet1',index = None, header=True)  # Save df in a sheet named 'RawData' 
        writer.save()  # Save the changes to the Excel file

        df1= df.copy(deep=True)
        df.drop(df.index,inplace=True)   
        return not (df1.empty)




    
    