from ast import Not
import tabula as tb
import re
from datetime import datetime

class pdftest:
    def __init__(self,filename,reportType, regexlist):
        """
        Class that test the file contents are extracted properly. Recieves file name path to test.
        """
        self.filename = filename
        #Read a json file with the regex values and import them to a dictionary    
        self.regexlist= regexlist
        self.reportType= reportType
        self.count_pages = 0
        self.count_nurses = 0
        self.count_nurses_data = 0
        self.count_empty_nurses = 0

    def is_str_line_empty(self,list):
        """
        Function that return the list in a single string. This is useful to evaluate if list only has white spaces and no data.
        """
        value = "".join(map(str,list))
        if value == "":
            return True
        else:
            return False
    
    def write_to_file(self,output_file,row,is_comment,line,name):
        """Write to output file the value sent. It writes with new line or not in case the value are comments."""
        if is_comment:
            with open(output_file,"a") as file_obj:
                for j, value in row.items():        #Iterate on the row values
                    if value != '':
                        line += str(value)
                file_obj.write(line)
        else:
            with open(output_file,"a") as file_obj:
                line += name + '|'
                for j, value in row.items():        #Iterate on the row values
                    if value != '':
                        line += str(value) + '|'
                file_obj.write(line)
    
    def audit_report(self):
        """
        Audit report to process getting the number the lines and nurses that should be in the output file.
        Recieves the file to process
        """
        table= tb.read_pdf(self.filename, pages='all',stream= True, lattice=False, silent=False, guess=False, multiple_tables=True, pandas_options={'header': None}, java_options="-Dfile.encoding=UTF8")
        #java_options="-Dfile.encoding=UTF8")
        
        nameVerif= ""                                   #This variable is used to verify if the next page is the same nurse
        output_file = self.getFileName()
        file_obj = open(output_file,"w")
        #Loop over the data
        for item in table:                              #Iterate on the list of DataFrames
            self.count_pages += 1
            search_data = False
            for i, row in item.iterrows():
                row = row.fillna('')                    #Replace the NaN values to blank spaces in the row
                first_column_data = row[0]
                if self.is_str_line_empty(row) == False:
                    if re.search(self.regexlist[self.reportType]["searchEmp"], str(first_column_data)):
                        name= self.getNurse(first_column_data)      #Call the function to get the nurse name and save it to an variable
                        name = str(name)
                        name = name.strip()
                        if nameVerif != name:
                            self.count_nurses += 1
                        nameVerif = name
                    elif re.search('Xfr\/Move:', str(first_column_data)):
                        search_data = True
                    elif re.search(self.regexlist[self.reportType]["brakeLoop"], str(first_column_data)):
                        search_data = False
                    elif search_data:
                        if re.search(self.regexlist[self.reportType]["searchDateTime"], str(first_column_data)):
                            line = '\n'
                            self.count_nurses_data += 1
                            comment_flag = False
                        else:
                            line = '|'
                            comment_flag = True
                        self.write_to_file(output_file,row,comment_flag,line,name)
        print(f'Nurses # {self.count_nurses}')
        print(f'Number of rows {self.count_nurses_data}')
        return self.count_pages

    def getNurse(self,value):
        nameAux= re.search(self.regexlist[self.reportType]["getEmp"], str(value))  #Search a match on the value by using a regex to get the nurse name
        name= nameAux.group(0)                               #Get only the needed value from the match                               
        return name
    
    def getCurrentDateTime(self):
        """
        Return in ext the current date/time in format mm-dd-yy hhmm
        """ 
        now = datetime.now().strftime("%m-%d-%Y %H%M%S")
        return now

    def getFileName(self):
        """ 
        Get the file path from json and add the curren file generated.
        """ 
        fileName = "Audit_" + self.getCurrentDateTime() + ".csv"
        filePath = self.regexlist[self.reportType]["output_file"]
        return filePath + fileName
