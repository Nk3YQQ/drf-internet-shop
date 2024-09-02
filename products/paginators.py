from rest_framework.pagination import PageNumberPagination


class Paginator(PageNumberPagination):
    """Класс для пагинации"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
