from django.contrib import admin

from products.models import ProductFile
from products.tasks import write_data_from_xlsx_file


@admin.register(ProductFile)
class ProductFileModelAdmin(admin.ModelAdmin):
    """ Модель файла с данными о товарах """

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        write_data_from_xlsx_file(obj.file.path)
        self.message_user(request, "Файл загружен и отправлен на обработку")
