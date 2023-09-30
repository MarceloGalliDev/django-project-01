# pylint: disable=all
# flake8: noqa
from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe
from django.db.models import Q
from .models import Recipe, Category
import os
from dotenv import load_dotenv
# from django.contrib import messages
from django.views.generic import ListView


load_dotenv()


# criando constantes por convenção
PER_PAGES = os.getenv('PER_PAGES', 6)


class RecipeListViewBase(ListView):
    model = Recipe
    # é o objeto padrão da classe
    context_object_name = 'recipes'
    # páginação de página pronto ou indicar uma
    # aqui indicamos objetos por página
    paginate_by = None
    # ordenação de objetos da classe
    ordering = ['-id']
    # usamos para modificar o nome do template padrão, que o django inclui um _list
    template_name = 'recipes/pages/home.html'
    
    # manipulando queryset, subscrevemos o método
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        qs = super().get_queryset(*args, **kwargs)
        # incluindo filtros para melhorar o desempenho
        qs = qs.filter(
            is_published=True
        )
        
        return qs
    
    # manipulando o context
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        # aqui esta vindo do context_object_name = 'recipes'
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'), 
            PER_PAGES
        )
        ctx.update({ 
            'recipes': page_obj,
            'pagination_range': pagination_range
        })
        
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'
    
    # como category tem uma foreignKey para recipe, dentro de recipe podemos acessar os dados de category
    # quando vou buscar um campo de Category apartir de Recipe, é necessário usar dois underline (__)
    # por exemplo category__id=category_id
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id'),
        )
        
        return qs
    

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx
    

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


 # enviando flash msg
# não tem necessidade de passar para o context, o Django ja envia isso para o template
# flash msg fica gravado na seção
# messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')