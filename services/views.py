# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import string
import sys
import traceback

from serializers import PaqueteriaSerializer
from constants import ORIGEN_ERROR, DESTINO_ERROR, ERROR, OK, UNKNOWN_ERROR

from prueba_scrapping import data_address
from prueba_scrapping.listeners import PaqueteExpress, Pitic, Castores, Tresguerras
from prueba_scrapping.exceptions import DestinationError, OriginationError

df = data_address('/home/roger/prueba_scrapping/equivalencias.csv')

scrape = {
    'paqueteexpress': PaqueteExpress,
    'pitic': Pitic,
    'castores': Castores,
    'tresguerras': Tresguerras
}

def services(function):
    def wrapper(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except Exception as exp:
            traceback.print_exception(*sys.exc_info())

            return Response({'description': UNKNOWN_ERROR, 'status': ERROR}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper

class IndividualScrapping(APIView):
    __TAG = 'IndividualScrapping'

    @services
    def get(self, request, pagina):
        print request.data, pagina

        serializer = PaqueteriaSerializer(data = request.data)
        pagina = string.lower(pagina)

        if serializer.is_valid():
            # print serializer.data, pagina

            if scrape.has_key(pagina):
                scrapping = scrape.get(pagina)(df)

                resultado = {}

                try:
                    source = scrapping.scrapping(
                        serializer.data['cp_origen'],
                        serializer.data['cp_destino'],
                        serializer.data['no_piezas'],
                        serializer.data['peso'],
                        serializer.data['largo'],
                        serializer.data['alto'],
                        serializer.data['ancho']
                    )
                except DestinationError as e:
                    return Response({'description': DESTINO_ERROR}, status = status.HTTP_400_BAD_REQUEST)
                except OriginationError as e:
                    return Response({'description': ORIGEN_ERROR}, status = status.HTTP_400_BAD_REQUEST)

                # print source

                total, iva, subtotal = scrapping.get_data(source)

                resultado['total'] = total
                resultado['iva'] = iva
                resultado['subtotal'] = subtotal

                return Response(resultado, status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @services
    def post(self, request, pagina):
        return self.get(request, pagina)

class WholeScrapping(APIView):
    __TAG = 'WholeScrapping'

    @services
    def get(self, request):
        print request.data

        serializer = PaqueteriaSerializer(data = request.data)

        resultados = []
        if serializer.is_valid():
            for k, v in scrape.iteritems():
                print k

                scrapping = v(df)

                resultado = {}

                try:
                    source = scrapping.scrapping(
                        serializer.data['cp_origen'],
                        serializer.data['cp_destino'],
                        serializer.data['no_piezas'],
                        serializer.data['peso'],
                        serializer.data['largo'],
                        serializer.data['alto'],
                        serializer.data['ancho']
                    )
                except DestinationError as e:
                    resultado['description'] = DESTINO_ERROR
                except OriginationError as e:
                    resultado['description'] = ORIGEN_ERROR
                except Exception as e:
                    resultado['description'] = UNKNOWN_ERROR
                else:
                    total, iva, subtotal = scrapping.get_data(source)

                    resultado['total'] = total
                    resultado['iva'] = iva
                    resultado['subtotal'] = subtotal

                sitio = {}

                sitio[k] = resultado

                resultados.append(sitio)

            return Response(resultados, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @services
    def post(self, request):
        return self.get(request)