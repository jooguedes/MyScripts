#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import codecs
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do Portador',required=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contatos', dest='contatos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamadosInternos', dest='chamadosInternos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamadosInternosMsg', dest='chamadosInternosMsg', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamadosExternos', dest='chamadosExternos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamadosExternosMsg', dest='chamadosExternosMsg', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--historicoEmails', dest='historicoEmails', type=str, help='Arquivo importacao',required=False)
args = parser.parse_args()


#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --nas=1 --pop=1 --portador=1 --clientes= --sync=1
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --contatos= 
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --titulos= --portador=2
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --chamadosInternos= 
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --chamadosInternosMsg= 
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --chamadosExternos= 
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --chamadosExternosMsg= 
#   python import_perfex.py --settings=sgp.wixnetbrasil.settings --historicoEmails= 


PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.admcore import models as admmodels
from apps.atendimento import models as amodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
from apps.cauth import models as authmodels

ust = lambda x: unicode(str(x))
ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n)

from unicodedata import normalize

from unicodedata import normalize

estados = [
  ['bahia','BA'],
  ['distrito federal','DF'],
  ['espirito santo','ES'],
  ['goias','GO'],
  ['minas gerais','MG'],
  ['parana','PR'],
  ['rio de janeiro','RJ'],
  ['rio grande do sul','RS'],
  ['santa catarina','SC'],
  ['sao paulo','SP']
]

def buscarUf(n, est):
  for e in est:
    if n.lower().strip() in e[0]:
        return e[1]
  return None

id_Contrato_chamados_internos = 2

usuario = admmodels.User.objects.get(username='sgp')

