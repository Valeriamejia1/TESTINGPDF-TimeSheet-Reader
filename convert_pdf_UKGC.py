from Modules.pdfUKGcommon import pdfUKGcommon

# Lista de nombres de archivos PDF a convertir
pdf_files = ["QA/UKG_Common/martin b.pdf", "QA/UKG_Common/Martin ppe 4.22.23.pdf"]  # Reemplaza con las rutas correctas
reportType = "UKG Common"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario
    
    # Llamar a la función main para convertir el PDF en Excel
    result = pdfUKGcommon.main(response, pdf_file, reportType,from_convert_pdf_UKGC=True)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")

