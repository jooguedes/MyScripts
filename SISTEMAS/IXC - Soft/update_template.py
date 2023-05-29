from apps.netcore import models
import csv
with open('/tmp/ixc-onus-perfis.csv.utf8', 'rb') as csvfile:
    conteudo=csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        onu=models.ONU.objects.filter(phy_addr=str(row[1].replace(':','')))
        for o in onu:
            print(o)

            if row[0]=='20':
                o.onutemplate=models.ONUTemplate.objects.get(id=33)
            elif row[0]=='21':
                o.onutemplate=models.ONUTemplate.objects.get(id=32)
            elif row[0]=='22':
                o.onutemplate=models.ONUTemplate.objects.get(id=22)
            elif row[0]=='24':
                o.onutemplate=models.ONUTemplate.objects.get(id=34)
            elif row[0]=='31':
                o.onutemplate=models.ONUTemplate.objects.get(id=31)

            try:
                o.save()
            except Exception as e:
                print(e)