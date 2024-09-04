import os
import shutil
from functools import wraps
from pathlib import Path
from random import randint

import numpy as np
import openpyxl
import pandas as pd
from django.db import connection

from openpyxl.drawing.image import Image


def upload_to(instance, filename: str) -> str:
    """ Функция для загрузки файла в директорию data """

    return os.path.join('data', filename)


def open_xlsx_file(file_path):
    """ Функция открывает файл с расширением xlsx """

    try:
        df = pd.read_excel(file_path, usecols="A:M", sheet_name=1, skiprows=2)
        return df[df['Unnamed: 12'].notna()]

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
    shutil.rmtree(directory, ignore_errors=True)

    os.makedirs(directory, exist_ok=True)

def save_image(image, count, output_folder):
    img_filename = f'product{count}.png'
    img_path = Path(output_folder).joinpath(img_filename)

    with open(img_path, 'wb') as img_file:
        img_file.write(image._data())


def get_images_from_xlsx(file_path, output_folder):
    clear_directory(output_folder)

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.worksheets[1]

    images = filter(lambda x: isinstance(x, Image), sheet._images)
    list(map(lambda x: save_image(x, sheet._images.index(x) + 1, output_folder), images))


def convert_id_to_int(data: dict) -> dict:
    data_id = data['id']
    data['id'] = int(data_id)

    return data

def check_id_from_row(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result: dict = func(*args, **kwargs)

        barcode = result.get('id')

        if barcode and len(str(barcode)) > 1:
            return convert_id_to_int(result)

        return {}

    return wrapper

@check_id_from_row
def _convert_row_to_dict(row: pd.Series, i: int) -> dict:

    if row['Unnamed: 12'] == 0.0:
        residue = randint(1, 100)
        is_stock = True

    else:
        residue = None
        is_stock = False

    weight = row['Вес, кг']

    if isinstance(weight, str):
        weight = float(weight.replace(',', '.')) if weight else None

    elif isinstance(weight, float):
        weight = weight

    price_less_200 = row['до 200 тыс руб']
    price_more_200 = row['от  200 тыс руб']
    price_more_500 = row['от 500 тыс руб']

    price_less_200 = float(price_less_200) if price_less_200 else 0.0
    price_more_200 = float(price_more_200) if price_more_200 else 0.0
    price_more_500 = float(price_more_500) if price_more_500 else 0.0

    return {
        'id': row['Штрих-код'],
        'brand': row['Бренд'],
        'title': row['Наименование'],
        'description': row['Описание'],
        'photo': f'products/product{i + 1}.png',
        'volume': row['Объем'],
        'weight': weight,
        'note': row['Примечания'],
        'price_less_200': price_less_200,
        'price_more_200': price_more_200,
        'price_more_500': price_more_500,
        'residue': residue,
        'is_stock': is_stock
    }

def convert_dataframe(df: pd.DataFrame, product_model) -> list[dict]:
    df.columns = df.columns.str.strip().str.replace('\n', '')
    df.replace({np.nan: None}, inplace=True)

    unique_data = {
        data['id']: data
        for i, row in df.iterrows()
        if (data := _convert_row_to_dict(row, hash(i))) and
           data['id'] not in {d['id'] for d in product_model.objects.values('id')}
    }

    return list(unique_data.values())

def truncate_table(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;')

def delete_data_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

path = Path(__file__).parent.parent.joinpath('media', 'data', 'data.xlsx')
