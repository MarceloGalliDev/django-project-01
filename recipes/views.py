# flake8: noqa
from django.shortcuts import render
from utils.recipes.factory import make_recipe
from .models import Recipe, Category


def home(request):
    # estamos filtrando todos os dados para que apareça somente os que tem True no is_published
    recipes = Recipe.objects.filter(
        is_published = True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        # tudo que estiver dentro do home será acessado pela chave recipe.
        # exemplo recipe.title, o title esta vindo do banco de dados relacionando o models a views
        'recipes': recipes,
    })


def category(request, category_id):
    # como category tem uma foreignKey para recipe, dentro de recipe podemos acessar os dados de category
    # quando vou buscar um campo de Category apartir de Recipe, é necessário usar dois underline (__)
    # por exemplo category__id=category_id
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published = True
    ).order_by('-id')
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
