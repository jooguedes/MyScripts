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
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo de titulos',required=False)
parser.add_argument('--gerencianet', dest='gerencianet', type=str, help='Arquivo de gerencianet',required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
args = parser.parse_args()

#python import_routerbox.py --settings=sgp.supernetpb.settings --portador=1 --clientes=routerbox-clientes.csv.utf8 --titulos=routerbox-titulos-id-6-gerencianet.csv.utf8 --planoadd=1 --portador=1 --nas=1 --vencimentoadd=1 --sync=1
PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

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
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)
ri = -1

incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 10000
if incrementar < 10000:
    incrementar = 10000
else:
    incrementar += 1

if args.clientes:
    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1
            idcliente = row[0]
            idcontrato = row[1]
            login = row[2]
            tipo = row[3]


            nome = ustr(row[4])
            cpfcnpj = ustr(row[5])[:20]
            rgie = ustr(row[6])[:20]
            data_nasc = row[7]
            if len(data_nasc) < 8:
                data_nasc = None
            profissao = ''
            sexo = None

            #
            # Endereço 
            #
            logradouro = ustr(row[8])
            numero = None
            try:
                numero = int(row[9])
            except:
                numero = None
                logradouro += ",%s" %row[8]
            complemento = ustr(row[10])
            bairro = ustr(row[11]).strip()[0:50]
            cep = ustr(row[12]).strip()[0:20]
            uf = ustr(row[13])
            cidade = ustr(row[14]).upper()[0:50]

            #
            # Contato
            #
            celular = ustr(row[15])
            telefonecom = ustr(row[16])
            email = ustrl(row[17])
            telefone = row[38]
            servico_obs=row[18]
            con_obs = ''
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 

            data_cadastro = row[19]
            if len(data_cadastro) < 8:
                data_cadastro=date.today().strftime('%Y-%m-%d')

            vencimento = row[20]
            desconto = row[21]
            isento = 0 if row[24] == 'N' else 100
            status = row[25]
            login = row[26]
            login = normalize('NFKD', unicode(login)).encode('ASCII','ignore')
            senha = row[27]
            if not senha:
                senha = login
            mac = row[28]
            plano = row[31]
            plano_valor = row[32]
            try:
                plano_download =int(row[33])
                plano_upload = int(row[34])
            except:
                 plano_download=0
                 plano_upload=0
            if plano_download=='' or not plano_download:
                plano_download=0
            
            if plano_upload=='' or not plano_upload:
                plano_upload=0

            print('Esse é meu upload e download: ', plano_download, plano_upload)
            '''cobendinst = row[41]
            cob_logradouro = row[42]
            cob_numero = row[43]
            cob_bairro = row[44][0:50]
            cob_cidade = row[45][0:50]
            cob_cep = row[46]
            cob_uf = row[47]
            cob_complemento = row[48]'''
            try:
                latitude = row[52]
                longitude = row[53]
            except:
                latitude = ''
                longitude = ''

            conexao_tipo = 'ppp'


            ip = None
            if len(mac) < 10: mac = None
            comodato = False

            status_cc = 1
            status_s = 1
            status_c = 1

            if status in ['B']:
                status_cc = 4
                status_s = 4
                status_c = 4

            if status in ['S','C']:
                status_cc = 3
                status_s = 3
                status_c = 3

            if vencimento == '0':
                vencimento = 10

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if args.planoadd:
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
                    new_plano_internet.save() 
                    print('criado plano %s' %plano)
                else:
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                    raise Exception('Não localizei plano %s' %plano)

            pop=admmodels.Pop.objects.get(id=1)

            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save() 

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent=login).count() == 0:
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
                    
                    if latitude and longitude:
                        new_endereco.map_ll='%s,%s' %(latitude,longitude)
                    new_endereco_cob = copy.copy(new_endereco)
                    '''if cobendinst == 'S':
                        new_endereco_cob = copy.copy(new_endereco)'''
                    '''else:
                        new_endereco_cob = admmodels.Endereco()

                        new_endereco_cob.logradouro = cob_logradouro
                        new_endereco_cob.numero = cob_numero
                        new_endereco_cob.bairro = cob_bairro
                        new_endereco_cob.cep = cob_cep
                        new_endereco_cob.cidade = cob_cidade
                        new_endereco_cob.uf = cob_uf 
                        new_endereco_cob.pais = 'BR'
                        new_endereco_cob.complemento = cob_complemento
                        if latitude and longitude:
                            new_endereco_cob.map_ll='%s,%s' %(latitude,longitude)
                        new_endereco_cob.pontoreferencia='''''

                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco.save() 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    

                    
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
        
                if len(contrato_check) == 0:
                    new_contrato.id = idcontrato
                else:
                    new_contrato.id = incrementar
                    incrementar += 1

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
                new_servico.clientecontrato = new_contrato 
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
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

    from apps.admcore import models as admmodels 
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)


