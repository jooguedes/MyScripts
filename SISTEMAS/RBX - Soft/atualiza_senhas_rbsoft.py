#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import re
from apps.admcore import models as admmodels
from django.db.models import Q, Max


with open('/opt/Atualizar_Senhas.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[5]
        senha=row[6]    
        
        try:
            admmodels.ServicoInternet.objects.filter(login__trim__lower=login.lower().strip()).update(login_password=senha, login_password_plain=senha)
        except:
            continue