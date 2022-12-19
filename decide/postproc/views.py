from rest_framework.views import APIView
from rest_framework.response import Response
from collections import Counter
import math
from math import floor


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
        res = []
        escanos_cociente = []
        residuos = []
        sum_e = 0
        votes = 0
        votosTotales = 0
        for x in options:
            votosTotales += x['votes']
        if votosTotales > 0 and numEscanos > 0:
            for option in options:
                votes += option['votes']
            cociente = votes / (numEscanos + 2)

            for i, option, in enumerate(options):
                ei = floor(option['votes']/cociente)
                ri = option['votes'] - cociente * ei
                escanos_cociente .append(ei)
                residuos.append((ri,i))
                sum_e += ei

            free_seats = numEscanos - sum_e
            residuos.sort(key = lambda x: -x[0])
            best_r_index = Counter(i for _, i in (residuos*free_seats)[:free_seats])
            
            for i, option in enumerate(options):
                res.append({
                    **option,
                    'postproc': escanos_cociente [i] + best_r_index[i] if i in best_r_index else escanos_cociente [i],
                })

            res.sort(key=lambda x: (-x['postproc'], -x['votes']))
            return Response(res)
        else:
            for x in options:
                x.update({'postproc' : 0})
            return Response(options)

    def function_hare_droop(self, options, numEscanos, q, e, r, sum_e, out):
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

    def hare(self, options, numEscanos):
        out = []

        e, r = [], []
        sum_e = 0
        m = sum([opt['votes'] for opt in options])
        q = round(m/numEscanos, 3)

        return self.function_hare_droop(options, numEscanos, q, e, r, sum_e, out)


    def droop(self, options, numEscanos):
        out = []

        e, r = [], []
        sum_e = 0
        m = sum([opt['votes'] for opt in options])
        q = round(1 + m / (numEscanos + 1))

        return self.function_hare_droop(options, numEscanos, q, e, r, sum_e, out)

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
        elif t == 'DROOP':
            return self.droop(options=opts, numEscanos=numEscanos)
        elif t == 'MULTIPREGUNTAS':
            questions = request.data.get('questions', [])
            return self.multiPreguntas(questions)


        return Response({})
