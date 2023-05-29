#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=False)

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max, F

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
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]

if args.arquivo:

    incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 5000
    if incrementar < 5000:
        incrementar = 5000
    else:
        incrementar += 1

    m = manage.Manage()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in conteudo:
            idcliente = int(row[0])
            idcontrato = int(row[45])
            
            #print row
            login=ustrl(row[1])
            if row[44]:
                senha=row[44]
            else:
                senha='controllr2sgp'
            if not login:
                login = 'c%s' %idcontrato
            #if not senha:
            #    senha = login


            #
            # Dados pessoais 
            #
            nome = ustr(row[3])
            cpfcnpj = ustr(row[5])
            rgie = ustr(row[8])
            profissao = ustr(row[9])
            tipo = ustr(row[2])

            if row[10] == 'Masculino':
                sexo = 'M'
            elif row[10] == 'Feminino':
                sexo = 'F'
            else:
                sexo = None
            data_nasc = None
            try:
                y_,m_,d_ = row[11].split(' ')[0].split('-')
                data_nasc=date(int(y_),int(m_),int(d_))
            except:
                pass

            #
            # Endereço 
            #
            logradouro = ustr(row[14])[0:255]
            numero = None
            try:
                numero = int(row[15])
            except:
                numero = None
                logradouro += ",%s" %row[15].upper()
            complemento = ustr(row[16])[0:255]
            bairro = ustr(row[17])[0:50]
            cep = ustr(row[18])
            uf = ustr(row[19])
            cidade = ustr(row[20]).upper()[0:50]

            #
            # Contato
            #
            celular = ustr(row[21]).replace('.0','')
            telefonecom = ustr(row[22]).replace('.0','')
            email = ustrl(row[23])   
            telefone = ''
            con_obs=''
            #con_obs = ustr(row[25])
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 

            data_cadastro = datetime.now()
            try:
                y_,m_,d_ = row[25].split(' ')[0].split('-')
                data_cadastro=datetime(int(y_),int(m_),int(d_),0,0,1)
            except:
                pass


            # 
            # Contrato
            # 

            # Servico
            nas_get = row[28].strip()
            plano = row[29].strip()
            plano_valor = str(row[30]).strip()
            plano_download = ustrl(row[31]) or 0
            plano_upload = ustrl(row[32]) or 0
            conexao_tipo = 'ppp'

            ip = ustr(row[33])
            if len(ip) < 7: ip = None

            mac = ustr(row[34])
            if len(mac) < 10: mac = None
            
            try:
                vencimento = int(row[35])
            except:
                vencimento = 10
                print 'erro row (%s)' %(row[35])

            comodato = ustrl(row[40]).lower()
            if comodato == 'sim':
                comodato = True
            elif comodato in ['nao','não','N_o']:
                comodato = False

            isento = ustr(row[41])
            if isento == 'sim':
                isento = 100
            else:
                isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            cliente_status = ustrl(row[42])
            contrato_status = ustrl(row[43])
            conexao_status = ustrl(row[46])

            if cliente_status == '1':
                status_cc = 3
                status_s = 3
                status_c = 3
            else:
                if contrato_status == '1':
                    status_cc = 3
                    status_s = 3
                    status_c = 3
                elif conexao_status == '4':
                    status_cc = 4
                    status_s = 4
                    status_c = 4

            #try:
            #    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            #except:
            #    if args.planoadd:
            #        new_plano = admmodels.Plano()
            #        new_plano.descricao=plano
            #        new_plano.preco = plano_valor
            #        new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
            #        new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
            #        try:
            #            new_plano.save()
            #        except:
            #            new_plano.preco=0.00
            #            new_plano.save()
#
            #        new_plano_internet = admmodels.PlanoInternet()
            #        new_plano_internet.plano = new_plano 
            #        new_plano_internet.download = plano_download
            #        new_plano_internet.upload = plano_upload
            #        new_plano_internet.save() 
            #        print('criado plano %s' %plano)
            #    else:
            #        raise Exception('Não localizei plano %s' %plano)
