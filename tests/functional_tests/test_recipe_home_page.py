# flake8: noqa

# LiveServerTestCase ele cria um servidor para testar
# Quando o teste termina o LiveServer é eliminado
import time
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import override_settings
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser


@override_settings(DEBUG=True)
class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        browser = make_chrome_browser()
        
        browser.get(self.live_server_url + '/home')
        self.sleep(60)
        
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)
        browser.quit()

