from seleniumwire import webdriver
import os

def get_os():
    if os.name == 'nt':
        return 'Windows'
    else:
        return 'Linux'

def start():
    path = os.path.dirname(os.path.dirname(__file__))
    DRIVERS = os.path.join(path, 'drivers')

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    if get_os() == 'Windows':
        chrome = os.path.join(DRIVERS, 'chromedriver.exe')
        browser = webdriver.Chrome(executable_path=chrome, options=options)
    else:
        chrome = os.path.join(DRIVERS, 'chromedrive')
        browser = webdriver.Chrome(executable_path=chrome, options=options)

    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    browser.maximize_window()

    return browser