if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
    pop_default = admmodels.Pop.objects.get(pk=args.pop_id)

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            
            #CLIENTE
            idcliente = row[0]
            idcontrato = row[24]      
            if idcontrato == '':
                idcontrato = int(admmodels.ClienteContrato.objects.all().order_by('-id')[0].id)+10000
            
            if idcliente == '':
                continue
            nome = ustr(row[1])
            cpfcnpj = fnum(row[2])
            rgie = ''
            profissao = ''
            tipo = ''
            observacao=str(row[8])
            data_cadastro = row[9].split()[0]
            if not data_cadastro or data_cadastro == '':
              data_cadastro = datetime.now()
            status=row[10]
            nome_pai = ''
            nome_mae = ''
            naturalidade = ''
            
            #CONTATO
            celular = ustr(row[3])

            #ENDERECO CADASTRO
            cidade = ustr(row[4])
            cep = fnum(row[5].strip())
            uf = normalize('NFKD', unicode(row[6])).encode('ASCII', 'ignore').decode('ascii')
            if len(uf) > 2:
              uf = buscarUf(uf, estados)
            logradouro = ustr(row[7])
            numero = fnum(row[7].split(',')[-1])
            if not numero or numero =='':
                numero = None
            complemento = ''
            bairro = ''

            #ENDERECO COBRANCA
            cidade_cob = ustr(row[12])
            cep_cob = fnum(row[14].strip())
            uf_cob = normalize('NFKD', unicode(row[13])).encode('ASCII', 'ignore').decode('ascii')
            if len(uf_cob) > 2:
              uf_cob = buscarUf(uf_cob, estados)
            logradouro_cob = ustr(row[11])
            numero_cob = fnum(row[11].split(',')[-1])
            if not numero or numero =='':
                numero = None
            complemento_cob = complemento
            bairro_cob = bairro


            #ENDERECO SERVICO
            cidade_inst = ustr(row[16])
            cep_inst = fnum(row[18].strip())
            uf_inst = normalize('NFKD', unicode(row[17])).encode('ASCII', 'ignore').decode('ascii')
            if len(uf_inst) > 2:
              uf_inst = buscarUf(uf_inst, estados)
            logradouro_inst = ustr(row[15])
            numero_inst = fnum(row[15].split(',')[-1])
            if not numero or numero =='':
                numero = None
            complemento_inst = complemento
            bairro_inst = bairro

            # SERVICO
            login = cpfcnpj
            if login == '':
                login = 'SEM_CPFCNPJ_%s'%idcontrato
            senha = login


            sexo = None
            data_nasc = None

            #if con_obs == 'NENHUMA':
            #    con_obs=''


            #
            # Contrato
            #

            # Servico
            plano = ust('Default').strip()
            conexao_tipo = 'ppp'
            ip = None
            mac = None
            vencimento = 10
            comodato = False

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            if str(status) in ['1']:
                status_cc = 1
                status_s = 1
                status_c = 1
            else:
                status_cc = 3
                status_s = 3
                status_c = 3

            plano_download = 2048
            plano_upload = 1024
            plano_valor = 0.00

            login_pai = login

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                print(plano,plano_download,plano_upload,plano_valor)
                new_plano = admmodels.Plano()
                new_plano.descricao=plano
                new_plano.preco = plano_valor
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano
                new_plano_internet.download = plano_download
                new_plano_internet.upload = plano_upload
                try:
                    new_plano_internet.save()
                except:
                    new_plano_internet.download = 307200
                    new_plano_internet.upload = 307200
                    new_plano_internet.save()
                print('criado plano %s' %plano)


            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save()

            #print pop
            #print row

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ClienteContrato.objects.filter(id=idcontrato).count() == 0:
                print "Import %s" %nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

                if len(cliente_check) == 0:

                    # Endereco
                    new_endereco = admmodels.Endereco()
                    new_endereco.logradouro = logradouro
                    new_endereco.numero = numero
                    new_endereco.bairro = bairro
                    new_endereco.cep = cep
                    new_endereco.cidade = cidade
                    new_endereco.uf = uf
                    new_endereco.pais = 'BR'
                    new_endereco.complemento = complemento
                    new_endereco.pontoreferencia=''

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_inst = copy.copy(new_endereco)
                    try:
                        new_endereco.save()
                        new_endereco_cob.save()
                        new_endereco_inst.save()
                    except Exception as a:
                        print(new_endereco)
                        print(a) 

                    tp = 'f'
                    if len(fnum(cpfcnpj)) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = profissao
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.nomepai = nome_pai
                        new_pessoa.nomemae = nome_mae
                        new_pessoa.naturalidade = naturalidade
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=''
                        try:
                            new_pessoa.save()
                        except:
                            try:
                                new_pessoa.datanasc='19%s' %data_nasc[-8:]
                                new_pessoa.save()
                            except:
                                new_pessoa.datanasc=None
                                new_pessoa.save()

                    if tp == 'j':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome

                        new_pessoa.nomefantasia = nome
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = ''
                        new_pessoa.tipo = 8
                        new_pessoa.save()

                    # Cliente
                    new_cliente = admmodels.Cliente()
                    new_cliente.id = idcliente
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.observacao=observacao
                    print(new_cliente)
                    print(type(idcontrato), type(data_cadastro), type(observacao))
                    try:
                        new_cliente.save()

                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()
                    except Exception as a:
                        print('Erro ao cadastrar cliente, erro: ', a)
                        break

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



                else:
                    new_endereco = cliente_check[0].endereco

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_cob.id = None
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_inst.id = None
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    new_cliente = cliente_check[0]


                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob
                new_cobranca.portador = portador
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
                new_cobranca.isento = isento
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
                new_contrato.id = idcontrato
                new_contrato.cliente = new_cliente
                new_contrato.pop = pop_default
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = data_cadastro
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                try:
                    new_contrato.save()

                    new_contrato.data_cadastro = data_cadastro
                    new_contrato.save()
                except Exception as a:
                    print('Erro ao cadastrar CONTRATO: erro: ', a)
                    break
                
                for ic in [6,2,status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario
                    new_status.data_cadastro = data_cadastro
                    new_status.save()

                    new_status.data_cadastro = data_cadastro
                    new_status.save()

                # Servico
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() > 0:
                    print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                    login,
                                                                                    str(new_contrato.id))
                    login += str(new_contrato.id)
                new_servico.login= login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password=senha
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                    new_servico.mac_dhcp = mac
                    new_servico.mac = mac
                try:
                    if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                        new_servico.ip = ip
                except:
                    new_servico.ip = None
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro=data_cadastro
                new_servico.observacao=''
                new_servico.save()


                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

                if login != login_pai:
                    servico_pai = admmodels.ServicoInternet.objects.filter(login=login_pai)
                    if servico_pai:
                        new_cobranca.cobranca_unificada=servico_pai[0].clientecontrato.cobranca
                        new_cobranca.save()

    from apps.admcore import models as admmodels
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)

