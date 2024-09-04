from django.contrib import admin
from django.core.cache import cache

from products.models import ProductFile
from products.tasks import write_data_from_xlsx_file

@admin.register(ProductFile)
class ProductFileModelAdmin(admin.ModelAdmin):
    """ Модель файла с данными о товарах """

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        task = write_data_from_xlsx_file.apply_async((obj.id, obj.file.path, request.user.id))
        task_id = task.id

        cache.set(f'task_{obj.id}', task_id, timeout=60 * 5)

        self.message_user(request, 'Файл загружен и обрабатывается')
