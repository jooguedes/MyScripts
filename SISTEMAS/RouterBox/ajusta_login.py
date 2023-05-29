#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import argparse
import csv
from turtle import update 
import re
from apps.admcore import  models as admmodels
with open('/tmp/Ajusta-senhas.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[6]
        senha=row[7]
        admmodels.ServicoInternet.objects.filter(login=login).update(login_password=senha, login_password_plain=senha)