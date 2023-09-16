# flake8: noqa
# pylint: disable=all

# LiveServerTestCase ele cria um servidor para testar
# Quando o teste termina o LiveServer é eliminado
import pytest
from django.test.utils import override_settings
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@override_settings(DEBUG=True)
@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    # incluido função de outro test via mocks
    # alterar nome para iniciar os testes
    @patch('recipes.views.PER_PAGES', new=3)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        # setUp comming here
        # criando receita via mixin
        self.make_recipe()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('', body.text)
        # tearDown finished here
    
    # alterar nome para iniciar os testes
    @patch('recipes.views.PER_PAGES', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        # colocando titulo nas receitas
        # titulo da receita 0
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # O usuário vê o que estava procurando na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )
    
    @patch('recipes.views.PER_PAGES', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )