# pylint: disable=all
# flake8: noqa
from django.urls import path
from . import views


# para fazer o name spacing usado no paramêtro name
app_name = 'recipes'


urlpatterns = [
    path(
        '', 
        views.RecipeListViewBase.as_view(), name='home'
    ),
    path(
        'home/', 
        views.RecipeListViewHome.as_view(), name='home_root'
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(), name="search"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(), name="category"
    ),
    path(
        'recipes/<int:id>/', 
        views.recipe, name='recipe'
    ),
]

# quanto mais especificado o url, passamos ele para as primeiras posições