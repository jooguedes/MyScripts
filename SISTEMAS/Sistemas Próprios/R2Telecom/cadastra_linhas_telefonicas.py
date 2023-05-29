#CADASTRO DE LINHAS
from datetime import datetime
from apps.admcore import models
import csv
with open('/tmp/Conv-exporta_contratos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        numero=row[13] or row[14]
        try:
            servicotelefonia= models.ServicoTelefonia.objects.filter(clientecontrato__cliente__id=row[0])[0]
        except:
            continue

        if str(row[13])!='':
            data_cadastro=datetime.now()
            dialpassword=row[16]
            id_cliente=row[13] or row[14]
            web_password=row[15]
            secret=row[14]
            djson={"dialpassword": dialpassword, 
                        "id_cliente": id_cliente, 
                        "userid": id_cliente, 
                        "webpassword": web_password, 
                        "id_ativacao": id_cliente, 
                        "secret": secret}

            new_linha=models.ServicoTelefoniaLinha()
            try:
                new_linha.servicotelefonia=models.ServicoTelefonia.objects.get(login=row[4])
            except:
                continue
            new_linha.numero=numero
            new_linha.djson=djson
            try:
                new_linha.save()
            except Exception as e:
                print('Erro ao salvar Linha: ', e)
        else:
            print('não tem linha associada')

