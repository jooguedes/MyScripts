#AJUSTE NOTA FISCAL ITEM
from apps.fiscal import models as fismodels
from django.db.models import F
nf=[8753,8754,8755,8756, 8757,8758,8759, 8760,8761,8762,8763,8764,8765,8766,8767,8768,8769,8770,8771,8772,8773,8774,8775,8776,8777,8778,8779,8780,8781,8782,8783,8784,8785,8786,8787,8788,8789,8790,8791,8792]
for n in nf:
    #print(n)
    try:
        nftitulo=fismodels.NotaFiscalItem.objects.filter(id=n)
        for nt in nftitulo:
            nota_id=int(nt.notafiscal_id) + 8751
            fismodels.NotaFiscalItem.objects.filter(id=nt.id).update(notafiscal=nota_id)
            print(nt, nota_id)
    except Exception as e:
            print(e)