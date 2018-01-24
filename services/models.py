# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Paqueteria(models.Model):
    cp_origen = models.IntegerField()
    cp_destino = models.IntegerField()
    peso = models.FloatField()
    no_piezas = models.IntegerField()
    alto = models.FloatField()
    largo = models.FloatField()
    ancho = models.FloatField()
