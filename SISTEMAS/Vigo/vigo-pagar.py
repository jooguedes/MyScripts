#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
import csv
from datetime import date, datetime
import copy
from unicodedata import normalize
from decimal import Decimal


parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--fornecedores', dest='fornecedores', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pcontas', dest='pcontas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--documentos', dest='documentos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--receber', dest='receber', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--caixalanc', dest='caixalanc', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--caixas', dest='caixas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--fluxo', dest='fluxo', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--notafiscal', dest='notafiscal', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--portador', dest='portador', type=int, help='Arquivo importacao',required=False)

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
from apps.fiscal import models as fismodels, constants as fisconstants

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')

if args.caixas:
    with open(args.caixas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            dados['id'] = row[0]
            dados['descricao'] = ustr(row[1])
            novo_caixa = fmodels.PontoRecebimento(**dados)
            novo_caixa.save()

if args.fornecedores:
    with open(args.fornecedores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            dados['id'] = int(row[0])
            dados['nome'] = row[1]
            dados['nomefantasia'] = row[2]
            dados['nomecontato'] = row[3]
            dados['telefones'] = row[4]
            dados['fax'] = row[5]
            dados['responsavelempresa'] = row[6]

            if row[7] == 'J':
                dados['insc_estadual'] = row[8]
            else:
                dados['rg'] = row[8]
            dados['cpfcnpj'] = row[9]

            dados['logradouro'] = row[10]
            dados['bairro'] = row[11]
            dados['cep'] = row[12]
            dados['cidade'] = row[13]
            dados['uf'] = row[14]
            dados['pontoreferencia'] = row[15]

            dados['email'] = row[16]
            dados['observacao'] = row[19]
            dados['ativo'] = True

            novo_fornecedor = fmodels.Fornecedor(**dados)
            novo_fornecedor.save()

if args.pcontas:
    with open(args.pcontas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            dados['codigo'] = row[3]
            dados['descricao'] = ustr(row[4])
            dados['tipo'] = row[5]
            dados['visivel'] = True
            dados['dre'] = False
            dados['padrao'] = False 

            novo_pcontas = fmodels.CentrodeCusto(**dados)
            novo_pcontas.save()


if args.documentos:
    with open(args.documentos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                dados = {} 
                dados['id'] = row[0]
                # row[1] - caixa
                # row[2] - empresa
                try:
                     dados['fornecedor'] = fmodels.Fornecedor.objects.get(pk=int(row[3]))
                except:
                     dados['fornecedor'] = None 
                try:
                    dados['tipodocumento'] = fmodels.TipoDocumento.objects.get(codigo=row[5])
                except:
                    dados['tipodocumento'] = None
                try:
                    dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo=row[7])
                except:
                    continue
                try:
                    dados['descricao'] = row[9][:100]
                except:
                    print "ERROR UTF8 enconding", row[9]
                dados['usuario'] = usuario
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.all()[0]
                dados['data_emissao'] = row[10]
                dados['data_cadastro'] = row[10]
                dados['data_alteracao'] = row[10]
                dados['data_vencimento'] = row[11]
                dados['valor'] = row[12]

                print(dados)

                pagar = fmodels.Pagar(**dados)
                pagar.save()
                pagar.data_cadastro=pagar.data_emissao
                pagar.save()

                #print pagar

                dadosparcela = {} 
                dadosparcela['pagar'] = pagar
                dadosparcela['valor'] = row[12]
                dadosparcela['parcela'] = 1
                dadosparcela['status'] = fmodels.PAGAR_STATUS_PENDENTE
                if row[13] == '1':
                    dadosparcela['status']= fmodels.PAGAR_STATUS_QUITADO
                    dadosparcela['data_pagamento'] = row[14]
                    dadosparcela['valor_pago'] = row[15]
                    dadosparcela['observacao'] = 'pago por: %s' %row[16]
                dadosparcela['data_vencimento'] = dados['data_vencimento']
                dadosparcela['data_cadastro'] = dados['data_cadastro']
                dadosparcela['juros'] = 0
                dadosparcela['multa'] = 0
                dadosparcela['desconto'] = 0
                dadosparcela['usuario'] = dados['usuario']

                #print(dadosparcela)

                pagaritem = fmodels.PagarItem(**dadosparcela)
                pagaritem.save()
                #print pagaritem

                if args.caixalanc:

                    if row[13] == '1':
                        try:
                            # lancamento do caixa
                            caixalanc = fmodels.CaixaLancamento()
                            caixalanc.ponto_recebimento = fmodels.PontoRecebimento.objects.get(id=row[1])
                            caixalanc.forma_pagamento = fmodels.FormaPagamento.objects.all()[0]
                            caixalanc.centrodecusto = pagar.centrodecusto
                            caixalanc.usuario = usuario
                            caixalanc.tipo_operacao = fmodels.CAIXA_OPERACAO_SAIDA
                            caixalanc.observacao = None
                            caixalanc.valor = abs(Decimal(pagaritem.valor_pago))
                            caixalanc.data_cadastro=pagaritem.data_pagamento
                            caixalanc.data_alteracao=pagaritem.data_pagamento
                            caixalanc.data_competencia = pagaritem.data_pagamento
                            caixalanc.save()
                            caixalanc.data_cadastro=pagaritem.data_pagamento
                            caixalanc.data_alteracao=pagaritem.data_pagamento
                            caixalanc.save()

                            caixalancpagaritem = fmodels.CaixaLancamentoPagarItem()
                            caixalancpagaritem.pagar_item = pagaritem
                            caixalancpagaritem.caixa_lancamento = caixalanc
                            caixalancpagaritem.save()
                            print 'Lancamento Caixa', pagaritem
                        except Exception as e:
                            print e
                else:
                    print 'Lancamento Caixa', pagaritem

            except:
                print '------------------- ERROR ------------------------'
                print row
                print '--------------------------------------------------'    


if args.receber:
    with open(args.receber, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                dados = {} 
                dados['id'] = row[0]
                # row[1] - caixa
                # row[2] - empresa
                try:
                     dados['fornecedor'] = fmodels.Fornecedor.objects.get(pk=int(row[3]))
                except:
                     dados['fornecedor'] = None 
                try:
                    dados['tipodocumento'] = fmodels.TipoDocumento.objects.get(codigo=row[5])
                except:
                    dados['tipodocumento'] = None
                try:
                    dados['planocontas'] = fmodels.CentrodeCusto.objects.get(codigo=row[7])
                except:
                    continue
                try:
                    dados['descricao'] = row[9][:100]
                except:
                    print "ERROR UTF8 enconding", row[9]
                dados['usuario'] = usuario
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.all()[0]
                dados['data_emissao'] = row[10]
                dados['data_cadastro'] = row[10]
                dados['data_alteracao'] = row[10]
                dados['data_vencimento'] = row[11]
                dados['valor'] = row[12]

                print(dados)

                receber = fmodels.Receber(**dados)
                receber.save()
                receber.data_cadastro=receber.data_emissao
                receber.save()
                #print receber

                dadosparcela = {} 
                dadosparcela['receber'] = receber
                dadosparcela['valor'] = row[12]
                dadosparcela['parcela'] = 1
                dadosparcela['status'] = fmodels.PAGAR_STATUS_PENDENTE
                if row[13] == '1':
                    dadosparcela['status']= fmodels.PAGAR_STATUS_QUITADO
                    dadosparcela['data_pagamento'] = row[14]
                    dadosparcela['valor_pago'] = row[15]
                    dadosparcela['observacao'] = 'pago por: %s' %row[16]
                dadosparcela['data_vencimento'] = dados['data_vencimento']
                dadosparcela['data_cadastro'] = dados['data_cadastro']
                dadosparcela['juros'] = 0
                dadosparcela['desconto'] = 0
                dadosparcela['usuario'] = dados['usuario']

                #print(dadosparcela)

                receberitem = fmodels.ReceberItem(**dadosparcela)
                receberitem.save()
                receberitem.data_cadastro=receber.data_cadastro
                receberitem.save()
                #print pagaritem

                if args.caixalanc:

                    if row[13] == '1':
                        try:
                            # lancamento do caixa
                            caixalanc = fmodels.CaixaLancamento()
                            caixalanc.ponto_recebimento = fmodels.PontoRecebimento.objects.get(id=row[1])
                            caixalanc.forma_pagamento = fmodels.FormaPagamento.objects.all()[0]
                            caixalanc.centrodecusto = receber.planocontas
                            caixalanc.usuario = usuario
                            caixalanc.tipo_operacao = fmodels.CAIXA_OPERACAO_ENTRADA
                            caixalanc.observacao = None
                            caixalanc.valor = abs(Decimal(receberitem.valor_pago))
                            caixalanc.data_cadastro=receberitem.data_pagamento
                            caixalanc.data_alteracao=receberitem.data_pagamento
                            caixalanc.data_competencia = receberitem.data_pagamento
                            caixalanc.save()
                            caixalanc.data_cadastro=receberitem.data_pagamento
                            caixalanc.data_alteracao=receberitem.data_pagamento
                            caixalanc.save()

                            caixalancreceberitem = fmodels.CaixaLancamentoReceberItem()
                            caixalancreceberitem.receber_item = receberitem
                            caixalancreceberitem.caixa_lancamento = caixalanc
                            caixalancreceberitem.save()

                            print 'Lancamento Caixa', receberitem
                        except Exception as e:
                            print e
                else:
                    print 'Lancamento Caixa', receberitem

            except Exception as ee:
                print '------------------- ERROR ------------------------'
                print ee,row
                print '--------------------------------------------------' 


if args.notafiscal:
    with open(args.notafiscal, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idbanco = row[1]

            if row[1] == '1':
                idbanco =  1
            elif row[1] == '2':
                idbanco = 2
            elif row[1] == '5':
                idbanco = 3
            elif row[1] == '7':
                idbanco = 4
            elif row[1] == '8':
                idbanco = 5
            elif row[1] == '9':
                idbanco = 6
            
            if args.portador:
                idbanco = args.portador

            titulos = fmodels.Titulo.objects.filter(nosso_numero_f__numfilter=row[0],portador__id=idbanco)
            if titulos:
                titulo = titulos[0]
                cliente = titulo.cliente

                v_nota = fismodels.NotaFiscal.objects.filter(numero=row[18],data_emissao='%s-%s-%s 00:00:00' %(row[15][0:4],row[15][4:6],row[15][6:8]))
                if len(v_nota) == 0:
        
                    nfdest = {}
                    nfdest['cliente'] = cliente
                    nfdest['cpfcnpj'] = row[2]
                    nfdest['inscricaoestadual'] = row[3]
                    nfdest['razaosocial'] = row[4]
                    nfdest['logradouro'] = row[5]
                    nfdest['numero'] = row[6]
                    nfdest['complemento'] = row[7]
                    nfdest['cep'] = row[8]
                    nfdest['bairro'] = row[9]
                    nfdest['cidade'] = row[10]
                    nfdest['uf'] = row[11]
                    nfdest['telefone'] = row[12]
                    nfdest['codigocliente'] = row[13]
                    nfdest['tipoassinante'] = row[14]

                    print nfdest
                    nfdest_obj = fismodels.NFDestinatario(**nfdest)
                    nfdest_obj.save()

                    nf = {}
                    nf['destinatario'] = nfdest_obj
                    nf['data_emissao'] = '%s-%s-%s 00:00:00' %(row[15][0:4],row[15][4:6],row[15][6:8])
                    nf['data_saida'] = '%s-%s-%s 00:00:00' %(row[15][0:4],row[15][4:6],row[15][6:8])
                    nf['modelo'] = row[16]
                    nf['tipoutilizacao'] = '4'
                    nf['serie'] = row[17]
                    nf['numero']= row[18]
                    nf['valortotal'] = Decimal('%s.%s' %(row[19][:-2],row[19][-2:]))
                    nf['icms'] = Decimal('%s.%s' %(row[20][:-2],row[20][-2:]))
                    nf['outrosvalores'] = Decimal('%s.%s' %(row[21][:-2],row[21][-2:]))
                    if row[23] == 'N':
                        nf['status'] = fisconstants.NOTAFISCAL_GERADA
                    else:
                        nf['status'] = fisconstants.NOTAFISCAL_CANCELADA
                        nf['data_cancela'] = '%s-%s-%s' %(row[15][0:4],row[15][4:6],row[15][6:8])
                    nf['bcicms'] = Decimal('%s.%s' %(row[24][:-2],row[24][-2:]))

                    nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                    nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                    try:
                        nf['cfop'] = fismodels.CFOP.objects.get(cfop=row[27])
                    except Exception as e:
                        print e
                        nf['cfop'] = fismodels.CFOP.objects.get(cfop='5307')

                    nf['usuario_g'] = titulo.usuario_g
                    nf['usuario_c'] = titulo.usuario_c

                    print nf

                    new_nf = fismodels.NotaFiscal(**nf)
                    new_nf.save()
                    new_nf.data_emissao=nf['data_emissao']
                    new_nf.data_saida=nf['data_saida']
                    new_nf.save()

                    # Cria nota fiscal com titulo
                    nft = fismodels.NotaFiscalTitulo()
                    nft.titulo = titulo
                    nft.notafiscal = new_nf
                    nft.save()

                else:
                    new_nf = v_nota[0]

                if new_nf.notafiscalitem_set.filter(item=int(row[42])).count() == 0:
                    nfitem = {}
                    nfitem['notafiscal'] = new_nf
                    nfitem['descricao'] = row[28]
                    nfitem['codigoservico'] = row[29]
                    nfitem['classificacao'] = row[30]
                    nfitem['unidade'] = row[31]
                    nfitem['qt_contratada'] = row[32]
                    nfitem['qt_fornecida'] = row[33]
                    nfitem['valortotal'] = Decimal('%s.%s' %(row[34][:-2],row[34][-2:]))
                    nfitem['desconto'] = Decimal('%s.%s' %(row[35][:-2],row[35][-2:]))
                    nfitem['acrescimo_despesa'] = Decimal('%s.%s' %(row[36][:-2],row[36][-2:]))
                    nfitem['bcicms'] = Decimal('%s.%s' %(row[37][:-2],row[37][-2:]))
                    nfitem['icms'] = Decimal('%s.%s' %(row[38][:-2],row[38][-2:]))
                    nfitem['outrosvalores'] = Decimal('%s.%s' %(row[39][:-2],row[39][-2:]))
                    nfitem['aliquotaicms'] = Decimal('%s.%s' %(row[41][:-2],row[41][-2:]))
                    nfitem['item'] = int(row[42])
                    nfitem['data_cadastro'] = new_nf.data_emissao
                    nfitem['data_alteracao'] = new_nf.data_emissao

                    print nfitem

                    new_nfitem = fismodels.NotaFiscalItem(**nfitem)
                    new_nfitem.save()
                    new_nfitem.data_cadastro=new_nf.data_emissao
                    new_nfitem.data_alteracao=new_nf.data_emissao
                    new_nfitem.save()



if args.fluxo:
    with open(args.fluxo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            try:
                dados['ponto_recebimento'] = fmodels.PontoRecebimento.objects.get(id=row[0])
            except:
                continue
            if u'Transferência entre caixas ORIGEM:' in row[4]:
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.all()[1]
            else:
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.all()[0]
            dados['data_cadastro'] = row[1]
            dados['data_alteracao'] = row[1]
            dados['data_competencia'] = row[1]
            dados['usuario'] = usuario
            if 'Tarifas bancárias do retorno processado referente ao arquivo' in row[4]:
                dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo=settings.CC_TARIFABANCARIA)

            if row[2] != '0':
                # debito
                dados['valor'] = abs(Decimal(row[2]))
                dados['tipo_operacao'] = fmodels.CAIXA_OPERACAO_SAIDA
            else:
                if row[4].startswith('Boleto'):
                    dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo='2.21.2102')   
                # credito
                dados['valor'] = abs(Decimal(row[3]))
                dados['tipo_operacao'] = fmodels.CAIXA_OPERACAO_ENTRADA

            dados['observacao'] = row[4]
            print dados

            if args.caixalanc:
                caixalanc = fmodels.CaixaLancamento(**dados)
                caixalanc.save()
                caixalanc.data_cadastro=caixalanc.data_competencia
                caixalanc.data_alteracao=caixalanc.data_cadastro
                caixalanc.save()


