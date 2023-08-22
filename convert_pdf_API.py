from Modules.pdfAPI import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/API/Mattox, Kyle.pdf", "QA/API/Dawson, Kathleen.pdf"] 
reportType = "API Format"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None
    delete_sched = True
      # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, delete_sched, from_convert_pdf_API=False)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    delete_sched = False
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, delete_sched, from_convert_pdf_API=False)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")
