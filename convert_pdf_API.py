from Modules.pdfAPI import main
import os

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/API/Dawson, Kathleen.pdf", "QA/API/Mattox, Kyle.pdf"]  # Reemplaza con las rutas a tus archivos PDF

reportType = "API Format"  # Reemplaza con el tipo de informe correcto
delete_sched = True  # Cambia esto según tus necesidades

for pdf_file in pdf_files:
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response=True, file=[pdf_file], reportType=reportType, delete_sched=delete_sched)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")

    # Obtener el nombre base del archivo PDF sin la extensión
    pdf_file_name = os.path.splitext(os.path.basename(pdf_file))[0]

   
delete_sched = False  # Cambia esto según tus necesidades

for pdf_file in pdf_files:
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response=True, file=[pdf_file], reportType=reportType, delete_sched=delete_sched)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")

    # Obtener el nombre base del archivo PDF sin la extensión
    pdf_file_name = os.path.splitext(os.path.basename(pdf_file))[0]


