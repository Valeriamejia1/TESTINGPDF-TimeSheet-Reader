import os
import pandas as pd
from Modules.pdfPaylocity import main

response = None
files = ["PDF/Haynie, Nathan.pdf", "PDF/Hobbs, Brandy.pdf"]
reportType = "Paylocity"

for file in files:
    result = main(response, file, reportType)
    if result:
        # Obtener la ruta al workspace de Jenkins
        workspace_path = os.environ.get('WORKSPACE', '')

        # Crear la ruta completa para el archivo Excel en el workspace
        excel_file_path = os.path.join(workspace_path, f'{file.split("/")[-1]}.xlsx')

        # Guardar el archivo Excel en la ubicación del workspace
        result.to_excel(excel_file_path, index=False)

        print(f"La conversión para el archivo '{file}' se realizó con éxito.")
    else:
        print(f"La conversión para el archivo '{file}' falló o no se encontraron datos.")

