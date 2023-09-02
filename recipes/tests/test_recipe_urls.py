# pylint: disable=all
from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_the_pytest_is_ok(self):
        assert 1 == 1, 'Um é igual a um'

    # todo método de teste tem que iniciar como test_
    def test_recipe_home_url_is_correct(self):
        # estou fazendo um teste para verificar se a url home ela é uma /
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', args=[1])
        self.assertEqual(url, '/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
        # self.fail(url)
