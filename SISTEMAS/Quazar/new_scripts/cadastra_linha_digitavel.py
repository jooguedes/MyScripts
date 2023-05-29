from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels

import csv
import re
from datetime import date, datetime

#nosso_numero = tf.getNossoNumero(portador) +

with open('/tmp/Titulos_Luana_Patricia.csv ', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[0]
        linha_digitavel=row[8]
        fmodels.Titulo.objetcs.filter(cliente__clientecontrato__servicointernet__login=login, numero_documento=row[2], portador=3).update(codigo_barras=linha_digitavel, linha_digitavel=linha_digitavel)