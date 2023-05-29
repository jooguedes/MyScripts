#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import os, sys
import socket, struct
from datetime import date, datetime
from django.db.models import Q, Max
import argparse


parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

#python import_duobox.py --settings=sgp.jvnnet.settings --nas=1 --pop=1 --vencimentoadd=1 --planoadd=1 --portador=1 --arquivo=duobox-clientes.csv.utf8


if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')
nas_default = nmodels.NAS.objects.get(pk='1')
def ip2long(num):
    """
    Convert an IP string to long
    """
    return socket.inet_ntoa(struct.pack('!L', long(num)))
m = manage.Manage()
with open('/tmp/teste.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        conexao_tipo = 'ppp'
        nas_get = ''
        try:
            nas = nmodels.NAS.objects.get(shortname__iexact=nas_get.strip())
        except:
            nas = nas_default
            print 'Não localizei NAS com nome %s. Definindo NAS: %s' %(nas_get,nas_default)
        tipo_pessoa = row[6]
        cpf = row[9]
        cnpj = row[10]

        if tipo_pessoa=='F':
            cpfcnpj=cpf
        else:
            cpfcnpj=cnpj
            
        status_cc = 1
        status_s = 1
        status_c = 1
        mac=None

        isento = ustr(row[84])
        if isento == '1':
            isento = 100
        else:
            isento = 0

        status = ustrl(row[85])

        ativo = row[83]

        isento = ustr(row[84])
        if isento == '1':
            isento = 100
        else:
            isento = 0

        status = ustrl(row[85])

        if ativo == '1':
            if status == '1':
                status_cc = 1
                status_s = 1
                status_c = 1
            else:
                status_cc = 4
                status_s = 4
                status_c = 4
        else:
            status_cc = 3
            status_s = 3
            status_c = 3



        login = row[80]
        if not login:
            login = 'c%s' %id
        if login == '0':
            continue 
        senha = row[81]
        if not senha:
            senha = '123456'
        ip = ustr(row[82])
        if ip and '.' not in ip:
            ip = ip2long(ip)
            if ip == '0.0.0.0':
                ip = None
            else:
                print 'IP:::::::::::::::::::::::::::::%s' %ip

        comodato = False
        plano = row[86].strip()
        print(row[50])
        data_cadastro = datetime.now()
        try:
            data_cadastro=row[50]
        except:
            pass


        if data_cadastro == '1':
            data_cadastro = datetime.now()
        
        data_inicio = date.today()
        try:
            diy,dim,did = data_cadastro.split(' ')[0].split('-')
            data_inicio = date(int(diy),int(dim),int(did))
        except:
            pass 


        planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
        cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)

        contrato_atual=admmodels.ClienteContrato.objects.filter(cliente=cliente[0].id)
        print(contrato_atual[0].id)
        endereco= admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
        
        print(endereco)
        endereco_inst=admmodels.Endereco.objects.filter(id=endereco.pessoa.endereco.id)
        endereco_inst.id=None
    
        

        
        cobranca= fmodels.Cobranca.objects.filter(cliente=cliente[0].id)
        new_contrato = admmodels.ClienteContrato()
        new_contrato.cliente = cliente[0]
        new_contrato.cobranca= cobranca[0]
        data_inicio = date.today()
        
        try:
           diy,dim,did = data_cadastro.split(' ')[0].split('-')
           data_inicio = date(int(diy),int(dim),int(did))
        except:
           pass 



        print(cobranca, cliente, planointernet)
        ################################# SAVE DOS NOVOS CONTRATOS #################################
        if args.sync_db:
            if cliente:
                contrato_atual=admmodels.ClienteContrato.objects.filter(cliente=cliente[0].id)
            if contrato_atual:
                admmodels.ServicoInternet.objects.filter(contrato=contrato_atual[0].id).delete()
                admmodels.ClienteContrato.objects.filter(cliente=cliente[0].id).delete()
                
            endereco_inst.save()
            planointernet.save()

            new_contrato.data_inicio = data_inicio 
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


            new_servico = admmodels.ServicoInternet()
            new_servico.clientecontrato = new_contrato 
            new_servico.status = status_s
            if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                    login,
                                                                                    str(new_contrato.id))
                login += str(new_contrato.id)
            new_servico.login= login
            new_servico.endereco = endereco_inst
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