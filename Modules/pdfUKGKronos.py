#Needed Libraries
import PyPDF2
import pandas as pd
import re
import warnings
from Classes.outputUKGKronos import UKGKronos
import os

#Remove warnings from the console logs
warnings.simplefilter(action='ignore', category=FutureWarning)   

global df
#Create a empty DataFrame with the required columns 
col=["EMPLID","NAME","DATE","AGENCY","GLCODE",'PRIMARY JOB',"PAYCODE","STARTDTM","ENDDTM","HOURLY RT","HOURS","WAGES","MULTIPLIER","ADDER","INVOICE ID","ApproveByAgency","ApproveByFacility","Pool","Comments"]
df= pd.DataFrame(columns=col)  #Create the empty dataframe  

def clear(): #clear data
        global name,PrimaryJob,date,inHour,hours,OutHour,paycode,comment
        name=""
        PrimaryJob=""
        date = ""
        inHour=""
        hours=""
        OutHour=""
        paycode=""
        comment=""

def writeDF(name,PrimaryJob, date, paycode, inHour,OutHour,hours,comment): #write data in the excel
        global df
        info = {'NAME': name, 'DATE': date, 'PRIMARY JOB': PrimaryJob, 'PAYCODE' : paycode,'STARTDTM' : inHour,'ENDDTM' :OutHour ,'HOURS':hours,'Comments': comment }
        df= df.append(info, ignore_index= True)

