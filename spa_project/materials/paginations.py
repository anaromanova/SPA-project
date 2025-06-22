from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # Сколько объектов отдавать по умолчанию
    page_size = 10
    # Позволяет клиенту задавать свой размер страницы через ?page_size=
    page_size_query_param = 'page_size'
    # Не даём запрашивать слишком много за раз
    max_page_size = 100
