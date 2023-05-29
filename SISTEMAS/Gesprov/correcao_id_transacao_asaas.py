from apps.financeiro import models
import csv


with open('/tmp/file', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            id_transacao_atual=row[22]
            new_id_transacao=row[21]
            portador=row[1]

            models.TituloGateway.objects.filter(titulo__portador=portador, idtrasacao=new_id_transacao,)
            