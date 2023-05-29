#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import codecs
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re
from decimal import *

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='arquivo de planos', required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='arquivo de titulos', required=False)
args = parser.parse_args()

################################################################################################################################################

# python import_meuconsultor.py --settings=sgp.local.settings --portador=1 --clientes=meuconsultor-clientes.csv --planos=meuconsultor-planos.csv --nas=1 --pop=1 --sync=1
# python import_meuconsultor.py --settings=sgp.local.settings --portador=1 --nas=1 --pop=1--titulos= --sync=1
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


fnum = lambda n: re.sub('[^0-9]','',n)

usuario = admmodels.User.objects.get(username='sgp')
formapagamento = fmodels.FormaPagamento.objects.all()[0]
planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]
nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)
pop_default = admmodels.Pop.objects.get(pk=args.pop_id)

def formata_data(dt):
    if dt !='':
        if '-' in dt:
            y,m,d=dt.strip().split('-')

            try:
                date(int(y),int(m),int(d))
                return '%s-%s-%s' %(y,m,d)
            except Exception as e:
                print('Erro na validação da data retornando None')
                return None
            
        elif '/' in dt:
            try:
                d,m,y=dt.strip().split('/')
                try:
                    date(int(y),int(m),int(d))
                    return '%s-%s-%s' %(y,m,d)
                except Exception as e:
                    print('Erro na validação da data retornando None')
                return None  
            except Exception as e:
                print('Erro ao atribuir valores: ')
                return datetime.now()
            
    else:
        return None
    
    


def verifica_vencimento(v):
    if v!='':
        if fmodels.Vencimento.objects.filter(dia=v).count() > 0:
            return int(v.strip())
        else:
            new_vencimento= fmodels.Vencimento()
            new_vencimento.dia=int(v.strip())
            new_vencimento.save()

            return int(v.strip())
    else:
        if fmodels.Vencimento.objects.filter(dia=10) > 0:
            return 10
        else:
            new_vencimento= fmodels.Vencimento()
            new_vencimento.dia=10
            new_vencimento.save()
            return 10
        

def cria_observacao(param1,param2):
    if param1!='' and param2!='':
        observacao="OBSERVACAO 01: ", param1, "\n", "OBSERVACAO 02: ", param2
        return observacao
    elif param1!='' or param2!='':
        if param1!='':
            observacao="OBSERVACAO: ",param1
            return observacao
        else:
            observacao="OBSERVACAO: ",param2
            return observacao

def verifica_plano(p):
    if admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=p.lower())>0:
        return admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=p.lower())[0]
    else:
        return admmodels.PlanoInternet.objects.filter(plano__id=args.plano_default)[0]




if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(descricao=row[1]).count()==0:
                new_plano = admmodels.Plano()
                new_plano.descricao=row[1]
                new_plano.preco = row[3].replace(',','.')
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano
                new_plano_internet.download = int(row[5].strip())
                new_plano_internet.upload = int(row[4].strip())
                new_plano_internet.save()
                print("Plano cadastrado ", row)
            


