from rest_framework.views import APIView
from rest_framework.response import Response


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


        #Primer for: Se añade un campo para el contador de escaños asignados a cada opción.
        #Segundo for: Para cada escaño, se recorren todas las opciones, usando la fórmula de d'Hont: número de votos a esa opción / (número de escaños asignados a esa opción + 1)
        #Lista de tamaño igual al número de opciones. Representa el recuento al aplicar la fórmula de cada opción, ordenados en la misma forma.
        #Se obtiene el índice del máximo valor en la lista de recuento de votos, es decir, el índice del ganador del escaño
        #Al estar ordenadas de la misma forma, en la posicion del ganador se le suma 1 escaño
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

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | DHONT 
         * options: [
            {
             option: str,
             number: int,
             votes: int,
            }
         * numEscanos: int
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanos = request.data.get('numEscanos', 0)

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'DHONT':
            return self.dHont(options=opts, numEscanos=numEscanos)

        return Response({})
