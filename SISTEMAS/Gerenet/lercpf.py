import csv 
import re 
cpfs=[]
with open('clientes_atuais.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cpfs.append(row[0])




print(cpfs, type(cpfs))