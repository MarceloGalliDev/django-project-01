import pytest
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        self.sleep()

    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            # is_displayed() seleciona todos campos disponiveis na tela
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    # callback é um forma de retornar algo depois de atender as necessidades
    # por exemplo uma função que deve retornar depois que outra função for finalizada
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        # aqui passamos o callback com form de parametro
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        # usamos a função callback para chamar a função
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Your first name here')
            first_name_field.send_keys(' ')
            # aqui a página atualizou
            first_name_field.send_keys(Keys.ENTER)

            # necessário devido a página ter sido atualizada
            form = self.get_form()

            # aqui queremos saber se o texto da esquerda está dentro do da direita
            # "text" > form.text
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        # usamos a função callback para chamar a função
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Your last name here')
            last_name_field.send_keys(' ')
            # aqui a página atualizou
            last_name_field.send_keys(Keys.ENTER)

            # necessário devido a página ter sido atualizada
            form = self.get_form()

            # aqui queremos saber se o texto da esquerda está dentro do da direita
            # "text" > form.text
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username here')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your email here')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Write your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password and password2 must be equal', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Your first name here').send_keys('First Name')
        self.get_by_placeholder(form, 'Your last name here').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your username here').send_keys('my_username')
        self.get_by_placeholder(
            form, 'Your email here').send_keys('email@valid.com')
        self.get_by_placeholder(
            form, 'Write your password').send_keys('P@ssw0rd1')
        self.get_by_placeholder(
            form, 'Repeat your password').send_keys('P@ssw0rd1')

        form.submit()

        self.assertIn(
            'Your user is created, please log in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
