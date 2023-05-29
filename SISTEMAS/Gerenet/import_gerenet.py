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
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--planos', dest='planos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--maclogin', dest='maclogin', type=bool, help='Arquivo importacao',required=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--avisos', dest='avisos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--loginobs', dest='loginobs', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--gerencianet', dest='gerencianet', type=bool, help='Arquivo importacao',required=False)
parser.add_argument('--gerencianetcarne', dest='gerencianetcarne', type=bool, help='Arquivo importacao',required=False)

'''
python import_gerenet.py --settings=sgp.local.settings --portador=1 --nas=1 --planos=gerenet-planos.csv.utf8
python import_gerenet.py --settings=sgp.local.settings --portador=1 --nas=1 --pop=1 --clientes=gerenet-clientes.csv.utf8 --sync=1
python import_gerenet.py --settings=sgp.local.settings --portador=1 --nas=1 --titulos=gerenet-recebidos-19.csv.utf8 --sync=1
python import_gerenet.py --settings=sgp.local.settings --portador=1 --nas=1 --gerencianet=1 --sync=1
'''


args = parser.parse_args()

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
if args.nas_id:
    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
if args.portador_id:
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
ri = -1




#
if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            id=int(row[0])
            if admmodels.PlanoInternet.objects.filter(id=id).count() == 0:
                ri += 1
                print(row)

                plano_id = int(row[0])  # A | 0
                plano_descricao = str(row[1]) # B | 1
                plano_valor = row[2] # C | 2
                plano_datacadastro=datetime.now()
                plano_valor_desconto = row[3] # D | 3
                plano_valor_rant = row[4]
                plano_grupo = row[5]
                plano_sici = row[6]
                plano_lan = row[7]
                plano_ativo = row[10]
                
                if row[8]:
                    try:
                        plano_download = int(fnum(row[8])) # H | 8
                        if(len(str(plano_download))<4):
                            plano_download=int(plano_download)*1024
                    except:
                        plano_download=25000
                else:
                    plano_download = 2048
                if row[9]:
                    try:
                        plano_upload = int(row[9]) # H | 9
                        if(len(str(plano_upload))<4):
                            plano_upload=int(plano_upload)*1024
                    except Exception as e:
                        plano_upload=25000
                else:
                    plano_upload = 2048
                
                new_plano = admmodels.Plano()
                new_plano.id=plano_id
                new_plano.descricao=plano_descricao
                new_plano.data_cadastro=plano_datacadastro
                new_plano.preco = plano_valor
                new_plano.desconto = plano_valor_desconto
                if plano_ativo == 'S':
                    new_plano.ativo = True
                else:
                    new_plano.ativo = False
                new_plano.contrato = admmodels.Contrato.objects.filter(grupo__nome='fibra')[0]
                new_plano.grupo = admmodels.Grupo.objects.filter(nome='fibra')[0]
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=plano_id
                new_plano_internet.plano = new_plano 
                new_plano_internet.download = plano_download
                new_plano_internet.upload = plano_upload
                new_plano_internet.save() 
                print('criado plano %s' %new_plano)
            else:
                continue
                
