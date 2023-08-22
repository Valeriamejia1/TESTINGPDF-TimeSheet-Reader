import os
import sys

# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre

# Ahora podemos importar el módulo pdfAPI
from Modules.pdfDefault import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/PDF/Default/Ewing PPE 3.11.23.pdf", "QA/PDF/Default/Agency Timecards 3.12-3.25.pdf"] 
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