if args.contatos:
  with open(args.contatos, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo: 
      id_cliente = row[1]
      email = row[4]
      telefone = row[5]
      
      try:
        cliente = admmodels.Cliente.objects.get(id=id_cliente)
      except Exception as e:
        print(id_cliente, email, telefone)
        print('Cliente não encontrato')
        continue

      # EMAIL
      try:
        if len(email) > 4:
            new_contato = admmodels.Contato()
            new_contato.tipo = 'EMAIL'
            new_contato.contato = email
            new_contato.observacao = '%s - %s %s'%(row[6], row[2], row[3]) 
            new_contato.save()
            new_ccontato = admmodels.ClienteContato()
            new_ccontato.cliente = cliente
            new_ccontato.contato = new_contato
            new_ccontato.save()

        # TELEFONE
        if len(telefone) > 4:
            new_contato = admmodels.Contato()
            new_contato.tipo = 'CELULAR_COMERCIAL'
            new_contato.contato = telefone
            new_contato.observacao = '%s - %s %s'%(row[6], row[2], row[3]) 
            new_contato.save()
            new_ccontato = admmodels.ClienteContato()
            new_ccontato.cliente = cliente
            new_ccontato.contato = new_contato
            new_ccontato.save()
      except Exception as a:
        print('Erro ao cadastrar contato, erro: ', a)


if args.titulos:
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
    usuario = authmodels.User.objects.get(username='sgp')
    fnum = lambda n: re.sub('[^0-9.]','',n)
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                cliente = admmodels.Cliente.objects.filter(id=row[2])    
                print(cliente)
                for c in cliente:
                    djson = {}
                    contrato = c.clientecontrato_set.all()
                    if contrato:
                        contrato = contrato[0]
                        cobranca = contrato.cobranca
                        usuario = authmodels.User.objects.get(username='sgp')
                        descricao = row[12]
                        nosso_numero_f = None
                        data_documento = row[6].strip().split()[0]
                        data_vencimento = row[7].strip()
                        data_pagamento = None
                        data_cancela = None
                        valorpago = None
                        usuario_b = None 
                        numero_documento = int(row[3])
                        nosso_numero = numero_documento
                        valor = row[11]
                        if row[11] == row[19]:
                            status =  fmodels.MOVIMENTACAO_PAGA
                            usuario_b = usuario 
                            data_pagamento = row[21]
                            if data_pagamento == '':
                                data_pagamento = data_vencimento
                            data_baixa = data_pagamento 
                            valorpago = row[19]
                            if valorpago == '':
                                valorpago=valor
                            data_documento = data_vencimento
                        elif row[19] != '':
                            status =  fmodels.MOVIMENTACAO_PAGA_PARCIAL
                            valorpago_parcial = row[19]
                            y, m, d = row[22].split()[0].split('-')
                            data_pagamento_parcial = '%s/%s/%s %s'%(d, m, y, row[22].split()[1])
                            djson = {
                            "pagamentos": [{
                                        "data_pagamento": data_pagamento_parcial,
                                        "user_id": 2,
                                        "formapagamento_id": 1,
                                        "pontorecebimento_descricao": "Ponto Local",
                                        "formapagamento_descricao": "Dinheiro",
                                        "observacao": "",
                                        "valor_pago": valorpago_parcial,
                                        "user_username": "sgp",
                                        "caixalancamento_id": 129,
                                        "pontorecebimento_id": 2,
                                        "data_cadastro": data_pagamento_parcial,
                                        "motivodesconto": "2222",
                                        "desconto": "0.00"
                                    }], 
                            }
                            data_documento = data_vencimento
                        else:
                            data_pagamento = None
                            data_baixa = None 
                            status = fmodels.MOVIMENTACAO_GERADA
                        
                        if row[23].strip() == '5':
                            data_cancela = data_vencimento
                            status = fmodels.MOVIMENTACAO_CANCELADA
                            data_baixa = None
                            data_pagamento = None
                            usuario_b = None
                            usuario_c = usuario

                        desconto = row[13]
                        linha_digitavel = ''
                        codigo_barras = ''
                        codigo_carne = ''

                        if nosso_numero:
                            if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                                dados = {'cliente': c,
                                        'cobranca': cobranca,
                                        'portador': portador,
                                        'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                                        'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                                        'modogeracao': 'l',
                                        'usuario_g': usuario,
                                        'usuario_b': usuario,
                                        'demonstrativo': descricao,
                                        'data_documento': data_documento,
                                        'data_alteracao': data_documento,
                                        'data_vencimento': data_vencimento,
                                        'data_cancela': data_cancela,
                                        'data_pagamento': data_pagamento,
                                        'data_baixa': data_baixa,
                                        'numero_documento': numero_documento,
                                        'nosso_numero': nosso_numero,
                                        'nosso_numero_f': nosso_numero_f,
                                        'linha_digitavel': linha_digitavel,
                                        'codigo_barras': codigo_barras,
                                        'valor': valor,
                                        'valorpago': valorpago,
                                        'desconto': desconto,
                                        'status': status,
                                        'observacao': codigo_carne,
                                        'djson': djson                                
                                    }
                                #print dados
                                print("Importando boleto",c,nosso_numero,data_vencimento,portador)
                                try:
                                    titulo = fmodels.Titulo(**dados)
                                    titulo.save()
                                    nosso_numero_f = titulo.getNossoNumero()
                                    if nosso_numero_f:
                                        titulo.nosso_numero_f = re.sub('[^0-9A-Z]', '', nosso_numero_f) 
                                    titulo.data_documento=data_documento
                                    titulo.data_alteracao=data_documento
                                    titulo.save()
                                    titulo.updateDadosFormatados()
                                except Exception as e:
                                    print("Erro cadastrar",e,dados)
                            else:
                                try:
                                    djson = fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador)[0].djson
                                    djson['pagamentos'].append({
                                            "data_pagamento": data_pagamento_parcial,
                                            "user_id": 2,
                                            "formapagamento_id": 1,
                                            "pontorecebimento_descricao": "Ponto Local",
                                            "formapagamento_descricao": "Dinheiro",
                                            "observacao": "",
                                            "valor_pago": valorpago_parcial,
                                            "user_username": "sgp",
                                            "caixalancamento_id": 129,
                                            "pontorecebimento_id": 2,
                                            "data_cadastro": data_pagamento_parcial,
                                            "motivodesconto": "2222",
                                            "desconto": "0.00"
                                        })
                                    titulo = fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador)[0]
                                    titulo.djson=djson
                                    titulo.save()
                                except Exception as a:
                                    print(a)
                                    break
            except Exception as e:
                print('nao achei login %s : %s' %(cliente,e))
                continue

