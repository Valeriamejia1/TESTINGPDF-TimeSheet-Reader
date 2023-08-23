import os
import sys
# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre


# Ahora podemos importar el módulo UKG Simplified

from Modules.pdfUKGsimplified import main
# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA\PDF/UKG_Simplified/TimeDetailsSorted_KEVCOL.pdf", 
             "QA/PDF/UKG_Simplified/Qualvis TimeSheets 2023-06-03.pdf",
             "QA/PDF/UKG_Simplified/UKG Simplified Empty.pdf"]
reportType = "UKG Simplified"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, from_convert_pdf_UKGS=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")