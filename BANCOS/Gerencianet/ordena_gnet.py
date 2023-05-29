# -*- coding: utf-8 -*-
import csv
from itertools import count
from operator import index
from os import sep
import pandas as pd
def array_sort(lst,key, reverse=False):
    new_list = sorted(lst, key= lambda d: d[key]) 
    if reverse:
        new_list.reverse()
        
    return new_list


df = pd.read_csv('Conta-API-GNET.csv', sep=",")

df2 = df.sort_values(['Número da Cobrança'], ascending=False)

print(df2.info())
'''df2.to_csv('file_name.csv',
 
 encoding='utf-8',
 header=False, index=False,
 na_rep='coluna_vazia',
 sep=';'

)'''

print(df)
print(df2)
'''
with open('Conta-API-GNET.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    #conteudo = array_sort(conteudo)
  
    print(list(conteudo)[0], type(conteudo))
    #tm= len(conteudo)
   # print('#####################################################\n')
   # print('esse e o conteudo da linha 0 do csv\n',conteudo[0] )
    #print('\n#####################################################')
    count=0
    for row in conteudo:
        if(count!=0):
            #print(row[0], type(row))
            pass
        count= count+1
'''
        
