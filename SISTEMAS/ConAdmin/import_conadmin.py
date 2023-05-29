#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from itertools import count
import os, sys
from posixpath import split
from datetime import date, datetime
import copy
from tkinter import EXCEPTION
from unicodedata import normalize
import csv 
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--updatetitulos', dest='updatetitulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--gerencianet', dest='gerencianet', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--caixas', dest='caixas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--pops', dest='pops', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--telefones', dest='telefones', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--emails', dest='emails', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=str, help='Criar vencimento para corrigir',required=False)
parser.add_argument('--adcobrancas', dest='adcobrancas', type=str, help='acrescimos/descontos',required=False)
parser.add_argument('--titulosreg', dest='titulosreg', type=str, help='titulos reg',required=False)
parser.add_argument('--remessa', dest='remessa', type=str, help='remessa',required=False)
parser.add_argument('--ordemservico', dest='ordemservico', type=str, help='Arquivo importacao',required=False)

#python import_conadmin.py --settings=sgp.hc2.settings --planos=conadmin-planos.csv.utf8

#python import_conadmin.py --settings=sgp.hc2.settings --clientes=conadmin-clientes.csv.utf8 --nas=1 --pop=1 --sync=1 

#python import_conadmin.py --settings=sgp.hc2.settings --portadores=conadmin-portadores.csv.utf8
#python import_conadmin.py --settings=sgp.hc2.settings --titulos=conadmin-titulos.csv.utf8 --sync=1
#python import_conadmin.py --settings=sgp.hc2.settings --ordemservico=conadmin-titulos.csv.utf8 --sync=1
# python import_conadmin.py --settings=sgp.hc2.settings --telefones=conadmin-telefones.csv.utf8 --sync=1
# python import_conadmin.py --settings=sgp.hc2.settings --emails=conadmin-emails.csv.utf8--sync=1
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q 
from django.db.utils import DataError

from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
from apps.atendimento import models as amodels

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

def format_data(data):
    try:
        d,m,y = data.split('/')
        f='%s-%s-%s' %(y,m,d)
        if f == '0000-00-00':
            return None
        return f
    except:
        return None

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
usuario = admmodels.User.objects.get(username='sgp')
if args.portador:
    portador = fmodels.Portador.objects.get(id=args.portador)

contador=0
if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2]:
                if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                    print row
                    new_portador = fmodels.Portador()
                    new_portador.id = row[0]
                    new_portador.descricao = row[1]
                    new_portador.codigo_banco = '999'
                    new_portador.agencia = row[2]
                    new_portador.agencia_dv = ''
                    new_portador.conta = row[3]
                    new_portador.conta_dv = row[4]
                    new_portador.convenio = ''
                    new_portador.carteira = row[5]
                    new_portador.localpag = row[7]
                    new_portador.instrucoes1 = row[8]
                    new_portador.instrucoes2 = row[9]
                    new_portador.instrucoes3 = row[10]
                    new_portador.instrucoes4 = row[11]
                    new_portador.instrucoes5 = row[12]
                    new_portador.multa = row[13]
                    new_portador.juros = row[14]
                    new_portador.cedente='PROVEDOR IMPORTADO'
                    new_portador.cpfcnpj = '0'
                    new_portador.save()

