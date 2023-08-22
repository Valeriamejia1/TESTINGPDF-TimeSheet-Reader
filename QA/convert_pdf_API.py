import os
import sys

# Obtiene el directorio base del script actual (donde se encuentra QA)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Agrega el directorio que contiene "Modules" al PATH
sys.path.append(os.path.join(base_dir, ".."))  # ".." significa el directorio padre

# Ahora podemos importar el módulo pdfAPI
from Modules.pdfAPI import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/PDF\API/Dawson, Kathleen.pdf", "QA/PDF/API\Mattox, Kyle.pdf"]  # Reemplaza con las rutas a tus archivos PDF

reportType = "API Format"  # Reemplaza con el tipo de informe correcto
delete_sched = True  # Cambia esto según tus necesidades

for pdf_file in pdf_files:
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response=True, file=[pdf_file], reportType=reportType, delete_sched=delete_sched)

    # Obtener el nombre base del archivo PDF sin la extensión
    pdf_file_name = os.path.splitext(os.path.basename(pdf_file))[0]

   
delete_sched = False  # Cambia esto según tus necesidades

for pdf_file in pdf_files:
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response=True, file=[pdf_file], reportType=reportType, delete_sched=delete_sched)

    # Obtener el nombre base del archivo PDF sin la extensión
    pdf_file_name = os.path.splitext(os.path.basename(pdf_file))[0]