if args.chamadosInternos:
    with open(args.chamadosInternos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=id_Contrato_chamados_internos)
                if clientecontrato:
                    print(row)
                    ocorrencia = {} 
                    ocorrencia['id'] = int(fnum(row[0]))
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    try:
                        if amodels.Tipo.objects.filter(descricao='suporte - Chamados Internos').count() == 0:
                            dados = {}
                            dados['codigo'] = int(amodels.Tipo.objects.all().order_by('-codigo')[0])+10
                            dados['descricao'] = 'suporte - Chamados Internos'
                            new_tipo = amodels.Tipo(**dados)
                            new_tipo.save()
                            new_motivoos = amodels.MotivoOS(**dados)
                            new_motivoos.save()

                        ocorrencia['tipo'] = amodels.Tipo.objects.get(descricao='suporte - Chamados Internos')
                    except:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(codigo=5)

                    ocorrencia['usuario'] = usuario
                    ocorrencia['numero'] = int(row[0])
                    if row[6] == 'ABERTO':
                        ocorrencia['status'] = amodels.OCORRENCIA_ABERTA
                    else:
                        ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA
                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['data_cadastro'] = row[4].split()[0]
                    ocorrencia['observacoes'] = 'Prioridade: %s, %s'%(row[3], row[1])
                    if row[5] != '':
                        ocorrencia['data_agendamento'] = row[5]
                    else:
                        ocorrencia['data_agendamento'] = None
                    
                    if row[6] != '':
                        ocorrencia['data_finalizacao'] = row[6].split()[0]
                    else:
                        ocorrencia['data_finalizacao'] = None

                    ocorrencia['conteudo'] = row[2]
                    for ok in ocorrencia:
                        if ocorrencia[ok] == '0000-00-00 00:00:00':
                            ocorrencia[ok] = None
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    try:
                        new_ocorrencia.save()

                        new_ocorrencia.data_cadastro= ocorrencia['data_cadastro']
                        new_ocorrencia.save()
                    except Exception as e:
                        print('Erro ao cadastrar OCORRENCIA, erro:', e)
        
                    ordem = {}
                    ordem['id'] = int(row[0])
                    ordem['ocorrencia'] = amodels.Ocorrencia.objects.get(id=int(row[0]))
                    ordem['status'] = amodels.OS_ENCERRADA if row[6] != '' else amodels.OS_ABERTA
                    ordem['usuario'] = usuario
                    ordem['setor'] = ocorrencia['setor']
                    try:
                        ordem['motivoos'] = new_motivoos
                    except:
                        ordem['motivoos'] = amodels.MotivoOS.objects.get(codigo=40)
                    ordem['data_cadastro'] = ocorrencia['data_cadastro']
                    ordem['data_agendamento'] = ocorrencia['data_agendamento']
                    ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                    ordem['conteudo'] = ocorrencia['conteudo']
        
                    for oser in ordem:
                        if ordem[oser] == '0000-00-00 00:00:00':
                            ordem[oser] = None
                    new_ordem = amodels.OS(**ordem)
                    new_ordem.save()

                    new_ordem.data_cadastro= ocorrencia['data_cadastro']
                    new_ordem.save()

            except Exception as e:
                print(e)

