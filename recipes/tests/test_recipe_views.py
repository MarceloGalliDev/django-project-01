# pylint: disable=all
# flake8: noqa
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest import skip
from unittest.mock import patch

# TDD = escrever os testes antes da aplicação


# para pular o teste usamos @skip
# @skip('WIP') WIP = working in progress
class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        # o view.func está vindo do debbug de view = resolve('/')
        # estamos testando a view function está executando mesmo a função home()
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # aqui estamos testando se existe aquele texto no conteúdo
    # o content foi retirado debugando o código
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        self.make_recipe()
        # apagando receita do setUP para este test
        # Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'By Galli Brothers Inc.',
            response.content.decode('utf-8')
        )
        # para sempre falhar o test, para lembrar de escrever testes
        # self.fail('para terminar de digitar')

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_template_loads_recipes(self):
        # estamos especificando dados
        self.make_recipe(
            title='Recipe Title',
            author_data={
                'first_name': 'joao'
            },
            category_data={
                'name': 'Café da manhã'
            }
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        # verificando quantos recipes tem no contexto
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('joao', content)
        self.assertIn('Café da manhã', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>Not Found</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        # pegando o id de recipe
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.id}))
        self.assertEqual(response.status_code, 404)

    # criando mocks
    # passamos o caminho da variável que desejamos manipular dentro do decorator
    # segundo paramêtro é o valor que desejamos
    @patch('recipes.views.PER_PAGES', new=3)
    def test_recipe_home_template_dont_load_recipes_not_published_v2(self):
        # criando receitas de recipe
        for i in range(18):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)
        
        response = self.client.get(reverse('recipes:home'))
        # o recipes passa por dentro do paginator
        recipes = response.context['recipes']
        paginator = recipes.paginator
        # vamos testar se o num_pages é = 2
        self.assertEqual(paginator.num_pages, 6)
        # navegando nas páginas, pagina 1 tem que ter 3 recipes
        self.assertEqual(len(paginator.get_page(1)), 3)