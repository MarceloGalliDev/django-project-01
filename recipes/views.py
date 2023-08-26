from django.shortcuts import render
from utils.recipes.factory import make_recipe


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        # tudo que estiver dentro do home será acessado pela chave recipe.
        # exemplo recipe.title, o title esta vindo do make_recipe
        'recipes': [make_recipe() for i in range(10)],
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
