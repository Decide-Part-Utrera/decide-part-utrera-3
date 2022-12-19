from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from base.tests import BaseTestCase

from django.conf import settings

from django.contrib.auth.models import User
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from census.models import Census

class DHontTest(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
            
    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def crear_votacion(self):
        question1 = Question(desc="Pregunta de prueba", question_opt=['Opcion 1', 'Opcion 2'])
        question1.save()
        voting1 = Voting(name="Voting prueba", desc="Esto es un voting de prueba", question=question1, numEscanos=50, tipo="DHONT", start_date=timezone.now())
        voting1.save()
        response =self.driver.get(f'{self.live_server_url}/visualizer/{voting1.id}/')
        vState= self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Votación en curso")

    '''
    def votacion_positiva(self):
        question1 = Question(desc="Pregunta de prueba", question_opt=['Opcion 1', 'Opcion 2'])
        question1.save()
        voting1 = Voting(name="Voting prueba", desc="Esto es un voting de prueba", question=question1, numEscanos=50, tipo="DHONT", start_date=timezone.now())
        voting1.save()
        voter1 = User(username="votertest1")
        voter1.set_password("test1234")
        voter1.save()
        census1 = Census(voting_id=voting1.id, voter_id=voter1.id)
        census1.save()
        self.driver.get(f'{self.live_server_url}/booth/{voting1.id}')
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        submit = self.driver.find_element_by_name("submit")
        username.send_keys('admin')
        password.send_keys('qwerty')
        submit.click()
        time.sleep(5)
    '''
