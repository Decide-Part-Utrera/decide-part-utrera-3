from rest_framework.views import APIView
from rest_framework.response import Response
from collections import Counter
import math


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def dHont(self, options, numEscanos):
        for option in options:
            option['postproc'] = 0
        for escano in range(0, numEscanos):
            recuento = []
            for option in options:
                r = option['votes'] / (option['postproc']+1)
                recuento.append(r)
            ganador = recuento.index(max(recuento))
            options[ganador]['postproc'] += 1

        return Response(options)

    def multiPreguntas(self, questions):
        for question in questions:
            for opt in question:
                opt['postproc'] = opt['votes']

            question.sort(key=lambda x: -x['postproc'])

        return Response(questions)


    def borda(self, options):
        res = options
        for op in res:
            votosTotal = 0
            opciones = len(op['votes'])
            for i in range(0, opciones):
                votosOpcion = op['votes'][i]
                votosBorda = votosOpcion * (opciones - i)
                votosTotal += votosBorda
            op['votes'] = votosTotal
        res.sort(key=lambda x: -x['votes'])
        return res

    def imperiali(self, numEscanos, options):
        votosTotales = 0
        for x in options:
            votosTotales += x['votes']

        if votosTotales > 0 and numEscanos > 0:
            if votosTotales>(numEscanos+2):
                q = round(votosTotales / (numEscanos+2), 0)
                
                escanosAsig = 0
                for x in options:
                    escanosSuelo = math.trunc(x['votes']/q)
                    x.update({'postproc' : escanosSuelo})
                    escanosAsig += x['postproc']               

                while(escanosAsig < numEscanos):
                    for x in options:
                        x.update({ 
                            'escanosRes' : x['votes'] - (q * x['postproc'])})

                    options.sort(key=lambda x : -x['escanosRes'])

                    opcionMasVotosResiduo = options[0]
                    opcionMasVotosResiduo.update({
                    'postproc' : opcionMasVotosResiduo['postproc'] + 1})
                    escanosAsig += 1

                    for i in options:
                        i.pop('escanosRes')
                options.sort(key=lambda x : -x['postproc'])
            else:
                escanosAsigQ= 0
                for x in options:
                    escanosQ= math.trunc(numEscanos/ len(options))
                    x.update({'postproc' : escanosQ}) 
                    escanosAsigQ += x['postproc']
                
                if escanosAsigQ < numEscanos:
                    for x in options:
                        options.sort(key=lambda x : -x['votes'])
                    options[0].update({'postproc' : options[0]['postproc']+1})
            return Response(options)
        else:
            for x in options:
                x.update({'postproc' : 0})
            return Response(options)

    def hare(self, options, numEscanos):
        out = []

        e, r = [], []
        sum_e = 0
        m = sum([opt['votes'] for opt in options])
        q = round(m/numEscanos, 3)

        for i, opt in enumerate(options):
            ei = math.floor(opt['votes'] / q)
            ri = opt['votes'] - q*ei
            e.append(ei)
            r.append((ri, i))
            sum_e += ei

        k = numEscanos - sum_e
        r.sort(key = lambda x: -x[0])
        best_r_index = Counter(i for _, i in (r*k)[:k])
        
        for i, opt in enumerate(options):
            out.append({
                **opt,
                'postproc': e[i] + best_r_index[i] if i in best_r_index else e[i],
            })

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | DHONT | IMPERIALI | DHONTBORDA | IMPERIALIBORDA | MULTIPREGUNTAS 
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanos = request.data.get('numEscanos', 0)

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'DHONT':
            return self.dHont(options=opts, numEscanos=numEscanos)
        elif t == 'IMPERIALI':
            return self.imperiali(numEscanos=numEscanos, options=opts)
        elif t == 'DHONTBORDA':
            return self.dHont(options=self.borda(options=opts), numEscanos=numEscanos)
        elif t == 'IMPERIALIBORDA':
            return self.imperiali(options=self.borda(options=opts), numEscanos=numEscanos)
        elif t == 'HARE':
            return self.hare(options=opts, numEscanos=numEscanos)
        elif t == 'MULTIPREGUNTAS':
            questions = request.data.get('questions', [])
            return self.multiPreguntas(questions)


        return Response({})
