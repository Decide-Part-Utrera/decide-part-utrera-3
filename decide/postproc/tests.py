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


    #Datos simulador
    def testImperiali1(self):
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 52588 },
                { 'option': 'B', 'number': 2, 'votes': 45682 },
                { 'option': 'C', 'number': 3, 'votes': 5322 },
                { 'option': 'D', 'number': 4, 'votes': 12374 },
                { 'option': 'E', 'number': 5, 'votes': 84126 },
                { 'option': 'F', 'number': 6, 'votes': 29428 },
                { 'option': 'G', 'number': 7, 'votes': 33333 },
            ],
            'numEscanos': 55,
        }

        expected_result = [
            { 'option': 'E', 'number': 5, 'votes': 84126, 'postproc': 18},
            { 'option': 'A', 'number': 1, 'votes': 52588, 'postproc': 11},
            { 'option': 'B', 'number': 2, 'votes': 45682, 'postproc': 10},
            { 'option': 'G', 'number': 7, 'votes': 33333, 'postproc': 7},
            { 'option': 'F', 'number': 6, 'votes': 29428, 'postproc': 6},
            { 'option': 'D', 'number': 4, 'votes': 12374, 'postproc': 2},
            { 'option': 'C', 'number': 3, 'votes': 5322, 'postproc': 1}
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Iguales
    def testImperiali2(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 1000},
                { 'option': 'B', 'number': 2, 'votes': 1000},
                { 'option': 'C', 'number': 3, 'votes': 1000},
                { 'option': 'D', 'number': 4, 'votes': 1000}
            ],
            'numEscanos': 20,
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 1000, 'postproc': 5},
            { 'option': 'B', 'number': 2, 'votes': 1000, 'postproc': 5},
            { 'option': 'C', 'number': 3, 'votes': 1000, 'postproc': 5},
            { 'option': 'D', 'number': 4, 'votes': 1000, 'postproc': 5}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Sin escaños
    def testImperiali3(self):
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 52588 },
                { 'option': 'B', 'number': 2, 'votes': 45682 },
                { 'option': 'C', 'number': 3, 'votes': 5322 },
                { 'option': 'D', 'number': 4, 'votes': 12374 },
                { 'option': 'E', 'number': 5, 'votes': 84126 },
                { 'option': 'F', 'number': 6, 'votes': 29428 },
                { 'option': 'G', 'number': 7, 'votes': 33333 },
            ],
            'numEscanos': 0,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 52588, 'postproc': 0},
            { 'option': 'B', 'number': 2, 'votes': 45682, 'postproc': 0},
            { 'option': 'C', 'number': 3, 'votes': 5322, 'postproc': 0},
            { 'option': 'D', 'number': 4, 'votes': 12374, 'postproc': 0},
            { 'option': 'E', 'number': 5, 'votes': 84126, 'postproc': 0},
            { 'option': 'F', 'number': 6, 'votes': 29428, 'postproc': 0},
            { 'option': 'G', 'number': 7, 'votes': 33333, 'postproc': 0},
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Datos simulador
    def testDHontBorda1(self):
        data = {
            'type': 'DHONTBORDA',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': [200, 300, 400, 250, 150, 380, 20] },
                { 'option': 'B', 'number': 2, 'votes': [100, 200, 300, 350, 250, 380, 120] },
                { 'option': 'C', 'number': 3, 'votes': [1000, 300, 100, 100, 100, 100, 0] },
                { 'option': 'D', 'number': 4, 'votes': [100, 300, 400, 100, 400, 200, 200] },
                { 'option': 'E', 'number': 5, 'votes': [100, 400, 150, 450, 250, 150, 200] },
                { 'option': 'F', 'number': 6, 'votes': [100, 150, 100, 400, 150, 250, 550] },
                { 'option': 'G', 'number': 7, 'votes': [100, 50, 250, 50, 400, 240, 610] }
            ],
            'numEscanos': 50,
        }

        expected_result = [
            { 'option': 'C', 'number': 3, 'votes': 10200, 'postproc': 11},
            { 'option': 'A', 'number': 1, 'votes': 7430, 'postproc': 8},
            { 'option': 'E', 'number': 5, 'votes': 6900, 'postproc': 7},
            { 'option': 'D', 'number': 4, 'votes': 6700, 'postproc': 7},
            { 'option': 'B', 'number': 2, 'votes': 6430, 'postproc': 7},
            { 'option': 'F', 'number': 6, 'votes': 5200, 'postproc': 5},
            { 'option': 'G', 'number': 7, 'votes': 4740, 'postproc': 5}
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Iguales
    def testDHontBorda2(self):
        data = {
            'type': 'DHONTBORDA',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'B', 'number': 2, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'C', 'number': 3, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'D', 'number': 4, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'E', 'number': 5, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'F', 'number': 6, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'G', 'number': 7, 'votes': [100, 100, 100, 100, 100, 100, 100] }
            ],
            'numEscanos': 70,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 2800, 'postproc': 10 },
            { 'option': 'B', 'number': 2, 'votes': 2800, 'postproc': 10 },
            { 'option': 'C', 'number': 3, 'votes': 2800, 'postproc': 10 },
            { 'option': 'D', 'number': 4, 'votes': 2800, 'postproc': 10 },
            { 'option': 'E', 'number': 5, 'votes': 2800, 'postproc': 10 },
            { 'option': 'F', 'number': 6, 'votes': 2800, 'postproc': 10 },
            { 'option': 'G', 'number': 7, 'votes': 2800, 'postproc': 10 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Sin escaños
    def testDHontBorda3(self):
        data = {
            'type': 'DHONTBORDA',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': [170, 170, 170, 170, 170, 170, 170] },
                { 'option': 'B', 'number': 2, 'votes': [170, 170, 170, 170, 170, 170, 170] },
                { 'option': 'C', 'number': 3, 'votes': [170, 170, 170, 170, 170, 170, 170] },
                { 'option': 'D', 'number': 4, 'votes': [170, 170, 170, 170, 170, 170, 170] },
                { 'option': 'E', 'number': 5, 'votes': [170, 170, 170, 170, 170, 170, 170] },
                { 'option': 'F', 'number': 6, 'votes': [170, 170, 170, 170, 170, 170, 170] },
                { 'option': 'G', 'number': 7, 'votes': [170, 170, 170, 170, 170, 170, 170] }
            ],
            'numEscanos': 0,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 4760, 'postproc': 0 },
            { 'option': 'B', 'number': 2, 'votes': 4760, 'postproc': 0 },
            { 'option': 'C', 'number': 3, 'votes': 4760, 'postproc': 0 },
            { 'option': 'D', 'number': 4, 'votes': 4760, 'postproc': 0 },
            { 'option': 'E', 'number': 5, 'votes': 4760, 'postproc': 0 },
            { 'option': 'F', 'number': 6, 'votes': 4760, 'postproc': 0 },
            { 'option': 'G', 'number': 7, 'votes': 4760, 'postproc': 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Datos simulador
    def testImperialiBorda1(self):
        data = {
            'type': 'IMPERIALIBORDA',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': [610, 240, 400, 50, 250, 50, 100] },
                { 'option': 'B', 'number': 2, 'votes': [550, 250, 150, 400, 100, 150, 100] },
                { 'option': 'C', 'number': 3, 'votes': [200, 150, 250, 450, 150, 400, 100] },
                { 'option': 'D', 'number': 4, 'votes': [200, 200, 400, 100, 400, 300, 100] },
                { 'option': 'E', 'number': 5, 'votes': [0, 100, 100, 100, 100, 100, 1000] },
                { 'option': 'F', 'number': 6, 'votes': [120, 380, 250, 350, 300, 200, 100] },
                { 'option': 'G', 'number': 7, 'votes': [20, 380, 150, 250, 400, 300, 200] }
            ],
            'numEscanos': 55,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 8860, 'postproc': 11 },
            { 'option': 'B', 'number': 2, 'votes': 8400, 'postproc': 10 },
            { 'option': 'F', 'number': 6, 'votes': 7170, 'postproc': 8 },
            { 'option': 'D', 'number': 4, 'votes': 6900, 'postproc': 8 },
            { 'option': 'C', 'number': 3, 'votes': 6700, 'postproc': 8 },
            { 'option': 'G', 'number': 7, 'votes': 6170, 'postproc': 7 },
            { 'option': 'E', 'number': 5, 'votes': 3000, 'postproc': 3 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Iguales
    def testImperialiBorda2(self):
        data = {
            'type': 'IMPERIALIBORDA',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'B', 'number': 2, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'C', 'number': 3, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'D', 'number': 4, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'E', 'number': 5, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'F', 'number': 6, 'votes': [100, 100, 100, 100, 100, 100, 100] },
                { 'option': 'G', 'number': 7, 'votes': [100, 100, 100, 100, 100, 100, 100] }
            ],
            'numEscanos': 217,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 2800, 'postproc': 31 },
            { 'option': 'B', 'number': 2, 'votes': 2800, 'postproc': 31 },
            { 'option': 'C', 'number': 3, 'votes': 2800, 'postproc': 31 },
            { 'option': 'D', 'number': 4, 'votes': 2800, 'postproc': 31 },
            { 'option': 'E', 'number': 5, 'votes': 2800, 'postproc': 31 },
            { 'option': 'F', 'number': 6, 'votes': 2800, 'postproc': 31 },
            { 'option': 'G', 'number': 7, 'votes': 2800, 'postproc': 31 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Sin escaños
    def testImperialiBorda3(self):
        data = {
            'type': 'IMPERIALIBORDA',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': [7000, 7000, 7000] },
                { 'option': 'B', 'number': 2, 'votes': [7000, 7000, 7000] },
                { 'option': 'C', 'number': 3, 'votes': [7000, 7000, 7000] }
            ],
            'numEscanos': 0,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 42000, 'postproc': 0 },
            { 'option': 'B', 'number': 2, 'votes': 42000, 'postproc': 0 },
            { 'option': 'C', 'number': 3, 'votes': 42000, 'postproc': 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_multi_preguntas1(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 17 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 14 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 10 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 19 }
                ],
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 12 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 26},
                    { 'option': 'Option 4', 'number': 4, 'votes': 9 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 20 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'Option 4', 'number': 4, 'votes': 19, 'postproc': 19 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 17, 'postproc': 17 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 14, 'postproc': 14 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 10 }
                ],
                [
                    { 'option': 'Option 3', 'number': 3, 'votes': 26, 'postproc': 26 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 20, 'postproc': 20 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 12, 'postproc': 12 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 9, 'postproc': 9 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 }
                ],
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_multi_preguntas2(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 22 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 26 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 23 }
                ],
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 1 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 4 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 2 },
                    { 'option': 'Option 6', 'number': 6, 'votes': 0 }
                ],
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 3 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 10 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 20 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'Option 2', 'number': 2, 'votes': 26, 'postproc': 26 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 23, 'postproc': 23 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 22, 'postproc': 22 }
                ],
                [
                    { 'option': 'Option 2', 'number': 2, 'votes': 4, 'postproc': 4 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 2, 'postproc': 2 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 1, 'postproc': 1 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1, 'postproc': 1 },
                    { 'option': 'Option 6', 'number': 6, 'votes': 0, 'postproc': 0 }
                ],
                [
                    { 'option': 'Option 4', 'number': 4, 'votes': 20, 'postproc': 20 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 10 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 3, 'postproc': 3 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 }
                ],
        ]
          
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
        #test con preguntas vacías
    def test_multi_preguntas3(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [  
                ],
                [  
                ],
            ]
        }

        expected_result = [
            [   
                ],
                [  
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_multi_preguntas4(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'Verde', 'number': 1, 'votes': 30 },
                    { 'option': 'Rojo', 'number': 2, 'votes': 20 },
                    { 'option': 'Blanco', 'number': 3, 'votes': 4 },
                    { 'option': 'Negro', 'number': 4, 'votes': 10 }
                ],
                [
                    { 'option': 'Betis', 'number': 1, 'votes': 20 },
                    { 'option': 'Sevilla', 'number': 2, 'votes': 0 },
                    { 'option': 'Almeria', 'number': 3, 'votes': 5 },
                    { 'option': 'Cadiz', 'number': 4, 'votes': 3 },
                    { 'option': 'Utrera', 'number': 5, 'votes': 10 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'Verde', 'number': 1, 'votes': 30, 'postproc': 30 },
                    { 'option': 'Rojo', 'number': 2, 'votes': 20, 'postproc': 20 },
                    { 'option': 'Negro', 'number': 4, 'votes': 10, 'postproc': 10},
                    { 'option': 'Blanco', 'number': 3, 'votes': 4, 'postproc': 4 }
                ],
                [
                    { 'option': 'Betis', 'number': 1, 'votes': 20, 'postproc': 20 },
                    { 'option': 'Utrera', 'number': 5, 'votes': 10, 'postproc': 10 },
                    { 'option': 'Almeria', 'number': 3, 'votes': 5, 'postproc': 5},
                    { 'option': 'Cadiz', 'number': 4, 'votes': 3, 'postproc': 3 },
                    { 'option': 'Sevilla', 'number': 2, 'votes': 0, 'postproc': 0 }
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_multi_preguntas5(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'AMN', 'number': 1, 'votes': 10 },
                    { 'option': 'CCG', 'number': 2, 'votes': 10 },
                    { 'option': 'GPF', 'number': 3, 'votes': 10 }
                ],
                [
                    { 'option': '1', 'number': 1, 'votes': 0 },
                    { 'option': '2', 'number': 2, 'votes': 0 },
                    { 'option': '3', 'number': 3, 'votes': 0 },
                    { 'option': '4', 'number': 4, 'votes': 0 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'AMN', 'number': 1, 'votes': 10, 'postproc': 10 },
                    { 'option': 'CCG', 'number': 2, 'votes': 10, 'postproc': 10 },
                    { 'option': 'GPF', 'number': 3, 'votes': 10, 'postproc': 10 }
                ],
                [
                    { 'option': '1', 'number': 1, 'votes': 0, 'postproc': 0 },
                    { 'option': '2', 'number': 2, 'votes': 0, 'postproc': 0 },
                    { 'option': '3', 'number': 3, 'votes': 0, 'postproc': 0 },
                    { 'option': '4', 'number': 4, 'votes': 0, 'postproc': 0 }
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_multi_preguntas6(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'ANGEL', 'number': 1, 'votes': 20 },
                    { 'option': 'GINES', 'number': 2, 'votes': 10 }
                ],
                [
                    { 'option': 'CARLOS', 'number': 1, 'votes': 11 },
                    { 'option': 'ANA', 'number': 2, 'votes': 9}
                ],
                [
                    { 'option': 'SERGIO', 'number': 1, 'votes': 14 },
                    { 'option': 'ENRIQUE', 'number': 2, 'votes': 16 }
                ],
                [
                    { 'option': 'ALBA', 'number': 1, 'votes': 20 },
                    { 'option': 'CARMEN', 'number': 2, 'votes': 0 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'ANGEL', 'number': 1, 'votes': 20, 'postproc': 20 },
                    { 'option': 'GINES', 'number': 2, 'votes': 10, 'postproc': 10 }
                ],
                [
                    { 'option': 'CARLOS', 'number': 1, 'votes': 11, 'postproc': 11 },
                    { 'option': 'ANA', 'number': 2, 'votes': 9, 'postproc': 9 }
                ],
                [
                    { 'option': 'ENRIQUE', 'number': 2, 'votes': 16, 'postproc': 16 },
                    { 'option': 'SERGIO', 'number': 1, 'votes': 14, 'postproc': 14}
                ],
                [
                    { 'option': 'ALBA', 'number': 1, 'votes': 20, 'postproc': 20 },
                    { 'option': 'CARMEN', 'number': 2, 'votes': 0, 'postproc': 0 }
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 

