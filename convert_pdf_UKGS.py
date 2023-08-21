from Modules.pdfUKGsimplified import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/UKG_Simplified/Qualvis TimeSheets 2023-06-03.pdf", "QA/UKG_Simplified/TimeDetailsSorted_KEVCOL.pdf"] 
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