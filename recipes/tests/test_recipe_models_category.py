# pylint: disable=all
from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

class RecipeCategoryModelTest(RecipeTestBase):
    # uma receita garantida em todos os testes
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_category_string_representation(self):
        i_needed = 'Category Testing'
        self.category.name = i_needed
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category), i_needed,
            msg=f'Recipe string representation must be "{i_needed}"'
                f'but was received "{str(self.category)}"'
        )

    def test_category_name_raises_error_if_title_has_more_than_65_char(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