def main(response, file, reportType, from_convert_pdf_UKGK=False):
    """
    Main code for PDF to Excel. Receives response whether or no convert hours and file to process.
    """
    regexlist = UKGKronos.readJsonRegex()

    currentTime = UKGKronos.date_time()
    pdf_file_name = os.path.splitext(os.path.basename(file))[0]

    if from_convert_pdf_UKGK:
        path = "Output/OUTPUT UKGKronos/" + pdf_file_name + ".xlsx"
    else:
        path = regexlist[reportType]["output_file"] + reportType + " output " + currentTime + ".xlsx"
    
    #desired_pages = list(range(139,141))  # Desired pages (range)
    global name,PrimaryJob,date,inHour,hours,OutHour,paycode,comment
    flag = "Emp"
    FlagExtraName= False
    flagExtraPayCode=False
    FlagExtraWrite=False
    FlagComments=False
    flagExtraHours = False 
    flagExtraOutHours=False
    FlagExtraName2=False
    FlagCommentsorDate=False
    clear()

    #Read the PDF file and create a list of dataframes with the PDF pages
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

                        #Get the nurse name
                        # Check if the search pattern matches and the flag is "Emp".
                        if re.search(regexlist[reportType]["searchName"], str(line)) and flag == "Emp":

                            # Check if the 'date' is not empty.
                            if date != "":
                                # Call the 'writeDF' function to write data.
                                writeDF(name, PrimaryJob, date, paycode, inHour, OutHour, hours, comment)

                            # Clear some variables or perform other tasks.
                            clear()

                            # Check if the 'getName' pattern matches in the line.
                            if re.search(regexlist[reportType]["getName"], str(line)):
                                # Extract the nurse's name and set flags.
                                name = ""
                                name = UKGKronos.getNurse(line, reportType, name)
                                #print(name)
                                FlagExtraName = True
                                flag = "SearchPrimaryJob"
                            else:
                                # Set the flag to "Getname".
                                flag = "Getname"
                                               

                        # Check if the search pattern specified is found in the current line, and if the flag is "Emp".
                        elif re.search(regexlist[reportType]["searchDate"], str(line)) and flag == "Emp":

                            # Set the 'FlagCommentsorDate' variable to True to indicate comments or date is found.
                            FlagCommentsorDate = True

                            # Set the 'flag' to "ExtraDate" to process additional date-related information.
                            flag = "ExtraDate"

                        # Check if the pattern specified is found in the line, and if both 'FlagCommentsorDate' and 'flag' are True and "ExtraDate" respectively.
                        elif re.search(regexlist[reportType]["getDate"], str(line)) and (FlagCommentsorDate==True and flag == "ExtraDate") :
                            # Set 'FlagCommentsorDate' to False.
                            FlagCommentsorDate=False

                            if date !="" :  # If 'date' is not empty, and there's data to write, call 'writeDF' function.
                                if FlagExtraWrite==True:
                                    writeDF(name,PrimaryJob, date, paycode, inHour,OutHour,hours,comment)
                                    
                            date=UKGKronos.getDate(line,reportType)  # Get the 'date' using 'UKGKronos.getDate()'.
                            #print(date)
                            paycode=""
                            hours=""
                            inHour=""
                            OutHour=""
                            comment=""
                            # Set flags for further processing.
                            FlagExtraWrite=True
                            FlagComments=False
                            
                            # Check for 'paycode' pattern, if found, get the 'paycode'.
                            if re.search(regexlist[reportType]["searchPaycode"], str(line)):
                                paycode=UKGKronos.getPaycode(line,reportType,paycode)
                                #print(paycode)
                                flagExtraPayCode=True
                            # Check for 'getInhour' pattern, if found, get the 'inHour' and set corresponding flags.
                            if re.search(regexlist[reportType]["getInhour"], str(line)):  #Search Time in 
                                inHour = UKGKronos.getInHour(line, reportType, date)
                                #print(inHour)
                                flagExtraPayCode=False
                                FlagComments= True
                            # Check for 'getOuthour' pattern, if found, get the 'OutHour' and set corresponding flags.
                            if re.search(regexlist[reportType]["getInhour"], str (line)):
                                OutHour=UKGKronos.getOutHour(line, reportType, date)
                                #print(OutHour)
                                FlagComments= True
                                if OutHour == "":
                                    flagExtraOutHours =True    
                            # Check for 'getHours' pattern, if found, get the 'hours' and set corresponding flags.
                            if re.search(regexlist[reportType]["getHours"], str(line)): #Search Hours
                                hours = UKGKronos.getHours(line, reportType) #Get hours
                                #print(hours)
                                if float(hours) >= 25.00:
                                    hours = ""
                                else:    
                                    flagExtraPayCode=False
                                    FlagComments= True
                                    flagExtraHours = False
                            else: 
                                flagExtraHours = True 
                                FlagComments = False
                            # Set 'flag' to "GetDateorComment" and reset 'comment'.
                            flag = "GetDateorComment" 
                            #comment=""     
                        
                        # Check if the pattern specified is found in the line and if either 'flag' is "Getname" or 'FlagExtraName' is True.
                        elif re.search(regexlist[reportType]["getName"], str(line)) and (flag == "Getname" or FlagExtraName == True) :          #Obtain the name 
                            # Obtain the name using 'UKGKronos.getNurse()' and update 'name'.
                            name= UKGKronos.getNurse(line, reportType,name) 

                            # Reset the 'FlagExtraName' and set 'FlagExtraName2' to True.
                            FlagExtraName=False
                            FlagExtraName2=True
                            #print(name)

                        # Check if the pattern specified is found in the line and if 'flag' is "SearchPrimaryJob".
                        elif re.search(regexlist[reportType]["searchPrimeryJob"], str(line)) and flag == "SearchPrimaryJob":
                            flag = "GetPrimaryJob" # Update 'flag' to "GetPrimaryJob".

                            # Reset 'FlagExtraName' and 'FlagExtraName2'.
                            FlagExtraName=False
                            FlagExtraName2=False

                        # Check if the pattern specified is found in the line and if either 'flag' is "Getname" or 'FlagExtraName2' is True.
                        elif re.search(regexlist[reportType]["getName"], str(line)) and (flag == "Getname" or FlagExtraName2 == True) :
                            name= UKGKronos.getNurse(line, reportType,name)  # Obtain the name using 'UKGKronos.getNurse()' and update 'name'.
                            FlagExtraName2=False # Reset 'FlagExtraName2'.

                        # Check if the pattern specified is found in the line and if 'flag' is "GetPrimaryJob".
                        elif re.search(regexlist[reportType]["GetPrimary"], str(line)) and flag == "GetPrimaryJob":
                            # Obtain the primary job using 'UKGKronos.getPrimaryJob()' and update 'PrimaryJob'.
                            PrimaryJob= UKGKronos.getPrimaryJob(line,reportType)
                            #print (PrimaryJob)
                            PrimaryJob2 = PrimaryJob
                            flag = "SearchDate"   # Update 'flag' to "SearchDate".

                        # Check if the pattern specified is found in the line and if 'flag' is "SearchDate".
                        elif re.search(regexlist[reportType]["searchDate"], str(line)) and flag =="SearchDate" :  
                            flag="GetDate" # Update 'flag' to "GetDate".
        
                        # Check if the pattern specified is found in the line and if 'flag' is either "GetDate" or "GetDateorComment".
                        elif re.search(regexlist[reportType]["getDate"], str(line)) and (flag == "GetDate" or flag == "GetDateorComment" ):
                            # If 'date' is not empty, and there's data to write, call 'writeDF' function.
                            if date !="" :
                                if FlagExtraWrite==True:
                                    writeDF(name,PrimaryJob, date, paycode, inHour,OutHour,hours,comment)
                            date=UKGKronos.getDate(line,reportType) # Get the 'date' using 'UKGKronos.getDate()'.
                            #print(date)
                            PrimaryJob = PrimaryJob2
                            paycode=""
                            hours=""
                            inHour=""
                            OutHour=""
                            comment=""
                            # Set/reset flags for further processing.
                            FlagExtraWrite=True
                            FlagComments=False

                            # Check for 'searchPaycode' pattern, if found, get the 'paycode'.
                            if re.search(regexlist[reportType]["searchPaycode"], str(line)):
                                paycode=UKGKronos.getPaycode(line,reportType,paycode)
                                #print(paycode)
                                flagExtraPayCode=True
                            # Check for 'getInhour' pattern, if found, get the 'inHour' and set corresponding flags.
                            if re.search(regexlist[reportType]["getInhour"], str(line)):  #Search Time in 
                                inHour = UKGKronos.getInHour(line, reportType, date)
                                #print(inHour)
                                flagExtraPayCode=False
                                FlagComments= True
                            
                            if re.search(regexlist[reportType]["getcomment"], str (line)):
                                 comment=UKGKronos.getComments(line,reportType,comment)
                                 comment = re.sub(regexlist[reportType]["getcomment2"], "", comment)      


                            # Check for 'getOuthour' pattern, if found, get the 'OutHour' and set corresponding flags.
                            if re.search(regexlist[reportType]["getInhour"], str (line)):
                                OutHour=UKGKronos.getOutHour(line, reportType, date)
                                #print(OutHour)
                                FlagComments= True
                                if OutHour == "":
                                    flagExtraOutHours =True    
                             # Check for 'getHours' pattern, if found, get the 'hours' and set corresponding flags.
                            if re.search(regexlist[reportType]["getHours"], str(line)): #Search Hours
                                hours = UKGKronos.getHours(line, reportType) #Get hours
                                #print(hours)
                                if float(hours) >= 25.00:
                                    hours = ""
                                else:    
                                    flagExtraPayCode=False
                                    FlagComments= True
                                    flagExtraHours = False
                            else: 
                                flagExtraHours = True 
                                #FlagComments = False
                            # Update 'flag' to "GetDateorComment" and reset 'comment'.
                            flag = "GetDateorComment" 
                            #comment=""  
              
                        # Check if the pattern specified is found in the line, and if 'flagExtraPayCode' is True.
                        elif re.search(regexlist[reportType]["searchPaycode"], str(line)) and flagExtraPayCode== True:
                            # Get the 'paycode' using 'UKGKronos.getPaycode()' and update 'paycode'.
                            paycode=UKGKronos.getPaycode(line,reportType,paycode)  

                            # Check for 'getInhour' pattern, if found, get the 'inHour' and set corresponding flags.
                            if re.search(regexlist[reportType]["getInhour"], str(line)):  #Search Time in 
                                inHour = UKGKronos.getInHour(line, reportType, date)
                                #print(inHour)
                                flagExtraPayCode=False 
                                FlagComments= True

                            # Check for 'getOutHour' pattern, if found, get the 'OutHour' and set corresponding flags.
                            if re.search(regexlist[reportType]["getInhour"], str (line)):
                                OutHour=UKGKronos.getOutHour(line, reportType, date)
                                #print(OutHour)
                                FlagComments= True
                                if OutHour == "":
                                    flagExtraOutHours =True            
                            
                            # Check for 'getHours' pattern, if found, get the 'hours' and set corresponding flags.
                            if re.search(regexlist[reportType]["getHours"], str(line)): #Search Hours
                                hours = UKGKronos.getHours(line, reportType) #Get hours
                                #print(hours)
                                if float(hours) >= 25.00:
                                    hours = ""
                                else:    
                                    flagExtraPayCode=False
                                    flagExtraHours = False
                            else:
                                flagExtraHours = True     
                                FlagComments= True

                        # Check if the pattern specified in regexlist[reportType]["breakLoop"] is found in the line.
                        elif re.search(regexlist[reportType]["breakLoop"], str(line)):    
                            # Get the match object for the pattern found.
                            breakloop = re.search(regexlist[reportType]["breakLoop"], str(line))

                            # Reset flags and update 'flag' to "StartPage".
                            flag="StartPage"
                            FlagComments=False

                            # Check the matched pattern and update 'flag' accordingly.
                            if breakloop.group(0) == "Time Detail":
                                flag = "Emp"   
                            if breakloop.group(0) == "Job Summary":
                                FlagCommentsorDate = False
                                flagExtraHours = False
                        
                        # Check if the pattern specified is found in the line, and if both 'FlagCommentsorDate' and 'flag' are True and "ExtraDate" respectively.
                        elif re.search(regexlist[reportType]["getcomment"], str (line)) and (FlagCommentsorDate==True and flag == "ExtraDate"):
                            # Get the comments using 'UKGKronos.getComments()' and update 'comment'.
                            comment=UKGKronos.getComments(line,reportType,comment)
                            if re.search(regexlist[reportType]["GetPrimary"], str(comment)):
                                PrimaryJob= UKGKronos.getPrimaryJob(comment,reportType)
                                
                            # Update 'flag' to "GetDateorComment" and set 'FlagComments' to True.
                            flag = "GetDateorComment"
                            FlagComments = True


                        # Check if the pattern specified is found in the line, and if 'flagExtraOutHours' is True.
                        elif re.search(regexlist[reportType]["getInhour"], str (line)) and flagExtraOutHours == True:

                            # Get the 'OutHour' using 'UKGKronos.getInHour()' and update 'OutHour'.
                            OutHour=UKGKronos.getInHour(line, reportType, date)
                            FlagComments = True

                            # Check for 'getHours' pattern, if found, get the 'hours' and reset 'flagExtraHours'.
                            if re.search(regexlist[reportType]["getHours"], str(line)): #Search Hours
                                hours = UKGKronos.getHours(line, reportType)
                                flagExtraHours = False

                            # Set 'FlagComments' to True and reset 'flagExtraOutHours'.
                            FlagComments= True
                            flagExtraOutHours=False

                        # Check if the pattern specified is found in the line and if 'flagExtraHours' is True.
                        elif re.search(regexlist[reportType]["getHours"], str(line)) and flagExtraHours == True:
                            if re.search(regexlist[reportType]["getcomment"], str (line)):
                                comment=UKGKronos.getComments(line,reportType,comment)
                            # Get the 'hours' using 'UKGKronos.getHours()' and update 'hours'.
                            hours = UKGKronos.getHours(line, reportType)
                            
                            # Check if 'hours' is greater than or equal to 25.00, reset 'hours'.
                            if float(hours) >= 25.00:
                                hours = ""
                            else:
                                # Set 'FlagComments' to True and reset 'flagExtraHours'.
                                FlagComments= True
                                flagExtraHours = False

                        # Check if the pattern specified is found in the line and if both 'FlagComments' and 'flag' are True and "GetDateorComment" respectively.
                        elif re.search(regexlist[reportType]["getcomment"], str (line)) and (FlagComments==True and flag == "GetDateorComment") :
                            # Get the comments using 'UKGKronos.getComments()' and update 'comment'.
                            comment=UKGKronos.getComments(line,reportType,comment)   
                            if re.search(regexlist[reportType]["GetPrimary"], str(comment)):
                                PrimaryJob= UKGKronos.getPrimaryJob(comment,reportType)      
                            

                        # Check if the pattern specified is found in the line and if 'flag' is "StartPage".
                        elif re.search(regexlist[reportType]["startPage"], str(line)) and flag == "StartPage": #when start to search a new nurse 

                            # Update 'flag' to "Emp" and reset 'FlagCommentsorDate'.
                            flag = "Emp"
                            FlagCommentsorDate==False

        writer = pd.ExcelWriter(path)
        df.to_excel(writer, sheet_name='Sheet1',index = None, header=True)  # Save df in a sheet named 'RawData' 
        writer.save()  # Save the changes to the Excel file

        df1= df.copy(deep=True)
        df.drop(df.index,inplace=True)   
        return not (df1.empty)