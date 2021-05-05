import hashlib
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from .forms import HashForm
from .models import Hash


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

class UnitTestCase(TestCase):

  def test_home_homepage_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'hashing/home.html')

  def test_hash_form(self):
    form = HashForm(data={'text':'hello'})
    self.assertTrue(form.is_valid())

  def test_hash_func_works(self):
    text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
    self.assertEqual('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', text_hash)

  # This is a helper method
  def saveHash(self):
    hash = Hash()
    hash.text = 'hello'
    hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    hash.save()
    return hash

  def test_hash_object(self):
    hash = self.saveHash()
    pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
    self.assertEqual(hash.text, pulled_hash.text)

  def test_viewing_hash(self):
    hash = self.saveHash()
    response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
    self.assertContains(response, 'hello')