from Modules.pdfPaylocity import main

# Definir los argumentos necesarios para la función main
response = None  # Puedes proporcionar el valor adecuado si es necesario

files = ["PDF\Haynie, Nathan.pdf", "PDF\Hobbs, Brandy.pdf"]

reportType = "Paylocity"

# Iterar sobre la lista de archivos y llamar a la función main para cada archivo
for file in files:
    result = main(response, file, reportType)
    if result:
        print(f"La conversión para el archivo '{file}' se realizó con éxito.")
    else:
        print(f"La conversión para el archivo '{file}' falló o no se encontraron datos.")
