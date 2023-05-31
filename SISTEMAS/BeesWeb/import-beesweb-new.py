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
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--suportes', dest='suportes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--suportesclientes', dest='suportesclientes', type=str, help='Arquivo importacao',required=False)
args = parser.parse_args()


#   python import_beesweb.py --settings=sgp.maxlink.settings --pop=1 --portador=1 --arquivo=
#   python import_beesweb.py --settings=sgp.maxlink.settings --suportesclientes= --suportes=

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
from apps.atendimento import models as amodels
from apps.netcore.utils.radius import manage


if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]

if args.pop_id:
    pop_default = admmodels.Pop.objects.get(pk=args.pop_id)

if args.portador_id:
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
count = 3
def convertdata(d):
    if d:
        if '/' in d:
            d,m,y = d.split('/')
            return '%s-%s-%s' %(y,m,d)
        return d
    return None

add_id_cliente = 0
add_id_contrato = 1
add_string_login = ''


m = manage.Manage()
if args.arquivo:
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            idcliente = int(row[0])+add_id_cliente
            nome = row[1]
            plano = row[22]
            try:
                vencimento = fnum(row[8])
            except:
                vencimento = 10
            cpfcnpj = row[7]
            #if not cpfcnpj:
                #cpfcnpj = row[6]
            login = '%s%s'%(row[24], add_string_login)

            if row[24] == '':
                login = 'SEM_LOGIN_%s'%idcliente

            if not login:
                login = 'sem_login_%i'%idcliente
            
            senha = row[25]
            if not senha:
                senha='123456789'
                


            tipo = ustr(row[5])
            #tipo = 'f'
            if len(cpfcnpj) > 15:
                tipo = 'j'

            sexo = None

            rgie = row[6]
            profissao = ''
            data_cadastro = convertdata(row[4])
            
            logradouro = row[14]
            try:
                numero = int(re.sub('[^0-9]','', str(row[15])))
            except:
                numero = None
            complemento = row[19]
            bairro = row[16]
            cidade = row[17]
            uf = row[18]
            cep = row[13]
            
            celular = row[9]
            telefone = row[10]
            telefonecom = row[11]
            telefonecom2 = row[12]

            email = row[2]

            con_obs=''

            data_nasc = convertdata(row[3])
            print(data_nasc)
            if not data_nasc:
                data_nasc = None


            #con_obs = ustr(row[25])
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 

            
            #try:
            #    d_,m_,y_ = row[26].split('/')
            #    data_cadastro='%s-%s-%s' %(y_,m_,d_)
            #except:
            #    pass


            # 
            # Contrato
            # 

            # Servico
            try:
                plano_valor = float(row[23].strip().replace(',','.')) or '0.00'
            except:
                plano_valor = '0.00'

            #conexao_tipo = ustrl(row[30])
            conexao_tipo = 'ppp'
            #if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            #if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'


            ip = ''
            if len(ip) < 7: ip = None

            mac = ''
            if len(mac) < 10: mac = None
            

            comodato = 'nao'
            if comodato == 'sim':
                comodato = True
            elif comodato in ['nao','não','N_o']:
                comodato = False

            isento = 'nao'
            if isento == 'Sim':
                isento = 100
            else:
                isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            status = row[28]

            if status in  ['Ativo']:
                    status_cc = 1
                    status_s = 1
                    status_c = 1

                    if row[27] in ['Bloqueio']:
                        status_cc = 4
                        status_s = 4
                        status_c = 4

            if status in ['Desativado']:
                status_cc = 3
                status_s = 3
                status_c = 3

            
            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                new_plano = admmodels.Plano()
                new_plano.descricao=plano
                new_plano.preco = plano_valor
                new_plano.contrato = admmodels.Contrato.objects.filter(grupo__nome='fibra')[0]
                new_plano.grupo = admmodels.Grupo.objects.filter(nome='fibra')[0]
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano 
                new_plano_internet.download = 10240
                new_plano_internet.upload = 5172
                new_plano_internet.save() 
                print('criado plano %s' %plano)
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]

            if nmodels.NAS.objects.filter(shortname=row[21]).count() == 0:
                new_nas = nmodels.NAS()
                new_nas.shortname= row[21]
                new_nas.secret = '123@mudar'
                new_nas.description = row[21]
                new_nas.nasname= '172.0.0.%s'%count
                new_nas.save()
                try:
                    new_nas.save()
                    count +=1
                    nas = new_nas
                except Exception as a:
                    print ('Erro ao cadastrar o NAS, erro: ', a)
            else:
                nas = nmodels.NAS.objects.get(shortname=row[21])

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                try:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()
                except:
                    vencimento='10'
                


            #print pop
            #print row
            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano, 'Plano Valor:', plano_valor
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True:
                print "Import %s" %nome
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
                
                new_endereco_cob = copy.copy(new_endereco)
                new_endereco_inst = copy.copy(new_endereco)
                new_endereco.save() 
                new_endereco_cob.save()
                new_endereco_inst.save()
                
                if admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj).count() == 0:

                    
                    tp = 'f'
                    if len(cpfcnpj) > 14 or tipo.lower() in [u'pessoa jur_dica',u'pessoa jurídica']:
                        tp = 'j'
                    
                    if tp in['f','F']:
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
                        new_pessoa.save()

                    
                    if tp in ['j','J']:
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome
                        
                        new_pessoa.nomefantasia = nome
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = iestadual
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
                        new_contato.tipo = 'CELULAR_COMERCIAL'
                        new_contato.contato = telefone 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 4
                    if len(telefonecom) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                        new_contato.contato = telefonecom 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    # contato 5
                    if len(telefonecom2) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'TELEFONE_FIXO_COMERCIAL'
                        new_contato.contato = telefonecom2 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                else:
                    new_cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)[0]
                
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
                if admmodels.ClienteContrato.objects.filter(id=add_id_contrato).count() > 0:
                    add_id_contrato += admmodels.ClienteContrato.objects.all().order_by('-id')[0]
                    
                new_contrato = admmodels.ClienteContrato()
                new_contrato.id = add_id_contrato
                new_contrato.cliente = new_cliente 
                new_contrato.pop = pop_default
                new_contrato.cobranca = new_cobranca
                
                new_contrato.data_inicio = data_cadastro 
                new_contrato.data_cadastro = data_cadastro 
                new_contrato.data_alteracao = data_cadastro
                try:
                    new_contrato.save()
                    add_id_contrato += 1
                except Exception as a:
                    print('Erro ao cadastrar CLIENTECONTRATO, erro: ', a)
                
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
                    login = '%s_import'%login
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
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

