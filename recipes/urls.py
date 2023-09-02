# pylint: disable=all
# flake8: noqa
from django.urls import path
from . import views


# para fazer o name spacing usado no paramêtro name
app_name = 'recipes'


urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/search/', views.search, name='search'),
    path('recipes/category/<int:category_id>/', views.category, name='category'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
]

# quanto mais especificado o url, passamos ele para as primeiras posições