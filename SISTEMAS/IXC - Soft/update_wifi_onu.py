from apps.admcore import models
from apps.netcore import models as netmodels
from django.db.models import F
onu=netmodels.ONU.objects.all()
for n in onu:
    print(n.service)
    try:
    	print(models.ServicoInternet.objects.filter(id=n.service.id))
        servico=models.ServicoInternet.objects.get(id=n.service.id)
        wifi_ssid=servico.wifi_ssid
        wifi_password=servico.wifi_password
        print(wifi_ssid,wifi_password)
        netmodels.ONU.objects.filter(id=n.id).update(onu_wifi_ssid=wifi_ssid, onu_wifi_password=wifi_password)
except Exception as e:
        print(e)