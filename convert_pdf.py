from Modules.pdfPaylocity import main
import os

# Lista de nombres de archivos PDF a convertir
pdf_files = ["PDF/Haynie, Nathan.pdf", "PDF/Hobbs, Brandy.pdf"]
reportType = "Paylocity"

for pdf_file in pdf_files:
    # Definir los argumentos necesarios para la función main
    response = None  # Puedes proporcionar el valor adecuado si es necesario

    # Obtener el nombre base del archivo PDF (sin la extensión)
    pdf_basename = os.path.basename(pdf_file)
    pdf_name_without_extension = os.path.splitext(pdf_basename)[0]

    # Nombre del archivo de Excel con la misma base que el archivo PDF
    excel_filename = f"{pdf_name_without_extension}.xlsx"

    # Llamar a la función main para convertir el PDF en Excel
    result = main(response, pdf_file, reportType, excel_filename)

    if result:
        print(f"La conversión del archivo {pdf_file} se realizó con éxito.")
    else:
        print(f"La conversión del archivo {pdf_file} falló o no se encontraron datos.")
