#Needed Libraries
import PyPDF2
import pandas as pd
import re
import warnings
from Classes.outputUKGSimplified import UKGSimplified

#Remove warnings from the console logs
warnings.simplefilter(action='ignore', category=FutureWarning)   

global df
#Create a empty DataFrame with the required columns 
col=["EMPLID","NAME","DATE","AGENCY","GLCODE","PAYCODE","STARTDTM","ENDDTM","HOURLY RT","HOURS","WAGES","MULTIPLIER","ADDER","INVOICE ID","ApproveByAgency","ApproveByFacility","Pool","Comments"]
df= pd.DataFrame(columns=col)  #Create the empty dataframe  


def writeDF(name, gl, paycode, date,hours,InHour): #write data in the excel
        global df
        info = {'NAME': name, 'DATE': date, 'GLCODE' : gl, 'PAYCODE' : paycode,'HOURS':hours,'STARTDTM' : InHour }
        df= df.append(info, ignore_index= True)

def main(response, file, reportType):
    """
    Main code for PDF to Excel. Receives response whether or no convert hours and file to process.
    """
    regexlist = UKGSimplified.readJsonRegex()

    currentTime = UKGSimplified.date_time()
    path = regexlist[reportType]["output_file"] + reportType + " output " + currentTime + ".xlsx"
    
    #desired_pages = list(range(5,8))  # Desired pages (range)

    flag = "Emp"
    flagEmpAux = False
    flagDateAux= False
    hours=""
    InHour=""
    flagPaycode = False
    paycode = ""

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
                        if re.search(regexlist[reportType]["searchName"], str(line)) and (flag == "Emp" or flag == "date" ):  #Obtain the name 
                            if re.search(regexlist[reportType]["getName"], str(line)):
                                name= UKGSimplified.getNurse(line, reportType)
                                #print(name)
                                gl = UKGSimplified.getGL(line, reportType)                                                          #Obtain the GL from the same iteration
                                #print(gl)
                                flag = "date"
                            else:        
                                flag= "Getname"
                            flagPaycode = False 

                        elif re.search(regexlist[reportType]["getName"], str(line)) and flag == "Getname":                                   #Obtain the name 
                            name= UKGSimplified.getNurse(line, reportType)                                                              #call method to get the name of nurse
                            #print(name)
                            gl = UKGSimplified.getGL(line, reportType)                                                                  #call method to get the name of nurse
                            #print(gl)
                            flag = "date"

                        elif re.search(regexlist[reportType]["searchDate"], str(line)) and (flag == "date" or flag == "InHourOrDate" or flag == "InHourorHour" ) :       #In case that not have Hours or In Hour , get the date
                            if ((flag == "InHourOrDate" or flag == "InHourorHour") and flagDateAux == True):
                              writeDF(name,gl, paycode, date,hours,InHour) 
                              hours =""
                              InHour =""
                              paycode = ""
                            date = UKGSimplified.getDate(line, reportType)                                                                                              #Obtain the date
                            #print(date)
                            flagPaycode = True
                            if re.search(regexlist[reportType]["getHours"], str(line)) : 
                                hours = UKGSimplified.getHours(line, reportType)                                                                                        #get the hours 
                            #print(hours)
                                flag = "InHourOrDate" 
                                flagDateAux= True  
                            else:            
                                flag = "InHourorHour"    
                                flagDateAux =True
                            if re.search(regexlist[reportType]["searchPaycode"], str(line)) :
                                paycode = UKGSimplified.getPaycodes(line, reportType, paycode)
                                if re.search(regexlist[reportType]["KeywordPaycode"], str(line)):
                                    flagPaycode = False
                                    if re.search(r'\sWorked\sShift', paycode):
                                        paycode = "Regular"
                            flagEmpAux = True
                            

                        elif re.search(regexlist[reportType]["searchPaycode"], str(line)) and (flagPaycode == True):
                            paycode = UKGSimplified.getPaycodes(line, reportType, paycode)
                            if re.search(regexlist[reportType]["KeywordPaycode"], str(line)):
                                flagPaycode = False
                                if re.search(r'\sWorked\sShift', paycode):
                                    paycode = "Regular"
                            if re.search(regexlist[reportType]["getHours"], str(line)):   #Search the Hours 
                                hours = UKGSimplified.getHours(line, reportType)                                     #get the hours 
                                #print(hours)
                                flag = "InHourOrDate" 
                                flagDateAux= True


                        elif re.search(regexlist[reportType]["getHours"], str(line)) and (flag == "InHourorHour")  :   #Search the Hours 
                            hours = UKGSimplified.getHours(line, reportType)                                     #get the hours 
                            #print(hours)
                            flag = "InHourOrDate" 
                            flagDateAux= True
                            flagPaycode = False
                        
                        elif re.search(regexlist[reportType]["getInhour"], str(line)) and flag == "InHourorHour":     #Search the In hour 
                            if re.search(regexlist[reportType]["getInhour"], str(line)):
                                InHour = UKGSimplified.getInHour(line, reportType, date)
                                flag = "date"
                                hours= ""
                                writeDF(name,gl, paycode, date,hours,InHour)                                                      #Write the information 
                                flagEmpAux = True
                                flagDateAux= False
                                date=""                                                                                  #Clear Variable
                                hours=""                                                                                
                                InHour =""
                                paycode = ""
                                flagPaycode = False

                        elif re.search(regexlist[reportType]["getInhour"], str(line)) and flag == "InHourOrDate"  :  #Search Time in 
                            InHour = UKGSimplified.getInHour(line, reportType,date)
                            #print(InHour)
                            writeDF(name,gl,paycode, date,hours,InHour)                                                        #Write the information
                            flagEmpAux = True
                            flag="date"
                            flagDateAux=False
                            date=""
                            hours=""
                            InHour =""
                            paycode = ""
                            flagPaycode = False

                        elif re.search(regexlist[reportType]["breakLoop"], str(line)):                              #To stop and not take more information        
                            name=""                                                                                 #Clear Variables and get false the flags
                            gl=""
                            date=""
                            hours=""
                            InHour =""
                            flag=""
                            paycode = ""
                            flagEmpAux=False
                            flagDateAux= False
                            flagPaycode = False 

                        elif re.search(regexlist[reportType]["searchName"], str(line)) and flagEmpAux == True : #when start to search a new nurse 
                            if ((flag == "InHourOrDate" or flag == "InHourorHour") and flagDateAux == True):
                              writeDF(name,gl,paycode, date,hours,InHour) 
                              hours =""
                              InHour =""
                            if re.search(regexlist[reportType]["searchName"], str(line)) :     #This statement verify if exist any other nurse name
                                nameAux= UKGSimplified.getNurse(line, reportType)                                     #Get the nurse name
                                glAux = UKGSimplified.getGL(line, reportType) 
                                flag="date"                                                 
                            if nameAux != name:                                                       #Veify if the nurse name is different of the new one
                                name= nameAux 
                                gl=glAux                                                        #Save the new name on the variable replacing the old one
                                flag= "date"      
                                date=""
                                hours=""
                                InHour =""  
                                paycode = ""  
                            flagPaycode = False                       

    writer = pd.ExcelWriter(path)
    df.to_excel(writer, sheet_name='Sheet1',index = None, header=True)  # Save df in a sheet named 'RawData' 
    writer.save()  # Save the changes to the Excel file

    df1= df.copy(deep=True)
    df.drop(df.index,inplace=True)
    df.drop(df.index,inplace=True)
    return not (df1.empty)



