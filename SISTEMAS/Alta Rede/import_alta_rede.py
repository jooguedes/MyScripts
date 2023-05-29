#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--planos', dest='planos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--logins', dest='logins', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)

#python import_altarede.py --settings=sgp.noivanet.settings --nas=1 --portador=1  --planos=Conv-JVN_PLANOS.csv --logins=Conv-JVN_LOGINS.csv --clientes=Conv-JVN_CLIENTES.csv --titulos=Conv-JVN_CONTASARECEBER.csv

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q 

from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage


if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n) 

usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]

nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)


if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idplano = int(row[0])
            if admmodels.Plano.objects.filter(id=idplano).count() == 0:
                print row
                new_plano = admmodels.Plano()
                new_plano.id = idplano
                new_plano.descricao=row[1]
                new_plano.preco = row[2]
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                new_plano.pospago = True
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=idplano
                new_plano_internet.plano = new_plano 
                new_plano_internet.download = int (row[3].strip())
                new_plano_internet.upload = int (row[4].strip())
                new_plano_internet.diasparabloqueio = 15
                new_plano_internet.save() 

if args.clientes and args.logins:
    logins = {}
    with open(args.logins, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2] not in logins:
                logins[row[2]] = [row]
            else:
                logins[row[2]].append(row)

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            logins_dados = logins.get(row[0])
            if not logins_dados:
                continue

            for l in logins_dados:
                idcliente = int(row[1])
                idcontrato = l[0]
                login = l[10]
                if not login or login=='':
                    login=str(idcliente)+'SEM LOGIN'
                senha = l[11]
                if not senha or senha=='':
                    senha='SEM SENHA'

                planoid = int(l[12])
                nome = ustr(row[3])
                cpfcnpj = ustr(row[8])[:20]
                rgie = ustr(row[9])[:20]
                profissao = ustr(row[31])
                tipo = row[6]
                sexo = row[14]
                if sexo not in ['M','F']:
                    sexo = None
                data_nasc = row[10]
                nome_pai = row[17]
                nome_mae = row[18]


                #
                # Endereço 
                #
                logradouro = "%s %s" %(row[21],row[22])
                numero = None
                try:
                    numero = int(row[15])
                except:
                    numero = None
                    logradouro += ",%s" %row[15]
                complemento = ustr(row[23])
                bairro = ustr(row[24]).strip()[0:50]
                cep = row[19]
                uf = ustr(row[26])
                cidade = ustr(row[25]).upper()[0:50]

                #
                # Contato
                #
                celular = ustr(row[29])
                telefonecom = ustr(row[28])
                email = ustrl(row[33])
                telefone = row[27]   
                servico_obs=row[20]
                if l[8]:
                    if servico_obs:
                        servico_obs = '%s \n %s' %(servico_obs,l[8])
                    else:
                        servico_obs = l[8]

                con_obs = ''
                #if con_obs == 'NENHUMA':
                #    con_obs=''

                #
                # DATAS 
                # 

                data_cadastro = row[11]


                # 
                # Contrato
                # 

                conexao_tipo = 'ppp'
                ip = None
                mac = None
                
                try:
                    vencimento = int(l[5])
                except:
                    vencimento = 10
                    print 'erro row (%s) - %s' %(row[34],ri)

                comodato = False

                isento = 0

                status_cc = 1
                status_s = 1
                status_c = 1

                status = row[52] #row[4]
                status_bloqueado = ustrl(row[42])

                if row[52] == 'ATIVO':
                    status_cc = 1
                    status_s = 1
                    status_c = 1

                    if row[4] == 'S':
                        status_cc = 4
                        status_s = 4
                        status_c = 4

                if status=='CANCELADO':
                    status_cc = 3
                    status_s = 3
                    status_c = 3
                print(l)
                print(planoid)
                if not planoid:
                    continue
                try:
                    planointernet = admmodels.PlanoInternet.objects.get(id=planoid)
                except:
                    planointernet= admmodels.PlanoInternet.objects.get(id=157)


                cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore').encode('ascii')
                try:
                    pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                    pop = pop_q
                except:
                    new_pop = admmodels.Pop()
                    new_pop.cidade=cidade_q.upper()
                    new_pop.uf= 'BA' if len(uf)>2 else uf
                    new_pop.save()
                    pop = new_pop

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
                naturalidade = ''

                print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
                print nome_pai, nome_mae, naturalidade
                print logradouro,numero or '',complemento,bairro,cidade,uf,cep
                print 'vencimento: ', vencimento, 'Plano: ', planointernet
                print telefone,telefonecom,celular,email,con_obs
                print login,senha,ip,mac
                print '####################################################'
                if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
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
                        new_endereco.save() 
                        new_endereco_cob.save()
                        new_endereco_inst.save()
                        
                        

                        
                        tp = 'f'
                        if len(fnum(cpfcnpj)) > 12:
                            tp = 'j'
                        
                        if tp == 'f':
                            new_pessoa = admmodels.Pessoa()
                            new_pessoa.tipopessoa='J'
                            
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
                        
                        # contato 2
                        if len(celular) > 4:
                            new_contato = admmodels.Contato()  
                            new_contato.tipo = 'CELULAR_PESSOAL'
                            new_contato.contato = celular 
                            new_contato.observacao = con_obs
                            new_contato.save() 
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()
                        
                        
                        # contato 3
                        if len(telefone) > 4:
                            new_contato = admmodels.Contato() 
                            new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                            new_contato.contato = telefone 
                            new_contato.save() 
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()

                        # contato 4
                        if len(telefonecom) > 4:
                            new_contato = admmodels.Contato() 
                            new_contato.tipo = 'TELEFONE_FIXO_COMERCIAL'
                            new_contato.contato = telefonecom
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
                        
                        
                        # Cliente
                        #new_cliente = imodels.Cliente()
                        #new_cliente.endereco = new_endereco
                        #new_cliente.pessoa = new_pessoa
                        #new_cliente.data_cadastro = data_cadastro
                        #new_cliente.data_alteracao = data_cadastro
                        #new_cliente.ativo = True 
                        #new_cliente.save()
                        #new_cliente.data_cadastro = data_cadastro
                        #new_cliente.save()
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
                    
                    contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
                    # Contrato 
                    new_contrato = admmodels.ClienteContrato()
                    #new_contrato.id = idcontrato
                    new_contrato.cliente = new_cliente 
                    new_contrato.pop = pop
                    new_contrato.cobranca = new_cobranca
                     
                    new_contrato.data_inicio = data_cadastro 
                    new_contrato.data_cadastro = data_cadastro 
                    new_contrato.data_alteracao = data_cadastro
                    new_contrato.save()
                    
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
                    #new_servico.id = idcontrato
                    new_servico.clientecontrato = new_contrato 
                    new_servico.status = status_s
                    new_servico.login= login
                    new_servico.endereco = new_endereco_inst
                    new_servico.login_password=senha 
                    new_servico.login_password_plain=senha
                    new_servico.central_password=senha
                    if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                        new_servico.mac_dhcp = mac
                        new_servico.mac = mac

                    if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                        new_servico.ip = ip 
                    new_servico.tipoconexao = conexao_tipo
                    new_servico.nas = nas
                    new_servico.planointernet = planointernet
                    new_servico.modoaquisicao = 1 if comodato == True else 0
                    new_servico.data_cadastro=data_cadastro
                    new_servico.observacao=servico_obs
                    new_servico.save()

                    new_servico.data_cadastro=data_cadastro
                    new_servico.save()

                    m.addRadiusServico(new_servico)


