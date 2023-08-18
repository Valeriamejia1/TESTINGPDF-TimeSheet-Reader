from Modules.pdfPaylocity import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["PDF/Haynie, Nathan.pdf", "PDF/Hobbs, Brandy.pdf"]
reportType = "Paylocity"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")
