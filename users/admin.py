from django.contrib import admin

class UserModelAdmin(admin.ModelAdmin):
    """ Модель пользователя для администратора """

    list_display = ('first_name', 'last_name', 'birthday_date', 'email')
    list_per_page = 20
    list_filter = ('date_joined',)
