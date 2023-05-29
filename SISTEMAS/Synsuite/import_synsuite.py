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
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--pessoas', dest='pessoas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--contratos', dest='contratos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--semlogin', dest='semlogin', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--conexoes', dest='conexoes', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--titulos2', dest='titulos2', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--updatevalor', dest='updatevalor', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--updatetitulos', dest='updatetitulos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--updateplanos', dest='updateplanos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--complementos', dest='complementos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--cep', dest='cep', type=str, help='Criar plano para corrigir',required=False)

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

portador = fmodels.Portador.objects.get(pk=args.portador_id)

if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(djson__synsuite=row[0]).count() == 0:
                print(row)
                new_plano = admmodels.Plano()
                new_plano.id = re.sub('[^0-9]', '', row[0])
                new_plano.descricao=row[1]
                new_plano.preco = row[13].replace(',','.')
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                if row[20] != 'Sim':
                    new_plano.ativo = False
                new_plano.descricao_boleto = row[38]
                new_plano.pospago = True
                new_plano.json={'synsuite': row[0]}
                new_plano.data_cadastro=datetime.now()
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=re.sub('[^0-9]', '', row[0])
                new_plano_internet.plano = new_plano 
                new_plano_internet.download=int(row[51] or '0')
                new_plano_internet.upload=int(row[50] or '0')
                new_plano_internet.diasparabloqueio = 15
                new_plano_internet.save() 


