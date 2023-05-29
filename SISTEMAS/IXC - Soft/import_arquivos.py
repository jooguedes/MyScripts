if args.arquivos:
    with open(args.arquivos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            if cliente:
                if admmodels.ClienteDocumento.objects.filter(cliente=cliente, descricao=row[1][0:200]).count() == 0:
                    try:
                        path = str('/usr/local/sgp/media/sgp/%s_arquivos/'%(cliente.id))
                        cliente = cliente[0]
                        print(cliente,row[2])
                        new_doc = admmodels.ClienteDocumento()
                        new_doc.cliente=cliente
                        new_doc.descricao=row[1][0:200]
                        new_doc.arquivo='/importacao/'+row[2]
                        new_doc.usuario = usuario 
                        new_doc.data_cadastro=row[3]
                        new_doc.save()
                        # Para importar os arquivos descomente o trecho abaixo e mova os arquivos dos cliente para uma pasta no tmp com o nome Arquivos_Clientes
                        
                        try:
                            path = str('/usr/local/sgp/media/sgp/%s_arquivos/'%(cliente.id))
                            if not os.path.isdir(path):
                                os.makedirs(path)
                            shutil.copy('/tmp/Arquivos_Clientes/%s'%row[2].split('/')[-1], '/usr/%s/sgp/media/sgp/%s_arquivos/'%(str(args.settings).split('.')[1], cliente.id))
                        except OSError as error:
                            print(error)
                        
                    except:
                        pass


if args.chamadosarquivos:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.chamadosarquivos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ocorrencia = amodels.Ocorrencia.objects.filter(id=int(row[1])).first()
            if ocorrencia:
                print(row)
                ocorrenciaanexo = amodels.OcorrenciaAnexo()
                ocorrenciaanexo.ocorrencia = ocorrencia
                ocorrenciaanexo.id = row[0]
                ocorrenciaanexo.descricao = row[2]
                ocorrenciaanexo.arquivo = '/importacao/'+row[3]
                ocorrenciaanexo.usuario = usuario
                ocorrenciaanexo.data_cadastro = row[4]
                ocorrenciaanexo.save()
                
                try:
                    path = str('/usr/local/sgp/media/sgp/arquivos/ocorrencias')
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    try:
                        shutil.copy('/tmp/Arquivos_Ocorrencias/612fea4f9c6e1.png', '/usr/%s/sgp/media/sgp/arquivos'%(str(args.settings).split('.')[1]))
                    except:
                        continue
                except OSError as error:
                    print(error)       