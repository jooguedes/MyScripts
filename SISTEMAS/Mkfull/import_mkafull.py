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
parser.add_argument('--subscribers', dest='subscribers', type=str, help='Subscribers CSV File',required=True)
parser.add_argument('--contracts', dest='contracts', type=str, help='Contracts CSV File',required=True)
parser.add_argument('--plans', dest='plans', type=str, help='Plans CSV File',required=True)
args = parser.parse_args()
#python import_mkafull.py --settings=sgp.gsnetlink.settings --nas=1 --portador=3 --subscribers=Conv-subscribers.csv --contracts=Conv-contracts.csv --plans=Conv-plans.csv
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

nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)

m = manage.Manage()
if args.subscribers and args.plans and args.contracts:
    contracts = {}
    plans = {}

    with open(args.plans, 'rb') as csvfile:
        content = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in content:
            plan_id = row[0]
            plans[plan_id] = row
    with open(args.contracts, 'rb') as csvfile:
        content = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in content:
            subscriber_id = row[6]
            contracts[subscriber_id ] = row
    with open(args.subscribers, 'rb') as csvfile:
        content = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in content:
            subscriber_id = row[0] 
            fullname = row[8]
            nickname = row[9]
            cpfcnpj = row[10]
            rgie = row[11]
            person_type = row[28]
            if person_type == "0":
                person_type = "F"
            else:
                person_type = "J"
            date_of_birth = row[16].strip()
            if not date_of_birth:
                date_of_birth = None 
            street = row[34]
            if street == "":
                street = "Sem logradouro no sistema anterior."
            number = row[35]
            if number == "":
                number = "0"
            complement = row[36]
            reference = row[37]
            neighborhood = row[38]
            if neighborhood == "":
                neighborhood = "Sem bairro no sistema anterior."
            city = ustr(row[39])
            if city == "":
                city = ustr("OLINDA")
            state = row[40]
            if state == "":
                state = "SP"
            zipcode = row[41]
            if zipcode == "":
                zipcode = "53370320"
            plan_name = ""
            plan_price = ""
            plan_download = ""
            plan_upload = ""
            created_at = ""
            payment_day = 10
            username = ""
            password = ""
            ip = ""
            mac = ""
            service_observation = ''
            sex = None
            profession = None
            place_of_birth = row[17]
            free = None
            bloqued = None
            simultaneous_login = None
            montly_discount = None
            montly_addition = None
            lending = None
            activation_fee = None
            punctuality_discount = None
            punctuality_discount_days = None
            days_before_block = None
            plan = None

            contract = contracts.get(subscriber_id)
            if not contract:
                continue

            if contract:
                plan_id = contract[5]
                plan = plans.get(plan_id)
                if plan:
                    plan_name = plan[5]
                    plan_price = float(plan[10])
                    plan_download = int(plan[8])
                    plan_upload = int(plan[9])
                    activation_fee = float(plan[11])
                    punctuality_discount = float(plan[12])
                    punctuality_discount_days = int(plan[13])
                    days_before_block = int(plan[21])
                created_at = row[43]
                if created_at == "":
                    created_at = date.today()
                else:
                    created_at = row[43].split(' ')[0]
                if not created_at:
                    created_at = date.today()
                payment_day = int(row[6])
                username = '%s@mkafull' %contract[10]
                password = contract[11]
                free = contract[13]
                if free == "1":
                    free = 100
                else:
                    free = "0"
                bloqued = contract[39]
                deactivated = contract[59]

                simultaneous_login = contract[12]
                montly_discount = contract[18]
                montly_addition = contract[17]
                lending = contract[16]
                if lending > 0:
                    lending = 1
                else:
                    lending = 0
                if not password:
                    password = 'sem_senha'
                ip = contract[24]
                mac = contract[26]
            email = row[18]
            email2 = row[19]
            phone1 = row[20]
            phone2 = row[21]
            phone3 = row[22]
            father = row[14]
            mother = row[15]
            gps = row[42]
            status_cc = 1
            status_s = 1
            status_c = 1

            if bloqued == '1':
                status_cc = 4
                status_s = 4
                status_c = 4

            if deactivated:
                status_cc = 3 
                status_s = 3
                status_c = 3 

            connection_type = "ppp"

            if plan:
                try:
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plan_name.lower())[0]
                except:
                    new_plan = admmodels.Plano()
                    new_plan.descricao=plan_name
                    new_plan.preco = plan_price
                    new_plan.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
                    new_plan.grupo = admmodels.Grupo.objects.get(nome='cabo')
                    new_plan.save()

                    new_plan_internet = admmodels.PlanoInternet()
                    new_plan_internet.plano = new_plan
                    new_plan_internet.download = plan_download
                    new_plan_internet.upload = plan_upload
                    new_plan_internet.save()
                    print('Creating plan %s' %plan_name)

            city_q = normalize('NFKD', city).encode('ASCII','ignore').decode('ascii')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %city_q)[0]
                pop = pop_q
            except:
                print(city_q.upper(),state)
                new_pop = admmodels.Pop()
                new_pop.cidade=city_q.upper()
                new_pop.uf=state
                new_pop.save()
                pop = new_pop

            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=payment_day)
            except:
                print "Payment day error: %s" %payment_day
                print('Revising payment day: %s' %payment_day)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = payment_day
                new_vencimento.save()

            print(fullname, cpfcnpj, date_of_birth, person_type)
            print(street, neighborhood, city, state, zipcode)
            print('Payment Day: ', payment_day, 'Plan: ', plan_name)
            print '##################################################'

            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=username).count() == 0:
                print "Import %s" %fullname

                new_address = admmodels.Endereco()
                new_address.logradouro = street
                new_address.numero = number
                new_address.bairro = neighborhood
                new_address.cep = zipcode
                new_address.cidade = city
                new_address.uf = state
                new_address.pais = 'BR'
                new_address.complemento = complement
                new_address.pontoreferencia = reference

                new_address_cob = copy.copy(new_address)
                new_address_inst = copy.copy(new_address)
                new_address.save()
                new_address_cob.save()
                new_address_inst.save()

                if person_type == "F":
                    new_person = admmodels.Pessoa()
                    new_person.tipopessoa="F"
                    new_person.nome = fullname
                    new_person.sexo = sex
                    new_person.datanasc = date_of_birth
                    new_person.profissao = profession
                    new_person.nacionalidade = "BR"
                    new_person.nomepai = father
                    new_person.nomemae = mother
                    new_person.naturalidade = place_of_birth
                    new_person.rg = rgie
                    new_person.cpfcnpj = cpfcnpj
                    new_person.rg_emissor = ""
                    try:
                        new_person.save()
                    except Exception as e:
                        print(e)
                        new_person.datanasc=None
                        new_person.save()

                if person_type == "J":
                    new_person = admmodels.Pessoa()
                    new_person.tipopessoa="J"
                    new_person.nome = fullname
                    new_person.nomefantasia = nickname
                    new_person.resempresa = ""
                    new_person.cpfcnpj = cpfcnpj
                    new_person.insc_estadual = ""
                    new_person.tipo = 8
                    new_person.save()

                # Cliente
                new_client = admmodels.Cliente()
                new_client.id=subscriber_id
                new_client.endereco = new_address
                new_client.pessoa = new_person
                new_client.data_cadastro = created_at
                new_client.data_alteracao = created_at
                new_client.ativo = True
                new_client.save()

                # contato 1
                if len(email) > 4:
                    new_contact = admmodels.Contato()
                    new_contact.tipo = 'EMAIL'
                    new_contact.contato = email
                    new_contact.save()
                    new_ccontact = admmodels.ClienteContato()
                    new_ccontact.cliente = new_client
                    new_ccontact.contato = new_contact
                    new_ccontact.save()

                # contato 2
                if len(phone1) > 4:
                    new_contact = admmodels.Contato()
                    new_contact.tipo = 'CELULAR_PESSOAL'
                    new_contact.contato = phone1
                    new_contact.save()
                    new_ccontact = admmodels.ClienteContato()
                    new_ccontact.cliente = new_client
                    new_ccontact.contato = new_contact
                    new_ccontact.save()

                # contato 3
                if len(phone2) > 4:
                    new_contact = admmodels.Contato()
                    new_contact.tipo = 'CELULAR_PESSOAL'
                    new_contact.contato = phone2
                    new_contact.save()
                    new_ccontact = admmodels.ClienteContato()
                    new_ccontact.cliente = new_client
                    new_ccontact.contato = new_contact
                    new_ccontact.save()

                # contato 4
                if len(phone3) > 4:
                    new_contact = admmodels.Contato()
                    new_contact.tipo = 'CELULAR_PESSOAL'
                    new_contact.contato = phone3
                    new_contact.save()
                    new_ccontact = admmodels.ClienteContato()
                    new_ccontact.cliente = new_client
                    new_ccontact.contato = new_contact
                    new_ccontact.save()

                # Cobranca
                new_charge = fmodels.Cobranca()
                new_charge.cliente = new_client
                new_charge.endereco = new_address_cob
                new_charge.portador = portador
                new_charge.vencimento = fmodels.Vencimento.objects.get(dia=payment_day)
                new_charge.isento = free
                new_charge.notafiscal = False
                new_charge.data_cadastro = created_at
                new_charge.datacobranca1 = created_at
                new_charge.usuariocad = usuario
                new_charge.formacobranca = formacobranca
                new_charge.status = status_c
                new_charge.save()

                new_charge.data_cadastro = created_at
                new_charge.save()

                # Contrato
                new_contract = admmodels.ClienteContrato()
                new_contract.cliente = new_client
                new_contract.pop = pop
                new_contract.cobranca = new_charge
                new_contract.data_inicio = created_at
                new_contract.data_cadastro = created_at
                new_contract.data_alteracao = created_at
                new_contract.save()

                for status_type in [6,2,status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contract
                    new_status.status = status_type
                    new_status.modo = 2
                    new_status.usuario = usuario
                    new_status.data_cadastro = created_at
                    new_status.save()

                # Servico
                if plan:
                    new_service = admmodels.ServicoInternet()
                    new_service.clientecontrato = new_contract
                    new_service.status = status_s
                    if admmodels.ServicoInternet.objects.filter(login=username).count() > 0:
                        print("Already exist service with this login %s. Adjusting login: %s%s" %(username, username, str(new_contract.id)))
                        username += str(new_contract.id)
                    new_service.login= username
                    new_service.endereco = new_address_inst
                    new_service.login_password = password
                    new_service.login_password_plain = password
                    new_service.central_password = password
                    if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                        new_service.mac_dhcp = mac
                        new_service.mac = mac
                    if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                        new_service.ip = ip
                    new_service.tipoconexao = connection_type
                    new_service.nas = nas
                    new_service.planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact = plan_name.lower())[0]
                    new_service.modoaquisicao = lending
                    new_service.data_cadastro=created_at
                    new_service.save()
                    m.addRadiusServico(new_service)

                admmodels.Endereco.objects.filter(servicointernet__login__iexact = username).update(map_ll = gps)
                admmodels.Endereco.objects.filter(cobranca__clientecontrato__servicointernet__login__iexact = username).update(map_ll = gps)

for p in admmodels.Pop.objects.all():
    for plano in admmodels.Plano.objects.all():
        plano.pops.add(p)
    for n in nmodels.NAS.objects.all():
        n.pops.add(p)