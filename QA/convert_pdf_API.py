import os
import sys



# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre

# Ahora podemos importar el módulo pdfAPI
from Modules.pdfAPI import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/PDF/API/Dawson, Kathleen.pdf", 
             "QA/PDF/API/Delta Health 4.15.23.pdf", 
             #"QA/PDF/API/Hannibal 4.15.23.pdf"             , pega jenkins
             "QA/PDF/API/Mattox, Kyle.pdf", 
             #"QA/PDF/API/TMMC W.E. 4.22.pdf"               , pega jenkins
             "QA/PDF/API/API Empty.pdf",
             "QA/PDF/API/Pages from 1-130 TMMC W.E. 4.22.pdf",
             "QA/PDF/API/Pages from 131-264 TMMC W.E. 4.22-5.pdf",
             "QA/PDF/API/Pages from 265-398TMMC W.E. 4.22-6.pdf",
             "QA/PDF/API/Pages from 359-517 TMMC W.E. 4.22.pdf",
             "QA/PDF/API/Pages from 1-95 Hannibal 4.15.23.pdf",
             "QA/PDF/API/Pages from 1-95 Hannibal 4.15.23.pdf",
             "QA/PDF/API/Pages from 96-191 Hannibal 4.15.23-2.pdf"

             ]  

reportType = "API Format"  # Reemplaza con el tipo de informe correcto

for pdf_file in pdf_files:

    delete_sched = True  # Cambia esto según tus necesidades

    # Llamar a la función main para convertir el PDF en Excel
    result = main(response=True, file=[pdf_file], reportType=reportType, delete_sched=delete_sched, from_convert_pdf_API=True)
    
    if result:
        print(f"La conversión del archivo {pdf_file} SCHED se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")
   


for pdf_file in pdf_files:

    delete_sched = False  # Cambia esto según tus necesidades

    # Llamar a la función main para convertir el PDF en Excel
    result = main(response=True, file=[pdf_file], reportType=reportType, delete_sched=delete_sched, from_convert_pdf_API=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")




