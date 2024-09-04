from django.db import models

from products.services import upload_to

NULLABLE = {"blank": True, "null": True}
DECIMAL = {'max_digits': 10, 'decimal_places': 2}

class Product(models.Model):
    """ Модель для продуктов """

    id = models.BigIntegerField(primary_key=True, verbose_name='Штрих-код')
    brand = models.CharField(max_length=50, verbose_name='Бренд')
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    photo = models.ImageField(upload_to='products/', verbose_name='Фото')
    volume = models.CharField(max_length=50, verbose_name='Объём', **NULLABLE)
    weight = models.FloatField(verbose_name='Вес', **NULLABLE)
    note = models.TextField(verbose_name='Примечание', **NULLABLE)
    price_less_200 = models.DecimalField(**DECIMAL, verbose_name='Цена до 200 тыс. рублей')
    price_more_200 = models.DecimalField(**DECIMAL,verbose_name='Цена от 200 тыс. рублей')
    price_more_500 = models.DecimalField(**DECIMAL,verbose_name='Цена от 500 тыс. рублей')
    residue = models.IntegerField(verbose_name='Остаток', **NULLABLE)
    is_stock = models.BooleanField(verbose_name='В наличии', default=True)

    def __str__(self):
        return f'{self.title} - {self.brand}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class ProductFile(models.Model):
    """ Модель для файла данных с товарами """

    file = models.FileField(upload_to=upload_to, verbose_name='Файл')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File "{self.file}" uploaded at {self.uploaded_at}'
