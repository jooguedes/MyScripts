#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.wsgi import get_wsgi_application
import argparse
from nis import cat
import os
import sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re
from decimal import Decimal
import codecs
from warnings import catch_warnings
import shutil

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django', required=True)
parser.add_argument('--sync', dest='sync_db', type=bool, help='Sync Database', default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo de postadores')
parser.add_argument('--pop', dest='pop', type=str, help='Arquivo de postadores',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Arquivo de postadores', required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo de postadores', required=False)
parser.add_argument('--ocorrencias', dest='ocorrencias', type=str, help='Arquivo de postadores', required=False)
parser.add_argument('--nf2122', dest='nf2122', type=str, help='Arquivos Notas fiscais', required=False)

# python import_hubsoft.py --settings=sgp.local.settings --pop=1 --nas=1 --clientes= --sync=1
# python import_hubsoft.py --settings=sgp.local.settings --portadores= --sync=1
# python import_hubsoft.py --settings=sgp.local.settings --titulos=hubsoft-titulos.csv --sync=1
# python import_hubsoft.py --settings=sgp.local.settings --ocorrencias=hubsoft-titulos.csv --sync=1
# python import_hubsoft.py --settings=sgp.local.settings --nf2122=hubsoft-notafiscal.csv
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
application = get_wsgi_application()
from django.db.models import Q
from apps.atendimento import models as amodels
from apps.netcore.utils.radius import manage
from apps.netcore import models as nmodels
from apps.fiscal import models as fismodels, constants as fisconstants
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels



#FUNCOES AUXILIARES
def fnum(n): return re.sub('[^0-9]', '', unicode(n))


def valida_data(dt):

    if len(dt.split(' '))>1:
        return dt.split(' ')[0]
    elif dt:
        return datetime.now()

def verifica_vencimento(v):
    if v=='ultimo_dia':
        return 23
    if v!='':
        if fmodels.Vencimento.objects.filter(dia=v).count() > 0:
            return int(v.strip())
        else:
            new_vencimento= fmodels.Vencimento()
            new_vencimento.dia=int(v.strip())
            new_vencimento.save()

            return int(v.strip())
    else:
        if fmodels.Vencimento.objects.filter(dia=10) > 0:
            return 10
        else:
            new_vencimento= fmodels.Vencimento()
            new_vencimento.dia=10
            new_vencimento.save()
            return 10


#VARIAVEIS GLOBAIS    
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome__icontains='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome__icontains='fibra').order_by('-id')[0]

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            
            codigo_banco = '999'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print row
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[2]
                new_portador.codigo_banco = codigo_banco
                new_portador.agencia =  '0'
                new_portador.agencia_dv = '0'
                new_portador.conta =  '0'
                new_portador.conta_dv = '0'
                new_portador.convenio = '0'
                new_portador.carteira = '0'
                new_portador.cedente = 'PROVEDOR X'
                new_portador.cpfcnpj = '0'
                new_portador.save()




if args.clientes:
    nas = nmodels.NAS.objects.all()[0]
    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    m = manage.Manage()

    with codecs.open(args.clientes, 'ru') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')

        for row in conteudo:
          
            if admmodels.ServicoInternet.objects.filter(login=row[15]).count() != 0:
                continue
            print row

            idcliente = int(row[0])

            idcontrato = int(row[33])
            if idcliente!='':
                pass
            else:
                continue

            if idcontrato=='' and idcliente!='':
                idcontrato=idcliente
           
            nome = row[1]
            nomefantasia = row[2]
            tipo = 'F' if row[7]=='pf' else 'J'
            rgie = row[6][0:20]
            sexo = ''
            data_nasc = valida_data(row[32])
            profissao = row[14]
            cpfcnpj = row[5][0:20]

            endereco_inst = {}
            endereco_inst['logradouro'] = row[28]  
            try:
                endereco_inst['numero'] = int(row[25])  
            except:
                endereco_inst['numero'] = None
            endereco_inst['complemento'] = row[26]
            endereco_inst['bairro'] = row[27][0:40]
            endereco_inst['cidade'] = row[31][0:40]
            endereco_inst['uf'] = 'PE'
            endereco_inst['cep'] = fnum(row[29])
            endereco_inst['pontoreferencia'] = ''

            celular = row[3]  
            celularcom = row[4]
            email = row[8]  
            email2=row[9]

            nomepai = row[12]
            nomemae = row[13]
        
            status = row[11]
            login = row[15]
            senha= row[16]
            if not login:
                login = 'semlogin_%s' % idcontrato
            if senha=='':
                senha='sem_senha'
            plano=row[17]
            try:
                plano = admmodels.PlanoInternet.objects.filter(plano__id=row[17])[0]
            except Exception:
                new_plano = admmodels.Plano()
                new_plano.id=row[17]
                new_plano.descricao=row[18]
                new_plano.preco = row[19]
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=row[17]
                new_plano_internet.plano = new_plano
                new_plano_internet.download = int(fnum(row[20]).strip())
                new_plano_internet.upload = int(fnum(row[21].strip()))
                try:
                    new_plano_internet.save()
                except Exception as e:
                    print(e)
                    new_plano_internet.download = 307200
                    new_plano_internet.upload = 307200
                    new_plano_internet.save()
                
                plano = admmodels.PlanoInternet.objects.filter(plano__id=row[17])[0]
                print('criado plano %s' %plano)
           
            portador = row[23]
            vencimento = verifica_vencimento(row[22])


            data_cadastro = valida_data(row[10])
            data_ativacao = data_cadastro


            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" % vencimento
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save()

            pop = admmodels.Pop.objects.filter(id=args.pop)[0]
            nas = nmodels.NAS.objects.filter(id=args.nas)[0]
            conexao_tipo = 'ppp'
            status_cc = 1
            status_s = 1
            status_c = 1

            if status in ['f']:
                status_cc = 3
                status_s = 3
                status_c = 3


            status_criar = [6, 2, status_cc]

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" % vencimento
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' % vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()

            # print pop
            # print row
            print status, login, nome, cpfcnpj, len(cpfcnpj), sexo, data_cadastro, data_nasc
            print endereco_inst
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print celular, email
            print login, senha
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" % nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

                if len(cliente_check) == 0:

                    # Endereco
                    new_endereco = admmodels.Endereco(**endereco_inst)
                    new_endereco_cob = admmodels.Endereco(**endereco_inst)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    new_endereco.save()
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    if tipo == 'F':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa = 'F'
                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = profissao
                        new_pessoa.nomepai = nomepai
                        new_pessoa.nomemae = nomemae
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor = ''
                        new_pessoa.save()

                    if tipo == 'J':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa = 'J'
                        new_pessoa.nome = nome
                        new_pessoa.nomefantasia = nomefantasia
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.tipo = 8
                        new_pessoa.save()
                        

                    # Cliente
                    new_cliente = admmodels.Cliente()
                    new_cliente.id = idcliente
                    new_cliente.pessoa = new_pessoa
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    if data_cadastro in ('0000-00-00'):
                        data_cadastro = datetime.now()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.observacao = ''
                    new_cliente.save()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()

                    # contato 1
                    if len(email) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'EMAIL'
                        new_contato.contato = email
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    if len(email2) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'EMAIL'
                        new_contato.contato = email2
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()


                    # contato 2
                    if len(celular) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular
                        new_contato.observacao = ''
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 5
                    if len(celularcom) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'CELULAR_COMERCIAL'
                        new_contato.contato = celularcom
                        new_contato.observacao = ''
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                else:
                    new_endereco = cliente_check[0].endereco

                    new_endereco_cob = admmodels.Endereco(**endereco_inst)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    new_cliente = cliente_check[0]

                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob

                try:
                    new_cobranca.portador = fmodels.Portador.objects.get(
                        pk=portador)
                except:
                    new_cobranca.portador = fmodels.Portador.objects.all()[0]

                new_cobranca.vencimento = fmodels.Vencimento.objects.get(
                    dia=vencimento)
                new_cobranca.notafiscal = False
                if str(data_cadastro) in ('0000-00-00'):
                    data_cadastro = datetime.now()
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
                new_contrato.id = idcontrato

                new_contrato.cliente = new_cliente
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = data_cadastro
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()

                for ic in status_criar:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo = 2
                    new_status.usuario = usuario
                    new_status.data_cadastro = data_cadastro
                    new_status.save()

                    new_status.data_cadastro = data_cadastro
                    new_status.save()

                # Servico
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                    print u'Já existe serviço com o login %s. Ajustando login: %s%s' % (login,
                                                                                        login,
                                                                                        str(new_contrato.id))
                    login += str(new_contrato.id)
                new_servico.login = login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password = senha
                new_servico.login_password_plain = senha
                new_servico.central_password = senha
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = plano
                new_servico.modoaquisicao =  0
                new_servico.data_cadastro = data_cadastro
                new_servico.save()
                new_servico.data_cadastro = data_cadastro
                new_servico.save()
                m.addRadiusServico(new_servico)



if args.titulos:
    with codecs.open(args.titulos, 'ru') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')

        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(clientecontrato__id=row[9])
            if not cliente:
                    continue

            cobranca = None
            contrato = None

            if cliente:
                cliente = cliente[0]
                contrato = admmodels.ClienteContrato.objects.filter(id=row[9])
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca

                
                portador = fmodels.Portador.objects.filter(id=row[1])
                if not portador:
                    continue
                else:
                    portador = portador[0]
                try:
                    nosso_numero=int(row[2])
                except:
                    continue
                if fmodels.Titulo.objects.filter(portador=portador, nosso_numero=row[2]).count() == 0:
                    print row
                    print('Passei do IF')
                    tdata = {}
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[2]  # nrboleto
                    tdata['numero_documento']= row[2]
                    tdata['parcela'] = 1  # parcela
                    tdata['portador'] = portador
                    tdata['valor'] = row[4]
                    tdata['observacao'] = ''
                    tdata['demonstrativo'] = ''
                    tdata['valorpago'] = row[5]
                    tdata['data_baixa'] = row[7]
                    tdata['data_pagamento'] = row[7]
                    tdata['data_documento'] = row[8]  # emissao
                    
                    tdata['data_vencimento'] = row[6]  # vencimento
                    if tdata['valorpago'] == '0' or tdata['valorpago'] == '' or tdata['valorpago'] == '0.00':
                        tdata['valorpago'] = None
                    tdata['usuario_b'] = usuario  # usuariobaixa 28
                    tdata['usuario_g'] = usuario  # usuariogerou 29
                    tdata['usuario_c'] = usuario  # usuariocancela 30
                    tdata['modogeracao'] = 'l'
                    tdata['motivocancela'] = None
                    tdata['motivodesconto'] = None

                    tdata['centrodecusto'] = fmodels.CentrodeCusto.objects.get(
                        codigo='01.01.01')
                    for k in tdata:
                        if tdata[k] in ['NULL', '0000-00-00', '']:
                            tdata[k] = None
                    if tdata['data_pagamento'] is None:
                        tdata['usuario_b'] = None
                        tdata['usuario_c'] = None


                    if tdata['data_pagamento'] :
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                        
                    else:
                        tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                    if tdata['demonstrativo'] is None:
                        tdata['demonstrativo'] = ''

                    print tdata
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']

                    new_titulo.save()




if args.ocorrencias:
    with codecs.open(args.ocorrencias, 'ru') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(id=row[2])
                if clientecontrato and amodels.Ocorrencia.objects.filter(numero=row[1][:13]).count()==0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['id'] = int(row[0])
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                
                    ocorrencia['tipo'] = amodels.Tipo.objects.get(id=6)
                    ocorrencia['usuario'] = usuario
                    ocorrencia['numero'] = row[1][:13]
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if row[7] != '' else amodels.OCORRENCIA_ABERTA

                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['data_cadastro'] = row[6]
                    ocorrencia['data_agendamento'] = None
                    ocorrencia['data_finalizacao'] = None if '0000-00-00' in row[7] or row[7]=='' else valida_data(row[7])
                    ocorrencia['conteudo'] = row[4] + "\n" + row[5]
                   
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()
                    new_ocorrencia.data_cadastro = row[6]
                    if new_ocorrencia.data_cadastro=='':
                        new_ocorrencia.data_cadastro= datetime.now()
                    
                    new_ocorrencia.save()
                else:
                    print('Ocorrencia já importada')
            except Exception as e:
                print(e)




if args.nf2122:
    with codecs.open(args.nf2122, 'ru') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[9]=='':
                cpfcnpj=='12924770000100'
            else:
                cpfcnpj=row[9]
            empresa = admmodels.Empresa.objects.filter(cpfcnpj__numfilter=cpfcnpj)[0]
            if empresa:
                empresa = empresa
                # nota
                v_nota = fismodels.NotaFiscal.objects.filter(
                    empresa=empresa, numero=row[1] or 0)
                
                cfop=row[3]
                cfop = fismodels.CFOP.objects.get(cfop=cfop)
                if len(v_nota) == 0:

                    # cliente
                    cliente = admmodels.Cliente.objects.filter(
                        id=row[8], pessoa__cpfcnpj__numfilter=row[11])
                    if cliente:
                        cliente = cliente[0]
                    else:
                        cliente = admmodels.Cliente.objects.filter(
                            pessoa__cpfcnpj__numfilter=row[11])
                        if cliente:
                            cliente = cliente[0]

                    if cliente:
                        endereco = cliente.endereco
                        try:
                            clientecontrato = cliente.clientecontrato_set.filter(
                            cliente__id=cliente.id)
                        except Exception as e:
                            print(e)
                            continue
                        if clientecontrato:
                            endereco = clientecontrato[0].cobranca.endereco
                        nfdest = {}
                        nfdest['cliente'] = cliente
                        nfdest['cpfcnpj'] = cliente.getCPFCNPJ()
                        nfdest['inscricaoestadual'] = cliente.getInscricaoEstadual()
                        nfdest['razaosocial'] = cliente.getNome()
                        nfdest['logradouro'] = endereco.logradouro
                        nfdest['numero'] = endereco.numero
                        nfdest['complemento'] = endereco.complemento
                        nfdest['cep'] = endereco.cep
                        nfdest['bairro'] = endereco.bairro
                        nfdest['cidade'] = endereco.cidade
                        nfdest['uf'] = row[18] if row[18] !='' else 'PE'
                        nfdest['telefone'] = row[21] if row[21]!='' else None
                        nfdest['codigocliente'] = cliente.id
                        nfdest['tipoassinante'] = '1'
                        print(nfdest)
                        nfdest_obj = fismodels.NFDestinatario(**nfdest)
                        nfdest_obj.save()
                        nf = {}
                        nf['empresa'] = empresa
                        nf['destinatario'] = nfdest_obj
                        nf['data_emissao'] = row[4]
                        nf['data_saida'] = row[4]
                        nf['modelo'] = 21
                        nf['tipoutilizacao'] = '4'
                        nf['serie'] = row[2]
                        try:
                            nf['numero'] = int(row[1])
                        except:
                            pass
                        nf['valortotal'] = row[6]
                        nf['icms'] = row[7]
                        nf['outrosvalores'] = row[6]
                        nf['djson'] = {}
                        
                        nf['status'] = fisconstants.NOTAFISCAL_GERADA
                        nf['bcicms'] = '0.00'
                        nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                        nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                        nf['cfop'] = cfop
                        nf['usuario_g'] = usuario
                        nf['usuario_c'] = usuario
                        print(
                            "################################################NF###########################", nf)
                        new_nf = fismodels.NotaFiscal(**nf)
                        try:
                            new_nf.save()
                        except:
                            print("essa foi a data que deu erro",
                                  nf['data_emissao'], nf['data_saida'])

                        new_nf.data_emissao = nf['data_emissao']
                        new_nf.data_saida = nf['data_saida']
                        new_nf.save()
                        nfitem = {}
                        nfitem['notafiscal'] = new_nf
                        nfitem['descricao'] = row[22]
                        nfitem['codigoservico'] = '010101'
                        nfitem['classificacao'] = '0104'
                        nfitem['unidade'] = '1'
                        nfitem['qt_contratada'] = '1'
                        nfitem['qt_fornecida'] = '1'
                        nfitem['valortotal'] = row[6]
                        nfitem['desconto'] = '0.00'
                        nfitem['acrescimo_despesa'] = '0.00'
                        nfitem['bcicms'] = '0.00'
                        nfitem['icms'] = '0.00'
                        nfitem['outrosvalores'] = nf['valortotal']
                        nfitem['aliquotaicms'] = '0.00'
                        nfitem['item'] = '1'
                        nfitem['data_cadastro'] = nf['data_emissao']
                        nfitem['data_alteracao'] = nf['data_emissao']
                        print(nfitem)
                        new_nfitem = fismodels.NotaFiscalItem(**nfitem)
                        new_nfitem.save()
                        new_nfitem.data_cadastro = nf['data_emissao']
                        new_nfitem.data_alteracao = nf['data_emissao']
                        new_nfitem.save()

                        if row[23]:
                            titulo = fmodels.Titulo.objects.filter(Q(cliente=cliente),
                                                                   Q(nosso_numero=row[23], valor=row[6]))
                            if len(titulo) == 1:
                                # Cria nota fiscal com titulo
                                nft = fismodels.NotaFiscalTitulo()
                                nft.titulo = titulo[0]
                                nft.notafiscal = new_nf
                                nft.save()

