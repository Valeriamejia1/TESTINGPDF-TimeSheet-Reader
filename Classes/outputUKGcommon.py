#Needed libraries
import json
import re  # regex
from datetime import datetime

class logUKGcommon:

    global regexlist

    def __init__(self, df, arrayCodeGL, arrayGLword, nurse):
        self.dataframe = df
        self.arrayGLword = arrayGLword
        self.arrayCodeGL = arrayCodeGL
        self.nurse = nurse
        self.codeGL = ""
        self.codeGLAux = ""
 
    def readJsonRegex():
    # read json file "Regex.json" that holds the regex that are required
        try:
            with open("Regex.json", "r") as read_file:
                data2 = json.load(read_file)           #Import the regex entries to a dictionary
                return data2                           #Return the dictionary
        except:
            print("Something happenned reading Json file")

    regexlist= readJsonRegex()

    def getDate(line, reportType):
        lineAux= re.search(regexlist[reportType]["getDate"], str(line)) #Search a match on the value by using a regex to get the date
        dateAux = lineAux.group(0)  #Get only the needed value from the match
        date = datetime.strptime(dateAux, "%Y-%m-%d").strftime("%m/%d/%Y")  #change date format
        return date
    
    def getNurse(line, reportType):
        nameAux= re.search(regexlist[reportType]["getEMPL"], str(line))   #Search a match on the value by using a regex to get the nurse name
        name= nameAux.group(0)                               #Get only the needed value from the match
        name= re.sub(r':\s', "", nameAux.group(0))            #Remove the blank space and the : from the name        
        return name    

    def getPaycode(line, reportType):
        paycodeAux = re.search(regexlist[reportType]["searchPaycode"], str(line)) #Search a match on the value by using a regex to get the paycode
        paycode = paycodeAux.group(0)  #Get only the needed value from the match
        return paycode
    
    def getInHour(line, reportType, date):
        lineAux = re.search(regexlist[reportType]["getInhour"], str(line)) #Search a match on the value by using a regex to get the time in
        inHourAux = lineAux.group()  #Get only the needed value from the match
        inHour = datetime.strptime(inHourAux, "%I:%M %p").strftime("%H:%M") #change hour format to 24H
        inHour = date + " " + inHour #concatenate 
        return inHour
    
    def getHours(line, reportType):
        hoursAux = re.search(regexlist[reportType]["getHours"], str(line)) #Search a match on the value by using a regex to get the hours
        hours = hoursAux.group(0) #Get only the needed value from the match
        return hours
    
    def getComments(line, comment, reportType):
        commentAux = line
        if re.search(r'\d{4}\-\d{4}\-\d{4,5}', line):
            commentAux = re.sub(r'\sCC:$', "", line)  #remove CC: from the variable line
        if re.search(r'^[^:\n]*\/[^:\n]*|^RN|^CN', line):
            commentAux = re.sub(r'\s', "", commentAux) #remove space blanks
            comment= comment + commentAux  #concatenate
        else: 
            comment= comment + " | " +commentAux  #concatenate
        return comment

    def getGLword(glWordAux):
        glWordAux2 = re.sub(r'\sCC', "", glWordAux) #remove CC from the variable glWordAux
        if re.search(r'Page\s+\d+\s+of\s+\d+', str(glWordAux2)):
            glWordAux2 = re.sub(r'Page\s+\d+\s+of\s+\d+', "", glWordAux2)
        glWord = re.sub(r'\s', "", glWordAux2) #Remove space blanks
        return glWord
    
    def getCodeGL(codeGLAux):
        codeGL = re.sub(r'\:', "", codeGLAux) #remove ":" from the variable codeGLAux
        return codeGL
    
    def getPrimaryJob(line, reportType, primaryJob):
        primaryJobAux = re.search(regexlist[reportType]["getPrimaryJob"], str(line)) #Search a match on the value by using a regex to get the primary job
        primaryJobAux2 =primaryJobAux.group(0) #Get only the needed value from the match
        if re.search(r'(\d{1,2}\/\d{1,2}\/\d{2})\s+(.*)', primaryJobAux2): #Search if have a date or more information in the variable witch is not needed
            primaryJobAux2 = re.sub(r'(\d{1,2}\/\d{1,2}\/\d{2})\s+(.*)', "", primaryJobAux2) #remove this information
        if re.search(r'\s', primaryJobAux2): #search if have space blanks
            primaryJobAux2 = re.sub(r'\s', "", primaryJobAux2) #remove space blanks
        primaryJob = primaryJob + primaryJobAux2 #concatenate
        return primaryJob
    
    def getComparationGl(self):
        #Filter by nurse
        dfNurse = self.dataframe[self.dataframe['NAME'] == self.nurse]
        # Iterate over unique dates in the nurse's DataFrame
        for date in dfNurse['DATE'].unique():
        # Filter the nurse's DataFrame for the current date
            dfDate = dfNurse[dfNurse['DATE'] == date]
            # Iterate over rows in the filtered DataFrame for the current date
            for index, row in dfDate.iterrows():
                # Extract 'Comments' and 'PrimaryJob' from the current row
                comment = row['Comments']
                primaryJob = row['PrimaryJob']
                
                # Initialize code variables
                self.codeGL = ""
                self.codeGLAux = ""
                
                # Check if 'Comments' is empty
                if comment.strip() == '':
                    # If 'PrimaryJob' is not empty, try to find a code
                    if primaryJob.strip() != "":
                        # Iterate through predefined words and codes
                        for i, glWord in enumerate(self.arrayGLword):
                            if primaryJob.strip() == glWord:
                                self.codeGL = self.arrayCodeGL[i]
                                break
                    else:
                        self.codeGL = ''
                else:
                    # Check for a pattern of digits separated by hyphens in 'Comments'
                    if re.search(r'\d{4}\-\d{4}\-\d{4,5}', comment):
                        comment = re.search(r'\d{4}\-\d{4}\-\d{4,5}', comment) 
                        self.codeGL = comment.group(0)
                    else:
                        # Check for a specific pattern in 'Comments'
                        if re.search(r'[^:\n]*\/(?:[^:\n]*\/)*(?=[^:\n]*)\w{2}', comment):
                            comment = re.search(r'[^:\n]*\/(?:[^:\n]*\/)*(?=[^:\n]*)\w{2}', comment) 
                            comment = comment.group(0)
                            # Search for a matching code in the predefined words and codes
                            for i, glWord in enumerate(self.arrayGLword):
                                if comment.strip() == glWord:
                                    self.codeGL = self.arrayCodeGL[i]
                                    break
                                else:
                                    # If no match is found, assign an empty code
                                    self.codeGL = ''
                        else:
                            if primaryJob.strip() != "":
                            # Iterate through predefined words and codes
                                for i, glWord in enumerate(self.arrayGLword):
                                    if primaryJob.strip() == glWord:
                                        self.codeGL = self.arrayCodeGL[i]
                                        break
                            else:
                                self.codeGL = ''
                
                # Search for a matching code for 'PrimaryJob' and assign it to self.codeGLAux
                for i, glWord in enumerate(self.arrayGLword):
                    if primaryJob.strip() == glWord:
                        self.codeGLAux = self.arrayCodeGL[i]
                        break
                
                # Update the 'GLCODE' and 'PrimaryJob' columns in the DataFrame
                self.dataframe.loc[index, 'GLCODE'] = self.codeGL
                self.dataframe.loc[index, 'PrimaryJob'] = primaryJob + "|" + self.codeGLAux

        # Clear arrays for codes and words
        self.arrayCodeGL.clear()
        self.arrayGLword.clear()

        # Return the updated DataFrame
        return self.dataframe

        