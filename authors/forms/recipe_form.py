from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr


# sempre que criado um form, é necessario valida-lo

class AuthorRecipeForm(forms.ModelForm):
    # vamos reescrever o init para incluir os atributos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adicionando o atributo no campo title, uma classe com nome de span-2
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', \
            'servings', 'servings_unit', 'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }
