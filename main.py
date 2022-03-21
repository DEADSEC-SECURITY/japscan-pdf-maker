import urllib.request
import os
import sys
import PIL
import img2pdf
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.selenium_starter import start
from utils.common import random_sleep

BASE_PATH = os.path.dirname(__file__)


class Mike():

    def __init__(self, url):
        self.page = 1
        self.imgs = []
        self.url = url

        self.browser = start()
        self.get_url()
        self.get_title()
        self.create_title_folder()

    def get_url(self):
        target_url = f'{self.url}{str(self.page)}.html'
        current_url = self.browser.current_url
        self.browser.get(target_url)

        WebDriverWait(self.browser, 10).until(
            EC.url_changes(current_url)
        )

        current_url = self.browser.current_url

        if current_url != target_url:
            self.save_img(self.imgs)
            self.make_pdf()
            self.exit()

    def get_requests(self):
        return self.browser.requests

    def filter_requests(self):
        requests = self.get_requests()

        base_url = 'cdn.statically.io/img/'
        for x in requests:
            if x.response:
                # Check if the request contains the base url for the images
                if base_url in x.url:
                    # Check if the image being viewd wasnt added yet
                    if x.url not in self.imgs:
                        self.imgs.append(x.url)

    def save_img(self, img_url_list):
        for index, value in enumerate(img_url_list):
            file = os.path.join(self.folder, f'{index}.jpg')
            urllib.request.urlretrieve(str(value), file)

    def make_pdf(self):
        imgs = os.listdir(self.folder)
        imgs_names = [int(x.replace('.jpg', '')) for x in imgs]
        imgs_names.sort()
        imgs = [os.path.join(self.folder, str(x) + '.jpg') for x in imgs_names]
        del imgs_names
        pdf_file = os.path.join(BASE_PATH, 'pdfs', f'{self.title}.pdf')

        with open(pdf_file, 'wb') as f:
            f.write(img2pdf.convert(imgs))

    def get_title(self):
        self.title = self.browser.find_element_by_xpath('/html/body/div[1]/h1').text
        self.title = self.title.replace(' ', '')
        self.title = self.title.replace(':', '')
        self.title = self.title.replace('/', '')

    def create_title_folder(self):
        self.folder = os.path.join(BASE_PATH, 'images', self.title.replace(' ', '').replace(':', ''))
        if os.path.isdir(self.folder):
            os.remove(self.folder)
        os.mkdir(self.folder)

    def exit(self):
        self.browser.quit()
        sys.exit()


def check_local_repo():
    # Create the image folder if it doesnt exists
    images_folder = os.path.join(BASE_PATH, 'images')
    if not os.path.isdir(images_folder):
        os.mkdir(images_folder)

    # Create the drivers folder if it doesnt exist
    drivers_folder = os.path.join(BASE_PATH, 'drivers')
    if not os.path.isdir(drivers_folder):
        os.mkdir(drivers_folder)
        print('Please go to https://chromedriver.chromium.org/downloads and download the driver for you system')
        print('Please save the driver binary to the drivers folder with the name "chromedriver.exe" for windows and "chromedriver" for linux and maxOS')
        sys.exit()


if __name__ == '__main__':
    # Check if all folders are created properly
    check_local_repo()
    scraper = Mike(url='https://www.japscan.ws/lecture-en-ligne/tokyo-ghoul-re/132/')
    while True:
        scraper.filter_requests()
        scraper.page += 1
        scraper.get_url()