if args.clientes:
   
    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            id_cliente=row[0]
            nome=row[1]
            cpfcnpj=row[2]
            rg=row[3]

            logradouro=row[4]
            numero=fnum(row[5]) if fnum(row[5])!='' else 0
            bairro=row[6]
            cidade=row[7]
            estado=row[8]
            cep=row[9]
            complemento=row[17]
            login=row[10]
            senha=row[11]
            mac= row[12] if row[12] !='' else None

            celular=row[13]
            celular02=row[14] 
            celular03=row[15]

            plano=row[16]

            coordenadas=row[18]
            data_nascimento=formata_data(row[19])
            data_cadastro=formata_data(row[20])
            vencimento=verifica_vencimento(row[21])

            ip=row[22] if row[22] !='' else None
            bloqueado=row[23]
            ativo=row[24]
            cancelado=row[25]

            status_cc = 1
            status_s = 1
            status_c = 1
            
                
            if bloqueado=='sim' and ativo=='sim':
                status_cc = 4
                status_s = 4
                status_c = 4
            
            elif cancelado=='sim' or ativo=='nao':
                status_cc = 3
                status_s = 3
                status_c = 3

            observacoes=cria_observacao(row[26], row[27])
            ativo_em=formata_data(row[28])

            planointernet = verifica_plano(plano)
            conexao_tipo = 'ppp'

            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                
                cliente_check = admmodels.Cliente.objects.filter(id=id_cliente)
                
                if len(cliente_check) == 0:
                    # Endereco
                    new_endereco = admmodels.Endereco()
                    new_endereco.logradouro = logradouro
                    new_endereco.numero = numero
                    new_endereco.bairro = bairro
                    new_endereco.cep = cep
                    new_endereco.cidade = cidade
                    new_endereco.uf = estado
                    new_endereco.pais = 'BR'
                    new_endereco.complemento = complemento
                    new_endereco.pontoreferencia=''

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_cob.id=None
                    new_endereco_inst.id=None

                    try:
                        new_endereco.save()
                        new_endereco_cob.save()
                        new_endereco_inst.save()
                    except Exception as a:
                        print(new_endereco)
                        print(a) 




                    tp = 'f'
                    if len(fnum(cpfcnpj)) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.sexo = None
                        new_pessoa.datanasc = data_nascimento
                        new_pessoa.profissao = ''
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.nomepai = ''
                        new_pessoa.nomemae = ''
                        new_pessoa.naturalidade = ''
                        new_pessoa.rg = rg
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=''
                        try:
                            new_pessoa.save()
                        except:
                            try:
                                new_pessoa.datanasc='19%s' %data_nascimento[-8:]
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
                    new_cliente.id = id_cliente
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.save()
                    
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()


                    # contato 2
                    if len(celular) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular
                        new_contato.observacao = ''
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()


                    # contato 3
                    if len(celular02) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                        new_contato.contato = celular02
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 4
                    if len(celular03) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'TELEFONE_FIXO_COMERCIAL'
                        new_contato.contato = celular03
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
                new_cobranca.isento = '0.00'
                new_cobranca.notafiscal = False
                new_cobranca.data_cadastro = data_cadastro
                new_cobranca.datacobranca1 = data_cadastro
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
                new_cobranca.fidelidade_renovacao_auto=False
                new_cobranca.save()

                new_cobranca.data_cadastro = data_cadastro
                new_cobranca.save()

               

                # Contrato
                new_contrato = admmodels.ClienteContrato()
                new_contrato.id = id_cliente
                new_contrato.cliente = new_cliente
                new_contrato.pop = pop_default
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
                new_servico.mac_dhcp = mac
                new_servico.mac = mac
                new_servico.ip = ip
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas_default
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 0
                new_servico.data_cadastro=data_cadastro
                new_servico.observacao=''
                new_servico.save()
                new_servico.data_cadastro=data_cadastro
                new_servico.save()
                m.addRadiusServico(new_servico)

                print("importando cliente: ", row)

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
            login = row[7]
            cliente = admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login)
            if cliente:
                print("Esse é meu cliente: ", cliente)
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    
                    idtransacao = row[10]
                    numero_documento = fnum(row[4])
                    nosso_numero = fnum(row[4])
                    nosso_numero_f = None
                    demonstrativo = ''
                    data_documento = formata_data(row[13])
                    data_vencimento = formata_data(row[3])
                    data_pagamento = None
                    data_baixa = data_pagamento
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None

                    link = row[12]
                    juros = row[9] if row[9]!='' else 0.00
                    codigo_barras=''
                    linha_digitavel=''
                    valor = row[2].replace(',','.')
                    carne_id = ''
                    carne_link =''
            
                    if row[1]!='':
                        valorpago = row[5].replace(',','.')
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None
                        data_pagamento = formata_data(row[1])
                    desconto = 0.00
                    linha_digitavel = ''
                    codigo_carne = ''
                    chave = ''
                   
                    if nosso_numero:
                        print('entrei no nosso numero')
                        if fmodels.Titulo.objects.filter(nosso_numero=fnum(nosso_numero),portador=portador).count() == 0:
                            dados = {'cliente': cliente,
                                     'cobranca': cobranca,
                                     'portador': portador,
                                     'codigo_barras':codigo_barras, 
                                     'linha_digitavel':linha_digitavel,
                                     'formapagamento': formapagamento,
                                     'centrodecusto': planocontas,
                                     'modogeracao': 'l',
                                     'usuario_g': usuario,
                                     'usuario_b': usuario_b,
                                     'usuario_c': usuario_c,
                                     'demonstrativo': demonstrativo,
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
                                     'desconto': desconto,
                                     'status': status,
                                     'observacao': codigo_carne,
                                     'djson': {'juros': juros }
                                     }
                            if not args.sync_db:
                                print(dados)
                            else:
                                if fmodels.TituloGateway.objects.filter(idtransacao=idtransacao).count() > 0:
                                    continue
                                print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                                try:
                                    titulo = fmodels.Titulo(**dados)
                                    titulo.save()
                                    titulo.data_documento=data_documento
                                    titulo.data_alteracao=data_documento
                                    titulo.save()

                                    novo_titulogateway = fmodels.TituloGateway()
                                    novo_titulogateway.titulo = titulo
                                    novo_titulogateway.gateway = titulo.portador.gateway_boleto
                                    novo_titulogateway.idtransacao = idtransacao
                                    novo_titulogateway.link = link
                                    novo_titulogateway.save()

                                except Exception as e:
                                    print "Erro cadastrar",e,dados
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)
            else:
                print("Cliente não encontrado")
                break
