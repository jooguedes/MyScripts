from apps.admcore import models as admmodels
with open('/tmp/Conv-Assinantes.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            print(admmodels.Endereco.objects.filter(servicointernet__clientecontrato__cliente__pessoa__cpfcnpj__numfilter=row[3]).update(map_ll=row[22]))
            print(admmodels.Endereco.objects.filter(cobranca__clientecontrato__cliente__pessoa__cpfcnpj__numfilter=row[3]).update(map_ll=row[22]))






from apps.admcore import models as admmodels
with open('/tmp/Conv-coordeanas-hopesfiber.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    if str(row[18])!='' and str(row[19]!=''):
        map_ll=str(row[18]) + ',' +str(row[19])
       
        admmodels.Endereco.objects.filter(servicointernet__clientecontrato__cliente__id=row[1]).update(map_ll=row[20])