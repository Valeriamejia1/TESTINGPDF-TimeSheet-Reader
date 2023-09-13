import os
import sys
# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre


# Ahora podemos importar el módulo UKG Simplified

from Modules.pdfUKGKronos import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/PDF/UKG_Kronos/Qualivis Time report PPE 062423.pdf",
             "QA/PDF/UKG_Kronos/UKG Kronos empty.pdf"] 
reportType = "UKG Kronos"

for file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, file, reportType, from_convert_pdf_UKGK=True)

    if result:
        print(f"The conversion File {file} was successful.")
    else:
        print(f"The conversion File {file} failed or no data was found.")