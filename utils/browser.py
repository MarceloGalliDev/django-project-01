import os
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv


load_dotenv()


# esse comando Path(__file__) traz o caminho completo deste arquivo
# o uso do parent me retorna a pasta acima deste arquivo
ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


# --headless = executa o serviço sem aparecer na tela
# *options está extraindo os argumentos, vai vir uma tupla cheio de args
def make_chrome_browser(*options):
    # arquivo de options chromedriver
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.getenv('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    # arquivo de service chromedriver
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    # arquivo de browser chromedriver
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    # browser = make_chrome_browser('--headless')
    browser.get('http://127.0.0.1:8000/')
    sleep(5)
    browser.quit()
