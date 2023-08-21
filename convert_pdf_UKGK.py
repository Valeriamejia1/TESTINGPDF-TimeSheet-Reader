from Modules.pdfUKGKronos import main

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/UKG_Kronos/Qualivis Time report PPE 062423.pdf"] 
reportType = "UKG Kronos"

for file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, file, reportType, from_convert_pdf_UKGK=True)

    if result:
        print(f"La conversión del archivo {file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {file} falló o no se encontraron datos.")