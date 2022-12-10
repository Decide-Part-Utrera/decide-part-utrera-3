from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Facilmente calculable a mano
    def testDHont1(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 10000},
                {'option':'OPT2','number':2,'votes': 132000},
                {'option':'OPT3','number':3,'votes': 98000},
                {'option':'OPT4','number':4,'votes': 225000},
                {'option':'OPT5','number':5,'votes': 170000},
                {'option':'OPT6','number':6,'votes': 12000}
            ],
            'numEscanos': 10
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 10000, 'postproc': 0},
            {'option':'OPT2','number':2,'votes': 132000, 'postproc': 2},
            {'option':'OPT3','number':3,'votes': 98000, 'postproc': 1},
            {'option':'OPT4','number':4,'votes': 225000, 'postproc': 4},
            {'option':'OPT5','number':5,'votes': 170000, 'postproc': 3},
            {'option':'OPT6','number':6,'votes': 12000, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 
           
    #Opciones muy repartidas
    def testDHont2(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 365487},
                {'option':'OPT2','number':2,'votes': 635874},
                {'option':'OPT3','number':3,'votes': 887456},
                {'option':'OPT4','number':4,'votes': 258793},
                {'option':'OPT5','number':5,'votes': 492335},
                {'option':'OPT6','number':6,'votes': 555555},
                {'option':'OPT7','number':7,'votes': 698742},
                {'option':'OPT8','number':8,'votes': 324822},
                {'option':'OPT9','number':9,'votes': 956978}
            ],
            'numEscanos': 25
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 365487,'postproc': 2},
            {'option':'OPT2','number':2,'votes': 635874,'postproc': 3},
            {'option':'OPT3','number':3,'votes': 887456,'postproc': 5},
            {'option':'OPT4','number':4,'votes': 258793,'postproc': 1},
            {'option':'OPT5','number':5,'votes': 492335,'postproc': 2},
            {'option':'OPT6','number':6,'votes': 555555,'postproc': 3},
            {'option':'OPT7','number':7,'votes': 698742,'postproc': 3},
            {'option':'OPT8','number':8,'votes': 324822,'postproc': 1},
            {'option':'OPT9','number':9,'votes': 956978,'postproc': 5}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Opciones poco repartidas
    def testDHont3(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 36548},
                {'option':'OPT2','number':2,'votes': 63587},
                {'option':'OPT3','number':3,'votes': 887456},
                {'option':'OPT4','number':4,'votes': 25879},
                {'option':'OPT5','number':5,'votes': 49233},
                {'option':'OPT6','number':6,'votes': 55555},
                {'option':'OPT7','number':7,'votes': 698742},
                {'option':'OPT8','number':8,'votes': 32482},
                {'option':'OPT9','number':9,'votes': 956978}
            ],
            'numEscanos': 50
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 36548,'postproc': 0},
            {'option':'OPT2','number':2,'votes': 63587,'postproc': 1},
            {'option':'OPT3','number':3,'votes': 887456,'postproc': 17},
            {'option':'OPT4','number':4,'votes': 25879,'postproc': 0},
            {'option':'OPT5','number':5,'votes': 49233,'postproc': 0},
            {'option':'OPT6','number':6,'votes': 55555,'postproc': 1},
            {'option':'OPT7','number':7,'votes': 698742,'postproc': 13},
            {'option':'OPT8','number':8,'votes': 32482,'postproc': 0},
            {'option':'OPT9','number':9,'votes': 956978,'postproc': 18}

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Sin escaños
    def testDHont4(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 25512},
                {'option':'OPT2','number':2,'votes': 89322},
                {'option':'OPT3','number':3,'votes': 97845},
                {'option':'OPT4','number':4,'votes': 75625},
                {'option':'OPT5','number':5,'votes': 11298}
            ],
            'numEscanos': 0
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 25512,'postproc': 0},
            {'option':'OPT2','number':2,'votes': 89322,'postproc': 0},
            {'option':'OPT3','number':3,'votes': 97845,'postproc': 0},
            {'option':'OPT4','number':4,'votes': 75625,'postproc': 0},
            {'option':'OPT5','number':5,'votes': 11298,'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Iguales
    def testDHont5(self): 
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 654858461},
                {'option':'OPT2','number':2,'votes': 654858461}
            ],
            'numEscanos': 30
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 654858461,'postproc': 15},
            {'option':'OPT2','number':2,'votes': 654858461,'postproc': 15}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)  