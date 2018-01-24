from rest_framework import serializers

from models import Paqueteria

class PaqueteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paqueteria
        fields = ('cp_origen', 'cp_destino', 'no_piezas', 'peso', 'alto', 'largo', 'ancho')
