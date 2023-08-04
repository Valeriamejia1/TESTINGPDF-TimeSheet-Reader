class outputAPI:
    def __init__(self, df, delete_sched):
        self.dataframe = df
        self.delete_sched = delete_sched

    def modifyDataPaycodes(self):
        # Remove rows with PayCodes "SHDIF" and "LCUP"
        condition = (self.dataframe['PAYCODE'] == "SHDIF") | (self.dataframe['PAYCODE'] == "LCUP") | (self.dataframe['PAYCODE'] == "LUNCH") | (self.dataframe['PAYCODE'] == "SCHED ORIENT")
        self.dataframe = self.dataframe.drop(self.dataframe[condition].index)

        if self.delete_sched == True:
            condition = (self.dataframe['PAYCODE'] == "SCHED")
            self.dataframe = self.dataframe.drop(self.dataframe[condition].index)
        else:
            uniqueNames = self.dataframe['NAME'].unique()  # Get unique nurse names
            for name in uniqueNames:
                nursedf = self.dataframe[self.dataframe['NAME'] == name] # Filter by nurse name
                uniqueDates = nursedf['DATE'].unique() # Get unique dates for each nurse
                for date in uniqueDates:
                    datedf = nursedf[nursedf['DATE'] == date] # Filter by date

                    schedRows = datedf[datedf['PAYCODE'] == 'SCHED'] # Filter rows with PayCode "SCHED"

                    regRows = datedf[datedf['PAYCODE'] == 'REG'] # Filter rows with PayCode "REG"
    
                    orienRows = datedf[datedf['PAYCODE'] == 'ORIEN'] # Filter rows with PayCode "ORIEN"

                    for index, rowSched in schedRows.iterrows():
                        schedHours = rowSched['HOURS']

                        matchingRegRows = regRows[regRows['HOURS'] == schedHours] # Find "REG" rows that match the hours of the "SCHED" row

                        if matchingRegRows.empty:
                            matchingOrienRows = orienRows[orienRows['HOURS'] == schedHours] # Find "ORIEN" rows that match the hours of the "SCHED" row
                            if matchingOrienRows.empty:
                                continue  # If no matching "REG" or "ORIEN" row is found, move to the next "SCHED" row

                        self.dataframe.drop(index, inplace=True) # Remove the "SCHED" row


        #print(self.dataframe)
        return self.dataframe
    
    def RemoveDuplicates(self):
        uniqueNames = self.dataframe['NAME'].unique()

        for name in uniqueNames:
            nursedf = self.dataframe[self.dataframe['NAME'] == name]  # Filter by nurse name
            uniqueDates = nursedf['DATE'].unique()  # Get unique dates for each nurse

            for date in uniqueDates:
                datedf = nursedf[nursedf['DATE'] == date]

                # Identify rows with PayCode "CBACK" and matching hours
                cback_rows = datedf[datedf['PAYCODE'] == 'CBACK']

                # Identify rows with PayCode "REG" and matching hours
                reg_rows = datedf[datedf['PAYCODE'] == 'REG']

                if len(cback_rows) > 0 and len(reg_rows) > 0:
                    # Find rows with matching hours in both PayCodes
                    common_hours = set(cback_rows['HOURS']).intersection(set(reg_rows['HOURS']))

                    # Remove the rows with PayCode "REG" and matching hours
                    for hours in common_hours:
                        reg_index = reg_rows[reg_rows['HOURS'] == hours].index
                        datedf = datedf.drop(reg_index)

                # Identify duplicate rows with PayCode "CALL"
                duplicated_rows = datedf[datedf.duplicated(subset=['PAYCODE'], keep=False) & (datedf['PAYCODE'] == 'CALL')]

                if len(duplicated_rows) > 1:
                    # Remove the first duplicate row
                    duplicated_index = duplicated_rows.index[0]
                    datedf = datedf.drop(duplicated_index)

                duplicated_rows2 = datedf[datedf.duplicated(subset=['PAYCODE'], keep=False) & (datedf['PAYCODE'] == 'PTONOP')]

                if len(duplicated_rows2) > 1:
                    # Remove the first duplicate row
                    duplicated_index = duplicated_rows2.index[0]
                    datedf = datedf.drop(duplicated_index)

                # Update the original DataFrame with the modified data
                self.dataframe.loc[(self.dataframe['NAME'] == name) & (self.dataframe['DATE'] == date)] = datedf

        self.dataframe = self.dataframe.dropna(subset=['PAYCODE'])  # Remove rows with empty PAYCODE

        return self.dataframe


    def checkInOut(self, date, inHour, outHour):
        # This function receives the date, the in hour, and the exit hour. It calculates a day change
        from datetime import datetime, timedelta
        import re

        self.dataframe['ENDDTM'] = self.dataframe['ENDDTM'].fillna('')
        if outHour == "":
            day= ""
        else:
            format = "%H:%M"
            h1 = datetime.strptime(inHour, format)
            h2 = datetime.strptime(outHour, format)
            result = h2 - h1 #Get the total hours worked
            
            result= str(result).split(':')
            result[0] = re.sub(r'(\-|\+)\d{1,2}\s\w+\,\s', "", result[0]) #Removes the "-1 day," format

            inHour = datetime.strptime(date +" "+ inHour, "%m/%d/%Y %H:%M")
            day = inHour + timedelta(hours=int(result[0]), minutes=int(result[1]), seconds=int(result[2])) #Calculate the exit date and time, performing a sum of the difference of hours with the in hour
            day= day.strftime("%m/%d/%Y %H:%M")
        return day
    

    def iterateDF(self):
        # This function iterate over the dataframe rows
        for index, row in self.dataframe.iterrows():
            dateHour = str(self.dataframe.at[index, 'STARTDTM']).split()
            out = self.dataframe.at[index, 'ENDDTM']
            outDateTime = self.checkInOut(dateHour[0], dateHour[1], out)
            self.dataframe.at[index, 'ENDDTM'] = outDateTime
        return self.dataframe
    
        