#
            cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                pass
                #pop = pop_default
                #print 'Não localizei cidade: %s - Definindo POP: %s' %(cidade_q,pop_default)

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save() 

            #
            # Endereço 
            #
            c_end_logradouro = ustr(row[47])[0:255]
            c_end_numero = None
            try:
                c_end_numero = int(row[48])
            except:
                c_end_numero = None
                c_end_logradouro += ",%s" %row[48].upper()
            c_end_complemento = ustr(row[49])[0:255]
            c_end_bairro = ustr(row[50])[0:50]
            c_end_cep = ustr(row[51])
            c_end_uf = ustr(row[52])
            c_end_cidade = ustr(row[53]).upper()[0:50]


            #
            # Endereço 
            #
            s_end_logradouro = ustr(row[54])[0:255]
            s_end_numero = None
            try:
                s_end_numero = int(row[55])
            except:
                s_end_numero = None
                s_end_logradouro += ",%s" %row[55].upper()
            s_end_complemento = ustr(row[56])[0:255]
            s_end_bairro = ustr(row[57])[0:50]
            s_end_cep = ustr(row[58])
            s_end_uf = ustr(row[59])
            s_end_cidade = ustr(row[60]).upper()[0:50]


            #print pop
            #print row


            
            print('CONSULTANDO CLIENTE %s Login %s' %(nome,login))
            servico = admmodels.ServicoInternet.objects.filter(Q(login=login),
                                                               Q(endereco__logradouro__iexact=F('clientecontrato__cliente__endereco__logradouro')),
                                                               Q(endereco__bairro__iexact=F('clientecontrato__cliente__endereco__bairro')),
                                                               Q(~Q(endereco__logradouro__iexact=s_end_logradouro)|
                                                                 ~Q(clientecontrato__cobranca__endereco__logradouro__iexact=c_end_logradouro)
                                                               )
                                                               ).first()

            if servico:
                endereco_contrato = servico.clientecontrato.cobranca.endereco 
                endereco_servico = servico.endereco

                #print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
                #print logradouro,numero or '',complemento,bairro,cidade,uf,cep
                #print c_end_logradouro,c_end_numero or '',c_end_complemento,c_end_bairro,c_end_cidade,c_end_uf,c_end_cep
                #print s_end_logradouro,s_end_numero or '',s_end_complemento,s_end_bairro,s_end_cidade,s_end_uf,s_end_cep
                #print 'vencimento: ', vencimento, 'Plano: ', plano
                #print telefone,telefonecom,celular,email,con_obs
                #print login,senha,ip,mac
                #print '####################################################'

                if endereco_contrato.logradouro.upper() != c_end_logradouro.upper():
                    change = True
                    print('UPDATE END CONTRATO',endereco_contrato.logradouro,c_end_logradouro)
                    print(c_end_logradouro,c_end_numero or '',c_end_complemento,c_end_bairro,c_end_cidade,c_end_uf,c_end_cep)
                    endereco_contrato.logradouro = c_end_logradouro.upper()
                    endereco_contrato.numero = c_end_numero
                    endereco_contrato.complemento = c_end_complemento.upper()
                    endereco_contrato.bairro = c_end_bairro.upper()
                    endereco_contrato.cep = c_end_cep.upper()
                    endereco_contrato.uf = c_end_uf.upper()
                    endereco_contrato_cidade = c_end_cidade.upper()
                    endereco_contrato.save()


                if endereco_servico.logradouro.upper() != s_end_logradouro.upper():
                    change = True
                    print('UPDATE END SERVICO',endereco_servico.logradouro,s_end_logradouro)
                    print(s_end_logradouro,s_end_numero or '',s_end_complemento,s_end_bairro,s_end_cidade,s_end_uf,s_end_cep)
                    endereco_servico.logradouro = s_end_logradouro.upper()
                    endereco_servico.numero = s_end_numero
                    endereco_servico.complemento = s_end_complemento.upper()
                    endereco_servico.bairro = s_end_bairro.upper()
                    endereco_servico.cep = s_end_cep.upper()
                    endereco_servico.uf = s_end_uf.upper()
                    endereco_servico_cidade = s_end_cidade.upper()
                    endereco_servico.save()



