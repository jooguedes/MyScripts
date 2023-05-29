import csv
from apps.admcore import  models as admmodels
from apps.atendimento import models as amodels
from datetime import date,datetime
from apps.cauth import models as authmodels

clientes={}
clientes_plano={}
ocorrencias={}
ordens_servico={}
usuario = authmodels.User.objects.get(username='sgp')




def convertdata(d):
    if "-" in d:
        return d
    else:
        try:
            d_,m_,y_ = d.strip().split('/')
            date(int(y_),int(m_),int(d_))
            return '%s-%s-%s' %(y_,m_,d_)
        except:
            return None

with open('/tmp/Conv-Ordem_Servico_Ocorrencia.csv', 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice=0
            for row in conteudo:
                ocorrencia={
                    'id_ordem_servico':row[1],
                    'data_ocorrencia': row[2],
                    'descricao': row[3],
                }
                ocorrencias[indice]=ocorrencia
                indice= indice+1



with open('/tmp/Conv-Cadastro_clientes.csv', 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
        indice=0
        for row in conteudo:
            cliente={
                'id': row[0],
                'tipo_pesssoa': row[1],
                'status': row[9],
                'nome': row[2],
                'cpfcnpj': row[3],
            }

            clientes[indice]=cliente
            indice=indice+1
  


with open('/tmp/Conv-Cliente_plano.csv', 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
       
        indice=0
        for row in conteudo:
            cliente_plano={
                'id':row[0],
                'id_cliente': row[1],
                'nome_plano':  row[2],
            }

            clientes_plano[indice]=cliente_plano
            indice=indice+1
    

######################### IMPORT ORDEM DE SERVIÇO #########################

cdtipo = 300
cdmotivo = 300
ocorrencia=[]
max_tipo = amodels.Tipo.objects.all().order_by('-id')[0]
if max_tipo.codigo > 200:
    cdtipo = max_tipo.codigo + 1
max_motivo = amodels.MotivoOS.objects.all().order_by('-id')[0]
if max_motivo.codigo > 200:
    cdmotivo = max_motivo.codigo + 1

metodo = amodels.Metodo.objects.all()[0]

with open('/tmp/Conv-Ordem_Servico.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo: 
        for cliente in clientes:
            for cliente_plano in clientes_plano:
                if row[2]== clientes_plano[cliente_plano]['id']:
                    if clientes_plano[cliente_plano]['id_cliente']==clientes[cliente]['id']:
                        ocorrencia={
                            'protocolo':row[1],
                            'data_abertura':row[3],
                            'data_finalizacao':row[4],
                            'descricao': row[5],
                            'login': usuario,
                            'id_cliente':clientes[cliente]['id']
                                        
                                }
        

                        for oc in ocorrencias:
                            if ocorrencias[oc]['id_ordem_servico']==row[0]:
                                msg=ocorrencia['descricao']
                                ocorrencia['descricao']=ocorrencias[oc]['descricao']
                            else:
                                continue
                
        

        print('Mensagem', msg, 'Descricao: ', ocorrencia['descricao'])
        msg2=ocorrencia['descricao']
        protocolo = ocorrencia['protocolo']
        if len(protocolo) > 14:
            protocolo = protocolo[0:13]


        print("importando ocorrência: ", protocolo, " Login: ", ocorrencia['login'])
        login = str(ocorrencia['login']).strip().lower()
        assunto = 'RADIUS_NET_OCORRENCIA'
        status ='aberto'
        data_cadastro = convertdata(ocorrencia['data_abertura'])
        data_finalizacao = convertdata(ocorrencia['data_finalizacao'])
        if data_finalizacao!='':
            status='fechado'
        
        
        conteudo = msg
        if conteudo == "" or conteudo is None:
            conteudo = "Campo conteúdo vazio no RADIUS NET."

        servico = admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__id=ocorrencia['id_cliente'])

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

            print('Esse é meu protocolo: ', protocolo)
            if amodels.Ocorrencia.objects.filter(numero=str(protocolo)).count() == 0:
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
                
                ocorrencia['data_finalizacao'] = data_finalizacao
                ocorrencia['conteudo'] = conteudo
                #ocorrencia['observacoes'] = servicoprestado
                for ok in ocorrencia:
                    if ocorrencia[ok] in ['0000-00-00 00:00:00','0000-00-00','']:
                        ocorrencia[ok] = None

                new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                new_ocorrencia.save()

                new_ocorrencia.data_cadastro = data_cadastro
                new_ocorrencia.data_finalizacao = data_finalizacao

                
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
                ordem['data_agendamento'] = None
                ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                ordem['conteudo'] = ocorrencia['conteudo']

                for oser in ordem:
                    if ordem[oser] in ['0000-00-00 00:00:00','0000-00-00']:
                        ordem[oser] = None

                new_ordem = amodels.OS(**ordem)
                new_ordem.save()
                new_ordem.data_cadastro = ocorrencia['data_cadastro']
                new_ordem.data_agendamento = None
                new_ordem.data_finalizacao = ocorrencia['data_finalizacao']
                #if str(new_ordem.data_agendamento) in ['0000-00-00 00:00:00','0000-00-00','']:
                    #  new_ordem.data_agendamento = None
                #if str(new_ordem.data_finalizacao) in ['0000-00-00 00:00:00','0000-00-00','']:
                    # new_ordem.data_agendamento = None
                new_ordem.save()


                #CADATRO DA MENSAGEM DA OCORRENCIA
                ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                new_ocorrencia_anotacao.ocorrencia= ocorrencia
                new_ocorrencia_anotacao.anotacao=msg2
                new_ocorrencia_anotacao.usuario= usuario
                new_ocorrencia_anotacao.save()
            else: 
                print('Protocolo já existe')
        else:
            print('servico não identificado')
    