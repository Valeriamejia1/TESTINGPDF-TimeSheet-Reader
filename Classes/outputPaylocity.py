import json
import re
import PyPDF2
import pandas as pd
from datetime import datetime

class outputPaylocity:

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
        # Get the current date and time using the datetime.now() function.
        current = datetime.now()
        # Format the current time to a string in the format "YYYY-MM-DD HH:MM:SS".
        currentTimeAux = str(current.strftime("%Y-%m-%d %H:%M:%S"))
        # Remove colons (:) from the time portion to get a string like "YYYY-MM-DD HHMMSS".
        currentTime = currentTimeAux.replace(":", "")
        # Return the formatted current date and time.
        return currentTime

    def getName(line, reportType):
        # Search for the name pattern in the given line using the regex from regexlist
        nameAux = re.search(regexlist[reportType]["getName"], str(line))
        # Extract the matched name group (the whole match) from the regex search result
        name = nameAux.group(0)
        # Return the extracted name
        return name

    def getDate(line, reportType):
        # Search for the date pattern in the given line using the regex from regexlist
        dateAux = re.search(regexlist[reportType]["getDate"], str(line))
        # Extract the matched date group (the whole match) from the regex search result
        date = dateAux.group(0)
        # Return the extracted date
        return date

    def getInHour(line, reportType):
        # Search for the inHour pattern in the given line using the regex from regexlist
        inHourAux = re.search(regexlist[reportType]["getInHour"], str(line))
        # Extract the matched inHour group (the whole match) from the regex search result
        inHour = inHourAux.group(0)
        # Convert the inHour format from "%I:%M%p"
        InHour = datetime.strptime(inHour, "%I:%M%p").strftime("%H:%M")
        # Return the inHour in 24-hour format
        return InHour

    def getHours(line, reportType):
        # Search for the hours pattern in the given line using the regex from regexlist
        hourAux = re.search(regexlist[reportType]["getHours"], str(line))
        # Extract the matched hours group (the whole match) from the regex search result
        hour = hourAux.group(0)
        # Return the extracted hours
        return hour

    def getPayType(line, reportType):
        # Search for the payType pattern in the given line using the regex from regexlist
        payTypeAux = re.search(regexlist[reportType]["searchPayType"], str(line))
        # Extract the matched payType group (the whole match) from the regex search result
        payType = payTypeAux.group(0)
        # Return the extracted payType
        return payType

    def getGLCode(line, reportType):
        # Search for the GL code pattern in the given line using the regex from regexlist
        glcodeAux = re.search(regexlist[reportType]["getGL"], str(line))
        # Extract the matched GL code group (the whole match) from the regex search result
        glcode = glcodeAux.group(0)
        # Return the extracted GL code
        return glcode



