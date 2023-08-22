import os
import sys

# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre

from Modules.pdfUKGcommon import pdfUKGcommon

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/PDF/API/Dawson, Kathleen.pdf", "QA/PDF/API/Mattox, Kyle.pdf"]  # Reemplaza con las rutas correctas
reportType = "UKG Common"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = pdfUKGcommon.main(response, pdf_file, reportType,from_convert_pdf_UKGC=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")

