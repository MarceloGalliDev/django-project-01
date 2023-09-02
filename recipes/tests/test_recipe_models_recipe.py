# pylint: disable=all
from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe
# não se testa funções do Django ou motor do Django pois ja foi testada

class RecipeModelTest(RecipeTestBase):
    # uma receita garantida em todos os testes
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        category = self.make_category(name='Test Default Category')
        author = self.make_author(username='newuser')

        recipe = Recipe(
            title="Receita 2",
            description="Receita 2",
            slug="receita-2",
            preparation_time=10,
            preparation_time_unit="minutos",
            servings=1,
            servings_unit="porção",
            preparation_steps="teste2",
            category=category,
            author=author,
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    # def test_recipe_title_raises_error_if_title_has_more_than_65_char_1(self):
    #     # no erro eu ja consigo ver o meu titulo
    #     self.fail(self.recipe.title)
    #     # vendo quantos caracteres tem o titulo
    #     # self.fail(len(self.recipe.title))

    # def test_recipe_title_raises_error_if_title_has_more_than_65_char_2(self):
    #     # vendo quantos caracteres tem o titulo
    #     self.fail(len(self.recipe.title))

    # def test_recipe_title_raises_error_if_title_has_more_than_65_char_3(self):
    #     self.recipe.title = 'A' * 70
    #     # método para limpa a cadeia de dados e ocorrer a validação dos dados acima
    #     self.recipe.full_clean()
    #     self.recipe.save()
    #     self.fail(self.recipe.title)

    def test_recipe_title_raises_error_if_title_has_more_than_65_char_4(self):
        self.recipe.title = 'A' * 70
        # verificando se recebemos um error
        # como é uma função do tipo context manager temos que usar o with
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    # desempacotamos os parametros da função
    # fizemos o desempacotamento é como se fosse title = field e 65 = max_lenght
    def test_recipe_fields_max_length(self, field, max_lenght):
        # vamos usar setattr() para mudar dinamicamente nossa lista de tuplas
        # setattr(nome do objeto, campos)
        # é um context manager do unittest, usando um subTest
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Preparation steps is not False'
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False'
        )

    def test_recipe_string_representation(self):
        i_needed = 'Testint representations'
        self.recipe.title = i_needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), i_needed,
            msg=f'Recipe string representation must be "{i_needed}"'
                f'but was received "{str(self.recipe)}"'
        )
