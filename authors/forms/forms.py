# pylint: disable=all
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# traduzindo isso em uma função
# self.fields['username'].widget.attrs['placeholder'] = 'Que legal'
def add_attr(field, attrs_name, attrs_new_value):
    existing_attrs = field.widget.attrs.get(attrs_name, '')
    field.widget.attrs[attrs_name] = f'{existing_attrs} {attrs_new_value}'.strip()

def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)

class RegisterForm(forms.ModelForm):
    # acessando o init da classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # adicionando args nos campos pela classe ou buscando um widget de dentro
        add_attr(self.fields['username'], 'placeholder', 'Your username here')
        add_placeholder(self.fields['email'], 'Your email here')

    # sempre que for subscrever um campo faça diretamenta aqui
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password',
            }
        ),
        error_messages={
            'required': 'This field must be a valid password',
        }
    )

    # meta dados para o form
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        # para excluir campos da renderização da page
        # exclude = ['first_name', 'last_name', 'username']

        # para alterar o nome dos labels da renderização da page
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid.',
        }
        error_messages = {
            'username': {
                'required': 'This field must be a valid username',
                'max_length': 'This is the maximum length of 50 caracters.',
                'invalid': 'This field is invalid.',
            }
        }
        # aqui subscrevemos os campos de widgets, todos campos do form tem o seu
        # aqui podemos inserir atributos nos campos
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Type your last name here',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter your password',
            })
        }

    # função de validação de um campo especifico
    def clean_password(self):
        # pegando o dado vindo do formulario
        # self.data é o dado cru
        # self.cleaned_data é o dado ja tratato
        data = self.cleaned_data.get('password')

        # no params o value vai para %(value)s, podendo ser qualquer nome
        if 'atenção' in data:
            raise ValidationError(
                message='Não digite "%(value)s" neste campo.',
                code='invalid',
                params={'value': 'atenção'}
            )

        return data

    # método clean validar o formulario como um todo
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        # atrelando o erro ao campo
        # posso colocar um ValidationError dentro de outro
        if password != password2:
            raise ValidationError({
                'password': ValidationError(
                    'Password and password2 must be equal',
                    code='invalid'
                ),
                'password2': 'Password and password2 must be equal'
            })
