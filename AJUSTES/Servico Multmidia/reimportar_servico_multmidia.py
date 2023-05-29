from apps.admcore import models as admmodels
import csv

contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj_multimidia = admmodels.Grupo.objects.filter(nome='multimidia').order_by('-id')[0]

with open('/tmp/vigo-clientes-telefonia-outros.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:

        idcontrato = int(row[0])
        cliente = cliente_check = admmodels.Cliente.objects.filter(id=idcontrato)
        plano_descricao = row[29].strip()

        status = row[42]        
        if status == 'L':
            status_s = 1
    
        if status == 'B':
            status_s = 4
    
        if status == 'X':
            status_s = 3

        try:
            admmodels.PlanoInternet.objects.filter(plano__descricao__lower__iexact=plano_descricao.lower()).delete()
        except Exception as e:
            print(e)
        try:
            plano = admmodels.Plano.objects.filter(descricao__lower__iexact=plano_descricao.lower())[0]
            if plano:
                try:
                    plano.contrato = contrato_obj
                    plano.grupo = grupo_obj_multimidia
                    plano.save()
                    new_plano = plano
                except Exception as e:
                    print('Erro ao atualizar PLNO, erro: ', e)
                    break
            else:
                plano = admmodels.Plano()
                plano.descricao = plano_descricao
                plano.contrato = contrato_obj
                plano.grupo = grupo_obj_multimidia
                try:
                    plano.save()
                    new_plano = plano
                except Exception as e:
                    print('Erro ao criar novo PLANO, erro: ', e)
                    break

            planotv = admmodels.PlanoMultimidia()
            planotv.plano = new_plano
            planotv.save()
        except Exception as e:
            print('Erro ao criar PLANO DE MULTIMIDA, erro: ', e)
            break
        
        cliente = admmodels.Cliente.objects.filter(id=idcontrato)
        if len(cliente) > 0:
            new_servico = admmodels.ServicoMultimidia()
            new_servico.clientecontrato = admmodels.ClienteContrato.objects.filter(cliente=cliente[0])[0]
            new_servico.status = status_s
            new_servico.endereco = cliente[0].endereco
            new_servico.email_password='senha'
            new_servico.central_password='senha'
            new_servico.email=
            new_servico.nas=None
            new_servico.plano = planotv
            new_servico.data_cadastro=None
            try:
                new_servico.save()
            except Exception as e:
                print('Erro ao criar novo SERVICO DE MULTIMIDEA, erro: ', e)
                break