# flake8: noqa
# pylint: disable=all
from django.test import TestCase
from recipes.models import Recipe, Category, User


# extraindo setUp e tearDown para uma classe
# usado para criar funções antes e depois dos testes
class RecipeTestBase(TestCase):
    # setUP method é responsavel por ser executado antes de cada test
    def setUp(self) -> None:
        return super().setUp()

    # tearDOWN é executado depois do test
    def tearDown(self) -> None:
        return super().tearDown()

    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        title="Receita 1",
        description="Receita 1",
        slug="receita-1",
        preparation_time=10,
        preparation_time_unit="minutos",
        servings=1,
        servings_unit="porção",
        preparation_steps="teste1",
        preparation_steps_is_html=False,
        is_published=True,
        category_data=None,
        author_data=None,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        # **category_data, é chamado de desempacotamento, para criar os parametros de acordo com a função
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
