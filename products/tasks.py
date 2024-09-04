import logging
from pathlib import Path

from celery import shared_task
from django.core.cache import cache
from django.db import transaction
from django.contrib import messages

from products.models import Product, ProductFile
from products.services import (open_xlsx_file, get_images_from_xlsx, convert_dataframe, truncate_table,
                               delete_data_directory)
from users.models import User


logger = logging.getLogger(__file__)

@shared_task
def check_task_status(task_id, admin_user_id):
    status = cache.get(task_id)

    logger.info(f'Status: {status}')

    if status:
        user = User.objects.get(pk=admin_user_id)

        if 'failed' in status:
            message = f'Ваше задание завершилось с ошибкой: {status}'
            messages.error(user, message)
            logger.info('Message send')

        else:
            message = 'Ваше задание выполнено успешно'
            messages.success(user, message)
            logger.info('Message send')

@shared_task
def write_data_from_xlsx_file(instance_id: int, file_path: str, admin_user_id: int) -> None:
    """ Функция записывает данные в базу данных """

    output_folder = Path(__file__).parent.parent.joinpath('media', 'products')
    directory = Path(__file__).parent.parent.joinpath('media', 'data')

    try:
        get_images_from_xlsx(file_path, output_folder)

        df = open_xlsx_file(file_path)
        converted_data = convert_dataframe(df, Product)

        with transaction.atomic():
            truncate_table('products_product')

            product_list = list(Product(**data) for data in converted_data)
            Product.objects.bulk_create(product_list)

        cache.set(f'task_{instance_id}', 'success', timeout=60 * 5)

    except Exception as e:
        cache.set(f'task_{instance_id}', f'failed: {str(e)}', timeout=60 * 5)

    finally:
        product_file = ProductFile.objects.filter(pk=instance_id).first()

        if product_file:
            product_file.delete()

        delete_data_directory(directory)

        check_task_status.apply_async((instance_id, admin_user_id), countdown=60*5)
