import csv # модуль чтения файлов
import os # модуль для работы с системой
import argparse # модуль для создания командных интерфейсов
from collections import defaultdict
from tabulate import tabulate # библиотека для постройки таблиц



def process_csv_files( csv_files = None ) -> tuple[dict, list]:
    """Обрабатывает CSV файлы из текущей директории или списка.
        Находит средние арифметические значения, сортирует на убывание.
    Arg:
        csv_files: указанные файлы формата .csv, если None ищет сам в текущей директории
    Return:
        sorted_result: пустой словарь или отсортированная таблица с параметрами из всех данных файлов
        first_header: заголовок столбца
    Raise:
        ValueError
        Exception: Ошибка чтения файла
    """

    country_gdp = defaultdict( list )
    first_header = None # заголовок

    # Если файлы не указаны — ищем все .csv
    if csv_files is None:
        folder_path = os.getcwd() # путь к нашей директории
        csv_files = [] # список ссылок на файлы
        for root, dirs, files in os.walk(folder_path): # ищет файлы в директории
            for filename in files:
                if filename.endswith( '.csv' ):
                    full_path = os.path.join( root, filename )
                    csv_files.append( full_path )

    for full_path in csv_files:
        print( f"Обрабатываем: {full_path}" )

        try: # обработка ошибок
            # читаем файл по строчно и записываем данные в простой словарь
            with open( full_path, 'r', newline='', encoding='utf-8' ) as csv_file:
                reader = csv.reader( csv_file )
                header = next(reader) # пропускаем заголовок

                if first_header is None:  # если нет заголовка то
                    first_header = header

                for row in reader:
                    if len( row ) >= 3:
                        country = row[0].strip()
                        try:
                            gdp = float( row[2].strip() )
                            country_gdp[country].append(gdp)

                        except ValueError:
                            continue

        except Exception as ex:
            print(f"Ошибка чтения {os.path.basename( full_path )}: {ex}")

    if not country_gdp: # если данных нет, возвращаем пустой словарь
        return {}, first_header

    # Средний GDP
    avg_gdp = {country: sum(gdp_list) / len(gdp_list)
               for country, gdp_list in country_gdp.items()}

    # Сортировка по уюыванию
    sorted_result = dict( sorted( avg_gdp.items(), key = lambda x: x[1], reverse=True ))

    return sorted_result, first_header


def main() -> None:
    """ Функция создает парсер аргументов,
    определяет параметры командной строки, читает аргументы.
    Аргументы передает в функцию для чтения csv файлов
    Производит отчет в таблице
    """
    parser = argparse.ArgumentParser( description='Анализатор макроэкономических данных' )
    parser.add_argument('--files', nargs='*',
                        help = 'Пути к CSV файлам (несколько через пробел)')
    parser.add_argument('--report', default='average-gdp',
                        help = 'Название отчёта')
    args = parser.parse_args()

    # Вызов функции для чтения файлов
    result, column_name = process_csv_files( args.files )

    if result: # если True выполнять
        print(f"\n{args.report.upper()}")

        table_data = [ [i + 1, country, f"{avg:.2f}"]
                      for i, (country, avg) in enumerate( result.items() ) ]   # автоматическое рисование таблицы

        headers = ["№", column_name[0], column_name[2] ]
        print( tabulate(table_data, headers = headers, tablefmt = "outline") )
    else: # иначе
        print("CSV файлы не найдены")



# запуск скрипта прямо из этого файла
if __name__ == '__main__':
    main()