if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if not row[14]:
                continue
            idcliente = row[0]
            cliente = admmodels.Cliente.objects.filter(id=idcliente)
            cobranca = None 
            contrato = None
            if cliente:
                cliente = cliente[0]
                if row[1]:
                    idcontrato = row[1]
                    contrato = cliente.clientecontrato_set.filter(id=idcontrato)
                    if contrato:
                        contrato = contrato[0]
                        cobranca = contrato.cobranca

                    elif cliente.clientecontrato_set.all():
                        contrato = cliente.clientecontrato_set.all()[0]
                        cobranca = contrato.cobranca 
                elif cliente.clientecontrato_set.all():
                    contrato = cliente.clientecontrato_set.all()[0]
                    cobranca = contrato.cobranca 

            if cliente:
                if fmodels.Titulo.objects.filter(portador=portador,
                                                 nosso_numero=row[4]).count() == 0:

                    
                    tdata = {} 
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[4] 
                    tdata['numero_documento'] = row[5] 
                    tdata['parcela'] = row[6] 
                    if not row[6]:
                        tdata['parcela'] = 1
                    tdata['portador'] = portador
                    tdata['valor'] = row[7]
                    tdata['desconto_venc'] = row[8]
                    tdata['observacao'] = row[9]
                    tdata['demonstrativo'] = ''
                    
                    tdata['desconto'] = row[11]
                    tdata['valorpago'] = None

                    if row[12]:
                        print('################### BOLETO PAGO ###########################')
                        tdata['data_pagamento'] = row[12].split()[0]
                        tdata['data_baixa'] = row[12]
                        tdata['valorpago'] = row[10]

                    else:
                        tdata['data_pagamento'] = None
                        tdata['data_baixa'] = None

                    tdata['data_documento'] = row[13] # emissao
                    tdata['data_vencimento'] = row[14] # vencimento

                    if row[15] == 'S':
                        tdata['data_cancela'] = row[16].split()[0]
                    else:
                        tdata['data_cancela'] = None
                    tdata['modogeracao'] = 'l'
                    
                    tdata['motivodesconto'] = None


                    tdata['usuario_g'] = usuario 

                    if tdata['valorpago'] == '0' or tdata['valorpago'] == '' or tdata['valorpago'] == '0.00':
                        tdata['valorpago'] = None
                        tdata['usuario_b'] = None
                        tdata['data_baixa'] = None
                        tdata['data_pagamento'] = None

                    tdata['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
                    for k in tdata:
                        if tdata[k] in ['NULL','0000-00-00','']:
                            tdata[k] = None
                    if tdata['data_baixa'] is None:
                        tdata['usuario_b'] = None
                    
                    if not tdata.get('data_vencimento'):
                        continue 

                    if tdata['data_cancela']:
                        tdata['motivocancela'] = row[17]
                        tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA
                        tdata['usuario_c'] = usuario
                        tdata['valorpago'] = None
                        tdata['usuario_b'] = None
                        tdata['data_baixa'] = None
                        tdata['data_pagamento'] = None

                    if tdata['data_baixa']:
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                        tdata['usuario_b'] = usuario 
                        tdata['usuario_c'] = None

                    if tdata['demonstrativo'] is None:
                        tdata['demonstrativo'] = ''
                    print(row)
                    print(tdata)
                    if args.sync_db:
                        print('importando titulo %s' %tdata['nosso_numero'])
                        new_titulo = fmodels.Titulo(**tdata)
                        new_titulo.save()
                        new_titulo.data_documento = tdata['data_documento']
                        new_titulo.save()



if args.gerencianet:
    with open(args.gerencianet, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            t = fmodels.Titulo.objects.filter(numero_documento=row[0],titulogateway__isnull=True)
            for i in t:
                gateway = i.portador.gateway_boleto
                if gateway:
                    novo_titulogateway = fmodels.TituloGateway()
                    novo_titulogateway.titulo = t
                    novo_titulogateway.gateway = gateway
                    novo_titulogateway.idtransacao = row[1]
                    novo_titulogateway.link = row[3]
                    novo_titulogateway.url_notificacao=row[7]
                    novo_titulogateway.save()
                    t.linha_digitavel=row[2]
                    if row[5]:
                        t.parcela=row[5]
                    t.save()
                    print(t,row[1])


#select
#       m.Documento,
#       g.Charge_id,
#       g.Barcode,
#       g.Link,
#       g.Status,
#       g.Carnet_parcel,
#       g.CarneId,
#       g.NotificationUrl
#from Movimento m 
#inner join _Integracao_Gerencianet_Transaction g on (g.MovSeq=m.Sequencia)
#INTO OUTFILE '/tmp/routerbox-titulos-gerencianet.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

    
#from apps.admcore import models as admmodels
#for f in open('/opt/telefones.txt','r').readlines():
#    idcliente,telefone = f.strip().split('|')
#    cliente = admmodels.Cliente.objects.filter(id=idcliente)
#    if cliente:
#        new_contato = admmodels.Contato() 
#        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
#        new_contato.contato = telefone 
#        new_contato.save() 
#        new_ccontato = admmodels.ClienteContato()
#        new_ccontato.cliente = cliente[0]
#        new_ccontato.contato = new_contato
#        new_ccontato.save()
#        print cliente[0],telefone
#
#        #