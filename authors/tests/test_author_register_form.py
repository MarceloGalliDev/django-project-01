# flake8: noqa
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
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'E-mail is required'),
        ('password', 'Password is required'),
        ('password2', 'Password2 is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        # quando temos um redirect e é necessario que a função siga o fluxo
        # é necessario incluir um follow=True
        response = self.client.post(url, data=self.form_data, follow=True)
        # conteúdo renderizado na tela
        self.assertIn(msg, response.content.decode('utf-8'))
        # dados do contexto
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        self.form_data['password2'] = 'abc123'  # Make sure to set this
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        weak_password_msgs = [
            'Invalid password, ',
            'Necessary a lowercase and a uppercase ',
            'Necessary a number ',
            'Necessary at least 8 characters'
        ]

        for message in weak_password_msgs:
            self.assertIn(message, response.context['form'].errors.get('password', []))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'  # Make sure to set this too
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        for message in weak_password_msgs:
            self.assertNotIn(message, response.context['form'].errors.get('password', []))

        # Check that the passwords are equal
        self.assertNotIn('Password and password2 must be equal', response.context['form'].errors.get('password', []))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and password2 must be equal'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))