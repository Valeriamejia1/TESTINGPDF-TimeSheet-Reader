from Modules.pdfPaylocity import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/Paylocity/Binder1.pdf", "QA/Paylocity/Master Timecard Detail-Josh Barker (7).pdf"]
reportType = "Paylocity"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, from_convert_pdf_Paylocity=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")