if args.caixas:
    with open(args.caixas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if fmodels.PontoRecebimento.objects.filter(id=row[0]).count() == 0:
                print row
                new_ponto = fmodels.PontoRecebimento()
                new_ponto.id = row[0]
                new_ponto.descricao = row[1]
                new_ponto.save()

if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(id=row[0]).count() == 0:
                print row
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao=row[1]
                new_plano.preco = row[2]
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                new_plano.pospago = True
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=row[0]
                new_plano_internet.plano = new_plano 

                try:
                    upload,download = row[3].split('/')
                except:
                    upload,download = 1024,2048
                if 'k' in download.lower():
                    new_plano_internet.download = int(fnum(download))
                elif 'm' in download.lower():
                    new_plano_internet.download = int(fnum(download)) * 1024
                else:
                    new_plano_internet.download = download

                if 'k' in upload.lower():
                    new_plano_internet.upload = int(fnum(upload))
                elif 'm' in upload.lower():
                    new_plano_internet.upload = int(fnum(upload)) * 1024
                else:
                    new_plano_internet.upload = row[3]
                
                if row[4]=='':
                    new_plano_internet.diasparabloqueio = 4
                else:
                    new_plano_internet.diasparabloqueio = row[4]
                
                new_plano_internet.diasparaaviso = 5 #row[5][]
                new_plano_internet.save() 

if args.nas:
    with open(args.nas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(id=row[0]).count() == 0:
                if row[6] == 'y':
                    print row
                    new_nas = nmodels.NAS()
                    new_nas.id=row[0]
                    new_nas.shortname=row[2]
                    new_nas.secret = row[3]
                    new_nas.xuser= row[4]
                    new_nas.xtype = 'mikrotik'
                    new_nas.xpassword = row[5]
                    new_nas.nasname= row[11]
                    new_nas.save()


if args.clientes:
    nas = nmodels.NAS.objects.all()[0]
    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    m = manage.Manage()

    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            idcliente = row[0]
            idcontrato = row[1]
            nome = row[2]
            razaosocial = row[3]
            respempresa = row[4]
            tipo = row[5]
            data_nasc = row[6]
            sexo = ''
            if row[7] == '2':
                sexo = 'F'
            elif row[7] == '1':
                sexo = 'M'
            rgie = row[8]
            insc_estadual = row[8]
            rg_emissor = row[9]
            cpfcnpj = row[10]
            estadocivil = row[11]
            insc_municipal = row[12]

            nomepai = row[15]
            nomemae = row[16]
            senha_central = row[17]
            # login criou 18 

            endereco_inst = {}
            endereco_inst['logradouro'] = str(row)[19][:48] # tipo_insta,endereco_insta
            try:
                endereco_inst['numero'] = int(row[20]) # numero_insta
            except:
                endereco_inst['numero'] = None 
            endereco_inst['complemento'] = str(row[21])[:48]
            endereco_inst['cep'] = row[22]
            endereco_inst['bairro'] = str(row[23])[:48]
            endereco_inst['cidade'] = row[26]
            endereco_inst['uf'] = row[27]

            endereco_inst['pontoreferencia'] = ''
            endereco_cob = {} 
            endereco_cob['logradouro'] = str(row[28])[:48] # tipo_insta,endereco_insta
            try:
                endereco_cob['numero'] = int(row[29]) # numero_insta
            except:
                endereco_cob['numero'] = None 
            endereco_cob['complemento'] =str(row[30])[:48]
            endereco_cob['cep'] = row[31]
            endereco_cob['bairro'] = str(row[32])[:48]
            endereco_cob['cidade'] = row[35]
            endereco_cob['uf'] = row[36]
           
            endereco_cob['pontoreferencia'] = ''

            vencimento = row[37]
            portador = row[38]
            data_cadastro = row[39]
            data_ativacao = data_cadastro
            status = row[40]

            login = row[41]
            senha = row[42]

            if not login:
                login = 'c%s' %idcontrato
            if not senha:
                senha = 'c%s' %idcontrato

            mac_dhcp = row[43]
            #ip = row[45]
            ip = None
            coip = None
            modoaquisicao = 1 if 'comodato' in row[45].lower() else 0
            tipo_equipamento = row[46]
            try:
                plano = admmodels.PlanoInternet.objects.get(id=row[47])
            except:
                plano= admmodels.PlanoInternet.objects.get(id=12)
            cli_obs = row[48]
            con_obs = row[49]


            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

            respempresa = ''
            respcpf = ''



            cidade_q = normalize('NFKD', unicode(endereco_inst['cidade'])).encode('ASCII','ignore')
            '''try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=endereco_inst['uf']
                new_pop.save()
                pop = new_pop'''
            pop=admmodels.Pop.objects.get(id=2)
            
            nas = nmodels.NAS.objects.get(id=2)

            notafiscal = False

            con_obs=''
            mac = None
            conexao_tipo = 'ppp'

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1
            
            if status == '202':
                isento = 100

            if status == '303':
                status_cc = 4
                status_s = 4
                status_c = 4

            if status == '1':
                status_cc = 3
                status_s = 3
                status_c = 3

            if status =='102':
                status_cc = 3
                status_s = 3
                status_c = 3
            status_criar = [6,2,status_cc]

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save() 

            #print pop
            #print row
            print status, login, nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print endereco_cob,endereco_inst
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print cli_obs,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True: # and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" %nome
                # Save Models 

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)
                if admmodels.ServicoInternet.objects.filter(login=login).count() != 0:
                    login=str(login)+'_repetido'+str(idcliente)+'_'+str(contador)
                if len(cliente_check) == 0:

                    # Endereco 
                    new_endereco = admmodels.Endereco(**endereco_cob)
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    try:
                        new_endereco.save() 
                        new_endereco_cob.save()
                        new_endereco_inst.save()

                    except Exception as e:
                        new_endereco.bairro='erro_utf8'
                        new_endereco.cidade='erro_utf8'
                        new_endereco.complemento='erro_utf8'
                        new_endereco.logradouro='erro_utf8'
                        new_endereco.save() 

                        new_endereco_inst.bairro='erro_utf8'
                        new_endereco_inst.cidade='erro_utf8'
                        new_endereco_inst.complemento='erro_utf8'
                        new_endereco_inst.logradouro='erro_utf8'
                        new_endereco_inst.save() 

                        new_endereco_cob.bairro='erro_utf8'
                        new_endereco_cob.cidade='erro_utf8'
                        new_endereco_cob.complemento='erro_utf8'
                        new_endereco_cob.logradouro='erro_utf8'
                        new_endereco_cob.save() 

                    
                    if tipo == '2':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'
                        
                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = ''
                        new_pessoa.nomepai = nomepai
                        new_pessoa.nomemae = nomemae
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=rg_emissor
                        if estadocivil:
                            new_pessoa.estadocivil=estadocivil.upper()[0]
                        try:
                            new_pessoa.save()
                        except:
                            try:
                                new_pessoa.save()
                            except:
                                new_pessoa.datanasc=None 
                                new_pessoa.save()
                    
                    if tipo == '1':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = razaosocial or nome
                        
                        new_pessoa.nomefantasia = nome
                        new_pessoa.respempresa = respempresa
                        new_pessoa.respcpf = respcpf
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = insc_estadual
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
                    new_cliente.observacao = cli_obs
                    new_cliente.save()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()
                
                else:
                    new_endereco = cliente_check[0].endereco
                    
                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_cob.id = None 
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_inst.id = None 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    

                    new_cliente = cliente_check[0]

                contador=contador+1
                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob
                try:
                    new_cobranca.portador = fmodels.Portador.objects.get(pk=portador)
                except:
                    new_cobranca.portador =fmodels.Portador.objects.get(pk=6)
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
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca
                 
                new_contrato.data_inicio = data_cadastro 
                new_contrato.data_cadastro = data_cadastro 
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()
                
                for ic in status_criar:
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
                new_servico.login= login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password=senha 
                new_servico.login_password_plain=senha
                new_servico.central_password=senha_central
                if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                    new_servico.mac_dhcp = mac_dhcp
                    new_servico.mac = mac

                if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                    new_servico.ip = ip 

                if not ip or ip=='':
                    new_servico.ip=None
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = plano
                new_servico.modoaquisicao = modoaquisicao
                new_servico.data_cadastro=data_cadastro
                new_servico.observacao=con_obs
                try:
                    new_servico.save()
                except Exception as e:
                    new_servico.login=str(login)+'_'+'repetido''_'+str(contador)+str(idcliente)
                    new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)


