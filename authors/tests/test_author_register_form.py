from django.test import TestCase
from authors.forms.forms import RegisterForm
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase
from django.urls import reverse

# unittest neste momento
class AuthorRegisterFormUnitTest(TestCase):
    def test_email_placeholder_is_correct(self):
        form = RegisterForm()
        # pegando o campo do formulário e não o valor do campo
        placeholder = form['email'].field.widget.attrs['placeholder']
        self.assertEqual('Your email here', placeholder)

    @parameterized.expand([
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
        ('password2', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
        ('email', 'The e-mail must be valid.'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


# test de integração, vários teste em um
class AuthorRegisterFormIntergrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@example.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must be a valid username')
    ])   
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        # quando temos um redirect e é necessario que a função siga o fluxo
        # é necessario incluir um follow=True
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
