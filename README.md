# ProcesoPDFs

Este proyecto procesa archivos PDF para extraer información específica (CUFE) y almacenarla en una base de datos SQLite.

## Requisitos técnicos

- Python 3.7 o superior
- Bibliotecas de Python:
  - PyPDF2
  - sqlite3 (incluido en la biblioteca estándar de Python)

## Instalación

1. Clona este repositorio o descarga los archivos del proyecto.

2. Instala las dependencias necesarias:
bash
pip install PyPDF2

## Uso

1. Coloca los archivos PDF que deseas procesar en el mismo directorio que el script `extract_cufe.py`.

2. Ejecuta el script:
bash
python extract_cufe.py

3. El script procesará todos los archivos PDF en el directorio, extraerá la información requerida y la almacenará en una base de datos SQLite llamada `pdf_info.db`.

4. Al finalizar, el script mostrará un resumen de los registros almacenados en la base de datos.

## Estructura de la base de datos

La base de datos SQLite `pdf_info.db` contiene una tabla llamada `pdf_info` con la siguiente estructura:

- `file_name`: TEXT (nombre del archivo PDF)
- `num_pages`: INTEGER (número de páginas del PDF)
- `cufe`: TEXT (Código Único de Factura Electrónica extraído)
- `file_size`: REAL (tamaño del archivo en KB)

## Notas adicionales

- El script utiliza multiprocesamiento para mejorar el rendimiento al procesar múltiples archivos PDF.
- Asegúrate de que los archivos PDF no estén encriptados y tengas los permisos necesarios para leerlos.
- Si encuentras algún error, verifica los permisos de los archivos y asegúrate de que los PDF sean válidos y legibles.