if args.titulosreg and args.remessa:
    with open(args.titulosreg, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|')

        remessaportador = fmodels.RemessaPortador()
        remessaportador.tipo = 'CB'
        remessaportador.usuario = usuario
        remessaportador.portador = portador
        remessaportador.numero_remessa = args.remessa or 1
        remessaportador.arquivo = '/tmp/%s' %args.remessa or '1'
        remessaportador.modelo_arquivo = 'CNAB240'
        remessaportador.observacao = 'reg importacao'
        remessaportador.save()
       
        for row in conteudo:
            #print row
            nnumero = row[3] or row[4]
            titulos = fmodels.Titulo.objects.filter(portador=portador,
                                                    remessaportadortitulo__isnull=True,
                                                    nosso_numero=nnumero,
                                                    data_pagamento__isnull=True,
                                                    data_cancela__isnull=True)[:1]
            for t in titulos:
                nrt = fmodels.RemessaPortadorTitulo()
                nrt.remessa = remessaportador
                nrt.titulo = t
                nrt.valor = t.valor
                nrt.data_vencimento = t.data_vencimento
                nrt.desconto = t.desconto_venc
                nrt.juros = t.getValorJurosDia()
                nrt.multa = t.getValorMultaDia()
                nrt.cod_movimento = '01'
                nrt.save()
                print(t,'01',t.data_documento,t.data_vencimento)


if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|')
        
            
        for row in conteudo:
            try:
               
                portador= fmodels.Portador.objects.get(id=row[14])
                
            except Exception as e:
                print(e)
                portador=portador = fmodels.Portador.objects.get(id=6)
                
            #print row
            try:
                cliente = admmodels.Cliente.objects.filter(id=row[1])
            except:
                continue
            cobranca = None 
            contrato = None

            if cliente:
                cliente = cliente[0]
                if row[2]:
                    contrato = admmodels.ClienteContrato.objects.filter(id=row[2])
                if not contrato:
                    contrato = cliente.clientecontrato_set.all()

                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                try:
                    nn =  row[4] # row[3] or
                except:
                    continue
                if fmodels.Titulo.objects.filter(portador=portador,nosso_numero=nn).count() == 0:
                    #print row
                    tdata = {} 
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] =  row[4] # nrboleto # row[3] or
                    tdata['numero_documento'] = row[4] # documento
                    tdata['parcela'] = row[5] or 1 #row[6] # parcela
                    tdata['data_documento'] = row[6]
                    tdata['data_vencimento'] = row[7]
                    tdata['data_pagamento'] = row[8].split(' ')[0]
                    tdata['data_baixa'] = row[8]
                    tdata['data_cancela'] = row[9].split(' ')[0]
                    tdata['valor'] = row[10]
                    tdata['valorpago'] = row[11]
                    
                    try:
                        if row[15]:
                            tdata['demonstrativo'] = 'Período %s' %row[15]
                        else:
                            tdata['demonstrativo'] = ''
                    except:
                        tdata['demonstrativo'] = ''

                    for k in tdata:
                        if tdata[k] in ['NULL','0000-00-00','']:
                            tdata[k] = None

                    #if not row[6]:
                    #    tdata['parcela'] = 1
                    tdata['portador'] = portador
                    tdata['desconto'] = '0.00'

                    try:
                        tdata['observacao'] = '%s: %s' %(row[12],row[13])
                    except:
                        pass
                    
                    tdata['usuario_g'] = usuario
                    tdata['status'] = fmodels.MOVIMENTACAO_GERADA

                    if tdata['data_pagamento']:
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                        tdata['usuario_b'] = usuario

                    if tdata['data_cancela']:
                        tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA
                        tdata['usuario_c'] = usuario

                    

                    tdata['modogeracao'] = 'l'
                    tdata['motivocancela'] = None
                    tdata['motivodesconto'] = None

                    tdata['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')


                    if tdata['demonstrativo'] is None:
                        tdata['demonstrativo'] = ''
                    print tdata
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']
                    new_titulo.save()

