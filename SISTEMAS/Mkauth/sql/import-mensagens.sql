select chamado,atendente, msg_data, msg from sis_msg INTO OUTFILE '/tmp/mkauth-msg-ocorrencia.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