if args.chamadosInternosMsg:
    with open(args.chamadosInternosMsg, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            protocolo = row[2]
            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            try:
                data= row[4]
            except:
                data='sem data'
            anotacao= row[1]
            try:
                ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
            except:
                continue
            usuario= usuario
            print(ocorrencia, usuario, data, anotacao)
            if ocorrencia:
                new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                new_ocorrencia_anotacao.ocorrencia= ocorrencia
                new_ocorrencia_anotacao.anotacao=str(data) + ' :: '+ str(anotacao)
                new_ocorrencia_anotacao.usuario= usuario
                new_ocorrencia_anotacao.save()

                new_ocorrencia_anotacao.data_cadastro=data
                new_ocorrencia_anotacao.save()




try:
    incremente_ocorrencia = int(amodels.Ocorrencia.objects.all().order_by('-numero')[0])
except:
    incremente_ocorrencia = 0

if args.chamadosExternos:
    with open(args.chamadosExternos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                idContrato = int(row[1])
                clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=idContrato)
                if clientecontrato:
                    print(row)
                    ocorrencia = {} 
                    ocorrencia['id'] = int(fnum(row[0]))
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    try:
                        if amodels.Tipo.objects.filter(descricao=row[7]).count() == 0:
                            try:
                                dados = {}
                                dados['descricao'] = row[7].strip()
                                dados['codigo'] = str(int(amodels.Tipo.objects.all().order_by('-codigo')[0].codigo)+100)
                                new_tipo = amodels.Tipo(**dados)
                                new_tipo.save()
                                new_motivoos = amodels.MotivoOS(**dados)
                                new_motivoos.save()
                            except Exception as a:
                                print('Erro ao cadastrar MotivoOS, erro: ', a)
                                break

                        ocorrencia['tipo'] = amodels.Tipo.objects.get(descricao__lower__trim=row[7].strip().lower())
                    except:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(codigo=5)
                    
                    ocorrencia['usuario'] = usuario
                    ocorrencia['numero'] = int(row[0])
                    if row[6] == 'Fechado':
                        ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA
                    else:
                        ocorrencia['status'] = amodels.OCORRENCIA_ABERTA
                    
                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    
                    ocorrencia['data_cadastro'] = row[10].split()[0]
                    if (fnum(ocorrencia['data_cadastro']) == '' or ocorrencia['data_cadastro'] == 'grep'):
                        ocorrencia['data_cadastro'] = datetime.now()
                    ocorrencia['observacoes'] = 'Prioridade: %s, E-mail: %s, Telefone: %s'%(row[5], row[2], row[3])
                    try:
                        if ocorrencia['data_cadastro'] != '':
                            ocorrencia['data_agendamento'] = ocorrencia['data_cadastro']
                        else:
                            ocorrencia['data_agendamento'] = None
                    
                        if row[11] != '':
                            ocorrencia['data_finalizacao'] = row[11].split()[0]
                        else:
                            ocorrencia['data_finalizacao'] = None
                    
                        ocorrencia['conteudo'] = row[8]+' - '+row[9]
                        for ok in ocorrencia:
                            if ocorrencia[ok] == '0000-00-00 00:00:00':
                                ocorrencia[ok] = None
                    
                        new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                        new_ocorrencia.save()
                        new_ocorrencia.data_cadastro=ocorrencia['data_cadastro']
                        new_ocorrencia.save()
                    except Exception as a:
                        print('Erro ao cadastrar OCORRENCIA, erro: ', a)
                        break
                    
                    
                    ordem = {}
                    ordem['id'] = int(row[0])
                    ordem['ocorrencia'] = new_ocorrencia
                    ordem['status'] = amodels.OS_ENCERRADA if row[6] == 'Fechado' else amodels.OS_ABERTA
                    ordem['usuario'] = usuario
                    ordem['setor'] = ocorrencia['setor']
                    try:
                        try:
                            ordem['motivoos'] = amodels.MotivoOS.objects.get(descricao=descricao)
                        except:
                            ordem['motivoos'] = amodels.MotivoOS.objects.get(codigo=40)
                        ordem['data_cadastro'] = ocorrencia['data_cadastro']
                        ordem['data_agendamento'] = ocorrencia['data_agendamento']
                        ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                        ordem['conteudo'] = ocorrencia['conteudo']
            
                        for oser in ordem:
                            if ordem[oser] == '0000-00-00 00:00:00':
                                ordem[oser] = None
                        new_ordem = amodels.OS(**ordem)
                        new_ordem.save()

                        new_ordem.data_cadastro = ocorrencia['data_cadastro']
                        new_ordem.save()
                    except Exception as a:
                        print('Erro ao cadastrar OS, erro: ', a)
                        break

            except Exception as e:
                print(e)

if args.chamadosExternosMsg:
    with open(args.chamadosExternosMsg, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[1] != '':
                protocolo = str(int(row[2])+incremente_ocorrencia)
                if len(protocolo) > 14:
                    protocolo = protocolo[0:13]
                try:
                    data= row[4]
                except:
                    data='sem data'
                anotacao= row[1]
                try:
                    ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                except:
                    continue
                usuario= usuario
                print(ocorrencia, atendente,usuario,data,anotacao)
                if ocorrencia:
                    new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                    new_ocorrencia_anotacao.ocorrencia= ocorrencia
                    new_ocorrencia_anotacao.anotacao='Criado em: ' + str(data) + ' \n '+ str(anotacao)
                    new_ocorrencia_anotacao.usuario= usuario
                    new_ocorrencia_anotacao.save()

                    new_ocorrencia_anotacao.data_cadastro= data
                    new_ocorrencia_anotacao.save()

if args.historicoEmails:
    with open(args.historicoEmails, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)