if args.updateplanos:
    with open(args.updateplanos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            for p in admmodels.PlanoInternet.objects.filter(plano__descricao=row[1])[:1]:
                print(row)
                print(p)
                p.plano.preco = row[13].replace(',','.')
                if row[20] != 'Sim':
                    p.plano.ativo = False
                p.plano.save()
                p.download=int(row[51] or '0')
                p.upload=int(row[50] or '0')
                p.save() 

if args.pessoas:
    m = manage.Manage()
    with open(args.pessoas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            idpessoa = int(row[0]) + 1000
            cpfcnpj = row[1]
            nome = row[2]
            fantasia = row[3]
            email = row[4]

            if row[5] != 'Sim':
                continue 
            d,m,y = row[6].split(' ')[0].split('/')
            data_cadastro = '%s-%s-%s' %(y,m,d)

            data_nasc = None
            if row[9] and '/' in row[9]:
                d,m,y = row[9].split(' ')[0].split('/')
                data_nasc = '%s-%s-%s' %(y,m,d)
            cliente_obs1 = row[10]

            logradouro = row[19]
            numero = None
            try:
                numero = int(row[20])
            except:
                numero = None
                logradouro += ",%s" %row[20]
            complemento = ustr(row[21])
            bairro = row[22]
            cidade = row[23]
            uf = row[24]
            cep = ''
            telefonecom = ''
            telefone = row[26]
            celular = row[27]            
            rgie = row[28].strip().replace(cpfcnpj,'')
            sexo = row[29]
            if sexo == 'Masculino':
                sexo = 'M'
            if sexo == 'Feminino':
                sexo = 'F'

            profissao = ''

            estado_civil = None
            if 'Solteiro' in row[30]:
                estado_civil = 'S'
            if 'Casado' in row[30]:
                estado_civil = 'C'
            nomemae = row[31]

            cliente_obs2 = row[38]
            cliente_obs3 = row[39]

            cidade_q = normalize('NFKD', unicode(cidade)).encode('ASCII','ignore').decode('ascii')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=uf
                new_pop.save()
                pop = new_pop

            print("-------------------------------------------------------")
            print nome,cpfcnpj,len(cpfcnpj),rgie,sexo, data_cadastro,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            
            if args.sync_db == True and admmodels.Cliente.objects.filter(Q(pessoa__id=idpessoa)).count() == 0:
                print "Import %s" %nome
                print("-------------------------------------------------------")
                # Save Models 
                
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
                new_endereco.save() 

               
                tp = 'f'
                if len(fnum(cpfcnpj)) > 11:
                    tp = 'j'
                
                if tp in['f','F']:
                    new_pessoa = admmodels.Pessoa()
                    new_pessoa.tipopessoa='F'
                    new_pessoa.id = idpessoa                    
                    new_pessoa.nome = nome
                    new_pessoa.sexo = sexo
                    new_pessoa.datanasc = data_nasc
                    new_pessoa.profissao = profissao
                    new_pessoa.nomemae = nomemae
                    new_pessoa.estadocivil=estado_civil
                    new_pessoa.nacionalidade = 'BR'
                    new_pessoa.rg = rgie
                    new_pessoa.cpfcnpj = cpfcnpj
                    new_pessoa.rg_emissor=''
                    new_pessoa.save()

                
                if tp in ['j','J']:
                    new_pessoa = admmodels.Pessoa()
                    new_pessoa.id = idpessoa
                    new_pessoa.tipopessoa='J'
                    new_pessoa.nome = nome                    
                    new_pessoa.nomefantasia = fantasia
                    new_pessoa.resempresa = ''
                    new_pessoa.cpfcnpj = cpfcnpj
                    new_pessoa.insc_estadual = rgie
                    new_pessoa.tipo = 8
                    new_pessoa.save()
                
                # Cliente
                new_cliente = admmodels.Cliente()
                new_cliente.id = idpessoa
                new_cliente.endereco = new_endereco
                new_cliente.pessoa = new_pessoa
                new_cliente.data_cadastro = data_cadastro
                new_cliente.data_alteracao = data_cadastro
                new_cliente.ativo = True 
                new_cliente.save()
                new_cliente.data_cadastro = data_cadastro
                new_cliente.data_alteracao = data_cadastro
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

                
if args.contratos:
    m = manage.Manage()
    with open(args.contratos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = int(row[1]) + 1000
            idcontrato = int(re.sub('[^0-9]', '', row[3])) + 1000
            data_cadastro = date.today()
            try:
                d_,m_,y_ = row[6].split('/')
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass
            vigencia = 'vigencia: %s - %s' %(row[7],row[8])

            vencimento = row[26]
            #portador= row[30]

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

            #portador = row[13]
            valor = row[33]
            status = row[45]    # situacao
            usuario = row[56]
            user = admmodels.User.objects.filter(username=row[56])
            if user:
                usuario = user[0]
            else:
                user = admmodels.User()
                user.username=row[56]
                user.name=row[56]
                user.set_unusable_password()
                user.is_staff = False
                user.save()
                usuario = user
            excluido = row[57]
            naosuspender = row[58] != 'Sim'
            concentrador = row[59]


            status_cc = 1
            status_s = 1
            status_c = 1
            isento = 0

            observacao = status

            if status == 'Cortesia':
                isento = 100

            if status in  ['Bloqueio Financeiro','Suspenso']:
                status_cc = 4
                status_s = 4
                status_c = 4

            if status in ['Cancelado']:
                status_cc = 3
                status_s = 3
                status_c = 3

            cliente_obj = admmodels.Cliente.objects.filter(Q(id=cliente))[:1]
            contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
            if cliente_obj and not contrato_check:
                new_cliente = cliente_obj[0]
                print('Importando contrato de %s' %new_cliente)

                new_endereco_cob = copy.copy(new_cliente.endereco)
                new_endereco_cob.id=None 
                new_endereco_cob.save()

                cidade_q = normalize('NFKD', new_cliente.endereco.cidade).encode('ASCII','ignore')
                try:
                    pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                    pop = pop_q
                except:
                    new_pop = admmodels.Pop()
                    new_pop.cidade=cidade_q.upper()
                    new_pop.uf=new_cliente.endereco.uf
                    new_pop.save()
                    pop = new_pop

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
                new_cobranca.nao_suspender = naosuspender
                new_cobranca.status = status_c
                new_cobranca.save()
                new_cobranca.valorfixo = row[33].replace(',','.')
                
                new_cobranca.data_cadastro = data_cadastro 
                new_cobranca.save()

                # Contrato 
                new_contrato = admmodels.ClienteContrato()
        
                new_contrato.cliente = new_cliente 
                new_contrato.id=idcontrato
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
                    if ic == 3:
                        new_status.observacao = row[48]
                        if row[47]:
                            d,m,y = row[47].strip().split('/')
                            data_cadastro = '%s-%s-%s' %(y,m,d)
                    else: 
                        new_status.observacao = '%s \n %s' %(vigencia,row[31])
                    new_status.modo=2
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_cadastro 
                    new_status.save()

                
                    new_status.data_cadastro = data_cadastro 
                    new_status.save() 
            

if args.conexoes:
    m = manage.Manage()
    nas = nmodels.NAS.objects.all()[0]
    
    with open(args.conexoes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            
            idservico = int(re.sub('[^0-9]', '', row[0])) + 1000
            idcontrato = int(re.sub('[^0-9]', '', row[1])) + 1000
            plano = re.sub('[^0-9]', '', row[4])
            login = row[7]
            if not login:
                continue
            senha = row[8]
            mac = row[9]
            ip = row[18]
            cep = row[25]
            if re.sub('[^0-9]', '', row[26]):
                numero = int(re.sub('[^0-9]', '', row[26]))
            else:
                numero = None
            if re.sub('[^a-zA-Z]', '', row[26]):
                complemento = re.sub('[^a-zA-Z]', '', row[26])
            else:
                complemento = ''
            bairro = row[27]
            logradouro = row[28]
            cidade = row[29]
            uf = row[30]
            latitude = row[31]
            longitude = row[32]

            print(plano)
            planointernet = admmodels.PlanoInternet.objects.filter(plano__id=plano)
            if not planointernet:
                continue

            if planointernet:
                planointernet = planointernet[0]

            new_contrato = admmodels.ClienteContrato.objects.filter(id=idcontrato)
            if new_contrato:
                new_contrato = new_contrato[0]

                if admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                    print "Import %s" %login

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
                    new_endereco.save() 

                    # Servico 
                    new_servico = admmodels.ServicoInternet()
                    new_servico.id=idservico
                    new_servico.clientecontrato = new_contrato 
                    new_servico.status = new_contrato.status.status
                    new_servico.login=login
                    if mac:
                        if admmodels.ServicoInternet.objects.filter(mac_dhcp__trim__lower=mac.strip().lower()).count() == 0:
                            new_servico.mac_dhcp = mac
                    new_servico.endereco = new_endereco
                    new_servico.login_password=senha 
                    new_servico.login_password_plain=senha
                    new_servico.central_password=senha
                    new_servico.tipoconexao = 'ppp'
                    new_servico.nas = nas
                    new_servico.planointernet = planointernet
                    new_servico.modoaquisicao = 0
                    new_servico.data_cadastro=new_contrato.data_cadastro
                    new_servico.observacao=''
                    new_servico.save()

                    new_servico.data_cadastro=new_contrato.data_cadastro
                    new_servico.save()

                    m.addRadiusServico(new_servico)




if args.titulos and portador:
    
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row[29])
            #print(row[13])
            #if not row[29] == 'Fatura':
            #    continue 

            #if not 'Santander' in row[23]:
            #    continue 
            
            if not row[15]:
                continue 
            cliente_obj = admmodels.Cliente.objects.filter(id=row[2])
            if cliente_obj:
                cliente = cliente_obj[0]
                cobranca = None
                if row[27]:
                    contrato = cliente.clientecontrato_set.filter(id=row[27])
                    if contrato:
                        cobranca = contrato[0].cobranca
                numero_documento = re.sub('[^0-9]', '', row[8]) 
                parcela = row[9]
                nosso_numero=re.sub('[^0-9]', '', row[10].split('-')[0])
                #nosso_numero = nosso_numero.replace('140000','').replace('240000','') 
                nosso_numero_f =nosso_numero
                valor=row[12].replace('.','').replace(',','.')

                try:
                    d_,m_,y_ = row[16].split(' ')[0].split('/')
                    data_documento='%s-%s-%s' %(y_,m_,d_)
                except:
                    pass

                try:
                    d_,m_,y_ = row[18].split('/')
                    data_vencimento='%s-%s-%s' %(y_,m_,d_)
                except:
                    pass

                demonstrativo = row[28]
                banco = row[23] # Santander - Boleto
                idcontrato = row[14]
                descricao = row[15]
                baixado = row[16]
                excluido = row[43].strip()

                aberto = row[18]
                valorpago = row[53].replace('.','').replace(',','.')

                data_cancela = None 
                usuario_c = None 
                usuario_g = usuario 
                usuario_b = None
                data_pagamento = None
                data_baixa = None
                status = fmodels.MOVIMENTACAO_GERADA

                if valorpago:
                    data_pagamento = data_vencimento
                    data_baixa = data_vencimento
                    usuario_b = usuario
                    status = fmodels.MOVIMENTACAO_PAGA
                else:
                    if aberto == 'Não':
                        data_pagamento = data_vencimento
                        data_baixa = data_vencimento
                        usuario_b = usuario
                        status = fmodels.MOVIMENTACAO_PAGA
                        valorpago = valor
                    else:
                        valorpago=None


                if excluido == 'Sim':
                    data_cancela = data_vencimento
                    status = fmodels.MOVIMENTACAO_CANCELADA
                    usuario_c = usuario
                    data_pagamento = None
                    data_baixa = None
                    valorpago=None

                linha_digitavel = row[38]
                codigo_barras = ''

                if nosso_numero:
                    if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                        dados = {'cliente': cliente,
                                 'cobranca': cobranca,
                                 'portador': portador,
                                 'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                                 'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                                 'modogeracao': 'l',
                                 'usuario_g': usuario_g,
                                 'usuario_b': usuario_b,
                                 'usuario_c': usuario_c,
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
                                 'desconto': '0.00',
                                 'status': status,
                                 }

                        print(dados)
                        if args.sync_db:

                            #print dados
                            print "Importando boleto",cliente,nosso_numero,data_vencimento,portador
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
                                print "Erro cadastrar",e,dados

if args.updatetitulos and portador:
    
    with open(args.updatetitulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            #print(row)
            #if 'santander' not in row[13]:
            #    continue 
            
            if not row[14]:
                continue 

            contrato = admmodels.ClienteContrato.objects.filter(id=row[14])
            if contrato:
                cliente = contrato[0].cliente
                cobranca = contrato[0].cobranca
                numero_documento = row[3][-7:]
                nosso_numero=row[4].split('-')[0][4:]
                nosso_numero_f =row[4]
                valor=row[5].replace('.','').replace(',','.')

                try:
                    d_,m_,y_ = row[9].split('/')
                    data_documento='%s-%s-%s' %(y_,m_,d_)
                except:
                    pass

                try:
                    d_,m_,y_ = row[12].split('/')
                    data_vencimento='%s-%s-%s' %(y_,m_,d_)
                except:
                    pass

                banco = row[13]
                idcontrato = row[14]
                descricao = row[15]
                baixado = row[16]
                excluido = row[17]

                aberto = row[18]
                valorpago = row[19].replace('.','').replace(',','.')

                data_cancela = None 
                usuario_c = None 
                usuario_g = usuario 
                usuario_b = None
                data_pagamento = None
                data_baixa = None
                status = fmodels.MOVIMENTACAO_GERADA

                if valorpago:
                    data_pagamento = data_vencimento
                    data_baixa = data_vencimento
                    usuario_b = usuario
                    status = fmodels.MOVIMENTACAO_PAGA
                else:
                    if aberto == 'Não':
                        data_pagamento = data_vencimento
                        data_baixa = data_vencimento
                        usuario_b = usuario
                        status = fmodels.MOVIMENTACAO_PAGA
                        valorpago = valor
                    else:
                        valorpago=None

                if excluido == 'Sim':
                    data_cancela = data_vencimento
                    status = fmodels.MOVIMENTACAO_CANCELADA
                    usaurio_c = usuario
                    data_pagamento = None
                    data_baixa = None
                    valorpago=None

                linha_digitavel = ''
                codigo_barras = ''

                if aberto == 'Não' and excluido == 'Não' and baixado == 'Não':
                    titulos = fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador,data_baixa__isnull=True,data_pagamento__isnull=True)
                    if titulos:
                        titulos.update(data_pagamento=data_pagamento,data_baixa=data_baixa,status=status,usuario_b=usuario_b,valorpago=valorpago)



if args.titulos2 and portador:
    
    with open(args.titulos2, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            #print(row)
            if 'Sicredi' not in row[13]:
                continue 
            
            if not row[14]:
                continue 

            contrato = admmodels.ClienteContrato.objects.filter(id=row[14])
            if contrato:
                cliente = contrato[0].cliente
                cobranca = contrato[0].cobranca
                numero_documento = row[3]
                nosso_numero=row[4].split('-')[0][4:]
                nosso_numero_f =row[4]
                valor=row[5]

                try:
                    d_,m_,y_ = row[9].split('/')
                    data_documento='%s-%s-%s' %(y_,m_,d_)
                except:
                    pass

                try:
                    d_,m_,y_ = row[12].split('/')
                    data_vencimento='%s-%s-%s' %(y_,m_,d_)
                except:
                    pass

                banco = row[13]
                idcontrato = row[14]
                descricao = row[15]
                baixado = row[16]
                excluido = row[18]

                #aberto = row[18]
                valorpago = row[19]

                data_cancela = None 
                usuario_c = None 
                usuario_g = usuario 
                usuario_b = None
                data_pagamento = None
                data_baixa = None
                status = fmodels.MOVIMENTACAO_GERADA

                if valorpago:
                    data_pagamento = data_vencimento
                    data_baixa = data_vencimento
                    usuario_b = usuario
                    status = fmodels.MOVIMENTACAO_PAGA
                else:
                    valorpago=None

                if excluido == 'Sim':
                    data_cancela = data_vencimento
                    status = fmodels.MOVIMENTACAO_CANCELADA
                    usaurio_c = usuario
                    data_pagamento = None
                    data_baixa = None
                    valorpago=None

                linha_digitavel = ''
                codigo_barras = ''

                if nosso_numero and args.updatevalor:
                    print(nosso_numero,valor,valorpago)
                    fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).update(valor=valor)
                    fmodels.Titulo.objects.filter(usuario_b__username='sgp',nosso_numero=nosso_numero,portador=portador,valorpago__isnull=False).update(valor=valor,valorpago=valorpago)
                else:
                    if nosso_numero:
                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                            dados = {'cliente': cliente,
                                     'cobranca': cobranca,
                                     'portador': portador,
                                     'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                                     'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                                     'modogeracao': 'l',
                                     'usuario_g': usuario_g,
                                     'usuario_b': usuario_b,
                                     'usuario_c': usuario_c,
                                     'demonstrativo': descricao,
                                     'data_documento': data_documento,
                                     'data_alteracao': data_documento,
                                     'data_vencimento': data_vencimento,
                                     'data_cancela': data_cancela,
                                     'data_pagamento': data_pagamento,
                                     'data_baixa': data_baixa,
                                     'numero_documento': nosso_numero,
                                     'nosso_numero': nosso_numero,
                                     'nosso_numero_f': nosso_numero_f,
                                     'linha_digitavel': linha_digitavel,
                                     'codigo_barras': codigo_barras,
                                     'valor': valor,
                                     'valorpago': valorpago,
                                     'desconto': '0.00',
                                     'status': status,
                                     }

                            print(dados)
                            if args.sync_db:

                                #print dados
                                print "Importando boleto",cliente,nosso_numero,data_vencimento,portador
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
                                    print "Erro cadastrar",e,dados


if args.complementos:
    with open(args.complementos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=row[1]))
            if cliente:
                cliente = cliente[0]
                print(cliente)
                e = cliente.endereco
                if not e.complemento:
                    e.complemento=row[2]
                    e.save()
                    print('update e1')
                for cc in cliente.clientecontrato_set.all():
                    e2 = cc.cobranca.endereco 
                    if not e2.complemento:
                        e2.complemento=row[2]
                        e2.save()
                        print('update e2')
                    for s in cc.servicointernet_set.all():
                        e3 = s.endereco 
                        if not e3.complemento:
                            e3.complemento=row[2]
                            e3.save()
                            print('update e3')

if args.cep:
    with open(args.cep, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            contrato = admmodels.ClienteContrato.objects.filter(id=row[0])
            if contrato:
                contrato = contrato[0]

                e1 = contrato.cliente.endereco
                if e1.cep is None or e1.cep.strip() == '':
                    e1.cep=row[3]
                    e1.save()
                e2 = contrato.cobranca.endereco
                if e2.cep is None or e2.cep.strip() == '':
                    e2.cep=row[3]
                    e2.save()
                e3 = contrato.servicointernet_set.all()[0].endereco
                if e3.cep is None or e3.cep.strip() == '':
                    e3.cep=row[3]
                    e3.save()
                print(contrato,e1,e2,e3)


if args.semlogin:
    m = manage.Manage()
    with open(args.semlogin, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idcontrato = row[1]
            new_contrato = admmodels.ClienteContrato.objects.filter(id=idcontrato,servicointernet__isnull=True)
            if new_contrato:
                new_contrato = new_contrato[0]
                login = 'conexao%s' %idcontrato
                senha = 'conexao%s' %idcontrato
                plano = '41510'
                print(plano)
                planointernet = admmodels.PlanoInternet.objects.filter(id=plano)[0]

                if admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                    print "Import %s" %login

                    new_endereco_inst = copy.copy(new_contrato.cliente.endereco)
                    new_endereco_inst.id=None 
                    new_endereco_inst.save()

                    # Servico 
                    new_servico = admmodels.ServicoInternet()
                    new_servico.clientecontrato = new_contrato 
                    new_servico.status = new_contrato.status.status
                    new_servico.login= login
                    new_servico.endereco = new_endereco_inst
                    new_servico.login_password=senha 
                    new_servico.login_password_plain=senha
                    new_servico.central_password=senha
                    new_servico.tipoconexao = 'ppp'
                    new_servico.nas_id = 1
                    new_servico.planointernet = planointernet
                    new_servico.modoaquisicao = 0
                    new_servico.data_cadastro=new_contrato.data_cadastro
                    new_servico.observacao=''
                    new_servico.save()

                    new_servico.data_cadastro=new_contrato.data_cadastro
                    new_servico.save()
