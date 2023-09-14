import re
from django.core.exceptions import ValidationError

# traduzindo isso em uma função
# self.fields['username'].widget.attrs['placeholder'] = 'Que legal'
def add_attr(field, attrs_name, attrs_new_value):
    existing_attrs = field.widget.attrs.get(attrs_name, '')
    field.widget.attrs[attrs_name] = f'{existing_attrs} {attrs_new_value}'.strip()

def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)

# fazendo validação do campo especifico
# usando expressões regulares
def strong_password(password):
    # o r'' é para indicar uma expressão regular
    # expressão regular que chega se o campo possui caracteres de a - z e etc...
    # o sinal de ^ indica o inicio e $ indica o final
    # .{8,} pelo menos 8 caracteres
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError([
            'Invalid password, ',
            'Necessary a lowercase and a uppercase ',
            'Necessary a number ',
            'Necessary at least 8 characters',
        ],
            code='invalid'
        )
