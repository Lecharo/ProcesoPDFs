import os
import re
import sqlite3
import PyPDF2
from multiprocessing import Pool, cpu_count

def extract_cufe(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        cufe_pattern = r'\b([0-9a-fA-F]\n*){95,100}\b'
        match = re.search(cufe_pattern, text)
        cufe = match.group(0) if match else None
        
        file_size = os.path.getsize(file_path) / 1024  # Size in KB
        
        return file_path, num_pages, cufe, file_size
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return file_path, None, None, None

def create_database():
    conn = sqlite3.connect('pdf_info.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdf_info (
        file_name TEXT PRIMARY KEY,
        num_pages INTEGER,
        cufe TEXT,
        file_size REAL
    )
    ''')
    conn.commit()
    conn.close()

def insert_record(record):
    conn = sqlite3.connect('pdf_info.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO pdf_info (file_name, num_pages, cufe, file_size)
    VALUES (?, ?, ?, ?)
    ''', record)
    conn.commit()
    conn.close()

def show_records():
    conn = sqlite3.connect('pdf_info.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pdf_info")
    records = cursor.fetchall()
    
    print("\nRegistros en la base de datos:")
    print("-" * 30)
    for record in records:
        print(f"Archivo: {record[0]}")
        print(f"Páginas: {record[1]}")
        print(f"CUFE: {record[2]}")
        print(f"Tamaño (KB): {record[3]:.2f}")
        print("-" * 30)
    
    conn.close()

def main():
    create_database()

    pdf_directory = '.'  # Current directory, change if needed
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) 
                 if f.lower().endswith('.pdf')]

    # Use all available CPU cores
    num_processes = cpu_count()
    
    with Pool(num_processes) as pool:
        results = pool.map(extract_cufe, pdf_files)
    
    for result in results:
        if result[1] is not None:  # Check if processing was successful
            insert_record((os.path.basename(result[0]), *result[1:]))
    
    show_records()

if __name__ == "__main__":
    main()