if args.clientes:
    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1


            idcliente = int(row[0])
            nome = row[1]
            nome_fantasia = row[2]
            rgie = fnum(row[3])
            cpfcnpj = fnum(row[4])
            data_nasc = row[5]
            nome_pai = row[6]
            nome_mae = row[7]


            #
            # Endereço
            #
            logradouro = row[8] 
            try:
                numero = int(row[9])
            except:
                numero = None
            complemento = row[10]
            if row[11]: complemento += ' BL: %s' %row[11]
            if row[12]: complemento += ' ANDAR: %s' %row[12]
            if row[13]: complemento += ' QUADRA: %s' %row[13]
            if row[14]: complemento += ' LOTE: %s' %row[14]
            if row[15]: complemento += ' CASA: %s' %row[15]
            bairro = row[16]
            cidade = row[18]
            uf = row[19]
            cep = row[20]


            #
            # Contato
            #
            celular1 = row[22]
            celular1_obs = row[23]  
            celular2 = row[24] 
            celular2_obs = row[25] 
            celular3 = row[26] 
            celular3_obs = row[27]  
            celular4 = row[28] 
            celular4_obs = row[29]  
            celular5 = row[30] 
            celular5_obs = row[31]  
            celular6 = row[32] 
            celular6_obs = row[33]  

            email_financeiro = row[34]
            email_tecnico = row[35] 

            #
            # Endereço Cobrança
            #

            logradouro_cob = row[36]
            numero_cob = None
            complemento_cob = row[37]
            bairro_cob = row[38]
            cidade_cob = row[39]
            uf_cob = row[40]
            cep_cob = row[41]

            data_cadastro = row[42]

            try:
                y_,m_,d_ = row[42].strip().split('-')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_[:2]))
                data_cadastro='%s-%s-%s' %(y_,m_,d_[:2])
            except:
                pass


            if not data_cadastro or '0000-00-00' in data_cadastro:
                data_cadastro = date.today()

            vencimento = row[49]
            carteira_cobranca = row[50]
            bloqueio_auto = row[52]
            data_alteracao = date.today()
            if not data_alteracao:
                data_alteracao = date.today()

            # Contrato 
            data_contrato = row[62]

            try:
                y_,m_,d_ = row[62].strip().split('-')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_[:2]))
                data_contrato='%s-%s-%s' %(y_,m_,d_[:2])
            except:
                 data_contrato = date.today()
           
            if not data_contrato:
                data_contrato = date.today()

            comodato = row[63]
            equipamento = row[64]
            plano_nome = row[65]
            #id_plano =int(row[66])+300
            try:
                id_plano=int(row[66])
                plano = admmodels.PlanoInternet.objects.get(id=id_plano)
            except:
                plano= admmodels.PlanoInternet.objects.get(id=14)
            status=row[67].strip()
            servico_obs = 'Ponto: %s' %(row[68])
            #if row[68] == '0':
            #    continue
            servico_obs += '\nEquip.: %s' %equipamento
            login = row[69]
            if not login:
                login = 'no_login_%s_%s' %(idcliente,row[68])
            senha = row[70]
            if not senha:
                senha = login
            mac = row[71]
            if mac in ['01:01:01:01:01:01','00:00:00:00:00:00','']:
                mac = None

            
            ip = None
            if mac and len(mac) < 5:
                mac = None

            if args.maclogin and mac:
                login = mac
                senha = mac
            #MariaDB [telecab]> select * from tva0900_sexo;
            #+--------+-------------+-------+
            #| codigo | nome        | ativo |
            #+--------+-------------+-------+
            #|      0 | Não Consta  | N     |
            #|      1 | Masculino   | S     |
            #|      2 | Feminino    | S     |
            #+--------+-------------+-------+
            #

            if row[72] == '1':
                sexo = 'M'
            elif row[72] == '2':
                sexo = 'F'
            else:
                sexo = None


            #MariaDB [telecab]> select * from tva0900_civil;
            #+--------+-------------+-------+
            #| codigo | nome        | ativo |
            #+--------+-------------+-------+
            #|      0 | Não Consta  | N     |
            #|      1 | Solteiro    | S     |
            #|      2 | Casado      | S     |
            #|      3 | Divorciado  | S     |
            #|      4 | Viúvo       | S     |
            #+--------+-------------+-------+

            estado_civil = None
            try:
                if row[73] in ['1','3','4']:
                    estado_civil = 'S'
                elif row[73] == '2':
                    estado_civil = 'C'
            except:
                estado_civil = 'S'

            rg_emissor = row[74]

            profissao = ''
            #idservico = row[75]
            login_obs = row[76]
            if login_obs:
                if servico_obs:
                    servico_obs = "%s\n%s" %(login_obs,servico_obs)
                else:
                    servico_obs = login_obs 

            #
            # Contato
            #
            telefonecom = ''
            telefone = ''
            con_obs = ''

            conexao_tipo = 'ppp'

            comodato = False
            isento = 0

            #MariaDB [telecab]> select CODIGO,NOME from tva1500;
            #+--------+----------------------+
            #| CODIGO | NOME                 |
            #+--------+----------------------+
            #|     19 | AGUARDA 1a. CON.     |
            #|     27 | ATIVO                |
            #|     35 | DESLIGADO            |
            #|     43 | CORTADO              |
            #|     51 | DESISTENTE           |
            #|      0 | não consta           |
            #|     58 | CONECTADO EM AVISO   |
            #|     52 | CANCELADO POR INADIM |
            #|     53 | PÓS-CANCELADO        |
            #|     26 | PRÉ-CONECTADO        |
            #|     10 | EM FECHAMENTO        |
            #|     11 | REDE INDISPONÍVEL    |
            #|     99 | INSTABILIDADE 99     |
            #|     96 | INSTABILIDADE 96     |
            #|     97 | INSTABILIDADE 97     |
            #|     98 | INSTABILIDADE 98     |
            #|      1 | CADASTRO SEM PONTO   |
            #|     59 | CONECTADO EM REAVISO |
            #+--------+----------------------+

            status_cc = 1
            status_s = 1
            status_c = 1

            if status in ['CORTADO','INADIMPLENTE']:
                status_cc = 4
                status_s = 4
                status_c = 4

            if status in ['CADASTRO SEM PONTO','CANCELADO POR INADIM','DESLIGADO','REDE INDISPONÍVEL','CANCELADO']:
                status_cc = 3
                status_s = 3
                status_c = 3

            if status in ['DESISTENTE','AGUARDA 1a. CON.','REDE INDISPONÍVEL']:
                status_cc = 5
                status_s = 5
                status_c = 5

            cidade_q = normalize('NFKD', unicode(cidade)).encode('ASCII','ignore').decode('ascii')
            print cidade_q
            print uf

            pop=admmodels.Pop.objects.get(id=args.pop_id)

            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

            naturalidade = ''

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print celular1,celular2,celular3,celular4,celular5,celular6,email_financeiro,email_tecnico,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" %nome
                # Save Models 


                check_cliente = admmodels.Cliente.objects.filter(id=idcliente)
                if len(check_cliente) == 0:

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
                    
                    if logradouro_cob and cidade_cob and cep_cob and bairro_cob:

                        new_endereco_cob = admmodels.Endereco()
                        new_endereco_cob.logradouro = logradouro_cob
                        new_endereco_cob.numero = numero
                        new_endereco_cob.bairro = bairro_cob
                        new_endereco_cob.cep = cep_cob
                        new_endereco_cob.cidade = cidade_cob
                        new_endereco_cob.uf = uf_cob 
                        new_endereco_cob.pais = 'BR'
                        new_endereco_cob.complemento = complemento_cob
                        new_endereco_cob.pontoreferencia=''
                        new_endereco_cob.save()

                    else:
                        new_endereco_cob = copy.copy(new_endereco)
                        new_endereco_cob.save()

                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco.save() 
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
                        new_pessoa.nomepai = nome_pai
                        new_pessoa.nomemae = nome_mae
                        new_pessoa.naturalidade = naturalidade
                        new_pessoa.estadocivil = estado_civil
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
                        if len(nome_fantasia) > 3:
                            new_pessoa.nomefantasia = nome_fantasia
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = rgie
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
                    if len(email_financeiro) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'EMAIL_COBRANCA'
                        new_contato.contato = email_financeiro
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 2
                    if len(email_tecnico) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'EMAIL'
                        new_contato.contato = email_tecnico
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    # contato 3
                    if len(celular1) > 4:
                        new_contato = admmodels.Contato()  
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular1
                        new_contato.observacao = celular1_obs
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    
                    # contato 4
                    if len(celular2) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular2
                        new_contato.observacao = celular2_obs 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 5
                    if len(celular3) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular3
                        new_contato.observacao = celular3_obs 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 6
                    if len(celular4) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular4
                        new_contato.observacao = celular4_obs 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 7
                    if len(celular5) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular5
                        new_contato.observacao = celular5_obs 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 8
                    if len(celular6) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular6
                        new_contato.observacao = celular6_obs 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                else:
                    new_cliente = check_cliente[0] 
                    new_endereco_inst = copy.copy(new_cliente.endereco)
                    new_endereco_inst.id = None 
                    new_endereco_cob = copy.copy(new_cliente.endereco)
                    new_endereco_cob.id = None
                    new_endereco_cob.save() 
                    new_endereco_inst.save()
                
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
                new_contrato.id = idcliente
                new_contrato.cliente = new_cliente 
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca
                 
                new_contrato.data_inicio = data_contrato 
                new_contrato.data_cadastro = data_contrato 
                new_contrato.data_alteracao = data_contrato
                new_contrato.save()
                
                for ic in [6,2,status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_alteracao 
                    new_status.save() 
                
                    new_status.data_cadastro = data_alteracao 
                    new_status.save() 
                
                # Servico 
                new_servico = admmodels.ServicoInternet()
                #if idservico:
                #    new_servico.id = idservico
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
                new_servico.planointernet = plano
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
        
        portador=fmodels.Portador.objects.get(pk=args.portador_id)
        for row in conteudo:
            incremento= int(row[1])
            cliente = admmodels.Cliente.objects.filter(id=incremento)
            cobranca = None
            if cliente:
                cliente = cliente[0]
                clientecontrato = cliente.clientecontrato_set.filter(status__status__in=[admmodels.CONTRATO_ATIVO,
                                                                                         admmodels.CONTRATO_SUSPENSO,
                                                                                         admmodels.CONTRATO_CANCELADO])
                if clientecontrato:
                    clientecontrato = clientecontrato[0]
                    cobranca = clientecontrato.cobranca

                descricao = ''
                data_documento = row[2]
                data_vencimento = row[3].split()[0]
                valor = row[4]
                nosso_numero = row[5]
                nosso_numero_f = row[5]
                numero_documento = row[0]
                if row[7]:
                    data_pagamento = row[7].split()[0]
                    data_baixa = row[7]
                else:
                    data_pagamento = None
                    data_baixa = None
                
                valorpago = row[9]
                if not valorpago:
                    valorpago = None
                statusid = row[10]
                idtransacao = row[11]
                link = row[12]
                codigo_barras = row[13]
                carne_id = row[14]
                carne_link = row[15]
    
                usuario_b = usuario 
                usuario_g = usuario 
                usuario_c = None
                data_cancela = None
                data_cancela = row[17]
                
                if statusid=='0':
                    usuario_c = usuario
                    usuario_b = None 
                    status = fmodels.MOVIMENTACAO_CANCELADA
                    data_baixa = None 
                    data_pagamento = None
                
                    if data_cancela != '0000-00-00 00:00:00':
                        data_cancela = data_cancela.split()[0]
                    
                    else:
                        data_cancela = datetime.now() 
                      
                elif statusid == '1':
                    data_pagamento = None
                    data_baixa = None
                    usuario_b = None
                    usuario_c = None
                    status = fmodels.MOVIMENTACAO_GERADA
                else:
                    status = fmodels.MOVIMENTACAO_PAGA
                desconto = 0.00

                linha_digitavel = ''
                observacao = ''
                if statusid and idtransacao and link:
                    observacao = """
status=%s
idtransacao=%s
link=%s
    carneid=%s
    carnelink=%s
""" %(statusid,idtransacao,link,carne_id,carne_link)

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
                                 'usuario_c':usuario_c,
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
                            print(e, dados)
                            #continue


if args.gerencianet:
    for t in fmodels.Titulo.objects.filter(observacao__contains='idtransacao',titulogateway__isnull=True):

        if t.portador.gateway_boleto:
            print t
            idtransacao=t.observacao.split('\n')[2].split('idtransacao=')[1]
            link=t.observacao.split('\n')[3].split('link=')[1]
            print idtransacao,link
            novo_titulogateway = fmodels.TituloGateway()
            novo_titulogateway.titulo = t
            novo_titulogateway.gateway = t.portador.gateway_boleto
            novo_titulogateway.idtransacao = idtransacao
            novo_titulogateway.link = link 
            novo_titulogateway.save()


if args.gerencianetcarne:
    carnes = {}
    print 'mapeando carnes'
    for t in fmodels.Titulo.objects.filter(observacao__contains='carnelink=http',titulogateway__isnull=False,carnetitulo__isnull=True):

        if t.portador.gateway_boleto:
            carneid=t.observacao.split('\n')[4].split('carneid=')[1].strip()
            carnelink = t.observacao.split('\n')[5].split('carnelink=')[1].strip()
            if carneid and carnelink:
                if carneid not in carnes:
                    carnes[carneid] = carnelink
                    print carneid

    for c in carnes:
        titulos = fmodels.Titulo.objects.filter(observacao__contains=carnes[c],titulogateway__isnull=False,carnetitulo__isnull=True).order_by('data_vencimento')

        if titulos:
            try:
                parcela = 1
                new_carne = fmodels.Carne()
                new_carne.cobranca = titulos[0].cobranca
                new_carne.usuario = usuario
                new_carne.save()
                for i in titulos:
                    print i.numero_documento,i.data_vencimento,i.cobranca
                    fmodels.CarneTitulo.objects.create(carne=new_carne,titulo=i)
                    fmodels.Titulo.objects.filter(id=i.id).update(parcela=parcela)
                    parcela += 1
                new_carne_gateway = fmodels.CarneGateway()
                new_carne_gateway.carne=new_carne
                new_carne_gateway.carne = new_carne
                new_carne_gateway.gateway = i.portador.gateway_boleto
                new_carne_gateway.link = carnes[c]
                new_carne_gateway.idtransacao = c
                new_carne_gateway.save()
                i.observacao=''
                i.save()
            except Exception as e:
                print(e)



if args.avisos:
    with open(args.avisos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idcliente = int(row[0]) + 60000
            anotacao = row[1]
            cliente = admmodels.Cliente.objects.filter(id=idcliente)
            if cliente:
                n_anotacao = admmodels.ClienteAnotacao()
                n_anotacao.cliente = cliente[0]
                n_anotacao.anotacao = anotacao
                n_anotacao.usuario = usuario
                n_anotacao.save()
                print(cliente)



if args.loginobs:
    with open(args.loginobs, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[0] and row[1]:
                servico = admmodels.ServicoInternet.objects.filter(login=row[0])
                if servico:
                    servico = servico[0]
                    print servico
                    if servico.observacao:
                        servico.observacao = "%s\n%s" %(row[1],servico.observacao)
                    else:
                        servico.observacao = row[1]
                    servico.save()


