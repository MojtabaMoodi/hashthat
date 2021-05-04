import hashlib
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


class FunctionalTestCase(TestCase):

  def setUp(self):
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    self.browser = webdriver.Firefox(options=opts)

  
  def test_there_is_homepage(self):
    self.browser.get('http://127.0.0.1:8000')
    self.assertIn('Enter hash here', self.browser.page_source)

  def test_hash_of_hello(self):
    self.browser.get('http://127.0.0.1:8000')
    text = self.browser.find_element_by_id('id_text')
    text.send_keys('hello')
    hashed_hello = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
    self.browser.find_element_by_name('submit').click()
    self.assertIn(hashed_hello, self.browser.page_source)


  def tearDown(self):
    self.browser.quit()
