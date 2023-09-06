# pylint: disable=all
# flake8: noqa
from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe
from django.db.models import Q
from .models import Recipe, Category
from django.contrib import messages
import os
from dotenv import load_dotenv

load_dotenv()

# criando constantes por convenção
PER_PAGES = os.getenv('PER_PAGES', 6)


def home(request):
    # estamos filtrando todos os dados para que apareça somente os que tem True no is_published
    recipes = get_list_or_404(
        Recipe.objects.filter(
            is_published=True
        ).order_by('-id')
    )
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    
    # enviando flash msg
    # não tem necessidade de passar para o context, o Django ja envia isso para o template
    # flash msg fica gravado na seção
    messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')

    return render(request, 'recipes/pages/home.html', context={
        # tudo que estiver dentro do home será acessado pela chave recipe.
        # exemplo recipe.title, o title esta vindo do banco de dados relacionando o models a views
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    # como category tem uma foreignKey para recipe, dentro de recipe podemos acessar os dados de category
    # quando vou buscar um campo de Category apartir de Recipe, é necessário usar dois underline (__)
    # por exemplo category__id=category_id
    # primeiro modelo
    # recipes = Recipe.objects.filter(
    #     category__id=category_id,
    #     is_published=True
    # ).order_by('-id')
    
    # # modelos de retorno 404
    # if not recipes:
    #     raise Http404('Not Found')
    
    # segundo modelo
    recipes = get_list_or_404(
        # queryset completo aqui dentro
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id')
    )
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    
    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        # aqui temos um queryset
        #'title': f'{recipes.first().category.name} - Category'
        # aqui temos uma lista
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    # pk é a primary key que é gerado automatico pelo django como id
    recipe = get_object_or_404(Recipe, pk=id, is_published=True, )
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })

def search(request):
    # verificar o debugger para obter as informações
    # caso não encontre o 'q' vai retornar '' como padrão
    search_term = request.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404()

    # aqui estamos usando dois title__icontains que seria a mesma coisa que colocar um ILIKE no sql, apos os __ é a inclusão do código slq aqui no Django
    # ordenando pelo id DESC
    # no debbuger para ver a query usamos no console, str(recipes.query)
    # indicando para o Django que queremos OR, usamos o Q importado do django.db.models
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')
    
    # eu posso continuar editando minha recipes
    # recipes = recipes.order_by('-id')
    # recipes = recipes.filter(is_published=True)
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    
    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