if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        c = 0
        for row in conteudo:
            c += 1
            print(row)
            print(c)
            try:
                idcliente = row[0].split('.')[1]
                cliente = admmodels.Cliente.objects.filter(id=idcliente)
                if cliente:
                    cliente = cliente[0]
                    clientecontrato = cliente.clientecontrato_set.filter(status__status__in=[admmodels.CONTRATO_ATIVO,
                                                                                             admmodels.CONTRATO_SUSPENSO,
                                                                                             admmodels.CONTRATO_CANCELADO])
                    if clientecontrato:
                        clientecontrato = clientecontrato[0]
                        cobranca = clientecontrato.cobranca

                        numero_documento = row[1]
                        data_documento = row[2]
                        nosso_numero = row[1]
                        nosso_numero_f = str(nosso_numero)
                        data_vencimento = row[2]
                        data_pagamento = row[3]
                        if not data_pagamento:
                            data_pagamento = None
                        data_baixa = row[3]
                        valor = row[4]
                        valorpago = row[8]
                        if not valorpago:
                            valorpago = None
                        descricao = row[9]
                        usuario_b = usuario 
                        usuario_g = usuario 
                        usuario_c = None
                        data_cancela = None
                        if not data_pagamento:
                            data_pagamento = None
                            data_baixa = None
                            usuario_b = None
                            usuario_c = None
                            status = fmodels.MOVIMENTACAO_GERADA
                        else:
                            status = fmodels.MOVIMENTACAO_PAGA

                        data_cancela = None
                        desconto = 0.00
                        data_cancela = None

                        linha_digitavel = ''
                        codigo_barras = ''
                        observacao = ''

                        if nosso_numero:
                            if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                                dados = {'cliente': cliente,
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
                                         'linha_digitavel': codigo_barras,
                                         'codigo_barras': codigo_barras,
                                         'valor': valor,
                                         'valorpago': valorpago,
                                         'desconto': desconto,
                                         'status': status,
                                         'observacao': observacao
                                         }
                                #print dados
                                print "Importando boleto",cliente,nosso_numero,data_documento,data_vencimento,portador
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
                                    print(e)
            except Exception as e:
                print(e)