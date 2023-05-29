from apps.admcore import models

NOVA_DATA = '2021-07-25'
ID_CONTRATO = [479]

try:
    models.ClienteContrato.objects.filter(id__in=ID_CONTRATO) \
                                    .update(data_cadastro=NOVA_DATA)
except Exception as e:
    print('Erro ao alterar a data, erro: ', e)