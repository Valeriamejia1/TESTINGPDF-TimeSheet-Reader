from ast import Not
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from functools import partial
import re
import Modules.pdfDefault as pdfDefault
import Modules.pdfAPI as pdfAPI
import Modules.pdfUKGcommon as pdfUKGcommon
import Modules.pdfUKGsimplified as pdfUKGSimplified
import Modules.pdfUKGKronos as pdfUKGKronos
import Modules.pdfPaylocity as pdfPaylocity

class windowshandler:
    def __init__(self, title, geometry = '600x400+50+50'):
        """
        Create a new windows with default size if is not given with a title.
        """
        self.title = title
        self.file_to_process = ''
        self.convert_dates = False
        self.finish_process = False

        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(geometry)
        self.root.resizable(0,0)

        self.menu= StringVar()
        self.reportType = ''

        self.delete_sched = False


    def select_file (self,file_type, file_descriptor):
        """
        Function for command button to open a new file in a window
        """
        if self.reportType == '':
            showinfo("Report Type","Please select the report type.")
        else:
            #set up file type
            file_types = ((file_descriptor,file_type), ("all files","*.*"))
            #File selector window

            if self.reportType == "API Format":
                
                filename = fd.askopenfilenames(
                title='Open files',
                initialdir='/',
                filetypes=file_types)
            else:
                filename = fd.askopenfilename(
                    title='Open a file',
                    initialdir='/',
                    filetypes=file_types)

            #Validate pdf file
            if self.reportType == "API Format":
                for file in filename:
                    isPDF = re.search(".pdf",file)
                    if not isPDF:
                        isPDF= False
                        break
                response2 = askyesno("Delete SCHED Paycodes","Do you want to remove the SCHED shift? It implies that the PDF has a mix of different paycodes which will appear modified in the OutputData sheet.\n"
                            "Important: All the raw data will be in the RawData sheet.")
                self.delete_sched = response2
                self.label_convert_dates.config(text=f'Delete SCHED Paycodes? {self.delete_sched}')


            else:
                isPDF = re.search(".pdf",filename)

            try:
                if isPDF:
                    if self.reportType == "Default":
                        #Check wheter Dates need to be converted or not
                        response = askyesno("Convert Dates","Need to Convert Minutes in the PDF?")
                        self.convert_dates = response
                        self.label_convert_dates.config(text=f'Convert Dates? {self.convert_dates}')
                    self.file_to_process = filename
                    self.label_file_explorer.config(text=f'File to process:\n {filename}')
                else:
                    showinfo("PDF file","Please select a PDF file.")
            except Exception as e:
                showinfo("PDF file","Please select a PDF file.")


    def ChooseOption(self, arg):
        self.reportType = self.menu.get()
        #print(self.reportType)


    def open_file_dialog(self, file_type = '*.pdf', file_descriptor = 'PDF Files'):
        """
        Creates a button and open a file type.
        """

        #Version Label
        self.versionlbl = Label(self.root,
                            text = "V7.0",
                            fg = "black")
        self.versionlbl.pack(side= BOTTOM, anchor=SE)


        #Label File Selected
        self.label_file_explorer = Label(self.root,
                            text = "Select the report type and browse for a PDF File to Process",
                            width = 100, height = 2,
                            fg = "blue")
        self.label_file_explorer.pack()

        # Dropdown menu
        self.menu.set("Select Report Type")
        drop= OptionMenu(self.root, self.menu,"Default", "API Format", "UKG Common", "UKG Simplified", "UKG Kronos", "Paylocity", command=self.ChooseOption)
        drop.pack()

        # open button
        open_button = tk.Button(
            self.root,
            text='Open a File',
            command=partial(self.select_file, file_type, file_descriptor)
        )

        #Label to Indicated wheter or not convert dates
        self.label_convert_dates = Label(self.root,text = f'Convert Dates? {self.convert_dates}', width = 100, height = 2, fg = "blue")
        self.label_convert_dates.pack()
        open_button.pack()

        # Process button
        self.process_button = tk.Button(self.root,text="Process File",command=self.process_file_command)
        self.process_button.pack()
        self.root.mainloop()



    def process_file_command(self):
        """
        Main code to process file.
        """
        if self.file_to_process != '' and self.reportType != '':

            if self.reportType == "Default":
                self.finish_process = pdfDefault.main(self.convert_dates, self.file_to_process, self.reportType)
            elif self.reportType == "API Format":
                self.finish_process = pdfAPI.main(self.convert_dates, self.file_to_process,self.reportType, self.delete_sched)
            elif self.reportType == "UKG Common":
                self.finish_process = pdfUKGcommon.pdfUKGcommon.main(self.convert_dates, self.file_to_process,self.reportType)
            elif self.reportType == "UKG Simplified":
                self.finish_process = pdfUKGSimplified.main(self.convert_dates, self.file_to_process,self.reportType)
            elif self.reportType == "UKG Kronos":
                self.finish_process = pdfUKGKronos.main(self.convert_dates, self.file_to_process,self.reportType)
            elif self.reportType == "Paylocity":
                self.finish_process = pdfPaylocity.main(self.convert_dates, self.file_to_process,self.reportType)
            else:
                showinfo("Please select the report type")

            if self.finish_process:
                showinfo("Success","File Processed. Check Output Folder")
            else:
                showinfo("Error","Something happened, please try again or verify.")