if args.suportes:
    cdtipo = 300
    cdmotivo = 300

    with open(args.suportesclientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        indice = 0
        dados_clientes = {}
        for row in conteudo:
            cliente={
                'cpfcnpj': row[7],
                'nome': row[1]
            }
            dados_clientes[indice]=cliente
            indice +=1

    max_tipo = amodels.Tipo.objects.all().order_by('-id')[0]
    if max_tipo.codigo > 200:
        cdtipo = max_tipo.codigo + 1
    max_motivo = amodels.MotivoOS.objects.all().order_by('-id')[0]
    if max_motivo.codigo > 200:
        cdmotivo = max_motivo.codigo + 1

    metodo = amodels.Metodo.objects.all()[0]

    with open(args.suportes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            protocolo = row[0].strip()

            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            login = row[2].strip().lower()
            assunto = row[2][:30]
            if row[7].strip() == 'Finalizado':
                status = amodels.OCORRENCIA_ENCERRADA
            else:
                status = amodels.OCORRENCIA_ABERTA
            try:
                data_cadastro = convertdata(row[8].split()[0])
            except:
                data_cadastro = datetime.now()

            try:
                data_agendamento = convertdata(row[9].split()[0])
            except:
                data_agendamento = None

            try:
                data_finalizacao = data_agendamento
            except:
                data_finalizacao = None
            conteudo = 'TÉCNICO: %s| Tipo:  %s | Prioridade: %s | Descriação: %s'%(row[6], row[5], row[4], row[3])
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no ReceitaNet."
            servicoprestado = ''

            for c in dados_clientes:
                if dados_clientes[c]['nome'] == row[1]:
                    cpfcnpj = dados_clientes[c]['cpfcnpj']
                    try:
                        clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj)[0]
                    except Exception as e:
                        continue

                    if clientecontrato:
                        try:
                            tipo_obj = amodels.Tipo.objects.get(descricao='Outros')
                        except:
                            tipo_obj = amodels.Tipo()
                            tipo_obj.codigo=cdtipo
                            tipo_obj.descricao='Outros'
                            try:
                                tipo_obj.save()
                                cdtipo += 1
                            except:
                                continue
                        
                        try:
                            motivo_obj = amodels.MotivoOS.objects.get(descricao='Outros')
                        except:
                            motivo_obj = amodels.MotivoOS()
                            motivo_obj.codigo=cdmotivo
                            motivo_obj.descricao='Outros'
                            try:
                                motivo_obj.save()
                                cdmotivo += 1
                            except:
                                continue

                        if amodels.Ocorrencia.objects.filter(numero=protocolo).count() == 0:
                            print(row)
                            ocorrencia = {}
                            ocorrencia['clientecontrato'] = clientecontrato
                            ocorrencia['tipo'] = tipo_obj
                            ocorrencia['usuario'] = usuario
                            ocorrencia['metodo'] = metodo
                            ocorrencia['numero'] = protocolo
                            ocorrencia['status'] = status
                            ocorrencia['responsavel'] = ocorrencia['usuario']

                            ocorrencia['data_cadastro'] = data_cadastro
                            ocorrencia['data_agendamento'] = data_agendamento
                            ocorrencia['data_finalizacao'] = data_finalizacao
                            ocorrencia['conteudo'] = conteudo
                            for ok in ocorrencia:
                                if ocorrencia[ok] in ['0000-00-00 00:00:00','0000-00-00','']:
                                    ocorrencia[ok] = None

                            new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                            new_ocorrencia.save()

                            new_ocorrencia.data_cadastro = data_cadastro
                            new_ocorrencia.data_agendamento = data_agendamento
                            new_ocorrencia.data_finalizacao = data_finalizacao

                            if str(new_ocorrencia.data_agendamento) in ['0000-00-00 00:00:00','0000-00-00','']:
                                new_ocorrencia.data_agendamento = None
                            if str(new_ocorrencia.data_finalizacao) in ['0000-00-00 00:00:00','0000-00-00','']:
                                new_ocorrencia.data_finalizacao = None
                            new_ocorrencia.save()

                            ordem = {}
                            ordem['ocorrencia'] = new_ocorrencia
                            ordem['status'] = status
                            ordem['usuario'] = usuario
                            ordem['motivoos'] = motivo_obj
                            ordem['data_cadastro'] = ocorrencia['data_cadastro']
                            ordem['data_agendamento'] = ocorrencia['data_agendamento']
                            ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                            ordem['conteudo'] = ocorrencia['conteudo']

                            for oser in ordem:
                                if ordem[oser] in ['0000-00-00 00:00:00','0000-00-00']:
                                    ordem[oser] = None

                            new_ordem = amodels.OS(**ordem)
                            new_ordem.save()
                            new_ordem.data_cadastro = ocorrencia['data_cadastro']
                            new_ordem.data_agendamento = ocorrencia['data_agendamento']
                            new_ordem.data_finalizacao = ocorrencia['data_finalizacao']
                            if str(new_ordem.data_agendamento) in ['0000-00-00 00:00:00','0000-00-00','']:
                                new_ordem.data_agendamento = None
                            if str(new_ordem.data_finalizacao) in ['0000-00-00 00:00:00','0000-00-00','']:
                                new_ordem.data_agendamento = None
                            new_ordem.save()

                            if servicoprestado != '':
                                new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                                new_ocorrencia_anotacao.ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                                new_ocorrencia_anotacao.anotacao=servicoprestado
                                new_ocorrencia_anotacao.usuario= usuario
                                new_ocorrencia_anotacao.save()