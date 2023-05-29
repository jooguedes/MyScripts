from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from datetime import datetime
import csv

contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj_telefonia=admmodels.Grupo.objects.filter(nome='telefonia').order_by('-id')[0]
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]


with open('/tmp/vigo-clientes-telefonia-outros.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:

        idcontrato = int(row[0])
        cliente = cliente_check = admmodels.Cliente.objects.filter(id=idcontrato)
        print(cliente)
        plano_descricao = row[29].strip()
        try:
            vencimento = int(row[35])
        except:
            vencimento = 10
        data_cadastro = datetime.now()
        try:
            data_cadastro=row[26]
        except:
            pass
        endereco = cliente[0].endereco
        endereco.id=None
        endereco.save()

        status = row[42]        
        if status == 'L':
            status_s = 1
            status_c = 1
    
        if status == 'B':
            status_s = 4
            status_c = 4
    
        if status == 'X':
            status_s = 3
            status_c = 3

        try:
            admmodels.PlanoInternet.objects.filter(plano__descricao__lower__iexact=plano_descricao.lower()).delete()
        except Exception as e:
            print(e)
        try:
            plano = admmodels.Plano.objects.filter(descricao__lower__iexact=plano_descricao.lower())
            if len(plano) > 0:
                try:
                    plano[0].contrato = contrato_obj
                    plano[0].grupo = grupo_obj_telefonia
                    plano[0].save()
                    new_plano = plano[0]
                except Exception as e:
                    print('Erro ao atualizar PLNO, erro: ', e)
                    break
            else:
                plano = admmodels.Plano()
                plano.descricao = plano_descricao
                plano.contrato = contrato_obj
                plano.grupo = grupo_obj_telefonia
                try:
                    plano.save()
                    new_plano = plano
                except Exception as e:
                    print('Erro ao criar novo PLANO, erro: ', e)
                    break
            
            try:
                planotelefonia = admmodels.PlanoTelefonia.objects.filter(plano__descricao__lower__iexact=plano_descricao.lower())[0]
            except:
                planotelefonia = admmodels.PlanoTelefonia()
                planotelefonia.plano = new_plano
                planotelefonia.save()
        except Exception as e:
            print('Erro ao criar PLANO DE TELEFONIA, erro: ', e)
            break
        try:
            print(admmodels.ClienteContrato.objects.get(cliente__id=idcontrato), idcontrato)
        except:
            new_cobranca = fmodels.Cobranca()
            new_cobranca.cliente = cliente[0]
            new_cobranca.endereco = endereco
            new_cobranca.portador = fmodels.Portador.objects.get(pk=1)
            new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
            new_cobranca.isento = 0
            new_cobranca.notafiscal = False
            new_cobranca.data_cadastro = data_cadastro
            new_cobranca.datacobranca1 = data_cadastro
            new_cobranca.usuariocad = usuario
            new_cobranca.formacobranca = formacobranca
            new_cobranca.status = status_c
            new_cobranca.save()

            new_cobranca.data_cadastro = data_cadastro
            new_cobranca.save()

              
            # Contrato
            new_contrato = admmodels.ClienteContrato()
            new_contrato.id=idcontrato
            new_contrato.cliente = cliente[0]
            new_contrato.pop =  admmodels.Pop.objects.get(pk=1)
            new_contrato.cobranca = new_cobranca

            new_contrato.data_inicio = data_cadastro
            new_contrato.data_cadastro = data_cadastro
            new_contrato.data_alteracao = data_cadastro
            try:
                new_contrato.save()
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()
            except Exception as e:
                print('Erro ao criar contrato, erro: ', e)


        if len(cliente) > 0:
            new_servico = admmodels.ServicoTelefonia()
            new_servico.clientecontrato = admmodels.ClienteContrato.objects.get(cliente__id=idcontrato)
            new_servico.status = status_s
            new_servico.login_password='123456@mudar'
            new_servico.login_password_plain='123456@mudar'
            new_servico.central_password='123456@mudar'
            new_servico.endereco = endereco
            new_servico.nas = None
            new_servico.plano = planotelefonia
            new_servico.data_cadastro=None
            try:
                new_servico.save()
            except Exception as e:
                print('Erro ao criar novo SERVICO DE MULTIMIDEA, erro: ', e)
                break