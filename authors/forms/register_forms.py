# pylint: disable=all
# flake8: noqa:E501
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr, add_placeholder, strong_password


# Formulario atrelado a um model
class RegisterForm(forms.ModelForm):
    # acessando o init da classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # adicionando args nos campos pela classe ou buscando um widget de dentro
        add_attr(self.fields['username'], 'placeholder', 'Your username here')
        add_placeholder(self.fields['email'], 'Your email here')

    # sempre que for subscrever um campo faça diretamenta aqui
    username = forms.CharField(
        required=True,
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, 
        max_length=150,
    )

    first_name = forms.CharField(
        required=True,
        label='First Name',
        error_messages={'required': 'Write your first name'},
    )

    last_name = forms.CharField(
        required=True,
        label='Last Name',
        error_messages={'required': 'Write your last name'},
    )

    email = forms.EmailField(
        required=True,
        label='E-mail',
        help_text='The e-mail must be valid.',
        error_messages={'required': 'E-mail is required'},
    )

    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Write your password',
            }
        ),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={'required': 'Password is required'},
        validators=[strong_password],
    )

    password2 = forms.CharField(
        required=True,
        label='Password2',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password',
            }
        ),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={'required': 'Password2 is required'},
        validators=[strong_password],
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
        # labels = {
        #     'first_name': 'First Name',
        #     'last_name': 'Last Name',
        #     'username': 'Username',
        #     'email': 'E-mail',
        # }
        # error_messages = {
        #     'username': {
        #         'required': 'This field must be a valid username',
        #         'max_length': 'This is the maximum length of 50 caracters.',
        #         'invalid': 'This field is invalid.',
        #     }
        # }
        # # aqui subscrevemos os campos de widgets, todos campos do form tem o seu
        # # aqui podemos inserir atributos nos campos
        # widgets = {
        #     'first_name': forms.TextInput(attrs={
        #         'placeholder': 'Type your first name here',
        #     }),
        #     'last_name': forms.TextInput(attrs={
        #         'placeholder': 'Type your last name here',
        #     }),
        # }

    # função de validação de um campo especifico
    # def clean_password(self):
    #     # pegando o dado vindo do formulario
    #     # self.data é o dado cru
    #     # self.cleaned_data é o dado ja tratato
    #     data = self.cleaned_data.get('password')

    #     # no params o value vai para %(value)s, podendo ser qualquer nome
    #     if 'atenção' in data:
    #         raise ValidationError(
    #             message='Não digite "%(value)s" neste campo.',
    #             code='invalid',
    #             params={'value': 'atenção'}
    #         )

    #     return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid',)
        
        return email
    

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