if args.updatetitulos:
    with open(args.updatetitulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|')
        for row in conteudo:
            if row[1]:
                if len(row[1].split()) > 1:
                    d,m,y = row[1].split()[0].split('-')
                    dt1=date(int(d),int(m),int(y)).strftime("%d/%m/%Y")
                    d,m,y = row[1].split()[1].split('-')
                    dt2=date(int(d),int(m),int(y)).strftime("%d/%m/%Y")
                    dem = 'Período Acesso de %s a %s' %(dt1,dt2)
                    t = fmodels.Titulo.objects.filter(Q(numero_documento=row[0]),Q(Q(demonstrativo='')|Q(demonstrativo__isnull=True))).update(demonstrativo=dem)
                    print(t,row[0],dem)


if args.gerencianet:
    with open(args.gerencianet, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            titulo = fmodels.Titulo.objects.filter(numero_documento=row[0])
            if titulo:
                titulo  = titulo[0]
                titulogateway = fmodels.TituloGateway()
                titulogateway.titulo = titulo
                titulogateway.gateway = titulo.portador.gateway_boleto
                titulogateway.link = row[2]
                titulogateway.idtransacao = row[1]
                titulogateway.save()


if args.telefones:
    from apps.admcore import models 
    import csv 
    from django.db.models import Q
    with open(args.telefones, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = row[0]
            telefone = row[1]
            cpfcnpj = row[2]
            clientes = models.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj))
            for c in clientes:
                if c.clientecontato_set.filter(contato__contato__numfilter=telefone).count() == 0:
                    print 'IMPORTADO CONTATO', telefone,c
                    new_contato = models.Contato()
                    new_contato.contato=telefone
                    new_contato.tipo = 'CELULAR_PESSOAL'
                    new_contato.save() 
                    new_clientecontato = models.ClienteContato()
                    new_clientecontato.cliente=c
                    new_clientecontato.contato=new_contato
                    new_clientecontato.save() 
                
if args.emails:
    from apps.admcore import models 
    import csv 
    from django.db.models import Q
    with open(args.emails, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = row[0]
            email = row[1]
            cpfcnpj = row[2]
            clientes = models.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj))
            for c in clientes:
                if c.clientecontato_set.filter(contato__contato__trim__lower=email.strip().lower()).count() == 0:
                    print 'IMPORTADO CONTATO', email, c
                    new_contato = models.Contato()
                    new_contato.contato=email
                    new_contato.tipo = 'EMAIL'
                    new_contato.save() 
                    new_clientecontato = models.ClienteContato()
                    new_clientecontato.cliente=c
                    new_clientecontato.contato=new_contato
                    new_clientecontato.save() 
                


