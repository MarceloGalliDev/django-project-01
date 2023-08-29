from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest_is_ok(self):
        assert 1 == 1, 'Um é igual a um'

    # todo método de teste tem que iniciar como test_
    def test_recipe_home_url_is_correct(self):
        # estou fazendo um teste para verificar se a url home ela é uma /
        url = reverse('recipes:home')
        self.assertEquals(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEquals(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEquals(url, '/recipes/1/')
