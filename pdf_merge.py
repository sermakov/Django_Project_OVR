import os
from PyPDF2 import PdfMerger
import argparse

def merge_pdfs_in_directory(directory, output_filename='Сборник практических заданий по Django (ОВР).pdf'):
    """
    Объединяет все PDF-файлы в указанной директории в один PDF-файл.

    :param directory: Путь к директории с PDF-файлами.
    :param output_filename: Имя итогового PDF-файла.
    """
    # Получаем список всех PDF-файлов в директории
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"В директории '{directory}' не найдено PDF-файлов для объединения.")
        return
    
    # Сортируем файлы по имени для предсказуемого порядка
    pdf_files.sort()
    
    merger = PdfMerger()
    
    print("Начинаем объединение следующих файлов:")
    for pdf in pdf_files:
        path = os.path.join(directory, pdf)
        merger.append(path)
        print(f" - {pdf}")
    
    # Путь к итоговому файлу
    output_path = os.path.join(directory, output_filename)
    
    # Записываем объединенный PDF
    merger.write(output_path)
    merger.close()
    
    print(f"\nОбъединение завершено. Итоговый файл сохранен как: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Объединение всех PDF-файлов в указанной директории в один PDF-файл.")
    parser.add_argument('directory', help='Путь к директории с PDF-файлами.')
    parser.add_argument('-o', '--output', default='merged.pdf', help='Имя итогового PDF-файла (по умолчанию: merged.pdf).')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Ошибка: Директория '{args.directory}' не существует.")
        return
    
    merge_pdfs_in_directory(args.directory, args.output)

if __name__ == "__main__":
    main()