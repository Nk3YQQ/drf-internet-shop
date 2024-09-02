from pathlib import Path

from celery import shared_task

from products.models import Product
from products.services import (open_xlsx_file, clear_directory, get_images_from_xlsx, convert_dataframe,
                               generate_converted_dict)


@shared_task
def write_data_from_xlsx_file(file_path: str) -> None:
    """ Функция записывает данные в базу данных """

    output_folder = Path(__file__).parent.parent.joinpath('media', 'products')

    clear_directory(output_folder)

    get_images_from_xlsx(file_path, output_folder)

    df = open_xlsx_file(file_path)

    converted_data = convert_dataframe(df)

    for data in generate_converted_dict(converted_data):
        try:
            product, _ = Product.objects.update_or_create(**data)

        except Exception as e:
            raise ValueError(f"Ошибка при добавлении товара в базу данных: {e}")