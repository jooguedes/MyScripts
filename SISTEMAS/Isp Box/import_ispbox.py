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
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
#parser.add_argument('--adcobranca', dest='adcobranca', type=str, help='adicionar remover acrescimos',required=False)
#parser.add_argument('--coordenadas', dest='coordenadas', type=str, help='adicionar remover acrescimos',required=False)
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
from apps.atendimento import models as amodels
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

def ajustaValores(valor):
    return valor.replace(',','.').strip



if args.clientes:
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

    m = manage.Manage()
    with open(args.clientes, 'rU') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1
            try:
                idcontrato = int(row[0])
            except:
                print("ocorreu uma excessao no contrato de id", idcontrato)
        
            login=ustrl(row[23])
            nome = ustr(row[1])
            cpfcnpj = ustr(row[3])[:20]
            rgie = ustr(row[4])[:20]
            tipo = ustr(row[2])
    
            if(row[8] == 'M' or 'm'):
                sexo = 'M'

            elif(row[8] == 'F' or 'f'):
                sexo = 'F'

            else:
                sexo = None

            data_nasc = None

            try:
                y_,m_,d_ = row[5].strip().split('-')

                if len(y_) == 2:
                    y_ = '19%s' %y_

                date(int(y_),int(m_),int(d_))
                data_nasc='%s-%s-%s' %(y_,m_,d_)
            
            except:
                pass

            #
            # Endereço
            #
            logradouro = ustr(row[9])
            numero = None
            try:
                numero = int(row[10])
            except:
                numero = None
                logradouro="sem dados"
            complemento = ustr(row[11])
            bairro = ustr(row[12]).strip()[0:50]
            cep = ustr(row[18]).strip()[0:20]
            uf = ustr(row[7])
            cidade = ustr(row[14]).upper()[0:50]

            #
            # Contato
            #
            celular = ustr(row[17])
            telefonecom = ustr(row[16])
            email = ustrl(row[19])
            try:
                telefone = row[16]
            except:
                print("cliente ",nome, " teve uma exessao no numero de telefone")
                telefone=None
                continue
            #servico_obs=row[9]
            con_obs = ''

            data_cadastro = datetime.now()
            try:
                y_,m_,d_ = row[21].strip().split('-')
                if len(y_) == 2:
                    y_ = '20%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass


            #
            # Contrato
            #

            # Servico
            plano = row[26].strip()
            conexao_tipo = ustrl(row[22])
            conexao_tipo = 'ppp'
            if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'

            ip = None
            mac = ustr(row[23])
            if len(mac) < 10: mac = None
            try:
                vencimento = int(row[34])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(row[34],ri)

            comodato = ustrl(row[39]).lower()
            if comodato in ['Sim','sim']:
                comodato = True
            elif comodato in ['nao','não','N_o']:
                comodato = False

            isento = None
            if isento in ['Sim','sim']:
                isento = 100
            else:
                isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            #status = ustrl(row[41])
            status_bloqueado = ustrl(row[42])

            '''if status in  ['Sim','sim','s']:
                status_cc = 1
                status_s = 1
                status_c = 1

                if status_bloqueado in ['Sim','sim']:
                    status_cc = 4
                    status_s = 4
                    status_c = 4

            if status in ['Não','Nao','nao','não','n']:
                status_cc = 3
                status_s = 3
                status_c = 3'''
                

            if row[43]:
                senha=row[43]
            else:
                senha='mkauth2sgp'

            plano_download = int(row[44].replace(".00",'') or 0)
            plano_upload = int(row[45].replace(".00",'') or 0)
            plano_valor = float(row[46].replace(",",".") or 0)
            
            if len(ustr(row[14])) == 0 and len(cidade.strip()) == 0:

                logradouro = ustr(row[50])
                numero = None
                try:
                    numero = int(row[51])
                except:
                    numero = None
                    logradouro += ",%s" %row[51]
                bairro = ustr(row[52]).strip()[0:50]
                cidade = ustr(row[53]).upper()[0:50]
                cep = ustr(row[54]).strip()[0:20]
                uf = ustr(row[55])
                complemento = ustr(row[56])

            nome_pai = row[57]
            nome_mae = row[58]
            naturalidade = row[59]

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if args.planoadd:
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
                    new_plano_internet.save()
                    print('criado plano %s' %plano)
                else:
                    raise Exception('Não localizei plano %s' %plano)

            cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=uf
                new_pop.save()
                pop = new_pop

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

            #print pop
            #print row

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                print "Import %s" %nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcontrato)

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
                    new_cliente.id = idcontrato
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


if args.chamados:
    cdtipo = 300
    cdmotivo = 300

    max_tipo = amodels.Tipo.objects.all().order_by('-id')[0]
    if max_tipo.codigo > 200:
        cdtipo = max_tipo.codigo + 1
    max_motivo = amodels.MotivoOS.objects.all().order_by('-id')[0]
    if max_motivo.codigo > 200:
        cdmotivo = max_motivo.codigo + 1

    metodo = amodels.Metodo.objects.all()[0]

    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            protocolo = row[0]
            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            login = row[1].strip().lower()
            assunto = row[2]
            status = row[3]
            data_cadastro = row[4]
            data_agendamento = row[5]
            data_finalizacao = row[6]
            conteudo = row[7]
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no ISPBOX."
            servicoprestado = row[8]

            servico = admmodels.ServicoInternet.objects.filter(login__trim__lower=login)

            if servico:
                clientecontrato = servico[0].clientecontrato
                tipo_obj = amodels.Tipo.objects.filter(descricao=assunto)
                motivo_obj = amodels.MotivoOS.objects.filter(descricao=assunto)

                if tipo_obj:
                    tipo_obj = tipo_obj[0]
                else:
                    tipo_obj = amodels.Tipo()
                    tipo_obj.codigo=cdtipo
                    tipo_obj.descricao=assunto
                    tipo_obj.save()
                    cdtipo += 1

                if motivo_obj:
                    motivo_obj = motivo_obj[0]
                else:
                    motivo_obj = amodels.MotivoOS()
                    motivo_obj.codigo=cdmotivo
                    motivo_obj.descricao=assunto
                    motivo_obj.save()
                    cdmotivo += 1

                if amodels.Ocorrencia.objects.filter(numero=protocolo).count() == 0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['clientecontrato'] = clientecontrato
                    ocorrencia['tipo'] = tipo_obj
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo
                    ocorrencia['numero'] = protocolo
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if status == 'fechado' else amodels.OCORRENCIA_ABERTA
                    ocorrencia['responsavel'] = ocorrencia['usuario']

                    ocorrencia['data_cadastro'] = data_cadastro
                    ocorrencia['data_agendamento'] = data_agendamento
                    ocorrencia['data_finalizacao'] = data_finalizacao
                    ocorrencia['conteudo'] = conteudo
                    ocorrencia['observacoes'] = servicoprestado
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
                    ordem['status'] = amodels.OS_ENCERRADA if status == 'fechado' else amodels.OS_ABERTA
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



if args.coordenadas:
    with open(args.coordenadas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            print(admmodels.Endereco.objects.filter(servicointernet__login__iexact=row[0]).update(map_ll=row[1]))
            print(admmodels.Endereco.objects.filter(cobranca__clientecontrato__servicointernet__login__iexact=row[0]).update(map_ll=row[1]))



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