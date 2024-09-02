import os.path
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.drawing.image import Image


def upload_to(instance, filename):
    """ Функция для загрузки файла в директорию data """

    return os.path.join('data', filename)


def open_xlsx_file(file_path) -> pd.DataFrame:
    """ Функция открывает файл с расширением xlsx """

    try:
        return pd.read_excel(file_path, sheet_name=1, header=1, skiprows=1)

    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла: {e}")


def check_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """ Функция проверяет наличие необходимых колон для записи данных """

    if not all(column in df.columns for column in required_columns):
        raise ValueError(f"Неверный формат файла. Требуемые колонки: {', '.join(required_columns)}")


def generate_converted_dict(converted_data: list[dict]):
    for data in converted_data:
        yield data


def clear_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
            os.remove(filepath)

def get_images_from_xlsx(file_path, output_folder):
    clear_directory(output_folder)

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.worksheets[1]

    count = 0

    for image in sheet._images:
        if isinstance(image, Image):
            count += 1

            img = image._data()

            img_filename = f'product{count}.png'
            img_path = Path(__file__).parent.parent.joinpath(output_folder, img_filename)

            with open(img_path, 'wb') as img_file:
                img_file.write(img)

def _convert_row_to_dict(row: pd.Series, i: int) -> dict:
    return {
        'barcode': row['Штрих-код'],
        'brand': row['Бренд'],
        'title': row['Наименование'],
        'description': row['Описание'],
        'photo': f'products/product{i + 1}.png',
        'volume': row['Объем'],
        'weight': row['Вес, кг'],
        'note': row['Примечания'],
        'price_less_200': row['до 200 тыс руб'],
        'price_more_200': row['от  200 тыс руб'],
        'price_more_500': row['от 500 тыс руб']
    }

def convert_dataframe(df: pd.DataFrame) -> list[dict]:
    df.columns = df.columns.str.strip().str.replace('\n', '')
    df.replace({np.nan: None}, inplace=True)

    return list(_convert_row_to_dict(row, hash(i)) for i, row in df.iterrows())

