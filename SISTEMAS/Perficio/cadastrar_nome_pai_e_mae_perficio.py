import csv
from logging import exception
import re 
from apps.admcore import models as models
from django.db.models import Q, Max

with open('/tmp/Conv-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
    	id= int(row[0]) + 140

    	if(str(row[11])!='' or str(row[12])!=''):
    		models.Pessoa.objects.filter(cliente__id=id).update(nomemae=row[12], nomepai=row[11])