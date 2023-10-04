# pylint: disable=all
# flake8: noqa
from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe
from django.db.models import Q, F
from .models import Recipe, Category
import os
from dotenv import load_dotenv
# from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.forms.models import model_to_dict
from tag.models import Tag

# relacionado ao SQL
from django.db.models.aggregates import Count
# para criar um valor que desejamos usamos esse import
from django.db.models import Value
from django.db.models.functions import Concat

load_dotenv()


# criando constantes por convenção
PER_PAGES = int(os.getenv('PER_PAGES', 6))


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
        
        qs = qs.select_related('author', 'category')
        
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
        
        if not qs:
            raise Http404()
        
        return qs

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        
        # vou pegar do context o valor de recipes
        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category | '
        })
        
        return ctx
         

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        # verificar o debugger para obter as informações
        # caso não encontre o 'q' vai retornar '' como padrão
        search_term = self.request.GET.get('q', '')
        
        if not search_term:
            raise Http404()
        
        qs = super().get_queryset(*args, **kwargs)
        # aqui estamos usando dois title__icontains que seria a mesma coisa que colocar um ILIKE no sql, apos os __ é a inclusão do código slq aqui no Django
        # ordenando pelo id DESC
        # no debbuger para ver a query usamos no console, str(recipes.query)
        # indicando para o Django que queremos OR, usamos o Q importado do django.db.models
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        # eu posso continuar editando minha recipes
        # recipes = recipes.order_by('-id')
        # recipes = recipes.filter(is_published=True)
        
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


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'
    
    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        
        # aqui estamos pegando o context e o atualizando
        # inserindo novos dados no context
        ctx.update({
            'is_detail_page': True,
        })
        
        return ctx


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
    
    # vamos subscrever o método render_to_response
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        
        # enviando os dados ao json
        # aqui dentro temos uma queryset
        recipes = self.get_context_data()['recipes']
        # aqui pegamos os valores dos objetos
        # faça o debugger para verificar os dados
        recipes_list = recipes.object_list.values()
        
        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeDetailAPI(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        # pegando o request de dentro da class para trazer a URL
        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:] # eliminando barra duplicada [1:]
        else:
            recipe_dict['cover'] = ''

        # apagando dado de ser mostrada na API
        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # aqui estamos usando dois title__icontains que seria a mesma coisa que colocar um ILIKE no sql, apos os __ é a inclusão do código slq aqui no Django
        # ordenando pelo id DESC
        # no debbuger para ver a query usamos no console, str(recipes.query)
        # indicando para o Django que queremos OR, usamos o Q importado do django.db.models
        qs = qs.filter(
            # kwargs vai vir da URL
            # tags__slug vem do model tags, que faz relação genérica com tag que tem slug
            tags__slug=self.kwargs.get('slug', ''),
        )
        
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        # filter sempre retorna uma queryset, ai necessario um first()
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title}- Tag | '

        ctx.update({
            'page_title': f'Search for "{page_title}" |',
        })

        return ctx


# enviando flash msg
# não tem necessidade de passar para o context, o Django ja envia isso para o template
# flash msg fica gravado na seção
# messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')

# verificar documentação para ver a qual se enquadra as view, por exemplo como DetailView

#________________________________________________________________
# Views de teoria
def theory(request, *args, **kwargs):
    # Recipe é um model
    # .objects é o manager
    # .all() é o método dentro do manager do model
    recipes = Recipe.objects.all()
    
    # Quando usamos um filter o Django inseri um LIMIT na query
    # icontains='Teste' está inserindo um ILIKE na query
    # o uso do title__ o uso dos dois underlines chama-se lookup
    # se começar com a letra i, significa que não é sensitive, não diferencia maiuscula de minuscula
        # https://docs.djangoproject.com/pt-br/4.2/ref/models/querysets/#field-lookups
    # filter nos retorna uma lista, um queryset
    # no template usamos recipes.0.title que nos retorna o titulo do primeiro indice do queryset
    # podemos usar o order_by()
    # podemos usar o .first() que vamos ver o primeiro objeto
    # podemos usar o .last() que vamos ver o ultimo objeto
        # quando usamos o .first() ou .last() retornamos um model view
    # __gt é maior que 2, vide documentação
    recipes = recipes.filter(
        title__icontains='Teste',
        id__gt=2
    )[:10]# para limitar a quantidade usamos um [:10]
    
    # outra forma de fazer também
    # a diferença consiste em como é tido o erro.
    # try:
        # recipes = Recipe.objects.get(id=1)
    # except ObjectDoesNotExist:
        # recipes = None
    #----------------------------------------------------------------
    
    #----------------------------------------------------------------
    # usando o OR, importamos o Q e o envolvemos os parametros dos métodos
    recipes = recipes.filter(
        Q(
            title__icontains='Teste',
            id__gt=2
        ) |
        Q(
            id__qt=1000
        )
    )[:10]
    #----------------------------------------------------------------
    
    #----------------------------------------------------------------
    # aqui vamos referenciar campos, outro campo de um outro model
    # estamos envolvendo o paramêtro com F, 
    # nessa caso o Django ja vai saber onde buscar
    recipes = recipes.filter(
        id=F('author__id')
    )[:10]# aqui podemos usar o LIMIT e o OFFSET setando onde iniciar a busca
    #----------------------------------------------------------------
    
    #----------------------------------------------------------------
    # especificando os campos
    # aqui retornamos um dicionário
    recipes = recipes.values(
        'id',
        'title',
        'author__username'
    )[:10]
    #----------------------------------------------------------------
    
    # quando usamos o only, retornamos objetos do recipe
    # tomar cuidado quando usado
    # observar os campos selecionados, pois caso esteja diferente ele fara uma consulta para cada id
    # podemos usar o only ou defer, defer é todos menos o campo selecionado
    recipes = recipes.only(
        'id',
        'title'
    )[:10]
    
    
    context = {
        'recipes': recipes,
    }
    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )
    #----------------------------------------------------------------
    
    #----------------------------------------------------------------
    # vamos utilizar os aggregate
    # Count conta quantos elementos temos de acordo com o paramêtro
    # nos retorna um dicionario
    recipes = recipes.values(
        'id',
        'title'
    )# podemos usar o filter aqui que sera alterado o Count
    # .first() por exemplo
    number_of_aggregations = Recipe.objects.aggregate(number=Count('id'))# number pode ser qualquer nome
    
    
    context = {
        'recipes': recipes,
        'number_of_aggregations': number_of_aggregations['number']
    }
    #--------------------------------------------------------
    
    #--------------------------------------------------------
    # usando annotate
    # ele nos cria um novo campo se necessário
    recipes = Recipe.objects.all().annotate(
        author_full_name=F('author__first_name')
    )
    #--------------------------------------------------------
    
    #--------------------------------------------------------
    # usando o Concat
    recipes = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'),       
        )
    )