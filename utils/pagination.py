# pylint: disable=all
import math
from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    # abs() retira o simbolo do número e me retorna um número absoluto
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        # se está aparecendo minha primeira página
        'first_page_out_of_range': current_page > middle_range,
        # se minha ultima página está aparecendo
        'last_page_out_of_range': stop_range < total_pages,
    }

def make_pagination(request, queryset, per_page, qty_pages=4):
    # pegando a query string para url
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    # passo os objetos e a quantidade a ser exibida
    paginator = Paginator(queryset, per_page)
    # obtendo a página
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        # pegando a quantidade de páginas pelo paginator
        paginator.page_range,
        # quantidade de numeros a ser exibido
        qty_pages,
        # página atual
        current_page
    )
    return page_obj, pagination_range
