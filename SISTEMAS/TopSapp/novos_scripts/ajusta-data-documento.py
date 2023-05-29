from apps.financeiro import models
import os, sys
import argparse
import csv
from turtle import update 
import re


with open('/tmp/topsapp-titulos-all.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        portador=row[20]
        data_documento=row[6]
        nosso_numero = row[10]
        models.Titulo.objects.filter(portador=portador, nosso_numero=nosso_numero).update(data_documento=data_documento)