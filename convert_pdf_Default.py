from Modules.pdfDefault import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/Default/Ewing PPE 3.11.23.pdf", "QA/Default/Qualivis Kronos Time Detail Report.WE 03.04.2023.pdf"] 
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