if args.adcobrancas:
    with open(args.adcobrancas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            clientecontrato = admmodels.ClienteContrato.objects.filter(Q(cliente__pessoa__nome__trim__upper__startswith=row[3]))
            if clientecontrato:
                clientecontrato = clientecontrato[0]
                print(clientecontrato)
                cobranca = clientecontrato.cobranca
                new_ad = fmodels.ADCobranca()
                new_ad.cobranca = cobranca
                new_ad.justificativa='%s %s' %(row[4],row[6])
                qtd = 1
                if 'Parcela' in row[6]:
                    qi,qf = row[6].split()[1].split('/')
                    if qi == qf:
                        qtd = 1
                    else:
                        qtd = int(qf)-int(qi) + 1 
                new_ad.parcelas=qtd
                new_ad.usuario = usuario
                new_ad.totalparcelas = qtd
                new_ad.valor=row[7]
                new_ad.save()

if args.ordemservico:
    usuario = admmodels.User.objects.get(username='sgp')
    with open(args.ordemservico, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        metodo = amodels.Metodo.objects.all()[0]
        
        for row in conteudo:
            assunto = row[5]
            try:
                clientecontrato= admmodels.ClienteContrato.objects.filter(cliente__id=row[2])[0]
            except:
                continue
            if amodels.Ocorrencia.objects.filter(numero=row[0]).count() == 0:
                print(row)
                status=row[4]
                ocorrencia = {}
                ocorrencia['clientecontrato'] = clientecontrato
                ocorrencia['tipo'] = amodels.Tipo.objects.filter(codigo=5)[0]
                ocorrencia['usuario'] = usuario 
                ocorrencia['numero'] = row[0]
                ocorrencia['metodo']= metodo
                ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if status != '' else amodels.OCORRENCIA_ABERTA
                ocorrencia['responsavel'] = ocorrencia['usuario']

                ocorrencia['data_cadastro'] = str(row[3]).split(" ")[0]
                print("MINHA DATA DE CADASTRO: ",ocorrencia['data_cadastro'])
                
                ocorrencia['data_finalizacao'] = row[4]
                ocorrencia['conteudo'] = row[8]
                new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                if str(new_ocorrencia.data_finalizacao)=='':
                    new_ocorrencia.data_finalizacao = None
                new_ocorrencia.data_agendamento = row[4]

                if new_ocorrencia.data_agendamento=='':
                    new_ocorrencia.data_agendamento=None
                try: 
                    new_ocorrencia.data_cadastro=row[3]
                    new_ocorrencia.save()
                except:
                    continue


                new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                new_ocorrencia_anotacao.ocorrencia= new_ocorrencia
                new_ocorrencia_anotacao.anotacao=row[10]
                new_ocorrencia_anotacao.usuario= usuario
                new_ocorrencia_anotacao.save()

            else:
                print('ocorrência já existe')