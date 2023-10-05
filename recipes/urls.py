# pylint: disable=all
# flake8: noqa
from django.urls import path
from . import views


# para fazer o name spacing usado no paramêtro name
app_name = 'recipes'


urlpatterns = [
    path(
        '', 
        views.RecipeListViewBase.as_view(), 
        name='home'
    ),
    path(
        'home/', 
        views.RecipeListViewHome.as_view(), 
        name='home_root'
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(), 
        name="search"
    ),
    # slug é uma mascara sob a url 
    # <slug:slug> slug esquerda é indicação que será slug
    # <slug:slug> slug direita é o nome do parametro
    # slug vem da busca com kwargs
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(), 
        name="category"
    ),
    path(
        'recipes/<int:pk>/', 
        views.RecipeDetailView.as_view(), 
        name='recipe'
    ),
    path(
        'recipes/api/v1/', 
        views.RecipeListViewHomeApi.as_view(), 
        name='recipes_api_v1'
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'recipes/theory/',
        views.theory,
        name='recipes_theory',
    )
]

# quanto mais especificado o url, passamos ele para as primeiras posições