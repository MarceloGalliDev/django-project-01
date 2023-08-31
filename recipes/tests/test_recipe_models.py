from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

# não se testa funções do Django ou motor do Django pois ja foi testada

class RecipeModelTest(RecipeTestBase):
    # uma receita garantida em todos os testes
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

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
