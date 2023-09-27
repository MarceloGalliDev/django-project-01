from collections import defaultdict
from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


# sempre que criado um form, é necessario valida-lo

class AuthorRecipeForm(forms.ModelForm):
    # vamos reescrever o init para incluir os atributos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # criamos uma lista com valores padrões
        # qualquer chave dentro desse padrão vai ser uma lista
        self._my_errors = defaultdict(list)

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

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data
        # pegando o campo title
        title = cd.get('title')
        description = cd.get('description')

        # criando validações de campos com defaultdict
        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        # criando validações de campos com defaultdict
        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        # criando validações de campos com defaultdict
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        # criando validações de campos com defaultdict
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')

        return field_value
