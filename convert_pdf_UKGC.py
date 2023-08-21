from Modules.pdfUKGcommon import main


# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/UKG_Common/martin b.pdf", "QA/UKG_Common/Martin Holiday Shifts 7.3 to 7.5.23.pdf"]
reportType = "UKG Common"

for file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, file, reportType, from_convert_pdf_UKGC=True)

    if result:
        print(f"La conversión del archivo {file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {file} falló o no se encontraron datos.")