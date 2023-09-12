import os
import sys

# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre

# Ahora podemos importar el módulo pdfAPI
from Modules.pdfDefault import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/PDF/Default/06-11.pdf",                                     #No se cae
             "QA/PDF/Default/1690203601050_1994364726.pdf",
             #"QA/PDF/Default/1690808400472_1671940182.pdf",
             #"QA/PDF/Default/Aya- WE 8.28.22.pdf",                          Se cae Jenkins
             #"QA/PDF/Default/Combined File.pdf",                            Se cae jenkins
             #"QA/PDF/Default/Kronos Timecards TC 07-30-22.pdf",
             #"QA/PDF/Default/Scripps Approved Kronos we 6.25.22.pdf",
             #"QA/PDF/Default/Time Detail_100822-102122.pdf",                Se cae jenkins
             #"QA/PDF/Default/Time Detail_July152022.pdf",                   Se cae jenkins
             "QA/PDF/Default/time weston.pdf",                               #No se cae  
             "QA/PDF/Default/Default Empty.pdf"                              #No se cae  
             ] 


reportType = "Default"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = True  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, from_convert_pdf_Default=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = False  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, from_convert_pdf_Default=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")