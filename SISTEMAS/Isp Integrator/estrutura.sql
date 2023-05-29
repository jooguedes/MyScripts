
-- Table structure for table `tipo_menu_telas`
--

DROP TABLE IF EXISTS `tipo_menu_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_menu_telas` (
  `codtmt` varchar(10) NOT NULL,
  `codist` varchar(10) NOT NULL,
  `classe` varchar(30) NOT NULL,
  `descri_tmt` varchar(30) NOT NULL,
  PRIMARY KEY (`codtmt`),
  KEY `codist` (`codist`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_menu_telas`
-- Table structure for table `servicos_desc`
--

DROP TABLE IF EXISTS `servicos_desc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_desc` (
  `codsdesc` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `nro_parcela` int(2) NOT NULL DEFAULT '0',
  `desconto` float(8,5) NOT NULL DEFAULT '0.00000',
  `promocional` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codsdesc`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_desc`
-- Table structure for table `interfaces_radios`
--

DROP TABLE IF EXISTS `interfaces_radios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaces_radios` (
  `codintr` varchar(10) NOT NULL DEFAULT '',
  `codrad` varchar(10) NOT NULL DEFAULT '',
  `codtintr` varchar(10) NOT NULL DEFAULT '',
  `service_name` varchar(50) NOT NULL DEFAULT '',
  `interface` varchar(50) NOT NULL,
  `nro` int(3) unsigned NOT NULL,
  `alias` varchar(20) NOT NULL DEFAULT '',
  `dns_name` varchar(50) NOT NULL DEFAULT '',
  `ip` varchar(20) NOT NULL DEFAULT '',
  `clase` char(3) NOT NULL DEFAULT '24',
  `gateway` varchar(15) NOT NULL DEFAULT '',
  `network` varchar(15) NOT NULL DEFAULT '',
  `broadcast` varchar(15) NOT NULL DEFAULT '',
  `mac` varchar(17) NOT NULL DEFAULT '',
  `ativa` char(1) NOT NULL DEFAULT 'S',
  `reservada` char(1) NOT NULL DEFAULT 'N',
  `codigo_externo` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codintr`),
  KEY `codrad` (`codrad`),
  KEY `codtintr` (`codtintr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interfaces_radios`
-- Table structure for table `status_fat`
--

DROP TABLE IF EXISTS `status_fat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_fat` (
  `codsta_f` char(1) NOT NULL DEFAULT '',
  `descri_sta_f` varchar(30) NOT NULL DEFAULT '',
  `ordem` int(2) NOT NULL,
  PRIMARY KEY (`codsta_f`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_fat`
-- Table structure for table `emissao_recibos`
--

DROP TABLE IF EXISTS `emissao_recibos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emissao_recibos` (
  `coderec` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL DEFAULT '',
  `data_hora` datetime NOT NULL,
  `compe` varchar(4) NOT NULL DEFAULT '',
  `ultimo_rec` int(8) unsigned NOT NULL,
  `codigos` mediumtext NOT NULL,
  PRIMARY KEY (`coderec`),
  KEY `codemp` (`codemp`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emissao_recibos`
-- Table structure for table `webhook`
--

DROP TABLE IF EXISTS `webhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webhook` (
  `codwbhook` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela',
  `api_integrator` varchar(80) NOT NULL DEFAULT '' COMMENT 'nome da api interna(integrator)',
  PRIMARY KEY (`codwbhook`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webhook`
-- Table structure for table `tipo_webhook`
--

DROP TABLE IF EXISTS `tipo_webhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_webhook` (
  `codtwbhook` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela',
  `url_api` mediumtext NOT NULL,
  `request_api` mediumtext NOT NULL,
  `tecnologia` varchar(20) NOT NULL DEFAULT '' COMMENT 'tipo de tecnologia usada api,cURL',
  PRIMARY KEY (`codtwbhook`),
  KEY `tecnologia` (`tecnologia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_webhook`
-- Table structure for table `webhook_log`
--

DROP TABLE IF EXISTS `webhook_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webhook_log` (
  `codwbhlog` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela',
  `codwbhapi` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela webhook_api',
  `codtwbhook` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela tipo_webhook',
  `codwbhook` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela webhook',
  `data_exec` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'data execucao',
  `funcao` varchar(30) NOT NULL DEFAULT '' COMMENT 'nome da funcao chamada',
  `atividade` varchar(300) NOT NULL DEFAULT '' COMMENT 'mensagem',
  `message_erro` text COMMENT 'mensagem de erro',
  `ordem_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'campo para ordenacao dos registros',
  PRIMARY KEY (`codwbhlog`),
  KEY `ids` (`codwbhapi`,`codtwbhook`,`codwbhook`),
  KEY `data_exec` (`data_exec`),
  KEY `ordem_id` (`ordem_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webhook_log`
-- Table structure for table `webhook_api`
--

DROP TABLE IF EXISTS `webhook_api`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webhook_api` (
  `codwbhapi` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela',
  `codtwbhook` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela tipo_webhook',
  `codwbhook` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela webhook',
  `codservp` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela servidores_pop',
  `api` varchar(80) NOT NULL DEFAULT '' COMMENT 'nome da api externa',
  `method` varchar(20) NOT NULL DEFAULT 'executar' COMMENT 'nome do metodo para a api',
  `inicial` char(1) DEFAULT 'N' COMMENT 'S - executa no inicio, antes da api do integrator || N - executa no final, depois da api do integrator',
  `ordem` int(3) DEFAULT '0' COMMENT 'ordem para listagem e execucao',
  `ativo` char(1) DEFAULT 'S' COMMENT 'S - Ativo || N - Inativo',
  `valRet` varchar(250) NOT NULL DEFAULT 'ok' COMMENT 'Valor que sera lido para validar se a resposta deu erro ou veio corretamente',
  `valRetTrue` varchar(250) NOT NULL DEFAULT 'True' COMMENT 'Valor para comparar com o valRet para validar a resposta',
  `abortErro` char(1) NOT NULL DEFAULT 'S' COMMENT 'Valida se o processo sera abortado caso tenha erro.',
  `RetTrue` varchar(250) DEFAULT 'list' COMMENT 'Tag a ser lida quando a api foi executada corretamente',
  `RetFalse` varchar(250) DEFAULT 'errmsg' COMMENT 'Tag a ser lida quando a api executada acusa erro',
  `data_cad` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'data de cadastro/atualizacao',
  `obs` text NOT NULL COMMENT 'observacao para programacao',
  PRIMARY KEY (`codwbhapi`),
  KEY `codwbhook` (`codwbhook`),
  KEY `codservp` (`codservp`),
  KEY `ordem` (`ordem`),
  KEY `ativo` (`ativo`),
  KEY `codtwbhook` (`codtwbhook`),
  KEY `inicial` (`inicial`),
  KEY `cnt` (`codwbhook`,`inicial`,`ativo`),
  CONSTRAINT `codtwbhook` FOREIGN KEY (`codtwbhook`) REFERENCES `tipo_webhook` (`codtwbhook`),
  CONSTRAINT `codwbhook` FOREIGN KEY (`codwbhook`) REFERENCES `webhook` (`codwbhook`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webhook_api`
-- Table structure for table `param_webhook`
--

DROP TABLE IF EXISTS `param_webhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `param_webhook` (
  `codwbhprm` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela',
  `codwbhapi` varchar(10) NOT NULL DEFAULT '' COMMENT 'id da tabela webhook_api',
  `param` varchar(80) NOT NULL DEFAULT '' COMMENT 'nome do parametro',
  `valor` varchar(80) DEFAULT NULL COMMENT 'valor do parametro',
  `ordem` int(3) DEFAULT '0' COMMENT 'ordem para listagem e execucao',
  `ativo` char(1) DEFAULT 'S' COMMENT 'S - Ativo || N - Inativo',
  `data_cad` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'data de cadastro/atualizacao',
  `obs` text NOT NULL COMMENT 'observacao para programacao',
  PRIMARY KEY (`codwbhprm`),
  KEY `codwbhapi` (`codwbhapi`),
  KEY `param` (`param`),
  KEY `ordem` (`ordem`),
  KEY `ativo` (`ativo`),
  CONSTRAINT `codwbhapi` FOREIGN KEY (`codwbhapi`) REFERENCES `webhook_api` (`codwbhapi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `param_webhook`
-- Table structure for table `classificacao_item_fiscal`
--

DROP TABLE IF EXISTS `classificacao_item_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classificacao_item_fiscal` (
  `codcif` char(4) NOT NULL,
  `grupo` char(100) NOT NULL DEFAULT '',
  `descri_cla` mediumtext,
  PRIMARY KEY (`codcif`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classificacao_item_fiscal`
-- Table structure for table `lacto_pad_banc`
--

DROP TABLE IF EXISTS `lacto_pad_banc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lacto_pad_banc` (
  `codpadban` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Codigo Padrao Bancario',
  `nro_ban` char(3) NOT NULL COMMENT 'Codigo Oficial Bancario',
  `codbanpad` char(5) DEFAULT NULL COMMENT 'Codigo padrao da transacao bancaria',
  `codtmov` varchar(10) DEFAULT NULL COMMENT 'Codigo do Tipo de Movimentacao bancaria',
  `describanpad` varchar(70) DEFAULT NULL COMMENT 'Descricao padrao do lancamento',
  `histo_mov` varchar(100) NOT NULL COMMENT 'Descricao do Lancamento a ser realizado',
  PRIMARY KEY (`codpadban`),
  KEY `nro_ban` (`nro_ban`),
  KEY `codbanpad` (`codbanpad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lacto_pad_banc`
-- Table structure for table `tipo_reducao_icms`
--

DROP TABLE IF EXISTS `tipo_reducao_icms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_reducao_icms` (
  `codtred` char(2) NOT NULL,
  `descricao` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`codtred`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_reducao_icms`
-- Table structure for table `saldos_nao_provisionados`
--

DROP TABLE IF EXISTS `saldos_nao_provisionados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `saldos_nao_provisionados` (
  `codsnp` varchar(10) NOT NULL,
  `codcli` int(6) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codest` varchar(10) NOT NULL,
  `codepsc` varchar(10) NOT NULL,
  `codextra` varchar(10) NOT NULL,
  `coddct` varchar(20) NOT NULL,
  `saldo` float(10,2) NOT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`codsnp`),
  KEY `codcli` (`codcli`),
  KEY `codsercli` (`codsercli`),
  KEY `codepsc` (`codepsc`),
  KEY `codextra` (`codextra`),
  KEY `coddct` (`coddct`),
  KEY `codest` (`codest`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saldos_nao_provisionados`
-- Table structure for table `historico_reajuste`
--

DROP TABLE IF EXISTS `historico_reajuste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_reajuste` (
  `codhreaj` varchar(10) NOT NULL DEFAULT '',
  `codreajst` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `update_exec` mediumtext NOT NULL,
  `update_rollback` mediumtext NOT NULL,
  `texto_mudanca` mediumtext NOT NULL,
  `texto_rollback` mediumtext NOT NULL,
  PRIMARY KEY (`codhreaj`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_reajuste`
-- Table structure for table `timer_atividade`
--

DROP TABLE IF EXISTS `timer_atividade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timer_atividade` (
  `codtativ` char(10) NOT NULL DEFAULT '',
  `codvint` varchar(40) NOT NULL DEFAULT '',
  `codigo_vint` char(10) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT '',
  `hora_ini` datetime NOT NULL,
  `hora_fim` datetime NOT NULL,
  `tempo` int(11) NOT NULL,
  `tempo_ex` varchar(100) NOT NULL DEFAULT '',
  `usuario_parou` char(1) NOT NULL DEFAULT 'S',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtativ`),
  KEY `codvint` (`codvint`),
  KEY `codigo_vint` (`codigo_vint`),
  KEY `hora_ini` (`hora_ini`),
  KEY `hora_fim` (`hora_fim`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timer_atividade`
-- Table structure for table `motivos_cancel`
--

DROP TABLE IF EXISTS `motivos_cancel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motivos_cancel` (
  `codcan` varchar(10) NOT NULL DEFAULT '',
  `descri_can` varchar(50) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `obs` text NOT NULL,
  PRIMARY KEY (`codcan`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivos_cancel`
-- Table structure for table `creditos`
--

DROP TABLE IF EXISTS `creditos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditos` (
  `codcre` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `code_f` varchar(10) NOT NULL,
  `codvcre` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `compe` varchar(4) NOT NULL,
  `data` date NOT NULL,
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `trafego_cre` int(6) unsigned NOT NULL,
  `codutfg` varchar(10) NOT NULL,
  `processado` char(1) NOT NULL DEFAULT 'N',
  `data_hora_pros` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`codcre`),
  KEY `codcrec` (`codcrec`),
  KEY `codvcre` (`codvcre`),
  KEY `codsercli` (`codsercli`),
  KEY `compe` (`compe`),
  KEY `code_f` (`code_f`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creditos`
-- Table structure for table `registros_novos_sincronismo`
--

DROP TABLE IF EXISTS `registros_novos_sincronismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registros_novos_sincronismo` (
  `codtab` char(10) NOT NULL DEFAULT '',
  `data_proc` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codigo` char(10) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `codtab` (`codtab`),
  KEY `data_proc` (`data_proc`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros_novos_sincronismo`
-- Table structure for table `estoque_kit_item`
--

DROP TABLE IF EXISTS `estoque_kit_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estoque_kit_item` (
  `codkit` varchar(10) NOT NULL,
  `kit` bigint(12) NOT NULL COMMENT 'Chave Routerbox',
  `estoque` varchar(10) NOT NULL COMMENT 'Chave da tb produto',
  `qtde` double(15,2) DEFAULT NULL COMMENT 'qtd do material',
  `consumo` char(1) DEFAULT 'N' COMMENT 'Material para consumo?',
  PRIMARY KEY (`codkit`,`estoque`),
  KEY `kit` (`kit`),
  KEY `patrimonio` (`estoque`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque_kit_item`
-- Table structure for table `enlaces`
--

DROP TABLE IF EXISTS `enlaces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enlaces` (
  `codenl` varchar(10) NOT NULL,
  `codtenl` varchar(10) NOT NULL,
  `codcon_o` int(4) unsigned DEFAULT NULL,
  `codcon_d` int(4) unsigned NOT NULL,
  `codintr_o` varchar(10) NOT NULL,
  `codintr_d` varchar(10) NOT NULL,
  PRIMARY KEY (`codenl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enlaces`
-- Table structure for table `habilitacao_provisoria`
--

DROP TABLE IF EXISTS `habilitacao_provisoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `habilitacao_provisoria` (
  `codhprov` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_fim` date NOT NULL,
  PRIMARY KEY (`codhprov`),
  KEY `codsercli` (`codsercli`),
  KEY `data_fim` (`data_fim`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habilitacao_provisoria`
-- Table structure for table `mov_cartoes`
--

DROP TABLE IF EXISTS `mov_cartoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mov_cartoes` (
  `codmcart` varchar(10) NOT NULL DEFAULT '',
  `codcart` varchar(10) NOT NULL DEFAULT '',
  `codpar` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `atual` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codmcart`),
  KEY `codpar` (`codpar`),
  KEY `codcart` (`codcart`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mov_cartoes`
-- Table structure for table `deslocamento_tec`
--

DROP TABLE IF EXISTS `deslocamento_tec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deslocamento_tec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codtec` char(10) NOT NULL DEFAULT '',
  `codords` char(10) NOT NULL DEFAULT '',
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `accuracy` decimal(10,8) DEFAULT NULL,
  `speed` decimal(10,8) DEFAULT NULL,
  `heading` decimal(10,8) DEFAULT NULL,
  `battery_level` int(11) DEFAULT NULL,
  `status` enum('I','F','L','A') NOT NULL,
  `created_at` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `codtec` (`codtec`),
  KEY `codords` (`codords`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deslocamento_tec`
-- Table structure for table `execucao_regras_cob`
--

DROP TABLE IF EXISTS `execucao_regras_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execucao_regras_cob` (
  `coderc` varchar(10) NOT NULL,
  `codacob` varchar(10) NOT NULL,
  `codrcob` varchar(10) NOT NULL,
  `data_leit` datetime NOT NULL,
  `data_exe` datetime NOT NULL,
  PRIMARY KEY (`coderc`),
  KEY `codacob` (`codacob`),
  KEY `codrcob` (`codrcob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `execucao_regras_cob`
-- Table structure for table `tipo_licencias_antivirus`
--

DROP TABLE IF EXISTS `tipo_licencias_antivirus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_licencias_antivirus` (
  `codtlav` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `descri_tlav` varchar(50) NOT NULL DEFAULT '',
  `distribuidor_id` int(8) NOT NULL,
  `produto_id` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtlav`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_licencias_antivirus`
-- Table structure for table `emails_responsaveis`
--

DROP TABLE IF EXISTS `emails_responsaveis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emails_responsaveis` (
  `tipo` varchar(10) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL DEFAULT '',
  `servidor` varchar(50) NOT NULL DEFAULT 'smtp.',
  `tipo_auth` varchar(5) NOT NULL DEFAULT 'PLAIN',
  `sem_dominio` char(1) NOT NULL DEFAULT 'N',
  `tls` char(1) NOT NULL DEFAULT 'S',
  `reply_to` varchar(50) NOT NULL DEFAULT '',
  `usuario` varchar(50) NOT NULL DEFAULT '',
  `senha` mediumtext NOT NULL,
  PRIMARY KEY (`tipo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_responsaveis`
-- Table structure for table `script_tipo_onu`
--

DROP TABLE IF EXISTS `script_tipo_onu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_tipo_onu` (
  `codsto` varchar(10) NOT NULL,
  `codseq` varchar(10) NOT NULL,
  `codtonu` varchar(10) NOT NULL,
  `codscp_onu` char(10) NOT NULL,
  `codprod` char(10) NOT NULL,
  PRIMARY KEY (`codsto`),
  KEY `codseq` (`codseq`),
  KEY `codtonu` (`codtonu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_tipo_onu`
-- Table structure for table `forma_cobrancas`
--

DROP TABLE IF EXISTS `forma_cobrancas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forma_cobrancas` (
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `descri_cob` varchar(50) NOT NULL DEFAULT '',
  `telefonica` char(1) NOT NULL DEFAULT '',
  `carne` char(1) NOT NULL DEFAULT 'N',
  `codban` varchar(10) NOT NULL DEFAULT '',
  `nro_arq` int(3) unsigned NOT NULL DEFAULT '0',
  `nosso_nro` int(9) unsigned NOT NULL DEFAULT '0',
  `tipo_cob` char(1) NOT NULL DEFAULT 'N',
  `codedeb` varchar(10) NOT NULL DEFAULT '',
  `codcob_o` varchar(10) NOT NULL DEFAULT '',
  `permite_protestar` char(1) NOT NULL DEFAULT 'N',
  `nf_fatura` char(3) DEFAULT NULL,
  `dias_baixa` int(3) unsigned NOT NULL,
  `registro_online` char(1) NOT NULL DEFAULT 'N',
  `pix` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codcob`),
  KEY `codafi` (`codafi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forma_cobrancas`
-- Table structure for table `registro_tributacao_det`
--

DROP TABLE IF EXISTS `registro_tributacao_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registro_tributacao_det` (
  `codrtrib` char(10) NOT NULL COMMENT 'Código do Regime de Tributação.',
  `codrtribdet` char(10) NOT NULL COMMENT 'Código do Detalhamento do Regime de Tributação.',
  `codbeneficio` char(10) NOT NULL DEFAULT '' COMMENT 'Código do Benefício concedido pelo Regime do ICMS.',
  `icms` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Alíquota do ICMS.',
  `origem` char(1) NOT NULL DEFAULT '' COMMENT 'Origem do Produto.',
  `icms_cst` char(3) NOT NULL DEFAULT '' COMMENT 'Código da Situação Tributária ICMS.',
  `pRedBC` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual de Redução da Base de Cálculo.',
  `modBC` char(1) NOT NULL DEFAULT '' COMMENT 'Modalidade da Determinação da Base de Cálculo.',
  `icmsst` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Alíquota ICMS Substituição Tributária.',
  `pRedBCST` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual de Redução da Base de Cálculo ICMS Substituição Tributaria.',
  `modBCST` char(1) NOT NULL DEFAULT '' COMMENT 'Modalidade da Determinação da Base de Cálculo do ICMS Substituição Tributária.',
  `pMVAST` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual da margem do valor adicionado ICMS Substituição Tributária.',
  `pdif` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual do Diferimento Parcial.',
  `ipi` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual de IPI.',
  `ipi_cst` char(2) NOT NULL DEFAULT '' COMMENT 'Código da Situação Tributária IPI.',
  `codcenq` char(3) NOT NULL DEFAULT '' COMMENT 'Código do Enquadramento.',
  `pis` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Aliquota do PIS.',
  `pis_cst` char(2) NOT NULL DEFAULT '' COMMENT 'Código Situação Tributária PIS.',
  `cofins` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Alíquota COFINS.',
  `cofins_cst` char(2) NOT NULL DEFAULT '' COMMENT 'Código Situação Tributária COFINS.',
  `adcIPI` char(1) NOT NULL DEFAULT 'N' COMMENT 'Adiciona IPI a Base de Cáluclo',
  `adcOutDesp` char(1) NOT NULL DEFAULT 'N' COMMENT 'Adiciona Outras Despesas.',
  `adcFrete` char(1) NOT NULL DEFAULT 'N' COMMENT 'Adiciona Frete.',
  `adcSeguro` char(1) DEFAULT 'N' COMMENT 'Adiciona Seguro.',
  PRIMARY KEY (`codrtribdet`),
  KEY `codrtrib` (`codrtrib`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_tributacao_det`
-- Table structure for table `tipo_conta_corrente`
--

DROP TABLE IF EXISTS `tipo_conta_corrente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_conta_corrente` (
  `codtcta` varchar(10) NOT NULL DEFAULT '',
  `descri_tcta` varchar(30) NOT NULL DEFAULT '',
  `codigo` varchar(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtcta`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_conta_corrente`
-- Table structure for table `prospect_web`
--

DROP TABLE IF EXISTS `prospect_web`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prospect_web` (
  `codprow` varchar(10) NOT NULL DEFAULT '0',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `nome_cli` varchar(50) NOT NULL DEFAULT '',
  `nome_fan` varchar(30) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `sala` varchar(10) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `CEP` varchar(9) NOT NULL DEFAULT '',
  `DDD` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `login` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `contato` varchar(50) NOT NULL DEFAULT '',
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `tipo_cliente` char(1) NOT NULL DEFAULT '',
  `endereco_cob` varchar(50) NOT NULL DEFAULT '',
  `bairro_cob` varchar(25) NOT NULL DEFAULT '',
  `cidade_cob` varchar(8) NOT NULL DEFAULT '',
  `CEP_cob` varchar(9) NOT NULL DEFAULT '',
  `CNPJ` varchar(18) NOT NULL DEFAULT '',
  `ICM` varchar(15) NOT NULL DEFAULT '',
  `RG` varchar(11) NOT NULL DEFAULT '',
  `CPF` varchar(14) NOT NULL DEFAULT '',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `obs` text NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codvenc` varchar(10) NOT NULL DEFAULT '',
  `n_fone` varchar(15) NOT NULL DEFAULT '',
  `n_cont` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(8) NOT NULL DEFAULT '0',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `dias_trail` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codprow`),
  KEY `nome_cli` (`nome_cli`),
  KEY `ativo` (`ativo`),
  KEY `codcon` (`codcon`),
  KEY `codafi` (`codafi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prospect_web`
-- Table structure for table `condominios`
--

DROP TABLE IF EXISTS `condominios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condominios` (
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codosr` varchar(10) NOT NULL DEFAULT '',
  `codrad` varchar(10) NOT NULL DEFAULT '',
  `codstc` varchar(10) NOT NULL DEFAULT '',
  `codtpr` varchar(10) NOT NULL DEFAULT '',
  `codpolt` varchar(10) NOT NULL,
  `codigo_externo` varchar(20) NOT NULL,
  `codtsici` varchar(10) NOT NULL,
  `codrds` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codima` varchar(15) NOT NULL,
  `nome_con` varchar(120) NOT NULL,
  `portaria` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(20) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  `posx` int(6) unsigned NOT NULL,
  `posy` int(6) unsigned NOT NULL,
  `contato` varchar(50) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `ddd` varchar(3) NOT NULL,
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `quant_salas` int(3) unsigned NOT NULL DEFAULT '0',
  `ip_inicio` varchar(15) NOT NULL DEFAULT '',
  `ip_fin` varchar(15) NOT NULL,
  `ipv6_ini` varchar(39) NOT NULL,
  `ipv6_fin` varchar(39) NOT NULL,
  `ipv6_fim` varchar(39) NOT NULL,
  `ipv6_sec_ini` varchar(39) NOT NULL,
  `ipv6_sec_fim` varchar(39) NOT NULL,
  `reajuste` float(8,2) NOT NULL DEFAULT '0.00',
  `formato_ips` varchar(15) NOT NULL DEFAULT '',
  `con_enlace` int(3) unsigned NOT NULL DEFAULT '0',
  `taxa_instalacao` float(10,2) NOT NULL DEFAULT '0.00',
  `quant_parcelas` int(2) unsigned NOT NULL DEFAULT '1',
  `gateway` varchar(15) NOT NULL DEFAULT '',
  `ip_inicio_sec` varchar(15) NOT NULL,
  `ip_fim_sec` varchar(15) NOT NULL,
  `gateway_sec` varchar(15) NOT NULL,
  `formato_ips_sec` varchar(15) NOT NULL,
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `limite_clientes` int(6) unsigned NOT NULL DEFAULT '0',
  `data_con_ini` date NOT NULL,
  `data_con_fim` date NOT NULL,
  `obs` text NOT NULL,
  `caracteristicas` mediumtext NOT NULL,
  `zoom_mapa` varchar(2) NOT NULL,
  `link_redundante` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codcon`),
  KEY `codafi` (`codafi`),
  KEY `codtpr` (`codtpr`),
  KEY `codpolt` (`codpolt`),
  KEY `codigo_externo` (`codigo_externo`),
  KEY `codrad` (`codrad`),
  KEY `codstc` (`codstc`),
  KEY `codtsici` (`codtsici`),
  KEY `codrds` (`codrds`),
  KEY `ativo` (`ativo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condominios`
-- Table structure for table `apache_server_status`
--

DROP TABLE IF EXISTS `apache_server_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apache_server_status` (
  `codservst` int(11) NOT NULL AUTO_INCREMENT,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `srv` varchar(20) DEFAULT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `acc` varchar(20) DEFAULT NULL,
  `m` varchar(20) DEFAULT NULL,
  `cpu` varchar(10) DEFAULT NULL,
  `ss` varchar(10) DEFAULT NULL,
  `req` varchar(10) DEFAULT NULL,
  `conn` varchar(20) DEFAULT NULL,
  `child` varchar(20) DEFAULT NULL,
  `slot` varchar(20) DEFAULT NULL,
  `client` varchar(250) DEFAULT NULL,
  `vhost` varchar(250) DEFAULT NULL,
  `request` varchar(255) DEFAULT NULL,
  `html` mediumtext,
  `array` mediumtext,
  PRIMARY KEY (`codservst`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apache_server_status`
-- Table structure for table `layout_graficos`
--

DROP TABLE IF EXISTS `layout_graficos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `layout_graficos` (
  `codlgr` varchar(10) NOT NULL,
  `codcgr` varchar(10) NOT NULL,
  `descri_lgr` varchar(50) NOT NULL,
  `cor_fundo` varchar(11) NOT NULL,
  `tipo_degrade` varchar(10) NOT NULL,
  `cor_degrade` varchar(11) NOT NULL,
  `tipo_grade` varchar(10) NOT NULL,
  `border` int(1) NOT NULL,
  `logo` varchar(50) NOT NULL,
  `fonte_tit` varchar(50) NOT NULL,
  `fonte_ind` varchar(50) NOT NULL,
  `tamanho_legenda` int(2) unsigned NOT NULL,
  `formato_datas` varchar(11) NOT NULL,
  PRIMARY KEY (`codlgr`),
  KEY `codcgr` (`codcgr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_graficos`
-- Table structure for table `comentarios`
--

DROP TABLE IF EXISTS `comentarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comentarios` (
  `codcom` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `ver_central` char(1) NOT NULL DEFAULT 'N',
  `codtca` varchar(10) NOT NULL,
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora` varchar(5) NOT NULL DEFAULT '',
  `descri_com` text NOT NULL,
  PRIMARY KEY (`codcom`),
  KEY `codoco` (`codoco`),
  KEY `ver_central` (`ver_central`),
  KEY `codusu` (`codusu`),
  KEY `data` (`data`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comentarios`
-- Table structure for table `contas_rec_a`
--

DROP TABLE IF EXISTS `contas_rec_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_rec_a` (
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `codcomp` varchar(4) NOT NULL DEFAULT '',
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `codbol` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codftm` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL,
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codadi` varchar(10) NOT NULL DEFAULT '',
  `codmed` varchar(10) NOT NULL,
  `nro_nta_fiscal` varchar(10) NOT NULL DEFAULT '',
  `codicr` varchar(10) NOT NULL DEFAULT '',
  `codnf` varchar(10) NOT NULL DEFAULT '',
  `codacob` char(10) NOT NULL DEFAULT '',
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `periodo` varchar(19) NOT NULL DEFAULT '',
  `p_desde` date NOT NULL DEFAULT '0000-00-00',
  `p_ate` date NOT NULL DEFAULT '0000-00-00',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `parcela` varchar(5) NOT NULL DEFAULT '',
  `data_bai` date NOT NULL DEFAULT '0000-00-00',
  `histo_rec` varchar(70) NOT NULL DEFAULT '',
  `valor_lan` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_pag` float(8,2) NOT NULL DEFAULT '0.00',
  `n_boleto` varchar(20) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `juros` float(8,2) NOT NULL DEFAULT '0.00',
  `data_trans` date NOT NULL DEFAULT '0000-00-00',
  `recebido` char(1) NOT NULL DEFAULT '',
  `arq_ret` varchar(15) NOT NULL DEFAULT '',
  `codstse` varchar(10) NOT NULL,
  `protocolo_can` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codcrec`),
  KEY `codcomp` (`codcomp`),
  KEY `codafi` (`codpop`),
  KEY `codbol` (`codbol`),
  KEY `codmov` (`codmov`),
  KEY `codcli` (`codcli`),
  KEY `codftm` (`codftm`),
  KEY `data_ven` (`data_ven`),
  KEY `codicr` (`codicr`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_rec_a`
-- Table structure for table `grupo_graficos_ind`
--

DROP TABLE IF EXISTS `grupo_graficos_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_graficos_ind` (
  `codggi` varchar(10) NOT NULL,
  `codibi` varchar(10) NOT NULL,
  `descri_ggi` varchar(50) NOT NULL,
  `titulo_ggi` varchar(30) NOT NULL,
  `tempo_atualizacao` int(3) unsigned NOT NULL,
  `logo` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  `nro_grupo` int(2) DEFAULT NULL,
  PRIMARY KEY (`codggi`),
  KEY `codibi` (`codibi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_graficos_ind`
-- Table structure for table `juros_contas_rec`
--

DROP TABLE IF EXISTS `juros_contas_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `juros_contas_rec` (
  `codjcr` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `codraz` varchar(10) NOT NULL,
  `codmov` char(10) NOT NULL DEFAULT '',
  `valor_multa` float(10,2) NOT NULL,
  `valor_juros` float(10,2) NOT NULL,
  PRIMARY KEY (`codjcr`),
  KEY `codcrec` (`codcrec`),
  KEY `codraz` (`codraz`),
  KEY `codmov` (`codmov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juros_contas_rec`
-- Table structure for table `syn_mov_bancario`
--

DROP TABLE IF EXISTS `syn_mov_bancario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syn_mov_bancario` (
  `codsmov` bigint(20) NOT NULL AUTO_INCREMENT,
  `codmov` char(10) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  `valor_mov` decimal(10,2) NOT NULL DEFAULT '0.00',
  `data_ua` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sincronizado` char(1) NOT NULL DEFAULT 'N',
  `data_sincronismo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `resp_sincronismo` varchar(20) NOT NULL DEFAULT '',
  `data_erro` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tentativa` int(11) NOT NULL DEFAULT '0',
  `log_erro` mediumtext,
  `campos` mediumtext,
  `id_sap` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsmov`),
  KEY `sincronizado` (`sincronizado`),
  KEY `acao` (`acao`),
  KEY `tentativa` (`tentativa`),
  KEY `data_ua` (`data_ua`),
  KEY `codmov` (`codmov`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syn_mov_bancario`
-- Table structure for table `necessidades_servicos`
--

DROP TABLE IF EXISTS `necessidades_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `necessidades_servicos` (
  `codnser` varchar(10) NOT NULL,
  `codnm` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  PRIMARY KEY (`codnser`),
  KEY `codnm` (`codnm`),
  KEY `codser` (`codser`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `necessidades_servicos`
-- Table structure for table `contatos_midias_sociais`
--

DROP TABLE IF EXISTS `contatos_midias_sociais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contatos_midias_sociais` (
  `codcms` char(10) NOT NULL DEFAULT '',
  `codco_cl` char(10) NOT NULL DEFAULT '',
  `id_whatsapp` varchar(100) NOT NULL DEFAULT '',
  `id_skype` varchar(100) NOT NULL DEFAULT '',
  `id_telegram` varchar(100) NOT NULL DEFAULT '',
  `id_messenger` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcms`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contatos_midias_sociais`
-- Table structure for table `detalhe_topc`
--

DROP TABLE IF EXISTS `detalhe_topc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_topc` (
  `coddtopc` varchar(10) NOT NULL,
  `codtopc` varchar(10) NOT NULL,
  `codapi` varchar(10) NOT NULL,
  PRIMARY KEY (`coddtopc`),
  KEY `codtopc` (`codtopc`),
  KEY `codapi` (`codapi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_topc`
-- Table structure for table `combo_condicao_regra`
--

DROP TABLE IF EXISTS `combo_condicao_regra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combo_condicao_regra` (
  `codcombocr` char(10) NOT NULL,
  `codcombo` char(10) NOT NULL DEFAULT '',
  `codcondr` char(10) NOT NULL DEFAULT '',
  `tipo_atribuicao` char(1) NOT NULL DEFAULT '' COMMENT 'I = taxa de instalação / A = taxa de adesao',
  PRIMARY KEY (`codcombocr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo_condicao_regra`
-- Table structure for table `velocidades_sici`
--

DROP TABLE IF EXISTS `velocidades_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `velocidades_sici` (
  `codvsici` varchar(10) NOT NULL,
  `descri_vsici` varchar(50) NOT NULL,
  PRIMARY KEY (`codvsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `velocidades_sici`
-- Table structure for table `fila_campanha_lig`
--

DROP TABLE IF EXISTS `fila_campanha_lig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fila_campanha_lig` (
  `codfcl` varchar(10) NOT NULL,
  `codcla` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `codlsu` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codfor` varchar(10) NOT NULL,
  `codfat` varchar(10) NOT NULL DEFAULT '',
  `fone` varchar(11) NOT NULL,
  `provisionado_avr` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codfcl`),
  KEY `codcla` (`codcla`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codlsu` (`codlsu`),
  KEY `codfat` (`codfat`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fila_campanha_lig`
-- Table structure for table `prospect_necessidades`
--

DROP TABLE IF EXISTS `prospect_necessidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prospect_necessidades` (
  `codprn` varchar(10) NOT NULL,
  `codnm` varchar(10) NOT NULL,
  `codpros` varchar(10) NOT NULL,
  `diponilibilidade` char(1) NOT NULL,
  PRIMARY KEY (`codprn`),
  KEY `codnm` (`codnm`),
  KEY `codpros` (`codpros`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prospect_necessidades`
-- Table structure for table `agenda_tarefas`
--

DROP TABLE IF EXISTS `agenda_tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_tarefas` (
  `codatar` varchar(10) NOT NULL DEFAULT '',
  `codtar` varchar(10) NOT NULL DEFAULT '',
  `tipo_tar` char(1) NOT NULL DEFAULT '',
  `minutos` int(4) unsigned NOT NULL DEFAULT '0',
  `hora` varchar(5) NOT NULL DEFAULT '',
  `dia` int(2) unsigned NOT NULL DEFAULT '0',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `nro_dia` int(1) unsigned NOT NULL DEFAULT '0',
  `domingo` int(1) NOT NULL DEFAULT '0',
  `segunda` int(1) NOT NULL DEFAULT '0',
  `terca` int(1) NOT NULL DEFAULT '0',
  `quarta` int(1) NOT NULL DEFAULT '0',
  `quinta` int(1) NOT NULL DEFAULT '0',
  `sexta` int(1) NOT NULL DEFAULT '0',
  `sabado` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codatar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_tarefas`
-- Table structure for table `tarefas`
--

DROP TABLE IF EXISTS `tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefas` (
  `codtar` varchar(10) NOT NULL DEFAULT '',
  `codcst` varchar(10) NOT NULL DEFAULT '',
  `codstar` varchar(10) NOT NULL DEFAULT 'AGUARDANDO',
  `codctar` varchar(10) NOT NULL,
  `codcbe` varchar(10) DEFAULT NULL,
  `nome_tar` varchar(50) NOT NULL DEFAULT '',
  `ultima_exe` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `url` varchar(200) NOT NULL DEFAULT '',
  `timeout` int(11) NOT NULL DEFAULT '60',
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `parametros` varchar(200) NOT NULL DEFAULT '',
  `emails_destino` text NOT NULL,
  `emails_erro` text NOT NULL,
  `cria_logs` char(1) NOT NULL DEFAULT 'S',
  `obs` text NOT NULL,
  PRIMARY KEY (`codtar`),
  KEY `codstar` (`codstar`),
  KEY `codctar` (`codctar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefas`
-- Table structure for table `tipo_ponto_roteamento`
--

DROP TABLE IF EXISTS `tipo_ponto_roteamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_ponto_roteamento` (
  `codtpr` varchar(10) NOT NULL DEFAULT '',
  `codemr` varchar(10) NOT NULL,
  `descri_tpr` varchar(30) NOT NULL DEFAULT '',
  `tipo_p_r` char(1) NOT NULL DEFAULT 'C',
  `imagem` varchar(20) NOT NULL DEFAULT '',
  `codima` varchar(15) NOT NULL,
  `ver_zoom` int(3) unsigned NOT NULL,
  `wireless` char(1) NOT NULL,
  PRIMARY KEY (`codtpr`),
  KEY `codima` (`codima`),
  KEY `codemr` (`codemr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_ponto_roteamento`
-- Table structure for table `indicadores_sici`
--

DROP TABLE IF EXISTS `indicadores_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `indicadores_sici` (
  `codisici` varchar(10) NOT NULL,
  `codvsici` varchar(10) NOT NULL,
  `codtsici` varchar(10) NOT NULL,
  `descri_isici` varchar(70) NOT NULL,
  `origem` char(1) NOT NULL,
  `tipo` char(1) NOT NULL,
  `filtro` text NOT NULL,
  `alias` varchar(20) NOT NULL,
  `periodicidade` char(1) NOT NULL,
  PRIMARY KEY (`codisici`),
  KEY `codvsici` (`codvsici`),
  KEY `codtsici` (`codtsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indicadores_sici`
-- Table structure for table `modelos_nf`
--

DROP TABLE IF EXISTS `modelos_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modelos_nf` (
  `codmnf` char(10) NOT NULL DEFAULT '',
  `codemp` char(10) NOT NULL,
  `codtnf` char(10) NOT NULL,
  `codrela` char(10) NOT NULL,
  `ultimo_nro` int(8) NOT NULL DEFAULT '0',
  `serie` char(4) NOT NULL,
  `serie_outro_uf` char(1) NOT NULL,
  `descri_mnf` varchar(50) NOT NULL,
  `retiene_imp` char(1) NOT NULL DEFAULT 'N',
  `impressao` text NOT NULL,
  `exportar_nfse` mediumtext NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `login_webserv` varchar(25) NOT NULL,
  `senha_webserv` varchar(50) NOT NULL,
  `copiar_arquivos` char(1) NOT NULL DEFAULT 'N',
  `ativo` char(1) NOT NULL DEFAULT 'N',
  `producao` char(1) NOT NULL DEFAULT 'N',
  `soap` char(1) NOT NULL DEFAULT 'S',
  `metodo_action` varchar(50) NOT NULL,
  `parametro_resposta` varchar(50) NOT NULL,
  `valor_parametro_resposta` varchar(50) NOT NULL,
  `host_homologacao` varchar(250) NOT NULL,
  `host_producao` varchar(250) NOT NULL,
  `permite_email` char(1) NOT NULL DEFAULT 'S',
  `matricial` char(1) NOT NULL DEFAULT 'N',
  `validar_esquema` char(1) NOT NULL DEFAULT 'N',
  `assinar_xml` char(1) NOT NULL DEFAULT 'N',
  `chave_privada` varchar(30) NOT NULL DEFAULT '',
  `tag_link_impressao` varchar(20) NOT NULL DEFAULT '',
  `tag_nro_nfse` varchar(50) NOT NULL,
  `tipo_consulta` char(10) NOT NULL DEFAULT '',
  `formato_nfse` char(5) NOT NULL,
  `time_out` int(8) NOT NULL,
  PRIMARY KEY (`codmnf`),
  KEY `codemp` (`codemp`),
  KEY `codtnf` (`codtnf`),
  KEY `codrela` (`codrela`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modelos_nf`
-- Table structure for table `det_previsoes_un`
--

DROP TABLE IF EXISTS `det_previsoes_un`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_previsoes_un` (
  `coddpun` varchar(10) NOT NULL,
  `codprev` varchar(10) NOT NULL,
  `codpop` varchar(10) NOT NULL,
  `valor` float(10,2) NOT NULL,
  `porcentagem` float(8,3) NOT NULL,
  PRIMARY KEY (`coddpun`),
  KEY `codprev` (`codprev`),
  KEY `codpop` (`codpop`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_previsoes_un`
-- Table structure for table `transmissao_pi`
--

DROP TABLE IF EXISTS `transmissao_pi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transmissao_pi` (
  `codtpi` varchar(10) NOT NULL,
  `codvind` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `ok` char(1) NOT NULL,
  PRIMARY KEY (`codtpi`),
  KEY `codvind` (`codvind`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transmissao_pi`
-- Table structure for table `grupo_comandos`
--

DROP TABLE IF EXISTS `grupo_comandos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_comandos` (
  `codgcom` varchar(10) NOT NULL DEFAULT '',
  `descri_gcom` varchar(50) NOT NULL DEFAULT '',
  `codtcom` char(1) NOT NULL DEFAULT '',
  `codaco` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codgcom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_comandos`
-- Table structure for table `busqueda_bkp`
--

DROP TABLE IF EXISTS `busqueda_bkp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `busqueda_bkp` (
  `codbus` varchar(10) NOT NULL DEFAULT '',
  `arquivo` varchar(4) NOT NULL DEFAULT '',
  `ordem` int(2) unsigned NOT NULL DEFAULT '0',
  `lbusq` varchar(20) NOT NULL DEFAULT '',
  `cbusq` varchar(100) NOT NULL,
  `campos` text NOT NULL,
  `mascara` varchar(20) NOT NULL DEFAULT '' COMMENT 'Máscara para ser aplicada no campo de pesquisa',
  PRIMARY KEY (`codbus`),
  KEY `arquivo` (`arquivo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `busqueda_bkp`
-- Table structure for table `det_conciliacao`
--

DROP TABLE IF EXISTS `det_conciliacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_conciliacao` (
  `id_movcon` bigint(18) NOT NULL,
  `codmov` varchar(10) DEFAULT NULL,
  `data_hora` datetime DEFAULT NULL,
  KEY `id_movcon` (`id_movcon`),
  KEY `codmov` (`codmov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_conciliacao`
-- Table structure for table `comandos`
--

DROP TABLE IF EXISTS `comandos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comandos` (
  `codcom` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idcomando` int(4) NOT NULL DEFAULT '0',
  `comando` varchar(150) NOT NULL DEFAULT '',
  `pasta` varchar(100) NOT NULL DEFAULT '',
  `descricao` varchar(255) NOT NULL DEFAULT '',
  `parametros` varchar(255) NOT NULL DEFAULT '',
  `os` varchar(20) NOT NULL DEFAULT '',
  `codtcom` char(1) NOT NULL DEFAULT '',
  `tipo_comp` char(1) NOT NULL DEFAULT '',
  `nargumentos` int(10) unsigned NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `codcom_d` int(4) unsigned NOT NULL DEFAULT '0',
  `help` text,
  PRIMARY KEY (`codcom`)
) ENGINE=MyISAM AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comandos`
-- Table structure for table `juros_contas_pag`
--

DROP TABLE IF EXISTS `juros_contas_pag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `juros_contas_pag` (
  `codjcp` varchar(10) NOT NULL,
  `codcpag` varchar(10) NOT NULL,
  `codraz` varchar(10) NOT NULL,
  `valor_multa` decimal(10,2) NOT NULL,
  `valor_juros` decimal(10,2) NOT NULL,
  PRIMARY KEY (`codjcp`),
  KEY `codcpag` (`codcpag`),
  KEY `codraz` (`codraz`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juros_contas_pag`
-- Table structure for table `equipamentos_rede_tipo_servicos`
--

DROP TABLE IF EXISTS `equipamentos_rede_tipo_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipamentos_rede_tipo_servicos` (
  `codeqrtserv` varchar(10) NOT NULL,
  `nome_servico` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`codeqrtserv`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos_rede_tipo_servicos`
-- Table structure for table `histo_nfe`
--

DROP TABLE IF EXISTS `histo_nfe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histo_nfe` (
  `codhisnfe` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `codstnfe` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  `codusu` varchar(2) NOT NULL,
  `ip` varchar(100) NOT NULL,
  `descri_hisnfe` varchar(100) NOT NULL,
  `xml_consulta` mediumtext NOT NULL,
  `xml_resposta` mediumtext NOT NULL,
  PRIMARY KEY (`codhisnfe`),
  KEY `codnf` (`codnf`),
  KEY `codstnfe` (`codstnfe`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `histo_nfe`
-- Table structure for table `provisionamento_desconexao`
--

DROP TABLE IF EXISTS `provisionamento_desconexao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `provisionamento_desconexao` (
  `codprdc` varchar(10) NOT NULL DEFAULT '',
  `codtsp` varchar(10) NOT NULL,
  `status` char(1) NOT NULL,
  `data_cadastro` datetime NOT NULL,
  `data_execucao` datetime NOT NULL,
  `nro_tentativa` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codprdc`),
  KEY `codtsp` (`codtsp`),
  KEY `status` (`status`),
  KEY `data_cadastro` (`data_cadastro`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provisionamento_desconexao`
-- Table structure for table `eventos_ppv`
--

DROP TABLE IF EXISTS `eventos_ppv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventos_ppv` (
  `codeppv` varchar(10) NOT NULL,
  `codcnl` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `codtppv` varchar(10) NOT NULL,
  `descri_eppv` varchar(50) NOT NULL,
  `data_hora` datetime NOT NULL,
  `tempo` int(3) unsigned NOT NULL,
  `valor` float(10,2) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codeppv`),
  KEY `codcnl` (`codcnl`),
  KEY `codservp` (`codservp`),
  KEY `codtppv` (`codtppv`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_ppv`
-- Table structure for table `dados_ftp`
--

DROP TABLE IF EXISTS `dados_ftp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dados_ftp` (
  `coddftp` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL DEFAULT '',
  `login` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(50) NOT NULL DEFAULT '',
  `caminho` varchar(50) NOT NULL DEFAULT '',
  `codcli` int(11) DEFAULT NULL,
  `obs` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddftp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_ftp`
-- Table structure for table `mapas`
--

DROP TABLE IF EXISTS `mapas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mapas` (
  `codmapa` varchar(10) NOT NULL,
  `nome_mapa` varchar(50) NOT NULL,
  `zoom` int(10) NOT NULL DEFAULT '0',
  `codarq` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codmapa`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mapas`
-- Table structure for table `unidades_financeiras`
--

DROP TABLE IF EXISTS `unidades_financeiras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades_financeiras` (
  `codu_f` char(3) NOT NULL DEFAULT '',
  `nome_u_f` varchar(30) NOT NULL DEFAULT '',
  `razao_social` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codu_f`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_financeiras`
-- Table structure for table `tipo_orden_s`
--

DROP TABLE IF EXISTS `tipo_orden_s`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_orden_s` (
  `codtords` varchar(10) NOT NULL DEFAULT '',
  `coddoc` varchar(10) NOT NULL,
  `descri_ords` varchar(50) NOT NULL,
  `valor_ords` decimal(8,2) NOT NULL DEFAULT '0.00',
  `codsad` varchar(10) NOT NULL DEFAULT '',
  `tipo_faturamento` char(1) NOT NULL,
  `gerar_cr` char(1) NOT NULL DEFAULT 'N',
  `dias_vencimento` int(3) NOT NULL DEFAULT '30',
  `parcelas` int(3) NOT NULL DEFAULT '1',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `fechar_automaticamente` char(1) NOT NULL DEFAULT 'N',
  `tempo_fechar_auto` char(5) NOT NULL,
  `externo` char(1) NOT NULL DEFAULT 'S',
  `checklist` mediumtext NOT NULL,
  `checklist_ret` mediumtext NOT NULL,
  `gerar_cobranca_os` char(1) NOT NULL DEFAULT 'S',
  `fecharos_semsinal` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codtords`),
  KEY `coddoc` (`coddoc`),
  KEY `ativo` (`ativo`),
  KEY ```gerar_cobranca_os``` (`gerar_cobranca_os`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_orden_s`
-- Table structure for table `servicos_cli_comi`
--

DROP TABLE IF EXISTS `servicos_cli_comi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_comi` (
  `codsccs` varchar(10) NOT NULL,
  `codtcs` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  PRIMARY KEY (`codsccs`),
  KEY `codtcs` (`codtcs`),
  KEY `codusu` (`codusu`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_comi`
-- Table structure for table `perguntas_aten`
--

DROP TABLE IF EXISTS `perguntas_aten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perguntas_aten` (
  `codp_a` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'S',
  `numero` int(6) NOT NULL DEFAULT '0',
  `titulo` varchar(200) NOT NULL DEFAULT '',
  `titulo_fc` varchar(7) NOT NULL DEFAULT '',
  `titulo_bc` varchar(7) NOT NULL DEFAULT '',
  `url` varchar(200) NOT NULL DEFAULT '',
  `titulo_url` varchar(100) NOT NULL DEFAULT '',
  `nome_ima` varchar(30) NOT NULL DEFAULT '',
  `sempai` char(1) NOT NULL DEFAULT 'N',
  `expli_cli_fc` varchar(7) NOT NULL DEFAULT '',
  `expli_cli_bc` varchar(7) NOT NULL DEFAULT '',
  `expli_sup_fc` varchar(7) NOT NULL DEFAULT '',
  `expli_sup_bc` varchar(7) NOT NULL DEFAULT '',
  `imagem` text NOT NULL,
  `expli_cli` text NOT NULL,
  `expli_sup` text NOT NULL,
  PRIMARY KEY (`codp_a`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perguntas_aten`
-- Table structure for table `tipo_codificadores`
--

DROP TABLE IF EXISTS `tipo_codificadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_codificadores` (
  `codtcdf` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `descri_tcdf` varchar(50) NOT NULL,
  `codigo_cas` varchar(30) NOT NULL,
  `valor_cdf_ex` float(10,2) NOT NULL,
  `lan` char(1) NOT NULL DEFAULT 'N',
  `ata` char(1) NOT NULL DEFAULT 'N',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtcdf`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_codificadores`
-- Table structure for table `contas_emails_a`
--

DROP TABLE IF EXISTS `contas_emails_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_emails_a` (
  `codcemail` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `login` varchar(100) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `foward` text NOT NULL,
  `copia` char(1) NOT NULL DEFAULT '',
  `data_a` date NOT NULL DEFAULT '0000-00-00',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcemail`),
  KEY `codsercli` (`codsercli`),
  KEY `codcli` (`codcli`),
  KEY `login` (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_emails_a`
-- Table structure for table `mod_email_depto`
--

DROP TABLE IF EXISTS `mod_email_depto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mod_email_depto` (
  `codmoded` varchar(10) NOT NULL,
  `codcar` varchar(10) NOT NULL,
  `coddep` varchar(10) NOT NULL,
  `codcbe` varchar(10) NOT NULL,
  PRIMARY KEY (`codmoded`),
  KEY `codcbe` (`codcbe`),
  KEY `coddep` (`coddep`),
  KEY `codcar` (`codcar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mod_email_depto`
-- Table structure for table `imagens_mr`
--

DROP TABLE IF EXISTS `imagens_mr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imagens_mr` (
  `codimr` varchar(10) NOT NULL,
  `descri_imr` varchar(50) NOT NULL,
  `nome_arq` varchar(30) NOT NULL,
  `url` varchar(100) NOT NULL,
  `imagem` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codimr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagens_mr`
-- Table structure for table `ciclos_grafico`
--

DROP TABLE IF EXISTS `ciclos_grafico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ciclos_grafico` (
  `codcgr` varchar(10) NOT NULL,
  `descri_cgr` varchar(50) NOT NULL,
  `tempo_dias` int(6) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `tipo_leitura` char(1) NOT NULL,
  `quant_ciclos` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codcgr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciclos_grafico`
-- Table structure for table `tipo_class_fiscal`
--

DROP TABLE IF EXISTS `tipo_class_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_class_fiscal` (
  `codtcf` varchar(10) NOT NULL,
  `descri_cf` varchar(50) NOT NULL,
  PRIMARY KEY (`codtcf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_class_fiscal`
-- Table structure for table `tipo_onu_fibra`
--

DROP TABLE IF EXISTS `tipo_onu_fibra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_onu_fibra` (
  `codtonu` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `descri_tonu` varchar(30) NOT NULL,
  `tecnologia` varchar(50) NOT NULL,
  `wireless` char(1) NOT NULL DEFAULT 'S',
  `pppoe` char(1) NOT NULL DEFAULT 'S',
  `tipo_conexao` char(1) NOT NULL,
  `lan_ports` int(2) NOT NULL,
  `voice_ports` int(2) NOT NULL,
  PRIMARY KEY (`codtonu`),
  KEY `codprod` (`codprod`),
  KEY `descri_tonu_IDX` (`descri_tonu`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_onu_fibra`
-- Table structure for table `status_os`
--

DROP TABLE IF EXISTS `status_os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_os` (
  `status_os` char(1) NOT NULL,
  `descri_st` varchar(30) NOT NULL,
  PRIMARY KEY (`status_os`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_os`
-- Table structure for table `prefixos`
--

DROP TABLE IF EXISTS `prefixos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefixos` (
  `codpref` varchar(10) NOT NULL DEFAULT '',
  `codtter` varchar(10) NOT NULL DEFAULT '',
  `prefixo` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `descri_pref` varchar(100) NOT NULL,
  `valor` float(7,4) NOT NULL,
  `disponivel` char(1) NOT NULL DEFAULT 'N',
  `mvno` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codpref`),
  KEY `codtter` (`codtter`),
  KEY `prefixo` (`prefixo`),
  KEY `cidade` (`cidade`),
  KEY `disponivel` (`disponivel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prefixos`
-- Table structure for table `franquia_extra`
--

DROP TABLE IF EXISTS `franquia_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franquia_extra` (
  `codfrx` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `franquia` int(8) unsigned NOT NULL,
  PRIMARY KEY (`codfrx`),
  KEY `codsercli` (`codsercli`),
  KEY `codcrec` (`codcrec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `franquia_extra`
-- Table structure for table `script_equipamentos`
--

DROP TABLE IF EXISTS `script_equipamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_equipamentos` (
  `codseq` varchar(10) NOT NULL,
  `script_criar` mediumtext NOT NULL,
  `script_apagar` mediumtext NOT NULL,
  `script_teste` mediumtext NOT NULL,
  PRIMARY KEY (`codseq`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_equipamentos`
-- Table structure for table `alertas_ocorridos`
--

DROP TABLE IF EXISTS `alertas_ocorridos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alertas_ocorridos` (
  `codaleoco` char(10) NOT NULL,
  `codale` char(10) NOT NULL,
  `tabela` varchar(50) NOT NULL,
  `codigo` char(10) NOT NULL,
  `data_inicio` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `motivo_fim` varchar(50) NOT NULL,
  PRIMARY KEY (`codaleoco`),
  KEY `data_inicio` (`data_inicio`),
  KEY `data_fim` (`data_fim`),
  KEY `fk_alertas_ocorridos_alertas1_idx` (`codale`),
  KEY `codigo` (`codigo`),
  KEY `tabela` (`tabela`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertas_ocorridos`
-- Table structure for table `proposta_comercial`
--

DROP TABLE IF EXISTS `proposta_comercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proposta_comercial` (
  `codpcom` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codeem` varchar(10) NOT NULL,
  `numero_pcom` int(6) unsigned NOT NULL,
  `data_cad` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '||-',
  `data_aut` date NOT NULL,
  `data_aprov` date NOT NULL,
  `data_validade` date NOT NULL,
  `taxa_inst` float(10,2) NOT NULL,
  `parcelas_int` int(6) unsigned NOT NULL,
  `valor` float(10,2) NOT NULL,
  `parcelas_inst` int(6) NOT NULL DEFAULT '0',
  `status` char(1) NOT NULL,
  `condicoes_especiais` mediumtext NOT NULL,
  `proposta` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codpcom`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codusu` (`codusu`),
  KEY `codeem` (`codeem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proposta_comercial`
-- Table structure for table `comissoes`
--

DROP TABLE IF EXISTS `comissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comissoes` (
  `codcomi` varchar(10) NOT NULL,
  `codven` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data` datetime NOT NULL,
  `p_ate` date NOT NULL,
  `p_desde` date NOT NULL,
  PRIMARY KEY (`codcomi`),
  KEY `codven` (`codven`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissoes`
-- Table structure for table `tabelas_sincronismo`
--

DROP TABLE IF EXISTS `tabelas_sincronismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabelas_sincronismo` (
  `codtsi` char(10) NOT NULL DEFAULT '',
  `codtab` char(10) NOT NULL DEFAULT '',
  `codssi` char(10) NOT NULL DEFAULT '',
  `data_ua` datetime NOT NULL,
  `continuo` char(1) NOT NULL DEFAULT '',
  `nome_tabela` varchar(50) NOT NULL DEFAULT '',
  `campo_primario` varchar(50) NOT NULL DEFAULT '',
  `consulta_sql` mediumtext NOT NULL,
  PRIMARY KEY (`codtsi`),
  KEY `codtab` (`codtab`),
  KEY `codssi` (`codssi`),
  KEY `data_ua` (`data_ua`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelas_sincronismo`
-- Table structure for table `alerta_metas_ind`
--

DROP TABLE IF EXISTS `alerta_metas_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alerta_metas_ind` (
  `codami` varchar(10) NOT NULL,
  `codmind` varchar(10) NOT NULL,
  `codalerta` char(1) NOT NULL,
  `cor_grafico` varchar(11) NOT NULL,
  `email_alerta` varchar(150) NOT NULL,
  `fones_alerta` varchar(100) NOT NULL,
  PRIMARY KEY (`codami`),
  KEY `codmind` (`codmind`),
  KEY `codalerta` (`codalerta`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerta_metas_ind`
-- Table structure for table `tipo_det_grafico_ind`
--

DROP TABLE IF EXISTS `tipo_det_grafico_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_det_grafico_ind` (
  `codtgraf` varchar(10) NOT NULL,
  `descri_tgraf` varchar(50) NOT NULL,
  `dimensoes` int(1) unsigned NOT NULL,
  `codigo_desk` varchar(11) NOT NULL,
  `codigo_fc` varchar(11) NOT NULL,
  `codigo_mobile` varchar(255) NOT NULL,
  `tipo` char(2) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtgraf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_det_grafico_ind`
-- Table structure for table `bancos`
--

DROP TABLE IF EXISTS `bancos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bancos` (
  `codban` char(10) NOT NULL DEFAULT '',
  `codexterno` varchar(20) NOT NULL,
  `codpop` char(10) NOT NULL,
  `codemp` char(10) NOT NULL,
  `codafi` char(10) NOT NULL DEFAULT '',
  `nome_ban` varchar(50) NOT NULL DEFAULT '',
  `razao_social` varchar(50) NOT NULL DEFAULT '',
  `nro_agencia` char(6) NOT NULL DEFAULT '',
  `nro_conta` char(10) NOT NULL DEFAULT '',
  `contato` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` char(8) NOT NULL DEFAULT '',
  `cep` char(9) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(9) NOT NULL DEFAULT '0',
  `fax` int(9) NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `aniversario` char(5) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL,
  `icm` varchar(15) NOT NULL DEFAULT '',
  `limite_cre` int(11) NOT NULL DEFAULT '0',
  `vencimento_cre` date NOT NULL DEFAULT '0000-00-00',
  `activo` char(1) NOT NULL DEFAULT '',
  `nro_banco` char(3) NOT NULL DEFAULT '',
  `nro_ban` char(3) NOT NULL,
  `nosso_nro` int(11) NOT NULL DEFAULT '0',
  `data_conci` date NOT NULL DEFAULT '0000-00-00',
  `cod_arq_mag` int(6) NOT NULL DEFAULT '0',
  `tipo` char(1) NOT NULL DEFAULT '',
  `nro_che` int(9) unsigned NOT NULL DEFAULT '0',
  `limite_cc` decimal(8,2) NOT NULL DEFAULT '0.00',
  `fluxo_cx` char(1) NOT NULL DEFAULT 'S',
  `obs` text NOT NULL,
  PRIMARY KEY (`codban`),
  KEY `codexterno` (`codexterno`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancos`
-- Table structure for table `tipo_olt_fibra`
--

DROP TABLE IF EXISTS `tipo_olt_fibra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_olt_fibra` (
  `codtolt` varchar(10) NOT NULL,
  `descri_tolt` varchar(30) NOT NULL,
  `porta_padrao` int(5) unsigned NOT NULL,
  `protocolo` varchar(10) NOT NULL,
  `versao_olt` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`codtolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_olt_fibra`
-- Table structure for table `tipo_unidade_indicador`
--

DROP TABLE IF EXISTS `tipo_unidade_indicador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_unidade_indicador` (
  `codtui` varchar(10) NOT NULL,
  `descri_tui` varchar(50) NOT NULL,
  `titulo` varchar(30) NOT NULL,
  `titulo_red` varchar(5) NOT NULL,
  `qnt_decimal` int(1) DEFAULT NULL,
  PRIMARY KEY (`codtui`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_unidade_indicador`
-- Table structure for table `tabelas_acct`
--

DROP TABLE IF EXISTS `tabelas_acct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabelas_acct` (
  `codtabacct` varchar(10) NOT NULL,
  `nome_tabacct` varchar(100) NOT NULL,
  `primeira_data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ultima_data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codservp` varchar(10) NOT NULL,
  PRIMARY KEY (`codtabacct`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelas_acct`
-- Table structure for table `equipes`
--

DROP TABLE IF EXISTS `equipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipes` (
  `codeqp` varchar(10) NOT NULL,
  `codlmp` varchar(10) NOT NULL,
  `nome_equipe` varchar(50) NOT NULL,
  PRIMARY KEY (`codeqp`),
  KEY `codlmp` (`codlmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipes`
-- Table structure for table `det_nota_fiscal_itens`
--

DROP TABLE IF EXISTS `det_nota_fiscal_itens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_nota_fiscal_itens` (
  `coddnfi` char(10) NOT NULL,
  `coddnf` char(10) NOT NULL COMMENT 'codigo det_nota_fiscal',
  `codnf` char(10) NOT NULL COMMENT 'codigo nota fiscal',
  `codpat` char(10) NOT NULL COMMENT 'codigo patrimonio',
  `codmvp` char(10) NOT NULL COMMENT 'codigo movimento patrimonio',
  PRIMARY KEY (`coddnfi`),
  KEY `coddnf` (`coddnf`),
  KEY `codnf` (`codnf`),
  KEY `codpat` (`codpat`),
  KEY `codmvp` (`codmvp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_nota_fiscal_itens`
-- Table structure for table `servicos_cli_del`
--

DROP TABLE IF EXISTS `servicos_cli_del`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_del` (
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `data_del` date NOT NULL,
  PRIMARY KEY (`codsercli`),
  KEY `codsercli` (`codsercli`),
  KEY `data_del` (`data_del`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_del`
-- Table structure for table `filmes`
--

DROP TABLE IF EXISTS `filmes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filmes` (
  `codflm` varchar(10) DEFAULT NULL,
  `descri_flm` varchar(50) DEFAULT NULL,
  `tempo` int(4) unsigned NOT NULL,
  `sipnosis` mediumtext NOT NULL,
  `imagem` mediumtext NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filmes`
-- Table structure for table `motivo_fechamento_os`
--

DROP TABLE IF EXISTS `motivo_fechamento_os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motivo_fechamento_os` (
  `codmfos` char(10) NOT NULL,
  `ativo` char(1) NOT NULL,
  `descri_mfos` varchar(70) NOT NULL,
  `codtec` char(10) NOT NULL DEFAULT '',
  `codcar` char(10) NOT NULL,
  `codusu_d` char(2) NOT NULL DEFAULT '',
  `codcar_d` char(10) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codmfos`),
  KEY `descri_mfos` (`descri_mfos`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivo_fechamento_os`
-- Table structure for table `registros_apagados_sincronismo`
--

DROP TABLE IF EXISTS `registros_apagados_sincronismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registros_apagados_sincronismo` (
  `codtab` char(10) NOT NULL DEFAULT '',
  `data_proc` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codigo` char(10) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `codtab` (`codtab`),
  KEY `data_proc` (`data_proc`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros_apagados_sincronismo`
-- Table structure for table `configu_radius`
--

DROP TABLE IF EXISTS `configu_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configu_radius` (
  `codcrad` varchar(10) NOT NULL DEFAULT '',
  `radcheck` varchar(50) NOT NULL DEFAULT 'radcheck',
  `radacct` varchar(50) NOT NULL DEFAULT 'radacct',
  `radgroupcheck` varchar(50) DEFAULT 'radgroupcheck',
  `usergroup` varchar(50) DEFAULT 'usergroup',
  `username` varchar(50) NOT NULL,
  `groupname` varchar(50) NOT NULL,
  `attribute` varchar(50) NOT NULL,
  `attribute_value` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  `radgroupreply` varchar(50) NOT NULL DEFAULT 'radgroupreply',
  `radius_restart` varchar(200) NOT NULL DEFAULT 'sudo /etc/init.d/freeradius restart',
  `radreply` varchar(50) NOT NULL DEFAULT 'radreply',
  `nas_insert` varchar(200) NOT NULL DEFAULT 'insert into nas (nasname,shortname,secret,community,type) values(''$host_nas'',''$shortname'',''$secret'',''$community'',''other'')',
  `nas_delete` varchar(200) NOT NULL DEFAULT 'delete from nas where nasname=''$host_nas''',
  `plugout` varchar(250) NOT NULL DEFAULT '' COMMENT '||AuthGatewayRadiusUConf plugout command',
  PRIMARY KEY (`codcrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configu_radius`
-- Table structure for table `interfaces`
--

DROP TABLE IF EXISTS `interfaces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaces` (
  `codinte` varchar(10) NOT NULL DEFAULT '',
  `codeqr` varchar(10) NOT NULL DEFAULT '',
  `codtintr` varchar(10) NOT NULL DEFAULT '',
  `codtcomu` varchar(10) DEFAULT NULL,
  `codsti` varchar(10) DEFAULT NULL,
  `service_name` varchar(50) DEFAULT NULL,
  `interface` varchar(20) NOT NULL DEFAULT '',
  `alias` varchar(20) DEFAULT NULL,
  `dns` varchar(50) DEFAULT NULL,
  `mac` varchar(17) DEFAULT '',
  PRIMARY KEY (`codinte`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interfaces`
-- Table structure for table `opcoes_aten`
--

DROP TABLE IF EXISTS `opcoes_aten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes_aten` (
  `codo_a` varchar(10) NOT NULL DEFAULT '',
  `codp_a` varchar(10) NOT NULL DEFAULT '',
  `tipo_resp` char(1) NOT NULL DEFAULT '',
  `valor_fixo` varchar(100) NOT NULL DEFAULT '',
  `codp_ad` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codo_a`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes_aten`
-- Table structure for table `tipo_servidor`
--

DROP TABLE IF EXISTS `tipo_servidor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_servidor` (
  `codtservp` varchar(10) NOT NULL DEFAULT '',
  `descri_tservp` varchar(30) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_servidor`
-- Table structure for table `envio_push`
--

DROP TABLE IF EXISTS `envio_push`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `envio_push` (
  `codepush` varchar(10) NOT NULL,
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL,
  `codpros` varchar(10) NOT NULL,
  `codcel` char(10) NOT NULL DEFAULT '',
  `assunto` varchar(100) NOT NULL DEFAULT '',
  `message` mediumtext NOT NULL,
  `enviado` char(1) NOT NULL DEFAULT 'N',
  `envio` longtext,
  `retorno` longtext,
  PRIMARY KEY (`codepush`),
  KEY `data` (`data`),
  KEY `codusu` (`codusu`),
  KEY `codcli` (`codcli`),
  KEY `codpros` (`codpros`),
  KEY `enviado` (`enviado`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `envio_push`
-- Table structure for table `historico_troca_status_prov`
--

DROP TABLE IF EXISTS `historico_troca_status_prov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_troca_status_prov` (
  `codhtsp` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `data_execucao` datetime NOT NULL,
  `nro_tentativas` int(2) unsigned NOT NULL,
  `ultimo_log` mediumtext NOT NULL,
  PRIMARY KEY (`codhtsp`),
  KEY `codsercli` (`codsercli`),
  KEY `data_execucao` (`data_execucao`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_troca_status_prov`
-- Table structure for table `venda_pat`
--

DROP TABLE IF EXISTS `venda_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venda_pat` (
  `codvpat` varchar(10) NOT NULL DEFAULT '',
  `valor` float(10,2) DEFAULT NULL,
  `parcelas` int(2) DEFAULT NULL,
  `numero_nf` int(9) DEFAULT NULL,
  PRIMARY KEY (`codvpat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda_pat`
-- Table structure for table `cancelamento_mov_pat`
--

DROP TABLE IF EXISTS `cancelamento_mov_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cancelamento_mov_pat` (
  `codcmvp` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(4) unsigned NOT NULL,
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(2) NOT NULL DEFAULT '',
  `data` date NOT NULL,
  `valor` float(10,2) NOT NULL,
  `motivo` mediumtext NOT NULL,
  PRIMARY KEY (`codcmvp`),
  KEY `codusu` (`codusu`),
  KEY `codlmp` (`codlmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancelamento_mov_pat`
-- Table structure for table `usu_tipo_os`
--

DROP TABLE IF EXISTS `usu_tipo_os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_tipo_os` (
  `codusutos` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codtords` varchar(10) NOT NULL,
  PRIMARY KEY (`codusutos`),
  KEY `codusu` (`codusu`),
  KEY `codtords` (`codtords`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_tipo_os`
-- Table structure for table `pacotes_sc`
--

DROP TABLE IF EXISTS `pacotes_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pacotes_sc` (
  `codpsc` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `data_ini` date NOT NULL,
  `data_can` date NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `codigo_externo` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codpsc`),
  KEY `codpac` (`codpac`),
  KEY `codsercli` (`codsercli`),
  KEY `ativo` (`ativo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacotes_sc`
-- Table structure for table `importacao_ponto`
--

DROP TABLE IF EXISTS `importacao_ponto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `importacao_ponto` (
  `codponto` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codigo_externo` varchar(20) NOT NULL,
  `data_ini` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `tempo` int(4) unsigned NOT NULL,
  PRIMARY KEY (`codponto`),
  KEY `codusu` (`codusu`),
  KEY `data_ini` (`data_ini`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `importacao_ponto`
-- Table structure for table `estacoes`
--

DROP TABLE IF EXISTS `estacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estacoes` (
  `codesta` char(10) NOT NULL,
  `descri_esta` varchar(45) NOT NULL,
  `nome_estacao` varchar(45) NOT NULL DEFAULT '',
  `nome_arq` varchar(45) NOT NULL DEFAULT '',
  `dhcp` char(1) NOT NULL DEFAULT 'N',
  `ip_est` varchar(15) NOT NULL DEFAULT '0.0.0.0',
  `codcar` char(10) NOT NULL DEFAULT '',
  `p0` mediumtext,
  `p1` varchar(64) NOT NULL,
  `p2` varchar(64) NOT NULL,
  `p3` varchar(64) NOT NULL,
  `p4` varchar(64) NOT NULL,
  `p5` varchar(64) NOT NULL,
  `p6` varchar(255) NOT NULL,
  `p7` int(11) DEFAULT '0',
  `p8` char(10) NOT NULL,
  PRIMARY KEY (`codesta`,`nome_arq`,`dhcp`),
  KEY `dhcp` (`dhcp`),
  KEY `codcar` (`codcar`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='	';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacoes`
-- Table structure for table `sap_ret_nf`
--

DROP TABLE IF EXISTS `sap_ret_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sap_ret_nf` (
  `codnf` char(10) NOT NULL,
  `docentry` int(11) NOT NULL,
  PRIMARY KEY (`codnf`),
  UNIQUE KEY `codnf_itemCode` (`codnf`,`docentry`),
  KEY `codnf` (`codnf`),
  KEY `docentry` (`docentry`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sap_ret_nf`
-- Table structure for table `servidores_sincronismo`
--

DROP TABLE IF EXISTS `servidores_sincronismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidores_sincronismo` (
  `codssi` char(10) NOT NULL DEFAULT '',
  `descri_ssi` varchar(30) NOT NULL DEFAULT '',
  `ip` varchar(20) NOT NULL DEFAULT '',
  `banco` varchar(30) NOT NULL DEFAULT '',
  `usuario` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `porta` int(10) unsigned NOT NULL,
  PRIMARY KEY (`codssi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidores_sincronismo`
-- Table structure for table `status_evento_f`
--

DROP TABLE IF EXISTS `status_evento_f`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_evento_f` (
  `codst_f` char(1) NOT NULL,
  `descri_stf` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codst_f`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_evento_f`
-- Table structure for table `classes_ip`
--

DROP TABLE IF EXISTS `classes_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes_ip` (
  `codcla` varchar(10) NOT NULL,
  `codcon` int(4) unsigned NOT NULL,
  `codbkn` varchar(10) NOT NULL,
  `ip` varchar(18) NOT NULL,
  `classe` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codcla`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes_ip`
-- Table structure for table `servicos_extras_contas_rec`
--

DROP TABLE IF EXISTS `servicos_extras_contas_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_extras_contas_rec` (
  `codsercr` varchar(10) NOT NULL,
  `codsercliex` varchar(10) NOT NULL,
  `codserex` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `code_f` varchar(10) NOT NULL,
  PRIMARY KEY (`codsercr`),
  KEY `codsercliex` (`codsercliex`),
  KEY `codserex` (`codserex`),
  KEY `codcrec` (`codcrec`),
  KEY `code_f` (`code_f`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_extras_contas_rec`
-- Table structure for table `campos_extra`
--

DROP TABLE IF EXISTS `campos_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campos_extra` (
  `codcpx` varchar(10) NOT NULL DEFAULT '',
  `tabela` varchar(50) NOT NULL DEFAULT '',
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `tipo_campo` char(1) NOT NULL DEFAULT '',
  `tamanho` int(3) unsigned NOT NULL DEFAULT '0',
  `padrao` varchar(50) NOT NULL DEFAULT '',
  `soleitura` char(1) NOT NULL DEFAULT 'N',
  `nome_campo` varchar(50) NOT NULL,
  `consulta_sql` mediumtext NOT NULL,
  PRIMARY KEY (`codcpx`),
  KEY `tabela` (`tabela`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campos_extra`
-- Table structure for table `favoritos_navbar`
--

DROP TABLE IF EXISTS `favoritos_navbar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favoritos_navbar` (
  `codfavnavb` varchar(10) NOT NULL,
  `codopc` varchar(3) DEFAULT NULL,
  `codusu` varchar(2) DEFAULT NULL,
  `mc` varchar(100) DEFAULT NULL,
  `nome_fav` varchar(50) DEFAULT NULL,
  `n_tree` int(4) DEFAULT NULL,
  PRIMARY KEY (`codfavnavb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favoritos_navbar`
-- Table structure for table `tipo_cla_cli`
--

DROP TABLE IF EXISTS `tipo_cla_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cla_cli` (
  `codtclc` varchar(10) NOT NULL DEFAULT '',
  `tipo_clc` char(1) NOT NULL DEFAULT 'F',
  `descri_tclc` varchar(50) NOT NULL DEFAULT '',
  `porcentagem` float(10,2) NOT NULL DEFAULT '0.00',
  `aviso` char(1) NOT NULL DEFAULT 'N',
  `consulta_sql` mediumtext NOT NULL,
  `mensagem` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtclc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cla_cli`
-- Table structure for table `fistel`
--

DROP TABLE IF EXISTS `fistel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fistel` (
  `codfist` varchar(10) NOT NULL,
  `nro_fistel` varchar(20) NOT NULL,
  `IAU1` varchar(20) NOT NULL,
  PRIMARY KEY (`codfist`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fistel`
-- Table structure for table `validacoes_telefones`
--

DROP TABLE IF EXISTS `validacoes_telefones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `validacoes_telefones` (
  `codvtc` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `codlsu` varchar(10) NOT NULL,
  `fone` varchar(11) NOT NULL DEFAULT '',
  PRIMARY KEY (`codvtc`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codlsu` (`codlsu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `validacoes_telefones`
-- Table structure for table `campos`
--

DROP TABLE IF EXISTS `campos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campos` (
  `codcamp` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `nome_camp` varchar(30) NOT NULL,
  `visivel` char(1) NOT NULL DEFAULT 'S',
  `descricao` varchar(200) NOT NULL,
  `tipo` char(2) NOT NULL,
  `tamanho` int(3) unsigned NOT NULL,
  `componente` varchar(30) NOT NULL,
  `titulo` varchar(30) NOT NULL,
  `titulo_resumido` varchar(15) NOT NULL,
  `valor_default` varchar(30) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcamp`),
  KEY `codtab` (`codtab`),
  KEY `nome_camp` (`nome_camp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campos`
-- Table structure for table `tabelas_ligacoes`
--

DROP TABLE IF EXISTS `tabelas_ligacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabelas_ligacoes` (
  `codtablig` varchar(10) NOT NULL,
  `nome_tablig` varchar(100) NOT NULL DEFAULT '',
  `primeira_data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ultima_data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`codtablig`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelas_ligacoes`
-- Table structure for table `descontos`
--

DROP TABLE IF EXISTS `descontos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `descontos` (
  `coddes` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `codftm` varchar(10) NOT NULL,
  `codtdes` varchar(10) NOT NULL DEFAULT '01FATURM',
  `codprom` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `valor_des` float(10,2) NOT NULL DEFAULT '0.00',
  `motivo` text NOT NULL,
  `desc_retorno` char(1) NOT NULL DEFAULT 'N',
  `coddrng` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddes`),
  KEY `codcrec` (`codcrec`),
  KEY `codftm` (`codftm`),
  KEY `codtdes` (`codtdes`),
  KEY `codcta` (`codcta`),
  KEY `data` (`data`),
  KEY `codprom` (`codprom`),
  KEY `codctc` (`codctc`),
  KEY `coddrng` (`coddrng`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `descontos`
-- Table structure for table `recibos`
--

DROP TABLE IF EXISTS `recibos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recibos` (
  `numero_rec` int(11) unsigned NOT NULL DEFAULT '0',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `valor` float(10,2) NOT NULL DEFAULT '0.00',
  `historico` text NOT NULL,
  PRIMARY KEY (`numero_rec`),
  KEY `codcli` (`codcli`),
  KEY `data` (`data`),
  KEY `codmov` (`codmov`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recibos`
-- Table structure for table `franquia_sc_terminacao`
--

DROP TABLE IF EXISTS `franquia_sc_terminacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franquia_sc_terminacao` (
  `codfscter` varchar(10) NOT NULL,
  `codfscv` varchar(10) NOT NULL,
  `codtter` varchar(10) NOT NULL,
  PRIMARY KEY (`codfscter`),
  KEY `codfsv` (`codfscv`),
  KEY `codtter` (`codtter`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `franquia_sc_terminacao`
-- Table structure for table `canais_sc`
--

DROP TABLE IF EXISTS `canais_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `canais_sc` (
  `codcnlsc` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codcnl` varchar(10) NOT NULL,
  `dias_trial` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codcnlsc`),
  KEY `codsercli` (`codsercli`),
  KEY `codcnl` (`codcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canais_sc`
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `coditem` varchar(10) NOT NULL DEFAULT '',
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `nome_item` varchar(50) NOT NULL DEFAULT '',
  `preco` decimal(8,2) NOT NULL DEFAULT '0.00',
  `desconto` decimal(5,2) NOT NULL DEFAULT '0.00',
  `tipo_medida` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`coditem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
-- Table structure for table `prospect`
--

DROP TABLE IF EXISTS `prospect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prospect` (
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `codestp` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(6) unsigned NOT NULL DEFAULT '0',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcon_t` int(3) unsigned NOT NULL DEFAULT '0',
  `codtpros` varchar(10) NOT NULL,
  `codusu_conv` char(2) NOT NULL,
  `nome_pros` varchar(50) NOT NULL DEFAULT '',
  `nome_fan` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `referencia` varchar(50) NOT NULL,
  `sala` varchar(10) NOT NULL,
  `apto` varchar(10) NOT NULL,
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `cidade` varchar(11) NOT NULL DEFAULT '',
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  `ddd` char(3) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `tipo_condominio` char(1) NOT NULL DEFAULT 'V',
  `quant_unidades` int(3) unsigned NOT NULL DEFAULT '0',
  `tipo_prospect` char(1) NOT NULL DEFAULT '',
  `tipo_cliente` char(1) NOT NULL DEFAULT '',
  `data_nac` date NOT NULL DEFAULT '0000-00-00',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `cpf` varchar(14) NOT NULL DEFAULT '',
  `rg` varchar(11) NOT NULL DEFAULT '',
  `rg_emissor` varchar(10) NOT NULL,
  `icm` varchar(15) NOT NULL DEFAULT '',
  `doc_validado` char(1) NOT NULL DEFAULT 'N',
  `obs` text NOT NULL,
  PRIMARY KEY (`codpros`),
  KEY `codven` (`codven`),
  KEY `codestp` (`codestp`),
  KEY `codtpros` (`codtpros`),
  KEY `codcli` (`codcli`),
  KEY `codusu_conv` (`codusu_conv`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prospect`
-- Table structure for table `registros_bloquetos`
--

DROP TABLE IF EXISTS `registros_bloquetos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registros_bloquetos` (
  `codrblo` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `ordem` int(1) NOT NULL DEFAULT '0',
  `grupo` char(1) NOT NULL DEFAULT 'D',
  PRIMARY KEY (`codrblo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros_bloquetos`
-- Table structure for table `para_defa`
--

DROP TABLE IF EXISTS `para_defa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `para_defa` (
  `codpar` char(1) NOT NULL DEFAULT '',
  `nome` varchar(10) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `estado1` char(2) NOT NULL DEFAULT '',
  `estado2` char(3) NOT NULL DEFAULT '',
  `imagem` varchar(100) NOT NULL DEFAULT '',
  `ci` int(11) NOT NULL DEFAULT '0',
  `li` int(11) NOT NULL DEFAULT '0',
  `cor1` int(11) NOT NULL DEFAULT '0',
  `cor2` int(11) NOT NULL DEFAULT '0',
  `cor3` int(11) NOT NULL DEFAULT '0',
  `pasta_trabalho` varchar(100) NOT NULL DEFAULT '',
  `pasta_dados` varchar(100) NOT NULL DEFAULT '',
  `recurso` varchar(100) NOT NULL DEFAULT '',
  `quant_reg` int(11) NOT NULL DEFAULT '0',
  `remota` char(1) NOT NULL DEFAULT '',
  `dia_venc` varchar(10) NOT NULL DEFAULT '',
  `ultima_versao` date NOT NULL DEFAULT '0000-00-00',
  `dominio` varchar(50) NOT NULL DEFAULT '',
  `nro_ocorrencia` int(9) unsigned NOT NULL DEFAULT '0',
  `e_mail_teste` text NOT NULL,
  `ultima_nota_fiscal` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `para_defa`
-- Table structure for table `det_rela_cubo`
--

DROP TABLE IF EXISTS `det_rela_cubo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_rela_cubo` (
  `coddrc` varchar(10) NOT NULL,
  `codrcb` varchar(10) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `ordem_det` int(2) unsigned NOT NULL,
  `nome_campo` varchar(50) NOT NULL,
  `formula` varchar(100) NOT NULL,
  `tipo_formula` int(4) unsigned NOT NULL,
  `dimensao` char(1) NOT NULL,
  `tipo_campo` int(2) NOT NULL,
  `titulo` varchar(30) NOT NULL,
  `fonte` varchar(50) NOT NULL,
  `formato` varchar(30) NOT NULL,
  `SourceAggregator` int(1) unsigned NOT NULL,
  `Algorithm` int(1) unsigned NOT NULL,
  `escala` int(3) unsigned NOT NULL,
  `engatado` char(1) NOT NULL DEFAULT 'N',
  `oculto` char(1) NOT NULL DEFAULT 'N',
  `total` char(1) NOT NULL DEFAULT 'N',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`coddrc`),
  KEY `codrcb` (`codrcb`),
  KEY `ordem` (`ordem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_rela_cubo`
-- Table structure for table `imagens`
--

DROP TABLE IF EXISTS `imagens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imagens` (
  `codima` varchar(15) NOT NULL DEFAULT '',
  `nome_ima` varchar(200) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `image` text NOT NULL,
  PRIMARY KEY (`codima`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagens`
-- Table structure for table `testes`
--

DROP TABLE IF EXISTS `testes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testes` (
  `codtest` varchar(10) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `ver_central` char(1) NOT NULL DEFAULT 'N',
  `codusu` char(2) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora` varchar(5) NOT NULL DEFAULT '',
  `data_fim` datetime NOT NULL,
  `descri_test` text NOT NULL,
  PRIMARY KEY (`codtest`),
  KEY `codoco` (`codoco`),
  KEY `ver_central` (`ver_central`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testes`
-- Table structure for table `ip`
--

DROP TABLE IF EXISTS `ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ip` (
  `codip` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codintr` varchar(10) NOT NULL DEFAULT '',
  `codpar` varchar(10) NOT NULL,
  `codpool` varchar(10) NOT NULL,
  `codinte` varchar(10) NOT NULL,
  `codigo_externo` varchar(20) NOT NULL,
  `queue` varchar(10) NOT NULL,
  `nro_ip` varchar(15) NOT NULL DEFAULT '',
  `nro_ip_v6` varchar(39) NOT NULL,
  `clase_ipv6` int(6) NOT NULL,
  `nro_ipv6_sec` varchar(45) NOT NULL,
  `clase_ipv6_sec` int(3) unsigned NOT NULL,
  `clase` int(3) unsigned NOT NULL DEFAULT '0',
  `submask` varchar(15) NOT NULL DEFAULT '',
  `ip_secundario` varchar(15) NOT NULL,
  `clase_sec` int(3) unsigned NOT NULL,
  `vlan` char(30) NOT NULL,
  `dns_primario` varchar(15) NOT NULL DEFAULT '',
  `dns_secundario` varchar(15) NOT NULL DEFAULT '',
  `gateway` varchar(15) NOT NULL DEFAULT '',
  `macadress1` varchar(17) NOT NULL DEFAULT '',
  `macadress2` varchar(17) NOT NULL DEFAULT '',
  `macadress3` varchar(17) NOT NULL DEFAULT '',
  `macadress4` varchar(17) NOT NULL DEFAULT '',
  `macadress5` varchar(17) NOT NULL DEFAULT '',
  `upload` int(6) unsigned NOT NULL DEFAULT '0',
  `codvel` varchar(10) NOT NULL,
  `max_limit_up` int(10) unsigned DEFAULT NULL,
  `burst_limit_up` int(10) unsigned DEFAULT NULL,
  `burst_threshold_up` int(10) unsigned DEFAULT NULL,
  `burst_time_up` int(10) unsigned DEFAULT NULL,
  `download` int(6) unsigned NOT NULL DEFAULT '0',
  `max_limit_dw` int(10) unsigned DEFAULT NULL,
  `burst_limit_dw` int(10) unsigned DEFAULT NULL,
  `burst_threshold_dw` int(10) unsigned DEFAULT NULL,
  `burst_time_dw` int(10) unsigned DEFAULT NULL,
  `upload_n` int(6) unsigned NOT NULL DEFAULT '0',
  `download_n` int(6) NOT NULL DEFAULT '0',
  `nro_regra_fw` int(6) unsigned NOT NULL DEFAULT '0',
  `proxy` char(1) NOT NULL DEFAULT 'S',
  `rede` char(1) NOT NULL DEFAULT 'N',
  `dhcp` char(1) NOT NULL DEFAULT 'N',
  `mac_e_login` char(1) NOT NULL DEFAULT 'N',
  `ip_publico` char(1) NOT NULL DEFAULT 'N',
  `hotspot` char(1) NOT NULL DEFAULT 'N',
  `cobrar_ip` char(1) NOT NULL DEFAULT 'N',
  `wpa2` varchar(63) NOT NULL,
  `mensagem_ip` varchar(100) NOT NULL DEFAULT '',
  `ip_framed_route` varchar(15) NOT NULL,
  `clase_framed_route` int(3) unsigned NOT NULL,
  `obs` text NOT NULL,
  PRIMARY KEY (`codip`),
  KEY `codintr` (`codintr`),
  KEY `codsercli` (`codsercli`),
  KEY `codpool` (`codpool`),
  KEY `codinte` (`codinte`),
  KEY `codigo_externo` (`codigo_externo`),
  KEY `codpar` (`codpar`),
  KEY `hotspot` (`hotspot`),
  KEY `macadress1` (`macadress1`),
  KEY `macadress2` (`macadress2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip`
-- Table structure for table `conf_boletos`
--

DROP TABLE IF EXISTS `conf_boletos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_boletos` (
  `codcfb` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codu_f` char(3) NOT NULL DEFAULT '',
  `codcart` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codseg` varchar(10) NOT NULL DEFAULT 'CARNES',
  `codservp` varchar(10) NOT NULL,
  `liberado_imp` char(1) NOT NULL DEFAULT 'N',
  `liberado_rem` char(1) NOT NULL DEFAULT 'N',
  `liberado_ret` char(1) NOT NULL DEFAULT 'N',
  `inativa` char(1) NOT NULL DEFAULT 'N',
  `gera_nosso_nro` char(1) NOT NULL DEFAULT 'S',
  `cobranca_registrada` char(1) NOT NULL DEFAULT 'N',
  `imp_boleto_impresso` char(1) NOT NULL DEFAULT 'N',
  `permite_cielo` char(1) NOT NULL DEFAULT 'N',
  `permite_pg_cartao` char(1) NOT NULL DEFAULT 'N',
  `nome_cedente` varchar(100) NOT NULL DEFAULT '',
  `nro_age` varchar(10) NOT NULL DEFAULT '',
  `nro_cta` varchar(15) NOT NULL DEFAULT '',
  `codconv` varchar(20) NOT NULL DEFAULT '',
  `nome_arquivo_rem` varchar(40) NOT NULL,
  `i_nosso_nro` varchar(10) NOT NULL DEFAULT '',
  `f_nosso_nro` varchar(10) NOT NULL DEFAULT '',
  `arq_logo` varchar(100) NOT NULL DEFAULT '',
  `codlayout` varchar(11) NOT NULL DEFAULT '',
  `layout_imp_l` varchar(10) NOT NULL DEFAULT '',
  `tipo_boleto` varchar(10) NOT NULL DEFAULT 'FEBRABAN',
  `ret_nro_doc` char(1) NOT NULL DEFAULT '',
  `ret_processa_bol` char(1) NOT NULL DEFAULT '',
  `ret_cobra_multa` varchar(1) NOT NULL DEFAULT 'N',
  `cod_barra_remesa` char(1) NOT NULL DEFAULT 'N',
  `ignorar_final_arq` char(1) NOT NULL DEFAULT 'N',
  `ignorar_espacos_branco` char(1) NOT NULL DEFAULT 'N',
  `codsad` varchar(10) NOT NULL,
  `perc_atrazo` float(6,3) NOT NULL DEFAULT '0.000',
  `perc_multa` float(6,3) NOT NULL DEFAULT '0.000',
  `multa_valor_fixo` char(1) NOT NULL DEFAULT 'N',
  `juros_evento_fat` char(1) NOT NULL DEFAULT 'N',
  `valor_minimo_eve_fat` decimal(6,2) NOT NULL,
  `perc_desconto` float(6,3) NOT NULL DEFAULT '0.000',
  `dias_desconto` int(2) unsigned NOT NULL DEFAULT '0',
  `dias_limite` int(3) unsigned NOT NULL DEFAULT '60',
  `valor_boleto` float(6,3) NOT NULL DEFAULT '0.000',
  `codcta` varchar(11) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codcbe` varchar(10) NOT NULL DEFAULT '',
  `inst_demo` mediumtext NOT NULL,
  `inst_caixa` mediumtext NOT NULL,
  `licencia` mediumtext NOT NULL,
  `script_rem` mediumtext NOT NULL,
  `b_nosso_nro` varchar(100) NOT NULL DEFAULT '',
  `formato_nosso_n` varchar(100) NOT NULL DEFAULT '',
  `pos_nro_arq` varchar(30) NOT NULL DEFAULT '',
  `formato_cartao` varchar(20) NOT NULL DEFAULT '',
  `padrao_razao` varchar(100) NOT NULL DEFAULT '',
  `cnab` char(3) DEFAULT '',
  `boleto_browser` char(1) NOT NULL DEFAULT 'N',
  `codcob_pix` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcfb`),
  KEY `codcob` (`codcob`),
  KEY `codcart` (`codcart`),
  KEY `codseg` (`codseg`),
  KEY `inativa` (`inativa`),
  KEY `codservp` (`codservp`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_boletos`
-- Table structure for table `contas_rec_cob`
--

DROP TABLE IF EXISTS `contas_rec_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_rec_cob` (
  `codcrc` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `codscc` varchar(10) NOT NULL,
  `codfat` varchar(10) NOT NULL,
  `data_ven` date NOT NULL,
  `saldo` float(10,2) NOT NULL,
  PRIMARY KEY (`codcrc`),
  KEY `codcrec` (`codcrec`),
  KEY `codscc` (`codscc`),
  KEY `codfat` (`codfat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_rec_cob`
-- Table structure for table `syn_contatos_cliente`
--

DROP TABLE IF EXISTS `syn_contatos_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syn_contatos_cliente` (
  `codsco_cl` bigint(20) NOT NULL AUTO_INCREMENT,
  `codcli` varchar(10) NOT NULL DEFAULT '',
  `codco_cl_p` varchar(10) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  `data_ua` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sincronizado` char(1) NOT NULL DEFAULT 'N',
  `data_sincronismo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `resp_sincronismo` varchar(20) NOT NULL DEFAULT '',
  `data_erro` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tentativa` int(11) NOT NULL DEFAULT '0',
  `log_erro` mediumtext,
  `campos` mediumtext,
  PRIMARY KEY (`codsco_cl`),
  KEY `sincronizado` (`sincronizado`),
  KEY `acao` (`acao`),
  KEY `data_sincronismo` (`data_sincronismo`),
  KEY `codcli` (`codcli`),
  KEY `codco_cl_p` (`codco_cl_p`),
  KEY `data_ua` (`data_ua`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syn_contatos_cliente`
-- Table structure for table `emails_tarefas_m`
--

DROP TABLE IF EXISTS `emails_tarefas_m`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emails_tarefas_m` (
  `codetm` varchar(10) NOT NULL DEFAULT '',
  `codtarm` varchar(10) NOT NULL DEFAULT '',
  `codcbe` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codetm`),
  KEY `codtarm` (`codtarm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_tarefas_m`
-- Table structure for table `modulos_int_sis`
--

DROP TABLE IF EXISTS `modulos_int_sis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modulos_int_sis` (
  `codmis` varchar(10) NOT NULL,
  `codist` varchar(10) NOT NULL,
  `descri_mis` varchar(30) NOT NULL,
  PRIMARY KEY (`codmis`),
  KEY `codist` (`codist`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modulos_int_sis`
-- Table structure for table `clientes_codigos_externos`
--

DROP TABLE IF EXISTS `clientes_codigos_externos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes_codigos_externos` (
  `codcce` varchar(10) NOT NULL,
  `codcli` int(10) unsigned NOT NULL,
  `codrad` varchar(10) NOT NULL,
  `codexterno` varchar(20) NOT NULL,
  PRIMARY KEY (`codcce`),
  KEY `codcli` (`codcli`),
  KEY `codrad` (`codrad`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_codigos_externos`
-- Table structure for table `formas_pagamento_for`
--

DROP TABLE IF EXISTS `formas_pagamento_for`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `formas_pagamento_for` (
  `codfpf` varchar(10) NOT NULL,
  `codfor` varchar(10) NOT NULL,
  `codtpf` varchar(10) NOT NULL,
  `codban` varchar(10) NOT NULL,
  `codccd` varchar(10) NOT NULL,
  `nro_ban` char(3) NOT NULL,
  `agencia` varchar(6) NOT NULL,
  `dig_agencia` varchar(1) NOT NULL,
  `conta` varchar(10) NOT NULL,
  `dig_conta` varchar(1) NOT NULL,
  `cpf_cnpj` varchar(18) NOT NULL,
  PRIMARY KEY (`codfpf`),
  KEY `codfor` (`codfor`),
  KEY `codtpf` (`codtpf`),
  KEY `codccd` (`codccd`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formas_pagamento_for`
-- Table structure for table `contas_rec_m`
--

DROP TABLE IF EXISTS `contas_rec_m`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_rec_m` (
  `codcrecm` varchar(20) NOT NULL,
  `codcrec` varchar(10) DEFAULT NULL,
  `codmoeda` varchar(10) DEFAULT NULL,
  `valor` float(14,2) DEFAULT NULL,
  PRIMARY KEY (`codcrecm`),
  KEY `codcrec` (`codcrec`),
  KEY `codmoeda` (`codmoeda`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_rec_m`
-- Table structure for table `detalhe_recibo`
--

DROP TABLE IF EXISTS `detalhe_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_recibo` (
  `coddrec` varchar(10) NOT NULL DEFAULT '',
  `numero_rec` int(11) unsigned NOT NULL DEFAULT '0',
  `codmov` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT 'E',
  `numero_che` int(8) unsigned NOT NULL DEFAULT '0',
  `nro_ban` char(3) NOT NULL DEFAULT '',
  `agencia` varchar(6) NOT NULL,
  `conta_cte` varchar(10) NOT NULL,
  `titular` varchar(70) NOT NULL,
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `status` char(1) NOT NULL DEFAULT 'C',
  `numero_cartao` varchar(16) NOT NULL,
  PRIMARY KEY (`coddrec`),
  KEY `numero_rec` (`numero_rec`),
  KEY `data_ven` (`data_ven`),
  KEY `codmov` (`codmov`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_recibo`
-- Table structure for table `servicos_imp_apagado`
--

DROP TABLE IF EXISTS `servicos_imp_apagado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_imp_apagado` (
  `codsimp` char(10) NOT NULL DEFAULT '',
  `codser` char(10) NOT NULL DEFAULT '',
  `codemp` char(10) NOT NULL DEFAULT '',
  `codtnf` char(10) NOT NULL DEFAULT '',
  `codcob` char(10) NOT NULL DEFAULT '',
  `codcta` char(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL DEFAULT '',
  `codtser` char(10) NOT NULL DEFAULT '',
  `codcif` char(4) NOT NULL DEFAULT '',
  `descri_simp` varchar(70) NOT NULL DEFAULT '',
  `descri_nf` varchar(40) NOT NULL DEFAULT '',
  `valor` decimal(10,3) NOT NULL DEFAULT '0.000',
  `icms` decimal(5,2) NOT NULL DEFAULT '0.00',
  `iss` decimal(5,2) NOT NULL DEFAULT '0.00',
  `fust` decimal(5,2) NOT NULL DEFAULT '0.00',
  `funtel` decimal(5,2) NOT NULL DEFAULT '0.00',
  `pis` decimal(5,2) NOT NULL DEFAULT '0.00',
  `cofins` decimal(5,2) NOT NULL DEFAULT '0.00',
  `iva` decimal(5,2) NOT NULL DEFAULT '0.00',
  `codigo_fiscal` char(6) NOT NULL DEFAULT '',
  `retem_imposto` char(1) NOT NULL DEFAULT '',
  `itemsgroupcode` char(3) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codsimp`),
  KEY `codser` (`codser`),
  KEY `codemp` (`codemp`),
  KEY `codtnf` (`codtnf`),
  KEY `codcob` (`codcob`),
  KEY `codcta` (`codcta`),
  KEY `codtser` (`codtser`),
  KEY `codcif` (`codcif`),
  KEY `codctc` (`codctc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=PlanServiceComposition|Desc=|Grupo=Plan';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_imp_apagado`
-- Table structure for table `comissoes_servico`
--

DROP TABLE IF EXISTS `comissoes_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comissoes_servico` (
  `codcser` varchar(10) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `porcentagem` float(6,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codcser`),
  KEY `codven` (`codven`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissoes_servico`
-- Table structure for table `movimentos_pat_apagar`
--

DROP TABLE IF EXISTS `movimentos_pat_apagar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentos_pat_apagar` (
  `codmvp` varchar(10) NOT NULL DEFAULT '',
  `codpat` varchar(10) NOT NULL DEFAULT '',
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codaqs` varchar(10) NOT NULL DEFAULT '',
  `codvpat` char(10) NOT NULL DEFAULT '',
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(4) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codords` char(10) NOT NULL DEFAULT '',
  `codprod` char(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL DEFAULT '',
  `codcfop` char(10) NOT NULL DEFAULT '',
  `quantidade` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tipo_mov` char(1) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atual` char(1) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  `vl_venda` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codmvp`),
  KEY `codpat` (`codpat`),
  KEY `codlmp` (`codlmp`),
  KEY `codcon` (`codcon`),
  KEY `codsercli` (`codsercli`),
  KEY `codadq` (`codaqs`),
  KEY `codfor` (`codfor`),
  KEY `codcmp` (`codcmp`),
  KEY `atual` (`atual`),
  KEY `codords` (`codords`),
  KEY `codprod` (`codprod`),
  KEY `codcfop` (`codcfop`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos_pat_apagar`
-- Table structure for table `servicos_cli_voz_redir`
--

DROP TABLE IF EXISTS `servicos_cli_voz_redir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_voz_redir` (
  `codscvrd` varchar(10) NOT NULL,
  `codndis` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `valor_sigame` float(10,4) NOT NULL,
  `parcelas` int(2) NOT NULL,
  `numero_sigame` varchar(100) NOT NULL,
  PRIMARY KEY (`codscvrd`),
  KEY `codndis` (`codndis`),
  KEY `codco_cl` (`codco_cl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_voz_redir`
-- Table structure for table `servicos_cli_mod_contratos`
--

DROP TABLE IF EXISTS `servicos_cli_mod_contratos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_mod_contratos` (
  `codscmc` char(10) NOT NULL,
  `codsercli` char(10) NOT NULL,
  `codmodc` char(10) NOT NULL,
  `validade` int(3) unsigned NOT NULL,
  `numero_con` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codscmc`),
  KEY `codsercli` (`codsercli`),
  KEY `codmodc` (`codmodc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_mod_contratos`
-- Table structure for table `conf_visual`
--

DROP TABLE IF EXISTS `conf_visual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_visual` (
  `codconvs` varchar(10) NOT NULL,
  `padrao_elite` char(1) NOT NULL DEFAULT 'S',
  `nome` varchar(50) NOT NULL DEFAULT '',
  `splash_screen_web` varchar(10) NOT NULL,
  `splash_screen_desk` varchar(10) NOT NULL,
  `logo_web` varchar(10) NOT NULL,
  `logo_desk` varchar(10) NOT NULL,
  `icone_web` varchar(10) NOT NULL,
  `icone_desk` varchar(10) NOT NULL,
  PRIMARY KEY (`codconvs`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_visual`
-- Table structure for table `condicao_regra`
--

DROP TABLE IF EXISTS `condicao_regra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condicao_regra` (
  `codcondr` char(10) NOT NULL,
  `descri_cond_regra` varchar(50) NOT NULL DEFAULT '',
  `qtd_parcelas_ini` int(11) NOT NULL DEFAULT '0',
  `qtd_parcelas_fim` int(11) NOT NULL DEFAULT '0',
  `porcentagem_desconto` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_desconto` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tipo_cob` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcondr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condicao_regra`
-- Table structure for table `cargos_inf`
--

DROP TABLE IF EXISTS `cargos_inf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargos_inf` (
  `codcarinf` varchar(10) NOT NULL,
  `codcar` varchar(10) DEFAULT NULL,
  `codinf` varchar(10) DEFAULT NULL,
  `p_exportar` char(1) DEFAULT NULL,
  PRIMARY KEY (`codcarinf`),
  KEY `codcar` (`codcar`),
  KEY `codinf` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos_inf`
-- Table structure for table `integracao_prod`
--

DROP TABLE IF EXISTS `integracao_prod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `integracao_prod` (
  `codiprod` char(10) NOT NULL,
  `codprod` char(10) NOT NULL,
  `tipo_iprod` char(2) NOT NULL,
  `codigo_interno` varchar(20) NOT NULL,
  `codtonu` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codiprod`),
  KEY `codprod` (`codprod`),
  KEY `interno_IDX` (`codigo_interno`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integracao_prod`
-- Table structure for table `troca_etapa_funil`
--

DROP TABLE IF EXISTS `troca_etapa_funil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `troca_etapa_funil` (
  `codtef` int(11) NOT NULL AUTO_INCREMENT,
  `codpint` char(10) NOT NULL DEFAULT '',
  `id_etapa_old` int(11) NOT NULL DEFAULT '0',
  `id_etapa_new` int(11) NOT NULL DEFAULT '0',
  `data_hora` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtef`),
  KEY `codpint` (`codpint`),
  KEY `id_etapa_old` (`id_etapa_old`),
  KEY `id_etapa_new` (`id_etapa_new`),
  KEY `data_hora` (`data_hora`),
  KEY `codven` (`codusu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `troca_etapa_funil`
-- Table structure for table `usu_arq`
--

DROP TABLE IF EXISTS `usu_arq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_arq` (
  `coduarq` varchar(10) NOT NULL DEFAULT '',
  `codarq` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`coduarq`),
  KEY `codarq` (`codarq`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_arq`
-- Table structure for table `det_previsoes_cta`
--

DROP TABLE IF EXISTS `det_previsoes_cta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_previsoes_cta` (
  `coddpct` varchar(10) NOT NULL,
  `codprev` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `valor` float(10,2) NOT NULL,
  `porcentagem` float(8,3) NOT NULL,
  PRIMARY KEY (`coddpct`),
  KEY `codprev` (`codprev`),
  KEY `codcta` (`codcta`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_previsoes_cta`
-- Table structure for table `parametros`
--

DROP TABLE IF EXISTS `parametros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parametros` (
  `codpar` char(1) NOT NULL DEFAULT '',
  `nome` varchar(10) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `estado1` char(2) NOT NULL DEFAULT '',
  `estado2` char(3) NOT NULL DEFAULT '',
  `imagem` varchar(100) NOT NULL DEFAULT '',
  `ci` int(11) NOT NULL DEFAULT '0',
  `li` int(11) NOT NULL DEFAULT '0',
  `cor1` int(11) NOT NULL DEFAULT '0',
  `cor2` int(11) NOT NULL DEFAULT '0',
  `cor3` int(11) NOT NULL DEFAULT '0',
  `pasta_trabalho` varchar(100) NOT NULL DEFAULT '',
  `pasta_dados` varchar(100) NOT NULL DEFAULT '',
  `recurso` varchar(100) NOT NULL DEFAULT '',
  `quant_reg` int(11) NOT NULL DEFAULT '0',
  `remota` char(1) NOT NULL DEFAULT '',
  `dia_venc` varchar(10) NOT NULL DEFAULT '',
  `ultima_versao` date NOT NULL DEFAULT '0000-00-00',
  `dominio` varchar(20) NOT NULL DEFAULT '',
  `nro_ocorrencia` int(9) unsigned NOT NULL DEFAULT '0',
  `e_mail_teste` text NOT NULL,
  PRIMARY KEY (`codpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros`
-- Table structure for table `aceite_contrato`
--

DROP TABLE IF EXISTS `aceite_contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aceite_contrato` (
  `codace` char(10) NOT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status_ace` char(1) NOT NULL DEFAULT 'N',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `codmodc` char(10) NOT NULL DEFAULT '',
  `codsercli` char(10) NOT NULL,
  `codscmc` char(10) NOT NULL DEFAULT '',
  `codco_cl` char(10) NOT NULL DEFAULT '',
  `obs_rejeicao` varchar(100) NOT NULL DEFAULT '',
  `chave_autenticacao` varchar(128) DEFAULT '',
  `codfot_original` char(10) DEFAULT '',
  `codfot_assinado` char(10) DEFAULT '',
  `descri_ser` varchar(100) DEFAULT NULL,
  `descri_modc` varchar(100) DEFAULT NULL,
  `tipo_aceite` char(1) NOT NULL DEFAULT '' COMMENT '||Utilizar E - Aceite por Email, S - Aceite por SMS',
  `codeem` char(10) NOT NULL DEFAULT '',
  `codesms` char(10) NOT NULL DEFAULT '',
  `hash_original` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`codace`),
  KEY `codsercli` (`codsercli`),
  KEY `data_hora` (`data_hora`),
  KEY `status_ace` (`status_ace`),
  KEY `codco_cl` (`codco_cl`),
  KEY `tipo_aceite` (`tipo_aceite`),
  KEY `codeem` (`codeem`),
  KEY `codesms` (`codesms`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aceite_contrato`
-- Table structure for table `mensagem`
--

DROP TABLE IF EXISTS `mensagem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mensagem` (
  `codmsg` char(10) NOT NULL,
  `assunto` varchar(100) NOT NULL,
  `mensagem` longtext NOT NULL,
  `prioridade` char(1) NOT NULL DEFAULT 'M',
  `data_lan` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `codaleoco` char(10) NOT NULL,
  PRIMARY KEY (`codmsg`),
  KEY `assunto` (`assunto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensagem`
-- Table structure for table `servicos_voz`
--

DROP TABLE IF EXISTS `servicos_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_voz` (
  `codsvoz` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `codvcre` varchar(10) NOT NULL,
  `quant_terminais` int(2) unsigned NOT NULL DEFAULT '0',
  `digitos_terminal` int(2) unsigned NOT NULL DEFAULT '0',
  `valor_adicional` float(10,4) NOT NULL DEFAULT '0.0000',
  `tipo_voz` char(1) NOT NULL DEFAULT 'U',
  `virtual_n` char(1) NOT NULL DEFAULT 'N',
  `batch_id` varchar(20) NOT NULL,
  `stfc` char(1) NOT NULL DEFAULT 'N',
  `simultaneas` int(3) unsigned NOT NULL,
  `credito_automatico` char(1) NOT NULL,
  `chamada_acobrar` char(1) NOT NULL DEFAULT 'S',
  `franquia_proporcional` char(1) NOT NULL,
  `mvno` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codsvoz`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_voz`
-- Table structure for table `crp_grupo`
--

DROP TABLE IF EXISTS `crp_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crp_grupo` (
  `codcrpg` varchar(10) NOT NULL,
  `nome` varchar(30) DEFAULT NULL,
  `imagem` varchar(50) DEFAULT NULL,
  `imagem_fundo` varchar(80) DEFAULT NULL,
  `visivel` varchar(1) DEFAULT NULL,
  `ordem` tinyint(4) DEFAULT NULL,
  `codcrph` varchar(10) DEFAULT NULL,
  `colunas` int(4) DEFAULT NULL,
  PRIMARY KEY (`codcrpg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crp_grupo`
-- Table structure for table `syn_det_mov_bancario`
--

DROP TABLE IF EXISTS `syn_det_mov_bancario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syn_det_mov_bancario` (
  `codmov` char(10) NOT NULL DEFAULT '',
  `codcli` int(11) NOT NULL DEFAULT '0',
  `valor_total` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_rec` decimal(10,2) NOT NULL DEFAULT '0.00',
  `juros_rec` decimal(10,2) NOT NULL DEFAULT '0.00',
  `desconto_rec` decimal(10,2) NOT NULL DEFAULT '0.00',
  `data_lan` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `codmov` (`codmov`),
  KEY `codcli` (`codcli`),
  KEY `codmov_codcli` (`codmov`,`codcli`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syn_det_mov_bancario`
-- Table structure for table `faturas_pix`
--

DROP TABLE IF EXISTS `faturas_pix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturas_pix` (
  `codfatpix` int(11) NOT NULL AUTO_INCREMENT,
  `status_pix` char(10) NOT NULL DEFAULT '',
  `codfat` char(10) NOT NULL DEFAULT '',
  `codcob` char(10) NOT NULL DEFAULT '',
  `location` varchar(100) DEFAULT NULL COMMENT '||-',
  `data_criacao` datetime DEFAULT '0000-00-00 00:00:00',
  `data_expiracao` datetime DEFAULT '0000-00-00 00:00:00',
  `calendario_criacao` datetime DEFAULT NULL,
  `data_pg_banco` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `calendario_expiracao` int(11) DEFAULT NULL,
  `tix` varchar(50) DEFAULT NULL,
  `textoImagemQRcode` mediumtext,
  `valor_pix` decimal(10,2) NOT NULL DEFAULT '0.00',
  `juros_pix` decimal(10,2) NOT NULL DEFAULT '0.00',
  `desconto_pix` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codfatpix`),
  UNIQUE KEY `codfatpix` (`codfatpix`),
  KEY `codfat` (`codfat`),
  KEY `tix` (`tix`),
  KEY `data_criacao` (`data_criacao`),
  KEY `data_expiracao` (`data_expiracao`),
  KEY `data_pg_banco` (`data_pg_banco`),
  KEY `codcob` (`codcob`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturas_pix`
-- Table structure for table `nro_bancos`
--

DROP TABLE IF EXISTS `nro_bancos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nro_bancos` (
  `nro_ban` char(3) NOT NULL DEFAULT '',
  `nome_banco` varchar(50) NOT NULL DEFAULT '',
  `nome_api` varchar(50) NOT NULL DEFAULT '',
  `id_pais` int(11) NOT NULL DEFAULT '28',
  PRIMARY KEY (`nro_ban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nro_bancos`
-- Table structure for table `protocolo_cancel`
--

DROP TABLE IF EXISTS `protocolo_cancel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `protocolo_cancel` (
  `codpcan` int(6) unsigned NOT NULL DEFAULT '0',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `codcan` varchar(10) NOT NULL DEFAULT '',
  `processado` char(1) NOT NULL DEFAULT 'N',
  `html` mediumtext NOT NULL,
  `script_t` mediumtext NOT NULL,
  `script` mediumtext NOT NULL,
  PRIMARY KEY (`codpcan`),
  KEY `codcrec` (`codcrec`),
  KEY `processado` (`processado`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocolo_cancel`
-- Table structure for table `macros_documentos`
--

DROP TABLE IF EXISTS `macros_documentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `macros_documentos` (
  `codmdc` varchar(10) NOT NULL,
  `nome_mdc` varchar(50) NOT NULL,
  `codigo_mdc` varchar(50) NOT NULL,
  `macro_mdc` varchar(30) NOT NULL,
  PRIMARY KEY (`codmdc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `macros_documentos`
-- Table structure for table `status_comp`
--

DROP TABLE IF EXISTS `status_comp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_comp` (
  `codscom` char(1) NOT NULL DEFAULT '',
  `descri_scom` varchar(30) NOT NULL DEFAULT '',
  `orden` int(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codscom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_comp`
-- Table structure for table `automacao`
--

DROP TABLE IF EXISTS `automacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `automacao` (
  `codauto` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `login` varchar(50) NOT NULL,
  `senha` varchar(50) NOT NULL,
  `serial_number` varchar(30) NOT NULL,
  PRIMARY KEY (`codauto`),
  KEY `codsercli` (`codsercli`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codpat` (`codpat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `automacao`
-- Table structure for table `geradoras`
--

DROP TABLE IF EXISTS `geradoras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `geradoras` (
  `codgcnl` varchar(10) NOT NULL,
  `descri_gcnl` varchar(50) NOT NULL,
  PRIMARY KEY (`codgcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `geradoras`
-- Table structure for table `base_conhecimento`
--

DROP TABLE IF EXISTS `base_conhecimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_conhecimento` (
  `codbacon` varchar(10) NOT NULL,
  `codoco` varchar(10) NOT NULL,
  `codusu` varchar(2) NOT NULL,
  `codtbacon` varchar(10) NOT NULL,
  `codcli` int(6) NOT NULL,
  `data` datetime NOT NULL,
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `descri_bacon` mediumtext NOT NULL,
  PRIMARY KEY (`codbacon`),
  KEY `codoco` (`codoco`),
  KEY `codtbacon` (`codtbacon`),
  KEY `codcli` (`codcli`),
  KEY `titulo` (`titulo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_conhecimento`
-- Table structure for table `interfaces_sistema`
--

DROP TABLE IF EXISTS `interfaces_sistema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaces_sistema` (
  `codist` varchar(10) NOT NULL,
  `codidm` varchar(10) NOT NULL,
  `descri_ist` varchar(30) NOT NULL,
  PRIMARY KEY (`codist`),
  KEY `codidm` (`codidm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interfaces_sistema`
-- Table structure for table `ocorrencias_sms`
--

DROP TABLE IF EXISTS `ocorrencias_sms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocorrencias_sms` (
  `codocos` varchar(30) NOT NULL DEFAULT '',
  `codesms` varchar(30) NOT NULL,
  `codoco` varchar(30) NOT NULL,
  PRIMARY KEY (`codocos`),
  KEY `codesms` (`codesms`),
  KEY `codoco` (`codoco`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocorrencias_sms`
-- Table structure for table `backbone`
--

DROP TABLE IF EXISTS `backbone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backbone` (
  `codbkn` varchar(10) NOT NULL,
  `codope` varchar(10) NOT NULL,
  `megas` int(4) unsigned NOT NULL,
  PRIMARY KEY (`codbkn`),
  UNIQUE KEY `codbkn` (`codbkn`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backbone`
-- Table structure for table `maparede_equipamentos`
--

DROP TABLE IF EXISTS `maparede_equipamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maparede_equipamentos` (
  `codmpeq` varchar(20) NOT NULL DEFAULT '',
  `codmpcon` varchar(20) NOT NULL DEFAULT '',
  `codrad` char(10) DEFAULT '',
  `descri_geoeq` varchar(120) NOT NULL DEFAULT '',
  `integrator` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codmpeq`),
  KEY `codgeocon` (`codmpcon`),
  KEY `codrad` (`codrad`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maparede_equipamentos`
-- Table structure for table `informacoes`
--

DROP TABLE IF EXISTS `informacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `informacoes` (
  `codinf` varchar(10) NOT NULL DEFAULT '',
  `codtab` varchar(10) NOT NULL,
  `codgrd` varchar(10) NOT NULL,
  `menu` char(1) NOT NULL DEFAULT '',
  `nome_inf` varchar(50) NOT NULL DEFAULT '',
  `formulario` varchar(30) NOT NULL DEFAULT '',
  `origem` char(1) NOT NULL DEFAULT '',
  `destino` char(2) NOT NULL DEFAULT '',
  `exportar` char(1) NOT NULL DEFAULT 'S',
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `limite_dias_datas` int(6) unsigned NOT NULL DEFAULT '0',
  `codservp` varchar(10) NOT NULL,
  `mapa` char(1) NOT NULL DEFAULT 'N',
  `permite_mala_direta` char(1) NOT NULL DEFAULT 'N',
  `alteracao` char(1) NOT NULL DEFAULT 'N',
  `consulta_sql` text NOT NULL,
  `script_pos` mediumtext NOT NULL,
  `script_ant` mediumtext NOT NULL,
  `versao` char(10) NOT NULL,
  `data_alteracao` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '||-',
  `documentacao` text NOT NULL,
  PRIMARY KEY (`codinf`),
  KEY `codtab` (`codtab`),
  KEY `codgrd` (`codgrd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informacoes`
-- Table structure for table `formula_comissao`
--

DROP TABLE IF EXISTS `formula_comissao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `formula_comissao` (
  `codfcs` varchar(10) NOT NULL,
  `descri_fcs` varchar(50) NOT NULL,
  `exe_sql` char(1) NOT NULL DEFAULT 'N',
  `porcentagem_padrao` float(6,3) NOT NULL,
  `formula_fcs` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codfcs`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formula_comissao`
-- Table structure for table `opcoes_grupo`
--

DROP TABLE IF EXISTS `opcoes_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes_grupo` (
  `codgrp` varchar(10) NOT NULL,
  `grupo` varchar(50) DEFAULT NULL,
  `codima` varchar(15) DEFAULT NULL,
  `hint` varchar(15) DEFAULT NULL,
  `menu` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`codgrp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes_grupo`
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresas` (
  `codemp` char(10) NOT NULL DEFAULT '',
  `codscp` char(10) NOT NULL DEFAULT '',
  `codfist` char(10) NOT NULL DEFAULT '',
  `codima` varchar(15) NOT NULL DEFAULT '',
  `codrela_reci` char(10) NOT NULL DEFAULT '',
  `codlmp` char(10) NOT NULL DEFAULT '',
  `codcfop` char(10) NOT NULL DEFAULT '',
  `nome_emp` varchar(100) NOT NULL DEFAULT '',
  `nome_fan` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(20) NOT NULL DEFAULT '',
  `cep` char(9) NOT NULL DEFAULT '',
  `cidade` char(8) NOT NULL DEFAULT '',
  `ddd` char(3) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL,
  `fax` int(8) unsigned NOT NULL,
  `celular` varchar(13) NOT NULL DEFAULT '',
  `nextel` varchar(13) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `icm` varchar(15) NOT NULL DEFAULT '',
  `ic_mun` varchar(15) NOT NULL DEFAULT '',
  `nome_resp` varchar(50) NOT NULL DEFAULT '',
  `cpf_resp` varchar(14) NOT NULL DEFAULT '',
  `rg_resp` varchar(20) NOT NULL DEFAULT '',
  `codcar_resp` char(10) NOT NULL DEFAULT '',
  `principal` char(1) NOT NULL DEFAULT 'S',
  `indicador_icm` char(10) NOT NULL DEFAULT '',
  `crt` int(3) unsigned NOT NULL DEFAULT '1',
  `ambiete_nfe55p` int(1) unsigned NOT NULL DEFAULT '2',
  `licenca_flexdocs_nfe` varchar(255) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  `certificado_digital` mediumtext NOT NULL,
  `modfrete` char(1) NOT NULL DEFAULT '',
  `usar_composicao` char(1) NOT NULL DEFAULT '',
  `logo_emp` mediumtext NOT NULL,
  `codigo_externo` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codemp`),
  KEY `codscp` (`codscp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
-- Table structure for table `tipo_locais_mp`
--

DROP TABLE IF EXISTS `tipo_locais_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_locais_mp` (
  `codtlmp` varchar(10) NOT NULL,
  `descri_tlmp` varchar(50) NOT NULL,
  PRIMARY KEY (`codtlmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_locais_mp`
-- Table structure for table `historico_mov`
--

DROP TABLE IF EXISTS `historico_mov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_mov` (
  `codhmov` varchar(10) NOT NULL DEFAULT '',
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `data_hora` datetime NOT NULL,
  `ip` varchar(50) NOT NULL DEFAULT '',
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codhmov`),
  KEY `codmov` (`codmov`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_mov`
-- Table structure for table `tipo_movimento_razao`
--

DROP TABLE IF EXISTS `tipo_movimento_razao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_movimento_razao` (
  `codtmr` varchar(10) NOT NULL DEFAULT '',
  `descri_tmr` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtmr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_movimento_razao`
-- Table structure for table `adicionais`
--

DROP TABLE IF EXISTS `adicionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adicionais` (
  `codadi` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codsad` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `descri_adi` varchar(50) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  PRIMARY KEY (`codadi`),
  KEY `codcli` (`codcli`),
  KEY `codsad` (`codsad`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adicionais`
-- Table structure for table `circuitos`
--

DROP TABLE IF EXISTS `circuitos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `circuitos` (
  `codcir` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codigo_cir` varchar(30) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcir`),
  KEY `codsercli` (`codsercli`),
  KEY `codigo_cir` (`codigo_cir`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `circuitos`
-- Table structure for table `topico_manual`
--

DROP TABLE IF EXISTS `topico_manual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topico_manual` (
  `codtpm` varchar(10) NOT NULL,
  `name_form` varchar(50) NOT NULL,
  `url` varchar(100) NOT NULL,
  PRIMARY KEY (`codtpm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topico_manual`
-- Table structure for table `servicos_tv_ex`
--

DROP TABLE IF EXISTS `servicos_tv_ex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_tv_ex` (
  `codste` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  PRIMARY KEY (`codste`),
  KEY `codser` (`codser`),
  KEY `codpac` (`codpac`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_tv_ex`
-- Table structure for table `interfaces_produtos`
--

DROP TABLE IF EXISTS `interfaces_produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaces_produtos` (
  `codiprod` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codtintr` varchar(10) NOT NULL,
  `interface` char(15) NOT NULL,
  PRIMARY KEY (`codiprod`),
  KEY `codprod` (`codprod`),
  KEY `codtint` (`codtintr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interfaces_produtos`
-- Table structure for table `documentos`
--

DROP TABLE IF EXISTS `documentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documentos` (
  `coddoc` varchar(10) NOT NULL DEFAULT '',
  `nome_doc` varchar(50) NOT NULL DEFAULT '',
  `codcbe` varchar(10) NOT NULL DEFAULT '',
  `classe` varchar(10) NOT NULL DEFAULT '',
  `local` char(1) NOT NULL,
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `tipo_doc` char(10) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`coddoc`),
  KEY `codcbe` (`codcbe`),
  KEY `tipo_doc` (`tipo_doc`),
  KEY `padrao` (`padrao`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos`
-- Table structure for table `ligacoes`
--

DROP TABLE IF EXISTS `ligacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ligacoes` (
  `codlig` bigint(20) NOT NULL AUTO_INCREMENT,
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codwsale` varchar(10) NOT NULL DEFAULT '',
  `codtter` varchar(10) NOT NULL DEFAULT '',
  `codflv` varchar(10) NOT NULL,
  `codftm` varchar(10) NOT NULL DEFAULT '',
  `codmed` varchar(10) NOT NULL,
  `codpref` varchar(10) NOT NULL,
  `prefixo` varchar(10) NOT NULL,
  `username` varchar(9) NOT NULL DEFAULT '',
  `calledstationid` varchar(50) NOT NULL DEFAULT '',
  `starttime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `stoptime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sessiontime` int(6) unsigned NOT NULL DEFAULT '0',
  `tarifacao` float(10,2) NOT NULL DEFAULT '0.00',
  `calledrate` float(7,5) NOT NULL DEFAULT '0.00000',
  `valor_pag` float(12,4) NOT NULL DEFAULT '0.0000',
  `valor_lig` float(12,5) NOT NULL DEFAULT '0.00000',
  `transactionID` bigint(20) NOT NULL,
  `data_cad` datetime NOT NULL,
  PRIMARY KEY (`codlig`),
  UNIQUE KEY `transactionID` (`transactionID`),
  KEY `codsercli` (`codsercli`),
  KEY `codtter` (`codtter`),
  KEY `username` (`username`),
  KEY `starttime` (`starttime`),
  KEY `stoptime` (`stoptime`),
  KEY `codftm` (`codftm`),
  KEY `prefixo` (`prefixo`),
  KEY `codpref` (`codpref`),
  KEY `codflv` (`codflv`),
  KEY `codmed` (`codmed`),
  KEY `codwsale` (`codwsale`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligacoes`
-- Table structure for table `permissao_contato_ex`
--

DROP TABLE IF EXISTS `permissao_contato_ex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permissao_contato_ex` (
  `codccper` char(10) NOT NULL,
  `p_insert` char(1) NOT NULL DEFAULT 'N',
  `p_delete` char(1) NOT NULL DEFAULT 'N',
  `p_update` char(1) NOT NULL DEFAULT 'N',
  `codace` char(10) NOT NULL,
  `descri_per` varchar(45) NOT NULL DEFAULT '',
  PRIMARY KEY (`codccper`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissao_contato_ex`
-- Table structure for table `troca_status_provisionamento`
--

DROP TABLE IF EXISTS `troca_status_provisionamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `troca_status_provisionamento` (
  `codtsp` int(10) NOT NULL AUTO_INCREMENT,
  `codsercli` varchar(10) NOT NULL,
  `codest` varchar(10) NOT NULL,
  `codextra` varchar(10) NOT NULL,
  `data_cadastro` datetime NOT NULL,
  `status` char(1) NOT NULL,
  `data_execucao` datetime NOT NULL,
  `nro_tentativa` int(2) unsigned NOT NULL,
  `obs` text NOT NULL,
  PRIMARY KEY (`codtsp`),
  KEY `codsercli` (`codsercli`),
  KEY `codest` (`codest`),
  KEY `codextra` (`codextra`),
  KEY `data_cadastro` (`data_cadastro`),
  KEY `status` (`status`),
  KEY `data_execucao` (`data_execucao`)
) ENGINE=MyISAM AUTO_INCREMENT=54984 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `troca_status_provisionamento`
-- Table structure for table `maparede_sinc_det`
--

DROP TABLE IF EXISTS `maparede_sinc_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maparede_sinc_det` (
  `codmps` varchar(20) NOT NULL DEFAULT '',
  `codmpcon` varchar(20) NOT NULL DEFAULT '',
  `resultado` mediumtext NOT NULL,
  `status` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codmps`,`codmpcon`),
  KEY `maparede_sinc_det_FK` (`codmpcon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maparede_sinc_det`
-- Table structure for table `consultas`
--

DROP TABLE IF EXISTS `consultas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultas` (
  `codcst` varchar(10) NOT NULL DEFAULT '',
  `titulo` varchar(100) NOT NULL DEFAULT '',
  `subtitulo` mediumtext NOT NULL,
  `sentencia` mediumtext NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT 'E',
  PRIMARY KEY (`codcst`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultas`
-- Table structure for table `param_comissao`
--

DROP TABLE IF EXISTS `param_comissao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `param_comissao` (
  `codpcm` varchar(10) NOT NULL,
  `compe` char(4) NOT NULL,
  `qtd_plano_meta_ind` int(4) NOT NULL,
  `qtd_plano_meta_col` int(4) unsigned NOT NULL,
  `qtd_plano_meta_dep` int(4) NOT NULL,
  `comissao_ind` float(10,2) NOT NULL,
  `comissao_s_meta` float(10,2) NOT NULL,
  `comissao_meta_col` float(10,2) NOT NULL,
  PRIMARY KEY (`codpcm`),
  KEY `compe` (`compe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `param_comissao`
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `codest` varchar(10) NOT NULL DEFAULT '',
  `codemr` varchar(10) NOT NULL,
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `descri_est` varchar(50) NOT NULL DEFAULT '',
  `gerar` char(1) NOT NULL DEFAULT '',
  `proximo` varchar(10) NOT NULL DEFAULT '',
  `codaco` char(1) NOT NULL DEFAULT '',
  `permite_alterar` char(1) NOT NULL DEFAULT 'N',
  `cria_login` char(1) NOT NULL DEFAULT 'N',
  `gerar_evento_desconto` char(1) NOT NULL DEFAULT 'N',
  `tarefa_programada` char(1) NOT NULL DEFAULT 'N',
  `enviar_email` char(1) NOT NULL DEFAULT 'N',
  `codcbe_email` varchar(10) NOT NULL DEFAULT '',
  `enviar_sms` char(1) NOT NULL DEFAULT 'N',
  `codcbe_sms` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codest`),
  KEY `codemr` (`codemr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
-- Table structure for table `codigos`
--

DROP TABLE IF EXISTS `codigos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codigos` (
  `tabela` varchar(20) NOT NULL DEFAULT '',
  `ultimo_codigo` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tabela`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos`
-- Table structure for table `aquisicoes`
--

DROP TABLE IF EXISTS `aquisicoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aquisicoes` (
  `codaqs` varchar(10) NOT NULL DEFAULT '',
  `numero` bigint(12) unsigned NOT NULL,
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL DEFAULT '0.00',
  `garantia` int(3) unsigned NOT NULL DEFAULT '0',
  `data_notafiscal` date NOT NULL,
  `num_notafiscal` int(11) unsigned NOT NULL,
  `notafiscal` varchar(1) NOT NULL,
  `justificativa` varchar(50) NOT NULL,
  `locacao` varchar(50) NOT NULL,
  `previsaoentrega` date NOT NULL,
  `condpagamento` varchar(50) NOT NULL,
  `observacao` varchar(100) NOT NULL,
  `autorizacaodata` datetime NOT NULL,
  `autorizacaousu` varchar(20) NOT NULL,
  `exclusao` char(1) NOT NULL DEFAULT 'S',
  `situacao` char(1) NOT NULL DEFAULT 'A',
  PRIMARY KEY (`codaqs`),
  KEY `codfor` (`codfor`),
  KEY `numero` (`numero`),
  KEY `data_notafiscal` (`data_notafiscal`),
  KEY `num_notafiscal` (`num_notafiscal`),
  KEY `previsaoentrega` (`previsaoentrega`),
  KEY `exclusao` (`exclusao`),
  KEY `situacao` (`situacao`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aquisicoes`
-- Table structure for table `segmento_arrecadacao`
--

DROP TABLE IF EXISTS `segmento_arrecadacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `segmento_arrecadacao` (
  `codseg` varchar(10) NOT NULL,
  `codigo` char(1) NOT NULL,
  `descri_seg` varchar(100) NOT NULL,
  PRIMARY KEY (`codseg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `segmento_arrecadacao`
-- Table structure for table `servicos_dom`
--

DROP TABLE IF EXISTS `servicos_dom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_dom` (
  `codsdom` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `quant_d` int(4) NOT NULL DEFAULT '0',
  `quota_dom` int(6) unsigned NOT NULL DEFAULT '0',
  `estatisticas` char(1) NOT NULL DEFAULT 'S',
  `quant_e_d` int(3) unsigned NOT NULL DEFAULT '0',
  `quant_ftp` int(4) unsigned NOT NULL DEFAULT '0',
  `quota_ed_s` int(6) unsigned NOT NULL DEFAULT '0',
  `valor_ed_adi` float(10,2) NOT NULL DEFAULT '0.00',
  `codservp_h` varchar(10) NOT NULL DEFAULT '',
  `codservp_c` varchar(10) NOT NULL DEFAULT '',
  `tipo_mta` char(1) NOT NULL DEFAULT 'Q',
  `quota_ftp` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codsdom`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_dom`
-- Table structure for table `faturas`
--

DROP TABLE IF EXISTS `faturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturas` (
  `codfat` char(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcob` char(10) NOT NULL DEFAULT '',
  `n_boleto` varchar(20) NOT NULL DEFAULT '',
  `codnf` char(10) NOT NULL DEFAULT '',
  `codarq` char(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `nro_doc` char(10) NOT NULL DEFAULT '',
  `status` char(1) NOT NULL DEFAULT '',
  `parcelamento` char(1) NOT NULL DEFAULT 'N',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_bai` date NOT NULL DEFAULT '0000-00-00',
  `valor_lan` float(8,2) NOT NULL DEFAULT '0.00',
  `histo_fat` varchar(70) NOT NULL DEFAULT '',
  `codrbrt` char(2) NOT NULL DEFAULT '',
  `idcarne` varchar(50) NOT NULL DEFAULT '',
  `codarq_b` char(10) NOT NULL DEFAULT '',
  `codmov` char(10) NOT NULL DEFAULT '',
  `codsta_f` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codfat`),
  KEY `codcli` (`codcli`),
  KEY `codcob` (`codcob`),
  KEY `n_boleto` (`n_boleto`),
  KEY `data_ven` (`data_ven`),
  KEY `data_lan` (`data_lan`),
  KEY `status` (`status`),
  KEY `parcelamento` (`parcelamento`),
  KEY `data_bai` (`data_bai`),
  KEY `codmov` (`codmov`),
  KEY `codsta_f` (`codsta_f`),
  KEY `codarq` (`codarq`),
  KEY `codarq_b` (`codarq_b`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturas`
-- Table structure for table `tipo_pagamento_for`
--

DROP TABLE IF EXISTS `tipo_pagamento_for`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_pagamento_for` (
  `codtpf` varchar(10) NOT NULL,
  `descri_tpf` varchar(40) NOT NULL,
  PRIMARY KEY (`codtpf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_pagamento_for`
-- Table structure for table `detalhe_movi`
--

DROP TABLE IF EXISTS `detalhe_movi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_movi` (
  `coddmovi` varchar(10) NOT NULL DEFAULT '',
  `codmovi` varchar(10) NOT NULL DEFAULT '',
  `coditem` varchar(10) NOT NULL DEFAULT '',
  `quant` float(6,2) NOT NULL DEFAULT '0.00',
  `preco` float(8,2) NOT NULL DEFAULT '0.00',
  `desconto` float(8,2) NOT NULL DEFAULT '0.00',
  `numero_serie` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddmovi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_movi`
-- Table structure for table `det_desc_negociacao`
--

DROP TABLE IF EXISTS `det_desc_negociacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_desc_negociacao` (
  `coddes` char(10) NOT NULL,
  `codndeb` char(10) DEFAULT NULL,
  KEY `coddes` (`coddes`),
  KEY `codndeb` (`codndeb`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_desc_negociacao`
-- Table structure for table `tipo_comi_gser`
--

DROP TABLE IF EXISTS `tipo_comi_gser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_comi_gser` (
  `codtcg` varchar(10) NOT NULL,
  `codtcs` varchar(10) NOT NULL,
  `codgser` varchar(10) NOT NULL,
  PRIMARY KEY (`codtcg`),
  KEY `codtcs` (`codtcs`),
  KEY `codgser` (`codgser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_comi_gser`
-- Table structure for table `operadoras_telefonia`
--

DROP TABLE IF EXISTS `operadoras_telefonia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operadoras_telefonia` (
  `codopertel` char(10) NOT NULL COMMENT 'Chave primária',
  `descri_opertel` varchar(45) NOT NULL COMMENT 'Nome da operadora',
  `csp` varchar(5) NOT NULL COMMENT 'Código de Seleção da Prestadora',
  PRIMARY KEY (`codopertel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operadoras_telefonia`
-- Table structure for table `status_site_survey`
--

DROP TABLE IF EXISTS `status_site_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_site_survey` (
  `codsss` varchar(10) NOT NULL DEFAULT '',
  `descri_sss` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsss`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_site_survey`
-- Table structure for table `embalagem_prod`
--

DROP TABLE IF EXISTS `embalagem_prod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `embalagem_prod` (
  `codepd` varchar(10) NOT NULL,
  `codtep` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `descri_un` varchar(10) NOT NULL,
  `quant` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codepd`),
  KEY `codtep` (`codtep`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `embalagem_prod`
-- Table structure for table `est_usu`
--

DROP TABLE IF EXISTS `est_usu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `est_usu` (
  `codestusu` char(10) NOT NULL,
  `codesta` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  PRIMARY KEY (`codestusu`),
  KEY `codesta` (`codesta`),
  KEY `codusu` (`codusu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `est_usu`
-- Table structure for table `det_indicadores`
--

DROP TABLE IF EXISTS `det_indicadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_indicadores` (
  `coddind` varchar(10) NOT NULL,
  `codind` varchar(10) NOT NULL,
  `codind_f` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `signo` char(1) NOT NULL DEFAULT '+',
  `alias` varchar(10) NOT NULL,
  PRIMARY KEY (`coddind`),
  KEY `codind` (`codind`),
  KEY `codind_f` (`codind_f`),
  KEY `codtab` (`codtab`),
  KEY `alias` (`alias`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_indicadores`
-- Table structure for table `opcoes`
--

DROP TABLE IF EXISTS `opcoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes` (
  `indice` char(3) NOT NULL DEFAULT '',
  `titulo` varchar(30) NOT NULL DEFAULT '',
  `codima` varchar(15) NOT NULL DEFAULT '',
  `codigo` varchar(20) NOT NULL DEFAULT '',
  `alias` varchar(5) NOT NULL DEFAULT '',
  `formulario` varchar(100) NOT NULL DEFAULT '',
  `executavel` varchar(30) NOT NULL DEFAULT '',
  `menu` char(1) NOT NULL DEFAULT '',
  `submenu` char(1) NOT NULL DEFAULT '',
  `destino` char(1) NOT NULL DEFAULT '',
  `comando` text NOT NULL,
  `lista` text NOT NULL,
  `hint` varchar(15) NOT NULL,
  `string_conexao_externa` mediumtext NOT NULL COMMENT '||-',
  `codservp` varchar(10) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`indice`),
  KEY `codima` (`codima`),
  KEY `menu` (`menu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes`
-- Table structure for table `movimentos_hist_bkp`
--

DROP TABLE IF EXISTS `movimentos_hist_bkp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentos_hist_bkp` (
  `codmovex` char(10) NOT NULL DEFAULT '',
  `codmvp` char(10) NOT NULL DEFAULT '',
  `codlic` char(10) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de Início do Serviço',
  `quantidade` decimal(10,2) NOT NULL DEFAULT '0.00',
  `codmvp_origem` char(10) NOT NULL DEFAULT '' COMMENT 'Campo para informar o codmvp de origem do movimento',
  PRIMARY KEY (`codmovex`),
  KEY `codmvp` (`codmvp`),
  KEY `codlic` (`codlic`),
  KEY `quantidade` (`quantidade`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos_hist_bkp`
-- Table structure for table `funil_venda`
--

DROP TABLE IF EXISTS `funil_venda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `funil_venda` (
  `id_funil` int(11) NOT NULL AUTO_INCREMENT,
  `nome_funil` varchar(45) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id_funil`),
  KEY `ativo` (`ativo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funil_venda`
-- Table structure for table `cfop`
--

DROP TABLE IF EXISTS `cfop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfop` (
  `codcfop` varchar(10) NOT NULL DEFAULT '',
  `descri_cfop` varchar(100) NOT NULL DEFAULT '',
  `tipo_cliente` char(1) NOT NULL DEFAULT 'J',
  `saida` char(1) NOT NULL,
  `tipo_cli_nf` char(2) NOT NULL DEFAULT '',
  `observacao` text NOT NULL,
  `finalidade` char(1) NOT NULL DEFAULT 'N' COMMENT 'N- Normal e D- Devolução',
  PRIMARY KEY (`codcfop`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cfop`
-- Table structure for table `tarefas_filhas_o`
--

DROP TABLE IF EXISTS `tarefas_filhas_o`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefas_filhas_o` (
  `codtfo` varchar(10) NOT NULL DEFAULT '',
  `codtaro` varchar(10) NOT NULL DEFAULT '',
  `codtaro_p` varchar(10) NOT NULL DEFAULT '',
  `codtaro_f` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtfo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefas_filhas_o`
-- Table structure for table `status_int`
--

DROP TABLE IF EXISTS `status_int`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_int` (
  `codsti` varchar(10) NOT NULL DEFAULT '',
  `descri_sti` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`codsti`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_int`
-- Table structure for table `det_paginas_ggi`
--

DROP TABLE IF EXISTS `det_paginas_ggi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_paginas_ggi` (
  `codcgi` varchar(10) NOT NULL,
  `codpgi` varchar(10) NOT NULL,
  `codgi` varchar(10) NOT NULL,
  `pos_top` int(4) unsigned NOT NULL,
  `pos_left` int(4) unsigned NOT NULL,
  `width` int(4) unsigned NOT NULL,
  `height` int(4) unsigned NOT NULL,
  `linhas` int(11) NOT NULL DEFAULT '0',
  `colunas` int(11) NOT NULL DEFAULT '0',
  `posicao` int(3) NOT NULL DEFAULT '0',
  `ordem` int(4) NOT NULL DEFAULT '9999',
  PRIMARY KEY (`codcgi`),
  KEY `codpgi` (`codpgi`),
  KEY `codgi` (`codgi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_paginas_ggi`
-- Table structure for table `ocop_grupo_clientes`
--

DROP TABLE IF EXISTS `ocop_grupo_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocop_grupo_clientes` (
  `codogc` varchar(10) NOT NULL,
  `codgcli` varchar(10) NOT NULL,
  `codocop` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL,
  PRIMARY KEY (`codogc`),
  KEY `codgcli` (`codgcli`),
  KEY `codocop` (`codocop`),
  KEY `tipo` (`tipo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocop_grupo_clientes`
-- Table structure for table `custo_produto`
--

DROP TABLE IF EXISTS `custo_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custo_produto` (
  `codcprd` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data` date NOT NULL,
  `p_desde` date NOT NULL,
  `p_ate` date NOT NULL,
  `quantidade` bigint(6) unsigned NOT NULL,
  `valor_min` float(10,2) NOT NULL,
  `valor_max` float(10,2) NOT NULL,
  `custo_medio` float(10,2) NOT NULL,
  PRIMARY KEY (`codcprd`),
  KEY `codprod` (`codprod`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custo_produto`
-- Table structure for table `produtos_imp`
--

DROP TABLE IF EXISTS `produtos_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produtos_imp` (
  `codimprod` char(10) NOT NULL DEFAULT '',
  `codprod` char(10) NOT NULL DEFAULT '',
  `codemp` char(10) NOT NULL DEFAULT '',
  `estado` char(2) NOT NULL DEFAULT '',
  `codcenq` char(3) NOT NULL,
  `icms_cb_cst` char(4) NOT NULL DEFAULT '',
  `icms_cb_orig` char(1) NOT NULL DEFAULT '',
  `ipi_cb_cst` char(2) NOT NULL DEFAULT '',
  `pis_cb_cst` char(2) NOT NULL DEFAULT '',
  `cofins_cb_cst` char(2) NOT NULL DEFAULT '',
  `modBCST` char(1) NOT NULL,
  `modBC` char(1) NOT NULL,
  `icms` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `ipi` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `pis` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `iva` decimal(10,4) NOT NULL,
  `cofins` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `pRedBCST` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `pMVAST` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `pICMSST` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `pRedBC` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `picms` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `bcicms` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `icmsop` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `bcicmsst` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `icmsst` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `pdif` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `codbeneficio` char(10) NOT NULL DEFAULT '',
  `somaripi` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codimprod`),
  KEY `codprod` (`codprod`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos_imp`
-- Table structure for table `detalhe_g_com`
--

DROP TABLE IF EXISTS `detalhe_g_com`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_g_com` (
  `coddgcom` varchar(10) NOT NULL DEFAULT '',
  `codgcom` varchar(10) NOT NULL DEFAULT '',
  `codcom` int(4) unsigned NOT NULL DEFAULT '0',
  `ordem` int(1) unsigned NOT NULL DEFAULT '0',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `codservp_p` text NOT NULL,
  PRIMARY KEY (`coddgcom`),
  KEY `codgcom` (`codgcom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_g_com`
-- Table structure for table `usuarios_tarefas_m`
--

DROP TABLE IF EXISTS `usuarios_tarefas_m`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_tarefas_m` (
  `codutm` varchar(10) NOT NULL DEFAULT '',
  `codtarm` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codutm`),
  KEY `codtarm` (`codtarm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_tarefas_m`
-- Table structure for table `clientes_prospect`
--

DROP TABLE IF EXISTS `clientes_prospect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes_prospect` (
  `codcli` int(6) NOT NULL DEFAULT '0',
  `nome_cli` varchar(50) NOT NULL DEFAULT '',
  `nome_fan` varchar(30) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `contato` varchar(50) NOT NULL DEFAULT '',
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `tipo_cliente` char(1) NOT NULL DEFAULT '',
  `endereco_cob` varchar(50) NOT NULL DEFAULT '',
  `bairro_cob` varchar(25) NOT NULL DEFAULT '',
  `cidade_cob` varchar(8) NOT NULL DEFAULT '',
  `cep_cob` varchar(9) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `icm` varchar(15) NOT NULL DEFAULT '',
  `rg` varchar(11) NOT NULL DEFAULT '',
  `cpf` varchar(14) NOT NULL DEFAULT '',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `obs` text NOT NULL,
  PRIMARY KEY (`codcli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_prospect`
-- Table structure for table `provedores`
--

DROP TABLE IF EXISTS `provedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `provedores` (
  `codprov` varchar(10) NOT NULL DEFAULT '',
  `nome_prov` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codprov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provedores`
-- Table structure for table `apis`
--

DROP TABLE IF EXISTS `apis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apis` (
  `codapi` varchar(10) NOT NULL,
  `descri_api` varchar(50) DEFAULT NULL,
  `codigo` int(6) DEFAULT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `method` varchar(10) NOT NULL DEFAULT 'execute',
  PRIMARY KEY (`codapi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis`
-- Table structure for table `controle_mov_pat`
--

DROP TABLE IF EXISTS `controle_mov_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controle_mov_pat` (
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codusu_g` char(2) NOT NULL DEFAULT '',
  `codusu_t` char(2) NOT NULL DEFAULT '',
  `codusu_c` char(2) NOT NULL DEFAULT '',
  `codlmp_o` varchar(10) NOT NULL,
  `confirmado` char(1) NOT NULL DEFAULT 'N',
  `numero` int(6) NOT NULL DEFAULT '0',
  `code_f` varchar(10) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcmp`),
  KEY `codusu_t` (`codusu_t`),
  KEY `codusu_c` (`codusu_c`),
  KEY `codusu_g` (`codusu_g`),
  KEY `codlmp_o` (`codlmp_o`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controle_mov_pat`
-- Table structure for table `parentesco`
--

DROP TABLE IF EXISTS `parentesco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parentesco` (
  `codpar` varchar(10) NOT NULL,
  `descri_par` varchar(30) NOT NULL,
  PRIMARY KEY (`codpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parentesco`
-- Table structure for table `int_templates`
--

DROP TABLE IF EXISTS `int_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_templates` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `modulo` int(2) NOT NULL DEFAULT '0',
  `nome` varchar(60) NOT NULL DEFAULT '',
  `valor` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_templates`
-- Table structure for table `opcoes_menu_telas`
--

DROP TABLE IF EXISTS `opcoes_menu_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes_menu_telas` (
  `codomt` varchar(10) NOT NULL,
  `codmenu` varchar(10) NOT NULL,
  `codgmt` varchar(10) NOT NULL,
  `codamt` varchar(10) NOT NULL,
  `codctl` varchar(10) NOT NULL,
  `codopc` char(3) NOT NULL,
  `nome` varchar(30) NOT NULL,
  `titulo` varchar(30) NOT NULL,
  `acao` varchar(30) NOT NULL,
  `imagem` varchar(30) NOT NULL,
  `v_left` int(4) unsigned NOT NULL,
  `v_width` int(4) unsigned NOT NULL,
  `ativo` char(1) NOT NULL,
  `anchor` int(1) unsigned NOT NULL,
  PRIMARY KEY (`codomt`),
  KEY `codmenu` (`codmenu`),
  KEY `codgmt` (`codgmt`),
  KEY `codamt` (`codamt`),
  KEY `codctl` (`codctl`),
  KEY `codopc` (`codopc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes_menu_telas`
-- Table structure for table `origem_comercial`
--

DROP TABLE IF EXISTS `origem_comercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `origem_comercial` (
  `codocm` varchar(10) NOT NULL,
  `codpros` varchar(10) NOT NULL,
  `codcli` int(6) unsigned NOT NULL,
  `codtocm` varchar(10) NOT NULL,
  `codoce` varchar(10) NOT NULL,
  `codigo_origem` varchar(10) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codocm`),
  KEY `codpros` (`codpros`),
  KEY `codcli` (`codcli`),
  KEY `codtocm` (`codtocm`),
  KEY `codoce` (`codoce`),
  KEY `codigo_origem` (`codigo_origem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `origem_comercial`
-- Table structure for table `tecnologia_sici`
--

DROP TABLE IF EXISTS `tecnologia_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tecnologia_sici` (
  `codtsici` varchar(10) NOT NULL,
  `descri_tsici` varchar(50) NOT NULL,
  `ponto_acesso` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codtsici`),
  KEY `ponto_acesso` (`ponto_acesso`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tecnologia_sici`
-- Table structure for table `grupo_comercial`
--

DROP TABLE IF EXISTS `grupo_comercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_comercial` (
  `codgcom` char(10) NOT NULL,
  `descri_gcom` varchar(45) NOT NULL,
  `ativo` char(1) NOT NULL,
  PRIMARY KEY (`codgcom`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_comercial`
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categorias` (
  `codcat` varchar(10) NOT NULL DEFAULT '',
  `descri_cat` varchar(50) NOT NULL DEFAULT '',
  `radio` char(1) NOT NULL DEFAULT 'N',
  `rede` char(1) DEFAULT 'N',
  `obs` text NOT NULL,
  PRIMARY KEY (`codcat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
-- Table structure for table `det_log_tarefa_cob`
--

DROP TABLE IF EXISTS `det_log_tarefa_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_log_tarefa_cob` (
  `coddltc` varchar(10) NOT NULL,
  `codltc` varchar(10) NOT NULL,
  `codtar` varchar(10) NOT NULL,
  `coderc` varchar(10) NOT NULL,
  `codscc` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `ok` char(1) NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`coddltc`),
  KEY `codltc` (`codltc`),
  KEY `codtar` (`codtar`),
  KEY `codscc` (`codscc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_log_tarefa_cob`
-- Table structure for table `cartaocredito`
--

DROP TABLE IF EXISTS `cartaocredito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cartaocredito` (
  `codcar` varchar(10) NOT NULL COMMENT 'Codigo do cartão (Bandeira)',
  `bandera` varchar(50) NOT NULL COMMENT 'Nome da Bandeira',
  PRIMARY KEY (`codcar`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartaocredito`
-- Table structure for table `licencias_antivirus`
--

DROP TABLE IF EXISTS `licencias_antivirus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `licencias_antivirus` (
  `codlav` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codtlav` varchar(10) NOT NULL DEFAULT '',
  `login` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `nro_licencia` varchar(30) NOT NULL DEFAULT '',
  `nro_ordem` varchar(10) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL,
  `sem_cargo` char(1) NOT NULL DEFAULT 'N',
  `ativa` char(1) NOT NULL DEFAULT 'N',
  `qnt_lic` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codlav`),
  KEY `codsercli` (`codsercli`),
  KEY `codtlav` (`codtlav`),
  KEY `qnt_lic` (`qnt_lic`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `licencias_antivirus`
-- Table structure for table `prefixos_reg_neg_voz`
--

DROP TABLE IF EXISTS `prefixos_reg_neg_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefixos_reg_neg_voz` (
  `codprnv` varchar(10) NOT NULL,
  `codrnv` varchar(10) NOT NULL,
  `codpref` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL,
  `valor` float(5,3) NOT NULL,
  PRIMARY KEY (`codprnv`),
  KEY `codrnv` (`codrnv`),
  KEY `codpref` (`codpref`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prefixos_reg_neg_voz`
-- Table structure for table `tipo_desconto`
--

DROP TABLE IF EXISTS `tipo_desconto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_desconto` (
  `codtdes` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `descri_tdes` varchar(50) NOT NULL DEFAULT '',
  `ativo` varchar(1) NOT NULL DEFAULT 'S',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtdes`),
  KEY `codcta` (`codcta`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_desconto`
-- Table structure for table `usu_locais`
--

DROP TABLE IF EXISTS `usu_locais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_locais` (
  `codulmp` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codulmp`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_locais`
-- Table structure for table `usu_unidades`
--

DROP TABLE IF EXISTS `usu_unidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_unidades` (
  `codupop` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codupop`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_unidades`
-- Table structure for table `vencimentos_pop`
--

DROP TABLE IF EXISTS `vencimentos_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vencimentos_pop` (
  `codvencp` varchar(10) NOT NULL DEFAULT '',
  `codvenc` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codvencp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vencimentos_pop`
-- Table structure for table `conf_int_radios`
--

DROP TABLE IF EXISTS `conf_int_radios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_int_radios` (
  `codcir` varchar(10) NOT NULL DEFAULT '',
  `codosr` varchar(10) NOT NULL DEFAULT '',
  `codtintr` varchar(10) NOT NULL DEFAULT '',
  `descri_cir` varchar(50) NOT NULL DEFAULT '',
  `ordem` int(2) unsigned NOT NULL DEFAULT '0',
  `comando` text NOT NULL,
  `obs` text NOT NULL,
  PRIMARY KEY (`codcir`),
  KEY `codosr` (`codosr`),
  KEY `codtintr` (`codtintr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_int_radios`
-- Table structure for table `servicos_bd`
--

DROP TABLE IF EXISTS `servicos_bd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_bd` (
  `codsbd` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codtbd` varchar(10) NOT NULL DEFAULT '',
  `quant_bd` int(2) unsigned NOT NULL DEFAULT '0',
  `quant_u_bd` int(2) unsigned NOT NULL DEFAULT '0',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `quota_bd` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codsbd`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_bd`
-- Table structure for table `tabela_imposto_retencao`
--

DROP TABLE IF EXISTS `tabela_imposto_retencao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabela_imposto_retencao` (
  `codtimret` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `comp` varchar(4) NOT NULL,
  `data_lan` date NOT NULL,
  `nome_tabela` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtimret`),
  KEY `codemp` (`codemp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabela_imposto_retencao`
-- Table structure for table `linhas_pop`
--

DROP TABLE IF EXISTS `linhas_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linhas_pop` (
  `codlin_p` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codcomp` varchar(4) NOT NULL DEFAULT '',
  `quant_linhas` int(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codlin_p`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linhas_pop`
-- Table structure for table `requisicaoitem`
--

DROP TABLE IF EXISTS `requisicaoitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requisicaoitem` (
  `codrequisitem` varchar(10) NOT NULL DEFAULT '',
  `codrequis` varchar(10) NOT NULL DEFAULT '',
  `codprod` varchar(10) NOT NULL DEFAULT '',
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `quantidade` double(10,2) NOT NULL DEFAULT '0.00',
  `quantidade_rec` double(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codrequisitem`),
  UNIQUE KEY `codrequisitem` (`codrequisitem`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requisicaoitem`
-- Table structure for table `dados_cel`
--

DROP TABLE IF EXISTS `dados_cel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dados_cel` (
  `codcel` char(10) NOT NULL,
  `codcli` int(6) NOT NULL,
  `id_device` varchar(250) NOT NULL DEFAULT '',
  `descri_cel` varchar(100) NOT NULL DEFAULT '',
  `plataforma` varchar(100) NOT NULL DEFAULT '',
  `status_cel` char(1) NOT NULL DEFAULT '',
  `data_lan` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_ativ` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_can` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codco_cl` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcel`),
  KEY `codcli` (`codcli`),
  KEY `data_lan` (`data_lan`),
  KEY `data_ativ` (`data_ativ`),
  KEY `id_device` (`id_device`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_cel`
-- Table structure for table `updates`
--

DROP TABLE IF EXISTS `updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `updates` (
  `codupd` varchar(10) NOT NULL DEFAULT '',
  `server` varchar(30) NOT NULL DEFAULT '',
  `login` varchar(20) NOT NULL DEFAULT '',
  `senha` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codupd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `updates`
-- Table structure for table `ccusto`
--

DROP TABLE IF EXISTS `ccusto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ccusto` (
  `codctc` char(8) NOT NULL,
  `descri_custo` varchar(40) NOT NULL,
  `tipo` char(1) NOT NULL,
  PRIMARY KEY (`codctc`),
  KEY `tipo` (`tipo`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ccusto`
-- Table structure for table `faturamentos_adiantados`
--

DROP TABLE IF EXISTS `faturamentos_adiantados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturamentos_adiantados` (
  `codftma` varchar(10) NOT NULL,
  `data_lan` date NOT NULL,
  `datas_ven` mediumtext NOT NULL,
  `codigos` mediumtext NOT NULL,
  PRIMARY KEY (`codftma`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturamentos_adiantados`
-- Table structure for table `historico_ocorrencias`
--

DROP TABLE IF EXISTS `historico_ocorrencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_ocorrencias` (
  `codhoco` varchar(10) NOT NULL,
  `codoco` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  `usuario` char(2) NOT NULL,
  `tabela` varchar(30) NOT NULL,
  `ip` varchar(50) NOT NULL,
  `texto` mediumtext NOT NULL,
  PRIMARY KEY (`codhoco`),
  KEY `codoco` (`codoco`),
  KEY `usuario` (`usuario`),
  KEY `data` (`data`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_ocorrencias`
-- Table structure for table `tipo_execucao`
--

DROP TABLE IF EXISTS `tipo_execucao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_execucao` (
  `codtexec` char(10) NOT NULL,
  `descri_tcmd` varchar(45) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtexec`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_execucao`
-- Table structure for table `servicos_dici`
--

DROP TABLE IF EXISTS `servicos_dici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_dici` (
  `codsdici` char(10) NOT NULL,
  `codser` char(10) DEFAULT NULL,
  `coddicita` char(10) DEFAULT NULL,
  `coddicitac` char(10) DEFAULT NULL,
  `coddicitec` char(10) DEFAULT NULL,
  `coddicitprod` char(10) DEFAULT NULL,
  `velocidade` decimal(15,5) NOT NULL DEFAULT '0.00000',
  `usu_proprio` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codsdici`),
  KEY `codser` (`codser`),
  KEY `usu_proprio` (`usu_proprio`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_dici`
-- Table structure for table `aviso_atraso_tarefas`
--

DROP TABLE IF EXISTS `aviso_atraso_tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aviso_atraso_tarefas` (
  `codaat` varchar(10) NOT NULL DEFAULT '',
  `codtarm` varchar(10) NOT NULL DEFAULT '',
  `codtaro` varchar(10) NOT NULL,
  `codutmp` varchar(10) NOT NULL DEFAULT '',
  `tempo` int(4) unsigned NOT NULL DEFAULT '0',
  `acao` char(1) NOT NULL DEFAULT 'E',
  PRIMARY KEY (`codaat`),
  KEY `codtarm` (`codtarm`),
  KEY `codtaro` (`codtaro`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aviso_atraso_tarefas`
-- Table structure for table `paginas_ggi`
--

DROP TABLE IF EXISTS `paginas_ggi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paginas_ggi` (
  `codpgi` varchar(10) NOT NULL,
  `codggi` varchar(10) NOT NULL,
  `codtpgi` varchar(10) NOT NULL,
  `descri_pgi` varchar(50) NOT NULL,
  `nro_pagina` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codpgi`),
  KEY `codggi` (`codggi`),
  KEY `codtpgi` (`codtpgi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paginas_ggi`
-- Table structure for table `exesu_opc`
--

DROP TABLE IF EXISTS `exesu_opc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exesu_opc` (
  `codesuopc` varchar(10) NOT NULL,
  `codexesu` varchar(10) DEFAULT NULL,
  `VFPSQL` char(1) DEFAULT NULL,
  `VFPRUNTIME` char(1) DEFAULT NULL,
  `VFPALLOPC` char(1) DEFAULT NULL,
  `VFPTXTSQL` char(1) DEFAULT NULL,
  `VFPCONSOLE` char(1) DEFAULT NULL,
  `VFPMACROC` varchar(1) DEFAULT 'S',
  PRIMARY KEY (`codesuopc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exesu_opc`
-- Table structure for table `zonas_ip`
--

DROP TABLE IF EXISTS `zonas_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zonas_ip` (
  `codaip` varchar(10) NOT NULL,
  `codcla` varchar(10) DEFAULT NULL,
  `codeqr` varchar(10) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `classe` int(3) DEFAULT NULL,
  `codinte` varchar(10) DEFAULT NULL,
  `pool_ip` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`codaip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zonas_ip`
-- Table structure for table `forma_arrecadacao`
--

DROP TABLE IF EXISTS `forma_arrecadacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forma_arrecadacao` (
  `codar` char(2) NOT NULL,
  `nro_ban` char(3) NOT NULL DEFAULT '',
  `descri_ar` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codar`),
  KEY `nro_ban` (`nro_ban`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forma_arrecadacao`
-- Table structure for table `dici_tipo_acesso`
--

DROP TABLE IF EXISTS `dici_tipo_acesso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dici_tipo_acesso` (
  `coddicitac` char(10) NOT NULL,
  `descricao` varchar(50) DEFAULT NULL,
  `ativo` char(1) DEFAULT 'S',
  PRIMARY KEY (`coddicitac`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dici_tipo_acesso`
-- Table structure for table `int_servers`
--

DROP TABLE IF EXISTS `int_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_servers` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `nome` varchar(20) NOT NULL DEFAULT '',
  `ip` varchar(25) NOT NULL DEFAULT '',
  `porta` int(5) NOT NULL DEFAULT '0',
  `ssl` int(1) NOT NULL DEFAULT '1',
  `ativo` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`,`nome`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_servers`
-- Table structure for table `detalhe_documento`
--

DROP TABLE IF EXISTS `detalhe_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_documento` (
  `codddoc` varchar(9) NOT NULL DEFAULT '',
  `coddoc` varchar(10) NOT NULL DEFAULT '',
  `codtdoc` varchar(10) NOT NULL DEFAULT '',
  `ordem` tinyint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codddoc`),
  KEY `coddoc` (`coddoc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_documento`
-- Table structure for table `razao`
--

DROP TABLE IF EXISTS `razao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `razao` (
  `codraz` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `compe` varchar(4) NOT NULL,
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL,
  `codtmr` varchar(10) NOT NULL,
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `data_raz` date NOT NULL DEFAULT '0000-00-00',
  `codcpag` varchar(10) NOT NULL DEFAULT '',
  `coddcp` char(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `codsac` varchar(10) NOT NULL,
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `histo_raz` varchar(70) NOT NULL DEFAULT '',
  `valor_raz` double(10,2) NOT NULL DEFAULT '0.00',
  `sacado` varchar(70) NOT NULL,
  `codfat` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codraz`),
  KEY `codmov` (`codmov`),
  KEY `codcta` (`codcta`),
  KEY `codcrec` (`codcrec`),
  KEY `codpop` (`codpop`),
  KEY `compe` (`compe`),
  KEY `codemp` (`codemp`),
  KEY `codtmr` (`codtmr`),
  KEY `codsac` (`codsac`),
  KEY `codcpag` (`codcpag`),
  KEY `codctc` (`codctc`),
  KEY `data_raz` (`data_raz`),
  KEY `coddcp` (`coddcp`),
  KEY `codfat` (`codfat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `razao`
-- Table structure for table `crp_icone`
--

DROP TABLE IF EXISTS `crp_icone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crp_icone` (
  `codcrpi` varchar(10) NOT NULL DEFAULT '',
  `icone` varchar(50) DEFAULT NULL,
  `iconeon` varchar(50) DEFAULT NULL,
  `nome` varchar(80) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `visivel` varchar(1) DEFAULT NULL,
  `ordem` tinyint(4) DEFAULT NULL,
  `codcrpg` varchar(10) DEFAULT NULL,
  `form` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`codcrpi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crp_icone`
-- Table structure for table `det_graficos_ind`
--

DROP TABLE IF EXISTS `det_graficos_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_graficos_ind` (
  `coddgi` varchar(10) NOT NULL,
  `codgi` varchar(10) NOT NULL,
  `codind` varchar(10) NOT NULL,
  `coddind` varchar(10) NOT NULL,
  `codtgraf` varchar(10) NOT NULL,
  `codcgr` varchar(10) NOT NULL,
  `codmind` varchar(10) NOT NULL,
  `mostrar_metas` char(1) NOT NULL DEFAULT 'N',
  `mostrar_composicao` char(1) NOT NULL,
  PRIMARY KEY (`coddgi`),
  KEY `codind` (`codind`),
  KEY `codtgraf` (`codtgraf`),
  KEY `codcgr` (`codcgr`),
  KEY `codmind` (`codmind`),
  KEY `codgi` (`codgi`),
  KEY `coddind` (`coddind`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_graficos_ind`
-- Table structure for table `canais`
--

DROP TABLE IF EXISTS `canais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `canais` (
  `codcnl` varchar(10) NOT NULL,
  `codtcnl` varchar(10) NOT NULL,
  `codfcnl` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `codgcnl` varchar(10) NOT NULL,
  `nome_cnl` varchar(50) NOT NULL,
  `nro_cnl` int(4) unsigned NOT NULL,
  `codigo_cas` varchar(50) NOT NULL,
  `valor_cnl` float(10,2) NOT NULL,
  `nivel` char(2) NOT NULL,
  `seac` varchar(30) NOT NULL,
  `ppv` char(1) NOT NULL DEFAULT 'N',
  `imagem_p` mediumtext NOT NULL,
  `imagem_g` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcnl`),
  KEY `codtcnl` (`codtcnl`),
  KEY `codfcnl` (`codfcnl`),
  KEY `codsad` (`codsad`),
  KEY `codgcnl` (`codgcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canais`
-- Table structure for table `inf_nota_fiscal`
--

DROP TABLE IF EXISTS `inf_nota_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inf_nota_fiscal` (
  `codinf` char(10) NOT NULL,
  `codnf` char(10) NOT NULL,
  `usar_composicao` char(1) NOT NULL,
  `modfrete` char(1) NOT NULL,
  `nro_protocolo_devol` varchar(10) NOT NULL,
  `outros_despesas` decimal(10,2) NOT NULL,
  `obs_adicional` mediumtext NOT NULL,
  PRIMARY KEY (`codinf`),
  KEY `codnf` (`codnf`),
  KEY `nro_protocolo_devol` (`nro_protocolo_devol`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inf_nota_fiscal`
-- Table structure for table `servidor_drm`
--

DROP TABLE IF EXISTS `servidor_drm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidor_drm` (
  `coddrm` varchar(10) NOT NULL,
  `codservp` varchar(10) DEFAULT NULL,
  `descri_drm` varchar(50) DEFAULT NULL,
  `porta` char(6) DEFAULT NULL,
  PRIMARY KEY (`coddrm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidor_drm`
-- Table structure for table `franquia_ser_nav`
--

DROP TABLE IF EXISTS `franquia_ser_nav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franquia_ser_nav` (
  `codfsn` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codvel` varchar(10) NOT NULL,
  `quant_mensal` int(6) unsigned NOT NULL,
  `codutfg` varchar(10) NOT NULL,
  `acao` char(1) NOT NULL DEFAULT 'C',
  `confirmar_usuario` char(1) NOT NULL DEFAULT 'N',
  `datas_venc` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codfsn`),
  KEY `codser` (`codser`),
  KEY `codvel` (`codvel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `franquia_ser_nav`
-- Table structure for table `tipo_enlace`
--

DROP TABLE IF EXISTS `tipo_enlace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_enlace` (
  `codtenl` varchar(10) NOT NULL,
  `descri_tenl` varchar(50) NOT NULL,
  PRIMARY KEY (`codtenl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_enlace`
-- Table structure for table `macros_comandos`
--

DROP TABLE IF EXISTS `macros_comandos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `macros_comandos` (
  `codmac` varchar(10) NOT NULL DEFAULT '',
  `macro` varchar(20) NOT NULL DEFAULT '',
  `descri_mac` varchar(50) NOT NULL DEFAULT '',
  `valor_mac` varchar(50) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'W',
  PRIMARY KEY (`codmac`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `macros_comandos`
-- Table structure for table `envio_sms`
--

DROP TABLE IF EXISTS `envio_sms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `envio_sms` (
  `codesms` varchar(10) NOT NULL,
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL,
  `codpros` varchar(10) NOT NULL,
  `codpint` char(10) NOT NULL DEFAULT '',
  `from_phone` varchar(13) NOT NULL DEFAULT '',
  `to_phone` text NOT NULL,
  `message` varchar(500) NOT NULL,
  `schedule` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `enviado` char(1) NOT NULL DEFAULT 'N',
  `codigo_externo` varchar(50) NOT NULL DEFAULT '',
  `rotina_sistema` varchar(50) DEFAULT '',
  `obs_sms` longtext,
  PRIMARY KEY (`codesms`),
  KEY `data` (`data`),
  KEY `codusu` (`codusu`),
  KEY `codcli` (`codcli`),
  KEY `codpros` (`codpros`),
  KEY `enviado` (`enviado`),
  KEY `codpint` (`codpint`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `envio_sms`
-- Table structure for table `dicionario_server`
--

DROP TABLE IF EXISTS `dicionario_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dicionario_server` (
  `codds` varchar(10) NOT NULL DEFAULT '',
  `codtservp` varchar(10) NOT NULL DEFAULT '',
  `atributo` varchar(50) NOT NULL DEFAULT '',
  `descri_ds` varchar(50) NOT NULL DEFAULT '',
  `valor_padrao` varchar(30) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `formato` char(1) NOT NULL DEFAULT '',
  `char_separacao` char(1) NOT NULL DEFAULT '',
  `mostrar` char(1) NOT NULL DEFAULT 'N',
  `editavel` char(1) NOT NULL DEFAULT 'N',
  `nome_api` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codds`),
  KEY `codtservp` (`codtservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dicionario_server`
-- Table structure for table `item_oco_vin`
--

DROP TABLE IF EXISTS `item_oco_vin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_oco_vin` (
  `codicov` char(10) NOT NULL DEFAULT '',
  `codoco` char(10) NOT NULL DEFAULT '',
  `codigo` char(10) NOT NULL DEFAULT '',
  `codigo_vin` char(10) NOT NULL DEFAULT '',
  `tabela` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codicov`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_oco_vin`
-- Table structure for table `usu_alerta`
--

DROP TABLE IF EXISTS `usu_alerta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_alerta` (
  `coduale` char(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codale` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coduale`),
  KEY `codusu` (`codusu`),
  KEY `codale` (`codale`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_alerta`
-- Table structure for table `parametros_doc`
--

DROP TABLE IF EXISTS `parametros_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parametros_doc` (
  `codpdoc` varchar(10) NOT NULL DEFAULT '',
  `coddoc` varchar(10) NOT NULL DEFAULT '',
  `nome_var` varchar(50) NOT NULL DEFAULT '',
  `nome_param` varchar(20) NOT NULL DEFAULT '',
  `valor_exemplo` varchar(30) NOT NULL,
  PRIMARY KEY (`codpdoc`),
  KEY `coddoc` (`coddoc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_doc`
-- Table structure for table `planejamento_fin_emp`
--

DROP TABLE IF EXISTS `planejamento_fin_emp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `planejamento_fin_emp` (
  `detplanemp` char(45) NOT NULL,
  `codplafin` char(10) NOT NULL,
  `codemp` char(10) NOT NULL,
  PRIMARY KEY (`detplanemp`),
  KEY `codemp` (`codemp`),
  KEY `codplafin` (`codplafin`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planejamento_fin_emp`
-- Table structure for table `vlan_pon`
--

DROP TABLE IF EXISTS `vlan_pon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vlan_pon` (
  `codvpolt` varchar(10) NOT NULL,
  `codpolt` varchar(10) NOT NULL,
  `codvolt` varchar(10) NOT NULL,
  PRIMARY KEY (`codvpolt`),
  KEY `codpolt` (`codpolt`),
  KEY `codvolt` (`codvolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vlan_pon`
-- Table structure for table `fotografias_cpag`
--

DROP TABLE IF EXISTS `fotografias_cpag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fotografias_cpag` (
  `codfcp` varchar(10) NOT NULL,
  `codfot` varchar(10) NOT NULL,
  `codcpag` varchar(10) NOT NULL,
  PRIMARY KEY (`codfcp`),
  KEY `codfot` (`codfot`),
  KEY `codcpag` (`codcpag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fotografias_cpag`
-- Table structure for table `afiliados`
--

DROP TABLE IF EXISTS `afiliados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `afiliados` (
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `sistema_a` char(1) NOT NULL DEFAULT '',
  `nome_afi` varchar(30) NOT NULL DEFAULT '',
  `razao_social` varchar(30) NOT NULL DEFAULT '',
  `contato` varchar(20) NOT NULL DEFAULT '',
  `cidade` varchar(10) NOT NULL DEFAULT '',
  `dominio_padrao` varchar(20) NOT NULL DEFAULT '',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `data_base` varchar(20) NOT NULL DEFAULT '',
  `login` varchar(20) NOT NULL DEFAULT '',
  `senha` varchar(15) NOT NULL DEFAULT '',
  `porta` varchar(4) NOT NULL DEFAULT '',
  `senha_adm` varchar(10) NOT NULL DEFAULT '',
  `login_r` varchar(30) NOT NULL DEFAULT '',
  `senha_r` varchar(30) NOT NULL DEFAULT '',
  `ip_r` varchar(15) NOT NULL DEFAULT '',
  `data_base_r` varchar(20) NOT NULL DEFAULT '',
  `porta_r` varchar(4) NOT NULL DEFAULT '',
  `senha_adm_r` varchar(10) NOT NULL DEFAULT '',
  `isp` char(1) NOT NULL DEFAULT 'N',
  `senha_inst` varchar(25) NOT NULL DEFAULT '',
  `ip_manager` varchar(15) NOT NULL DEFAULT '',
  `data_base_m` varchar(20) NOT NULL DEFAULT '',
  `porta_manager` varchar(4) NOT NULL DEFAULT '',
  `login_manager` varchar(15) NOT NULL DEFAULT '',
  `senha_manager` varchar(15) NOT NULL DEFAULT '',
  `senha_adm_m` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codafi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `afiliados`
-- Table structure for table `grupo_cobrancas`
--

DROP TABLE IF EXISTS `grupo_cobrancas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_cobrancas` (
  `codgcob` varchar(10) NOT NULL,
  `codrcob` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `descri_gcob` varchar(100) NOT NULL,
  `valores` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codgcob`),
  KEY `codrcob` (`codrcob`),
  KEY `codtab` (`codtab`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_cobrancas`
-- Table structure for table `erros_apis`
--

DROP TABLE IF EXISTS `erros_apis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `erros_apis` (
  `coderro` int(12) unsigned NOT NULL,
  `descri_erro` varchar(125) NOT NULL,
  `messagem_padrao` text NOT NULL,
  `url_wiki` varchar(250) NOT NULL,
  PRIMARY KEY (`coderro`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Contem os codigos de erro de API';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `erros_apis`
-- Table structure for table `contas_pag`
--

DROP TABLE IF EXISTS `contas_pag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_pag` (
  `codcpag` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codban` varchar(10) NOT NULL,
  `codcomp` char(4) NOT NULL,
  `codtmov` varchar(10) NOT NULL,
  `codpar` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codfpf` varchar(10) NOT NULL,
  `codtpf` varchar(10) NOT NULL,
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `data_ass` date NOT NULL,
  `codigo_barras` varchar(50) NOT NULL,
  `linha_digitavel` varchar(50) NOT NULL,
  `status_cpag` varchar(10) NOT NULL,
  `assinatura` varchar(100) NOT NULL,
  `nro_nta_fiscal` varchar(15) NOT NULL,
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_fat` date NOT NULL,
  `parcela` varchar(5) NOT NULL DEFAULT '',
  `data_bai` date NOT NULL DEFAULT '0000-00-00',
  `histo_pag` varchar(100) NOT NULL DEFAULT '',
  `valor_lan` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_pag` decimal(10,2) NOT NULL DEFAULT '0.00',
  `registro_comissao` char(1) NOT NULL DEFAULT 'N',
  `observacoes` mediumtext NOT NULL,
  `obs_reprovacao` mediumtext NOT NULL,
  PRIMARY KEY (`codcpag`),
  KEY `codfor` (`codfor`),
  KEY `data_ven` (`data_ven`),
  KEY `codban` (`codban`),
  KEY `codcomp` (`codcomp`),
  KEY `codpop` (`codpop`),
  KEY `codpar` (`codpar`),
  KEY `codusu` (`codusu`),
  KEY `codfpf` (`codfpf`),
  KEY `codtpf` (`codtpf`),
  KEY `status_cpag` (`status_cpag`),
  KEY `codtmov` (`codtmov`),
  KEY `codctc` (`codctc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_pag`
-- Table structure for table `status_contas_rec`
--

DROP TABLE IF EXISTS `status_contas_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_contas_rec` (
  `codscr` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `codstse` varchar(10) NOT NULL,
  `codacob` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  PRIMARY KEY (`codscr`),
  KEY `codcrec` (`codcrec`),
  KEY `codstse` (`codstse`),
  KEY `codacob` (`codacob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_contas_rec`
-- Table structure for table `dici_tipo_produto`
--

DROP TABLE IF EXISTS `dici_tipo_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dici_tipo_produto` (
  `coddicitprod` char(10) NOT NULL,
  `descricao` varchar(50) DEFAULT NULL,
  `ativo` char(1) DEFAULT 'S',
  PRIMARY KEY (`coddicitprod`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dici_tipo_produto`
-- Table structure for table `unidades_trafego`
--

DROP TABLE IF EXISTS `unidades_trafego`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades_trafego` (
  `codutfg` varchar(10) NOT NULL DEFAULT '',
  `descri_utfg` varchar(50) NOT NULL DEFAULT '',
  `abreviado` char(4) NOT NULL DEFAULT '',
  `formula` varchar(50) NOT NULL,
  `ordem` int(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codutfg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_trafego`
-- Table structure for table `motivo_visita`
--

DROP TABLE IF EXISTS `motivo_visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motivo_visita` (
  `codmvis` varchar(10) NOT NULL,
  `descri_mvis` varchar(50) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codmvis`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivo_visita`
-- Table structure for table `troca_status_oco`
--

DROP TABLE IF EXISTS `troca_status_oco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `troca_status_oco` (
  `codtso` int(8) NOT NULL AUTO_INCREMENT,
  `codoco` varchar(10) NOT NULL,
  `codsto_n` varchar(10) NOT NULL,
  `codsto_a` varchar(10) NOT NULL,
  `codusu` varchar(2) NOT NULL,
  `data` datetime NOT NULL,
  PRIMARY KEY (`codtso`),
  UNIQUE KEY `codtso` (`codtso`),
  KEY `codoco` (`codoco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `troca_status_oco`
-- Table structure for table `conf_habilitacao_prov_velocidade`
--

DROP TABLE IF EXISTS `conf_habilitacao_prov_velocidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_habilitacao_prov_velocidade` (
  `codchprovvel` char(10) NOT NULL,
  `dias_central` int(2) unsigned NOT NULL DEFAULT '2',
  `dias_web` int(2) unsigned NOT NULL DEFAULT '2',
  `dias_desk` int(2) unsigned NOT NULL DEFAULT '2',
  PRIMARY KEY (`codchprovvel`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_habilitacao_prov_velocidade`
-- Table structure for table `remessa_arquivos_fisco`
--

DROP TABLE IF EXISTS `remessa_arquivos_fisco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `remessa_arquivos_fisco` (
  `codraf` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL DEFAULT '',
  `data_hora` datetime NOT NULL,
  `nome_raf` varchar(20) NOT NULL DEFAULT '',
  `referencia` varchar(4) NOT NULL DEFAULT '',
  `numero_ini` int(6) unsigned NOT NULL,
  `numero_fim` int(6) unsigned NOT NULL,
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `valor_total` float(10,2) NOT NULL,
  `base_calculo` float(10,2) NOT NULL,
  `icms` float(10,2) NOT NULL,
  `isentos` float(10,2) NOT NULL,
  `outros` float(10,2) NOT NULL,
  `descontos` float(10,2) NOT NULL,
  `quant_nf` int(6) unsigned NOT NULL,
  `versao` char(4) NOT NULL DEFAULT '',
  PRIMARY KEY (`codraf`),
  KEY `codemp` (`codemp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remessa_arquivos_fisco`
-- Table structure for table `cargo_contato_cli`
--

DROP TABLE IF EXISTS `cargo_contato_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargo_contato_cli` (
  `codccc` varchar(10) NOT NULL,
  `descri_ccc` varchar(50) NOT NULL,
  `ativo` char(1) NOT NULL,
  PRIMARY KEY (`codccc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargo_contato_cli`
-- Table structure for table `pacotes_eppv`
--

DROP TABLE IF EXISTS `pacotes_eppv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pacotes_eppv` (
  `codpep` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  `codeppv` varchar(10) NOT NULL,
  `codtppv` varchar(10) NOT NULL,
  `obrigatorio` char(1) NOT NULL,
  PRIMARY KEY (`codpep`),
  KEY `codpac` (`codpac`),
  KEY `codeppv` (`codeppv`),
  KEY `codtppv` (`codtppv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacotes_eppv`
-- Table structure for table `equipamentos_rede_servicos`
--

DROP TABLE IF EXISTS `equipamentos_rede_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipamentos_rede_servicos` (
  `codeqrserv` varchar(10) NOT NULL,
  `codeqr` varchar(10) DEFAULT NULL,
  `codeqrtserv` varchar(10) DEFAULT NULL,
  `versao` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`codeqrserv`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos_rede_servicos`
-- Table structure for table `upd_cliente`
--

DROP TABLE IF EXISTS `upd_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `upd_cliente` (
  `codagu` char(10) NOT NULL,
  `nro_lic` int(5) NOT NULL,
  KEY ```codagu``` (`codagu`),
  KEY ```nro_lic``` (`nro_lic`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `upd_cliente`
-- Table structure for table `ocop_cargos`
--

DROP TABLE IF EXISTS `ocop_cargos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocop_cargos` (
  `codocar` varchar(10) NOT NULL,
  `codcar` varchar(10) NOT NULL,
  `codocop` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL,
  PRIMARY KEY (`codocar`),
  KEY `codcar` (`codcar`),
  KEY `codocop` (`codocop`),
  KEY `tipo` (`tipo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocop_cargos`
-- Table structure for table `cotacoes`
--

DROP TABLE IF EXISTS `cotacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cotacoes` (
  `codcot` varchar(10) NOT NULL DEFAULT '',
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codprod` varchar(10) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL DEFAULT '0.00',
  `garantia` int(3) unsigned NOT NULL DEFAULT '0',
  `moeda` varchar(10) NOT NULL DEFAULT 'Real',
  `data_cad` date NOT NULL,
  `data_fim` date NOT NULL DEFAULT '0000-00-00',
  `url` varchar(50) NOT NULL,
  `obs` text NOT NULL,
  PRIMARY KEY (`codcot`),
  KEY `codfor` (`codfor`),
  KEY `codprod` (`codprod`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotacoes`
-- Table structure for table `grupos_grids`
--

DROP TABLE IF EXISTS `grupos_grids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupos_grids` (
  `codggrd` varchar(10) NOT NULL,
  `codgrd` varchar(10) NOT NULL,
  `codcgrd` varchar(10) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `fonte_grupo` varchar(50) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `contar` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codggrd`),
  KEY `codgrd` (`codgrd`),
  KEY `codcgrd` (`codcgrd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_grids`
-- Table structure for table `estacoes_cidades`
--

DROP TABLE IF EXISTS `estacoes_cidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estacoes_cidades` (
  `codecid` varchar(10) NOT NULL,
  `codesici` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `codigo_ibge` varchar(10) NOT NULL,
  PRIMARY KEY (`codecid`),
  KEY `codesici` (`codesici`),
  KEY `cidade` (`cidade`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacoes_cidades`
-- Table structure for table `contatos_cliente`
--

DROP TABLE IF EXISTS `contatos_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contatos_cliente` (
  `codco_cl` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `codtco_cl` varchar(10) NOT NULL DEFAULT '',
  `data_cad` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codpar` varchar(10) NOT NULL,
  `codprf` varchar(10) NOT NULL,
  `codccc` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `nome_co_cl` varchar(50) NOT NULL DEFAULT '',
  `cargo` varchar(30) NOT NULL DEFAULT '',
  `e_mail` varchar(200) NOT NULL,
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `sms` char(1) NOT NULL DEFAULT 'N',
  `movil` varchar(8) NOT NULL,
  `cpf` varchar(14) NOT NULL DEFAULT '',
  `rg` varchar(20) NOT NULL,
  `data_nac` date NOT NULL DEFAULT '0000-00-00',
  `sexo` char(1) NOT NULL,
  `estado_civil` char(1) NOT NULL,
  `obs` text NOT NULL,
  `nome_mae` varchar(50) NOT NULL DEFAULT '',
  `nome_pai` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(100) NOT NULL DEFAULT '',
  `lembrar_senha` varchar(100) NOT NULL DEFAULT '',
  `mudar_senha` char(1) NOT NULL DEFAULT 'N',
  `acesso_central` char(1) NOT NULL DEFAULT '',
  `codco_cl_p` char(10) NOT NULL DEFAULT '',
  `nome_social` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codco_cl`),
  KEY `codcli` (`codcli`),
  KEY `data_cad` (`data_cad`),
  KEY `codpros` (`codpros`),
  KEY `codtco_cl` (`codtco_cl`),
  KEY `codpar` (`codpar`),
  KEY `codprf` (`codprf`),
  KEY `codccc` (`codccc`),
  KEY `ativo` (`ativo`),
  KEY `ddd` (`ddd`),
  KEY `fone` (`fone`),
  KEY `fax` (`fax`),
  KEY `celular` (`celular`),
  KEY `sms` (`sms`),
  KEY `codco_cl_p` (`codco_cl_p`),
  KEY `e_mail` (`e_mail`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contatos_cliente`
-- Table structure for table `int_servicos_poolip`
--

DROP TABLE IF EXISTS `int_servicos_poolip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_servicos_poolip` (
  `codintservpi` varchar(10) NOT NULL,
  `codservint` varchar(10) DEFAULT NULL,
  `codaip` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codintservpi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_servicos_poolip`
-- Table structure for table `autorizacao_sc`
--

DROP TABLE IF EXISTS `autorizacao_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `autorizacao_sc` (
  `codasc` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `autorizado` char(1) NOT NULL,
  `data` datetime NOT NULL,
  `ip` varchar(100) NOT NULL,
  `motivo` mediumtext NOT NULL,
  PRIMARY KEY (`codasc`),
  KEY `codsercli` (`codsercli`),
  KEY `codusu` (`codusu`),
  KEY `autorizado` (`autorizado`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autorizacao_sc`
-- Table structure for table `dicionario_mikrotik`
--

DROP TABLE IF EXISTS `dicionario_mikrotik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dicionario_mikrotik` (
  `coddcmkt` varchar(10) NOT NULL DEFAULT '',
  `versao_mkt` char(1) NOT NULL DEFAULT '',
  `comando` varchar(250) DEFAULT '',
  `descri_dcmkt` varchar(20) DEFAULT '',
  `valor_padrao` varchar(250) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddcmkt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dicionario_mikrotik`
-- Table structure for table `controle_mov_pat_bkp`
--

DROP TABLE IF EXISTS `controle_mov_pat_bkp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controle_mov_pat_bkp` (
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codusu_g` char(2) NOT NULL DEFAULT '',
  `codusu_t` char(2) NOT NULL DEFAULT '',
  `codusu_c` char(2) NOT NULL DEFAULT '',
  `codlmp_o` char(10) NOT NULL DEFAULT '',
  `confirmado` char(1) NOT NULL DEFAULT '',
  `numero` int(6) NOT NULL DEFAULT '0',
  `code_f` varchar(10) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcmp`),
  KEY `codusu_t` (`codusu_t`),
  KEY `codusu_c` (`codusu_c`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controle_mov_pat_bkp`
-- Table structure for table `ip_interfaces`
--

DROP TABLE IF EXISTS `ip_interfaces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ip_interfaces` (
  `codipi` varchar(10) NOT NULL,
  `codinte` varchar(10) NOT NULL,
  `ip` varchar(18) NOT NULL,
  `classe` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codipi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_interfaces`
-- Table structure for table `familia_canais`
--

DROP TABLE IF EXISTS `familia_canais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `familia_canais` (
  `codfcnl` varchar(10) NOT NULL,
  `codgcnl` varchar(10) NOT NULL,
  `descri_fcnl` varchar(50) NOT NULL,
  `ordem` int(1) unsigned NOT NULL,
  `codigo_cas` varchar(50) DEFAULT '',
  PRIMARY KEY (`codfcnl`),
  KEY `codgcnl` (`codgcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `familia_canais`
-- Table structure for table `tipo_reajustes_contrato`
--

DROP TABLE IF EXISTS `tipo_reajustes_contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_reajustes_contrato` (
  `codtrejcon` varchar(10) NOT NULL,
  `descri_trejcon` varchar(50) NOT NULL,
  `descri_for` mediumtext NOT NULL,
  `formula_sql` text NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtrejcon`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_reajustes_contrato`
-- Table structure for table `busqueda`
--

DROP TABLE IF EXISTS `busqueda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `busqueda` (
  `codbus` varchar(10) NOT NULL DEFAULT '',
  `arquivo` varchar(4) NOT NULL DEFAULT '',
  `ordem` int(2) unsigned NOT NULL DEFAULT '0',
  `lbusq` varchar(20) NOT NULL DEFAULT '',
  `cbusq` varchar(100) NOT NULL,
  `campos` text NOT NULL,
  `mascara` varchar(20) NOT NULL DEFAULT '' COMMENT 'Máscara para ser aplicada no campo de pesquisa',
  PRIMARY KEY (`codbus`),
  KEY `arquivo` (`arquivo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `busqueda`
-- Table structure for table `historico_os`
--

DROP TABLE IF EXISTS `historico_os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_os` (
  `codhords` varchar(10) NOT NULL,
  `codords` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_hora` datetime NOT NULL,
  `ip` varchar(20) NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codhords`),
  KEY `codords` (`codords`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_os`
-- Table structure for table `ocorrencias_anexo`
--

DROP TABLE IF EXISTS `ocorrencias_anexo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocorrencias_anexo` (
  `codocoa` varchar(10) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `codvis` varchar(10) DEFAULT NULL,
  `codusu` varchar(10) DEFAULT '',
  `data` datetime NOT NULL,
  `hora` varchar(5) DEFAULT NULL,
  `nome_anexo` varchar(100) NOT NULL DEFAULT '',
  `anexo` mediumtext,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codocoa`),
  KEY `codoco` (`codoco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocorrencias_anexo`
-- Table structure for table `vlan_olt`
--

DROP TABLE IF EXISTS `vlan_olt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vlan_olt` (
  `codvolt` varchar(10) NOT NULL,
  `codolt` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT 'I',
  `vlan` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codvolt`),
  KEY `codolt` (`codolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vlan_olt`
-- Table structure for table `rotas_equipamentos_rede`
--

DROP TABLE IF EXISTS `rotas_equipamentos_rede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rotas_equipamentos_rede` (
  `codeqrrota` varchar(10) NOT NULL,
  `codeqr` varchar(10) DEFAULT NULL,
  `ip_dest` varchar(15) DEFAULT NULL,
  `mascara` varchar(15) DEFAULT NULL,
  `gateway` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`codeqrrota`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rotas_equipamentos_rede`
-- Table structure for table `grupo_elementos_mr`
--

DROP TABLE IF EXISTS `grupo_elementos_mr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_elementos_mr` (
  `codgemr` varchar(10) NOT NULL,
  `codimr` varchar(10) NOT NULL,
  `descri_gemr` varchar(30) NOT NULL,
  `titulo` varchar(20) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codgemr`),
  KEY `codimr` (`codimr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_elementos_mr`
-- Table structure for table `nota_fiscal`
--

DROP TABLE IF EXISTS `nota_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nota_fiscal` (
  `codnf` char(10) NOT NULL DEFAULT '',
  `codtnf` char(10) NOT NULL,
  `codemp` char(10) NOT NULL,
  `codraf` char(10) NOT NULL,
  `codrnf` char(10) NOT NULL,
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codmnf` char(10) NOT NULL DEFAULT '',
  `codfor` char(10) NOT NULL,
  `codemp_d` char(10) NOT NULL,
  `codigo_cnf` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `data_cad` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codnf_o` char(10) NOT NULL,
  `cfop` char(10) NOT NULL,
  `serie_nf` char(4) NOT NULL DEFAULT '',
  `numero_nf` int(9) NOT NULL DEFAULT '0',
  `data_lan` date NOT NULL,
  `data_can` date NOT NULL,
  `nro_protocolo` varchar(50) NOT NULL,
  `nro_recibo` varchar(20) NOT NULL,
  `valor_nf` decimal(10,2) NOT NULL DEFAULT '0.00',
  `base_icms` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_icms` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_fust` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_funtel` decimal(8,2) NOT NULL DEFAULT '0.00',
  `base_iss` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_iss` decimal(8,2) NOT NULL DEFAULT '0.00',
  `base_pis` decimal(8,2) NOT NULL,
  `valor_pis` decimal(8,2) NOT NULL DEFAULT '0.00',
  `base_cofins` decimal(8,2) NOT NULL,
  `valor_cofins` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_ipi` decimal(8,2) NOT NULL,
  `base_iva` decimal(10,2) NOT NULL,
  `valor_iva` decimal(10,2) NOT NULL,
  `valor_simp` decimal(8,2) NOT NULL DEFAULT '0.00',
  `identificacao` varchar(39) NOT NULL DEFAULT '',
  `cancelada` char(1) NOT NULL DEFAULT 'N',
  `credito` char(1) NOT NULL DEFAULT 'N',
  `xml` mediumtext NOT NULL,
  `nome_nf` varchar(100) NOT NULL,
  `link_pdf` varchar(250) NOT NULL,
  `obs` mediumtext NOT NULL,
  `codrtrib` char(10) NOT NULL COMMENT ' referente a tabela nova de registro_tributacao',
  `obs_fiscal` mediumtext NOT NULL COMMENT 'Informação adicional fisco',
  `nota_referenciada` varchar(44) NOT NULL DEFAULT '' COMMENT 'Referenciar uma Nota Fiscal Eletrônica emitida anteriormente, vinculada a NF-e atual.',
  `valor_outras_despesas` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Outras despesas acessórias',
  `valor_seguro` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor total do seguro',
  `valor_desconto` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do desconto',
  `valor_frete` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor total do frete',
  `adic_outras_despesas` char(1) NOT NULL DEFAULT '' COMMENT 'adicionar outras dispesas',
  `adic_seguro` char(1) NOT NULL DEFAULT '' COMMENT 'adicionar seguro',
  `base_icms_st` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'base de calculo icms st',
  `valor_icms_st` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor icms st',
  `valor_ipi_devolvido` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor ipi devolvido',
  `valor_total_produtos` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor total de produtos',
  `valor_ipi_devol` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do IPI de Devolução de Produtos.',
  PRIMARY KEY (`codnf`),
  UNIQUE KEY `codigo_cnf` (`codigo_cnf`),
  KEY `codcli` (`codcli`),
  KEY `codmnf` (`codmnf`),
  KEY `codrnf` (`codrnf`),
  KEY `codraf` (`codraf`),
  KEY `codtnf` (`codtnf`),
  KEY `codemp` (`codemp`),
  KEY `data_cad` (`data_cad`),
  KEY `codfor` (`codfor`),
  KEY `codemp_d` (`codemp_d`),
  KEY `codnf_o` (`codnf_o`),
  KEY `cancelada` (`cancelada`),
  KEY `data_lan` (`data_lan`),
  KEY `numero_nf` (`numero_nf`),
  KEY `codrtrib` (`codrtrib`),
  KEY `ix_nota_fiscal_codnf_codtnd_codemp_codcli_data_lan` (`codnf`,`codtnf`,`codemp`,`codcli`,`data_lan`)
) ENGINE=InnoDB AUTO_INCREMENT=27839 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_fiscal`
-- Table structure for table `det_forma_cobranca`
--

DROP TABLE IF EXISTS `det_forma_cobranca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_forma_cobranca` (
  `coddcob` varchar(10) NOT NULL COMMENT 'Codigo do Detalhamento da Forma de Cobranca',
  `codcob` varchar(10) NOT NULL COMMENT 'Codigo da Forma de cobranca',
  `codban` varchar(10) NOT NULL COMMENT 'Codigo da Conta Financeira',
  `identificacao` varchar(30) NOT NULL COMMENT 'Identificacao da conta financeira no arquivo de retorno',
  `codcob_d` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddcob`),
  KEY `codcob` (`codcob`),
  KEY `codban` (`codban`),
  KEY `identificacao` (`identificacao`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_forma_cobranca`
-- Table structure for table `parametros_consulta`
--

DROP TABLE IF EXISTS `parametros_consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parametros_consulta` (
  `codpcst` varchar(10) NOT NULL,
  `codcst` varchar(10) DEFAULT NULL,
  `nome_parametro` varchar(50) DEFAULT NULL,
  `alias_parametro` varchar(5) DEFAULT NULL,
  `nome_exibe` varchar(50) DEFAULT NULL,
  `expressao` varchar(250) DEFAULT NULL,
  `obs` mediumtext,
  `operador` varchar(10) DEFAULT NULL,
  `obrigatorio` char(1) DEFAULT 'N',
  `tipo` char(1) DEFAULT NULL,
  `consulta` mediumtext,
  PRIMARY KEY (`codpcst`),
  KEY `codcst` (`codcst`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_consulta`
-- Table structure for table `tipo_contatos`
--

DROP TABLE IF EXISTS `tipo_contatos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_contatos` (
  `tipo_contato` char(1) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'A',
  `descri_tcon` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`tipo_contato`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_contatos`
-- Table structure for table `indicadores_radius`
--

DROP TABLE IF EXISTS `indicadores_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `indicadores_radius` (
  `codindrad` char(10) NOT NULL DEFAULT '',
  `codservp` char(10) NOT NULL DEFAULT '',
  `log_so` text,
  `log_radius` text,
  `porc_cpu` text,
  `porc_memoria` text,
  `porc_hd` text,
  `porc_particao_radius` text,
  `porc_particao_mysql` text,
  `tempo_log_so` char(10) NOT NULL DEFAULT '',
  `tempo_log_radius` char(10) NOT NULL DEFAULT '',
  `tempo_porc_cpu` char(10) NOT NULL DEFAULT '',
  `tempo_porc_memoria` char(10) NOT NULL DEFAULT '',
  `tempo_porc_hd` char(10) NOT NULL DEFAULT '',
  `tempo_porc_particao_radius` char(10) NOT NULL DEFAULT '',
  `tempo_porc_particao_mysql` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codindrad`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indicadores_radius`
-- Table structure for table `idiomas`
--

DROP TABLE IF EXISTS `idiomas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idiomas` (
  `codidm` varchar(10) NOT NULL,
  `idioma` varchar(20) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codidm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idiomas`
-- Table structure for table `servicos_ant`
--

DROP TABLE IF EXISTS `servicos_ant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_ant` (
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codgser` varchar(10) NOT NULL DEFAULT '',
  `descri_ser` varchar(50) NOT NULL DEFAULT '',
  `formula` text NOT NULL,
  `tipo_pag` char(1) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codest` varchar(10) NOT NULL DEFAULT '',
  `horas` int(6) unsigned NOT NULL DEFAULT '0',
  `d_trail` int(3) unsigned NOT NULL DEFAULT '0',
  `obs` text NOT NULL,
  `quant_emails` int(2) unsigned NOT NULL DEFAULT '0',
  `valor_excedente` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `valor_email_adicional` decimal(5,2) NOT NULL DEFAULT '0.00',
  `quota_email` decimal(5,2) NOT NULL DEFAULT '0.00',
  `permite_email` char(1) NOT NULL DEFAULT '',
  `codservp_e` varchar(10) NOT NULL DEFAULT '',
  `autentica_radius` char(1) NOT NULL DEFAULT '',
  `codservp_r` varchar(10) NOT NULL DEFAULT '',
  `salva_c_dominio` char(1) NOT NULL DEFAULT 'N',
  `grupo_radius` varchar(15) NOT NULL DEFAULT '',
  `permite_dominio` char(1) NOT NULL DEFAULT '',
  `codservp_w` varchar(10) NOT NULL DEFAULT '',
  `servico_ivr` char(1) NOT NULL DEFAULT 'N',
  `ivr_down` int(6) NOT NULL DEFAULT '0',
  `ivr_up` int(6) unsigned NOT NULL DEFAULT '0',
  `comissao_vendedor` decimal(7,2) NOT NULL DEFAULT '0.00',
  `valor_fixo_comissao` char(1) NOT NULL DEFAULT '',
  `grafico` varchar(20) NOT NULL DEFAULT '',
  `web` char(1) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `cob_adiantada` char(1) NOT NULL DEFAULT '',
  `pontos_ser` decimal(5,2) NOT NULL DEFAULT '0.00',
  `obs_web` text NOT NULL,
  `valor_web` decimal(7,2) NOT NULL DEFAULT '0.00',
  `habi_web` decimal(7,5) NOT NULL DEFAULT '0.00000',
  PRIMARY KEY (`codser`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_ant`
-- Table structure for table `nota_fiscal_adi`
--

DROP TABLE IF EXISTS `nota_fiscal_adi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nota_fiscal_adi` (
  `codnf` char(10) NOT NULL,
  `outras_dispesas` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_seguro` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_desconto` decimal(10,2) NOT NULL DEFAULT '0.00',
  `nf_refen` varchar(50) NOT NULL DEFAULT '',
  `adc_out_dispesa` char(1) NOT NULL DEFAULT 'N',
  `adc_seguro` char(1) NOT NULL DEFAULT 'N',
  `infadc` mediumtext NOT NULL,
  `infadcif` mediumtext NOT NULL,
  PRIMARY KEY (`codnf`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_fiscal_adi`
-- Table structure for table `cargos_opc`
--

DROP TABLE IF EXISTS `cargos_opc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargos_opc` (
  `codcaropc` varchar(10) NOT NULL,
  `codcar` varchar(10) DEFAULT NULL,
  `codopc` char(3) DEFAULT NULL,
  `pn` char(1) DEFAULT NULL,
  `pa` char(1) DEFAULT NULL,
  PRIMARY KEY (`codcaropc`),
  KEY `codcar` (`codcar`),
  KEY `codopc` (`codopc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos_opc`
-- Table structure for table `projetos`
--

DROP TABLE IF EXISTS `projetos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projetos` (
  `codprj` varchar(10) NOT NULL,
  `nome_projeto` varchar(70) NOT NULL,
  `produto` varchar(40) NOT NULL,
  `versao` varchar(9) NOT NULL,
  `andamento` int(2) DEFAULT NULL,
  PRIMARY KEY (`codprj`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
-- Table structure for table `execucao_provisionamentos_sc`
--

DROP TABLE IF EXISTS `execucao_provisionamentos_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execucao_provisionamentos_sc` (
  `codepsc` varchar(10) NOT NULL DEFAULT '',
  `codspsc` varchar(10) NOT NULL,
  `codextra` varchar(10) NOT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`codepsc`),
  KEY `codspsc` (`codspsc`),
  KEY `codextra` (`codextra`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `execucao_provisionamentos_sc`
-- Table structure for table `cfps`
--

DROP TABLE IF EXISTS `cfps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfps` (
  `codcfps` char(4) NOT NULL,
  `descri_cfps` varchar(100) NOT NULL,
  `retencao` char(1) NOT NULL,
  PRIMARY KEY (`codcfps`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cfps`
-- Table structure for table `estacoes_sici`
--

DROP TABLE IF EXISTS `estacoes_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estacoes_sici` (
  `codesici` varchar(10) NOT NULL,
  `nome_esici` varchar(50) NOT NULL,
  `numero_estacao` varchar(30) NOT NULL,
  `codigo_ibge` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codesici`),
  KEY `cidade` (`cidade`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacoes_sici`
-- Table structure for table `tempo_captura_ind`
--

DROP TABLE IF EXISTS `tempo_captura_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tempo_captura_ind` (
  `codtci` varchar(10) NOT NULL,
  `descri_tci` varchar(30) NOT NULL,
  `minutos` int(8) NOT NULL,
  PRIMARY KEY (`codtci`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tempo_captura_ind`
-- Table structure for table `det_nota_fiscal_n`
--

DROP TABLE IF EXISTS `det_nota_fiscal_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_nota_fiscal_n` (
  `coddnf` varchar(10) NOT NULL DEFAULT '',
  `codnf` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `coddes` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  `codrimp` varchar(10) NOT NULL,
  `descri_nf` varchar(120) NOT NULL,
  `base_icms` float(10,2) NOT NULL,
  `valor_icms` float(7,2) NOT NULL,
  `valor_fust` float(7,2) NOT NULL,
  `valor_funtel` float(7,2) NOT NULL,
  `base_iss` float(10,2) NOT NULL,
  `valor_iss` float(7,2) NOT NULL,
  `valor_ipi` float(7,2) NOT NULL,
  `base_iva` float(10,2) NOT NULL,
  `valor_iva` float(10,2) NOT NULL,
  `valor_simp` float(10,2) NOT NULL,
  PRIMARY KEY (`coddnf`),
  KEY `codnf` (`codnf`),
  KEY `codcrec` (`codcrec`),
  KEY `codpat` (`codpat`),
  KEY `codrimp` (`codrimp`),
  KEY `coddes` (`coddes`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_nota_fiscal_n`
-- Table structure for table `oco_central`
--

DROP TABLE IF EXISTS `oco_central`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oco_central` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codocop` varchar(10) DEFAULT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `descricao` varchar(250) DEFAULT NULL,
  `id_pai` int(11) DEFAULT NULL,
  `tipo` int(11) DEFAULT NULL,
  `listar` char(1) NOT NULL DEFAULT 'N',
  `fechar` char(1) NOT NULL DEFAULT 'N',
  `criar` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oco_central`
-- Table structure for table `servicos_pant`
--

DROP TABLE IF EXISTS `servicos_pant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_pant` (
  `codpant` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `dia_mes` int(2) unsigned NOT NULL DEFAULT '0',
  `dias_antes` int(3) unsigned NOT NULL DEFAULT '0',
  `porcentagem` float(8,4) NOT NULL DEFAULT '0.0000',
  `valor_desc` float(12,4) NOT NULL DEFAULT '0.0000',
  `absoluto` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codpant`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_pant`
-- Table structure for table `estacao_radio`
--

DROP TABLE IF EXISTS `estacao_radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estacao_radio` (
  `codeb` varchar(10) NOT NULL DEFAULT '',
  `nome_eb` varchar(50) NOT NULL DEFAULT '',
  `latitude` decimal(9,5) NOT NULL DEFAULT '0.00000',
  `longitude` decimal(9,5) NOT NULL DEFAULT '0.00000',
  `alt` decimal(5,2) NOT NULL DEFAULT '0.00',
  `modelo_r` int(2) unsigned NOT NULL DEFAULT '0',
  `mac` varchar(7) NOT NULL DEFAULT '',
  `serial` varchar(15) NOT NULL DEFAULT '',
  `tipo_r` int(1) unsigned NOT NULL DEFAULT '0',
  `tipo_estacao` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codeb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacao_radio`
-- Table structure for table `conf_radius`
--

DROP TABLE IF EXISTS `conf_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_radius` (
  `codcnfr` varchar(10) NOT NULL DEFAULT '',
  `codcrad` varchar(20) NOT NULL DEFAULT '',
  `conf_name` varchar(50) NOT NULL DEFAULT '',
  `value` varbinary(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcnfr`,`codcrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_radius`
-- Table structure for table `turno`
--

DROP TABLE IF EXISTS `turno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turno` (
  `codtur` varchar(10) NOT NULL,
  `descri_tur` varchar(30) NOT NULL,
  PRIMARY KEY (`codtur`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turno`
-- Table structure for table `webservices`
--

DROP TABLE IF EXISTS `webservices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webservices` (
  `codweb` varchar(10) NOT NULL DEFAULT '',
  `descricao` varchar(30) NOT NULL DEFAULT '',
  `quant_p` int(2) unsigned NOT NULL DEFAULT '0',
  `consulta` text NOT NULL,
  PRIMARY KEY (`codweb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webservices`
-- Table structure for table `servicos_imp`
--

DROP TABLE IF EXISTS `servicos_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_imp` (
  `codsimp` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL,
  `codtnf` varchar(10) NOT NULL,
  `codcob` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codtser` varchar(10) NOT NULL,
  `codcif` char(4) NOT NULL DEFAULT '',
  `descri_simp` varchar(70) NOT NULL,
  `descri_nf` varchar(40) NOT NULL,
  `valor` decimal(10,3) NOT NULL DEFAULT '0.000',
  `icms` float(5,2) NOT NULL DEFAULT '0.00',
  `iss` float(5,2) NOT NULL,
  `fust` float(5,2) NOT NULL DEFAULT '0.00',
  `funtel` float(5,2) NOT NULL DEFAULT '0.00',
  `pis` float(5,2) NOT NULL DEFAULT '0.00',
  `cofins` float(5,2) NOT NULL,
  `iva` float(5,2) NOT NULL,
  `codigo_fiscal` varchar(6) NOT NULL,
  `retem_imposto` char(1) NOT NULL DEFAULT 'N',
  `itemsgroupcode` char(3) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codsimp`),
  KEY `codser` (`codser`),
  KEY `codemp` (`codemp`),
  KEY `codtnf` (`codtnf`),
  KEY `codcob` (`codcob`),
  KEY `codcta` (`codcta`),
  KEY `codtser` (`codtser`),
  KEY `codcif` (`codcif`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_imp`
-- Table structure for table `agenda_upd`
--

DROP TABLE IF EXISTS `agenda_upd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_upd` (
  `codagu` char(10) NOT NULL,
  `data_upd` datetime NOT NULL,
  `remove_arquivos` char(1) DEFAULT 'N',
  `ativo` char(1) DEFAULT 'N',
  `geral` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codagu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_upd`
-- Table structure for table `usu_pastas`
--

DROP TABLE IF EXISTS `usu_pastas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_pastas` (
  `codupas` varchar(10) NOT NULL DEFAULT '',
  `codpas` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `permissao` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codupas`),
  KEY `codpas` (`codpas`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_pastas`
-- Table structure for table `enquetes`
--

DROP TABLE IF EXISTS `enquetes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enquetes` (
  `codenq` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codperg` varchar(10) NOT NULL DEFAULT '',
  `codresp` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `obs` text NOT NULL,
  PRIMARY KEY (`codenq`),
  KEY `codcli` (`codcli`),
  KEY `codperg` (`codperg`),
  KEY `codresp` (`codresp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enquetes`
-- Table structure for table `servicos_cli_reaj`
--

DROP TABLE IF EXISTS `servicos_cli_reaj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_reaj` (
  `codscrj` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data` date NOT NULL,
  `data_ven` date NOT NULL,
  `validade` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codscrj`),
  KEY `codsercli` (`codsercli`),
  KEY `codusu` (`codusu`),
  KEY `data_ven` (`data_ven`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_reaj`
-- Table structure for table `faturamentos_ligacoes`
--

DROP TABLE IF EXISTS `faturamentos_ligacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturamentos_ligacoes` (
  `codflv` varchar(10) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL,
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codflv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturamentos_ligacoes`
-- Table structure for table `logs_apis`
--

DROP TABLE IF EXISTS `logs_apis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_apis` (
  `codlapi` int(11) NOT NULL AUTO_INCREMENT,
  `codusu` char(10) NOT NULL DEFAULT '',
  `integracao` varchar(50) NOT NULL DEFAULT '',
  `endereco_url` mediumtext NOT NULL,
  `envio` mediumtext NOT NULL,
  `retorno` mediumtext NOT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`codlapi`),
  KEY `codusu` (`codusu`),
  KEY `integracao` (`integracao`),
  KEY `data_hora` (`data_hora`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_apis`
-- Table structure for table `menus_telas`
--

DROP TABLE IF EXISTS `menus_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menus_telas` (
  `codmenu` varchar(10) NOT NULL,
  `codtel` varchar(10) NOT NULL,
  `codtmt` varchar(10) NOT NULL,
  `nome_menu` varchar(30) NOT NULL,
  `alias` varchar(10) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codmenu`),
  KEY `codtel` (`codtel`),
  KEY `codtmt` (`codtmt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus_telas`
-- Table structure for table `valores_creditos`
--

DROP TABLE IF EXISTS `valores_creditos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_creditos` (
  `codvcre` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `codvel` varchar(10) NOT NULL,
  `descri_vcre` varchar(50) NOT NULL DEFAULT '',
  `valor_lan` float(8,2) NOT NULL DEFAULT '0.00',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `valor_cre` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_par` float(8,2) NOT NULL,
  `tempo_cre` int(8) NOT NULL DEFAULT '0',
  `codutmp` varchar(10) NOT NULL DEFAULT '',
  `trafego_cre` int(8) NOT NULL DEFAULT '0',
  `codutfg` varchar(10) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `gerar_boleto` char(1) NOT NULL DEFAULT 'N',
  `prazo` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codvcre`),
  KEY `codsad` (`codsad`),
  KEY `codvel` (`codvel`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_creditos`
-- Table structure for table `promocoes`
--

DROP TABLE IF EXISTS `promocoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promocoes` (
  `codprom` varchar(10) NOT NULL,
  `codtprom` varchar(10) NOT NULL,
  `descri_prom` varchar(50) NOT NULL,
  `ativa` char(1) NOT NULL DEFAULT 'S',
  `valor` float(10,2) NOT NULL,
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `quantidade` int(3) unsigned NOT NULL,
  `recursivo` char(1) NOT NULL DEFAULT 'N',
  `funcionario` char(1) NOT NULL DEFAULT 'N',
  `proporcional` char(1) NOT NULL DEFAULT 'N',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codprom`),
  KEY `codtprom` (`codtprom`),
  KEY `ativa` (`ativa`),
  KEY `data_ini` (`data_ini`),
  KEY `data_fim` (`data_fim`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promocoes`
-- Table structure for table `combo_cidades`
--

DROP TABLE IF EXISTS `combo_cidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combo_cidades` (
  `codcombocid` char(10) NOT NULL,
  `combo_codcombo` char(10) NOT NULL,
  `cidades_cidade` char(10) NOT NULL,
  PRIMARY KEY (`codcombocid`),
  KEY `combo_codcombo` (`combo_codcombo`,`cidades_cidade`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo_cidades`
-- Table structure for table `changelog`
--

DROP TABLE IF EXISTS `changelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `changelog` (
  `codchl` char(10) NOT NULL DEFAULT '',
  `codver` char(7) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `interface` varchar(50) NOT NULL DEFAULT '',
  `data` date NOT NULL,
  `descri_chl` mediumtext NOT NULL,
  `exemplo` mediumtext NOT NULL,
  `desde` date DEFAULT NULL,
  `ate` date DEFAULT NULL,
  PRIMARY KEY (`codchl`),
  KEY `versao` (`codver`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `changelog`
-- Table structure for table `reten_impostos`
--

DROP TABLE IF EXISTS `reten_impostos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reten_impostos` (
  `codret` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `nro_nta_fiscal` varchar(10) NOT NULL DEFAULT '',
  `valor_nf` decimal(7,2) NOT NULL DEFAULT '0.00',
  `cofins` decimal(5,2) NOT NULL DEFAULT '0.00',
  `pis` decimal(5,2) NOT NULL DEFAULT '0.00',
  `csll` decimal(5,2) NOT NULL DEFAULT '0.00',
  `irr` decimal(5,2) NOT NULL DEFAULT '0.00',
  `data` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`codret`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reten_impostos`
-- Table structure for table `tipo_favorito`
--

DROP TABLE IF EXISTS `tipo_favorito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_favorito` (
  `codtfav` varchar(10) NOT NULL,
  `nome_tipo_favorito` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`codtfav`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_favorito`
-- Table structure for table `tipo_elem_desk_mr`
--

DROP TABLE IF EXISTS `tipo_elem_desk_mr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_elem_desk_mr` (
  `codtemr` varchar(10) NOT NULL,
  `descri_temr` varchar(50) NOT NULL,
  `shapetype` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  PRIMARY KEY (`codtemr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_elem_desk_mr`
-- Table structure for table `valores_dicionario_server`
--

DROP TABLE IF EXISTS `valores_dicionario_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_dicionario_server` (
  `codvds` varchar(10) NOT NULL DEFAULT '',
  `codds` varchar(10) NOT NULL DEFAULT '',
  `descri_vds` varchar(50) NOT NULL DEFAULT '',
  `valor` varchar(30) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codvds`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_dicionario_server`
-- Table structure for table `tabela_valor`
--

DROP TABLE IF EXISTS `tabela_valor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabela_valor` (
  `codigo` varchar(10) NOT NULL,
  `mostrar` varchar(30) NOT NULL,
  `tipo` char(2) NOT NULL,
  KEY `tipo` (`tipo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabela_valor`
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `codusu` char(2) NOT NULL DEFAULT '',
  `data_lan` datetime NOT NULL,
  `data_can` datetime NOT NULL,
  `codpar` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codcar_e` varchar(10) NOT NULL DEFAULT '',
  `codtec` varchar(10) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `coddep` varchar(10) NOT NULL,
  `codigo_externo` varchar(20) NOT NULL,
  `usuario_externo` varchar(50) NOT NULL,
  `codtur` varchar(10) NOT NULL,
  `adm_sistema` char(1) NOT NULL DEFAULT 'N',
  `login` varchar(10) NOT NULL DEFAULT '',
  `senha` int(10) NOT NULL DEFAULT '0',
  `contrasenha` varchar(10) NOT NULL DEFAULT '',
  `nome_usu` varchar(35) NOT NULL DEFAULT '' COMMENT '||-',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `ramal_ura` varchar(20) NOT NULL,
  `senha_ramal` varchar(30) NOT NULL,
  `endereco` varchar(30) NOT NULL DEFAULT '',
  `bairro` varchar(10) NOT NULL DEFAULT '',
  `cidade` varchar(15) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL,
  `fax` varchar(15) NOT NULL DEFAULT '',
  `bipper` char(3) NOT NULL DEFAULT '',
  `e_mail` varchar(60) NOT NULL,
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT '',
  `tecnico` char(1) NOT NULL DEFAULT '',
  `vendedor` char(1) NOT NULL DEFAULT '',
  `ver_cliente` char(1) NOT NULL DEFAULT 'T',
  `ver_prospect` char(1) NOT NULL DEFAULT 'T',
  `controla_email` char(1) NOT NULL DEFAULT '',
  `controla_oco_lem` char(1) NOT NULL DEFAULT '',
  `tempo_control` int(2) unsigned NOT NULL DEFAULT '0',
  `obs` text NOT NULL,
  `bloqueado` char(1) NOT NULL DEFAULT 'N',
  `codlmp` char(10) NOT NULL DEFAULT '',
  `data_troca_senha` date NOT NULL DEFAULT '0000-00-00',
  `id_funil` int(11) NOT NULL DEFAULT '0',
  `usu_img` mediumtext,
  PRIMARY KEY (`codusu`),
  KEY `codven` (`codven`),
  KEY `codpar` (`codpar`),
  KEY `codtec` (`codtec`),
  KEY `usuario_externo` (`usuario_externo`),
  KEY `codlmp` (`codlmp`),
  KEY `data_troca_senha` (`data_troca_senha`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
-- Table structure for table `historico_status`
--

DROP TABLE IF EXISTS `historico_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_status` (
  `codhest` varchar(10) NOT NULL,
  `codest` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_hora` datetime NOT NULL,
  `ip` varchar(50) NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codhest`),
  KEY `codcpag` (`codest`),
  KEY `codusu` (`codusu`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_status`
-- Table structure for table `tipo_arquivo`
--

DROP TABLE IF EXISTS `tipo_arquivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_arquivo` (
  `codtarq` varchar(10) NOT NULL DEFAULT '',
  `descri_tarq` varchar(50) NOT NULL DEFAULT '',
  `extensao` varchar(4) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtarq`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_arquivo`
-- Table structure for table `campo_forma_cob`
--

DROP TABLE IF EXISTS `campo_forma_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campo_forma_cob` (
  `codcampfc` char(10) NOT NULL,
  `nro_ban` char(3) NOT NULL DEFAULT '',
  `codcart` char(10) NOT NULL DEFAULT '',
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `tipo_campo` char(1) NOT NULL DEFAULT '',
  `tamanho` int(3) NOT NULL DEFAULT '0',
  `padrao` varchar(50) NOT NULL DEFAULT '',
  `soleitura` char(1) NOT NULL DEFAULT 'N',
  `visivel` char(1) NOT NULL DEFAULT 'S',
  `ordem` int(3) NOT NULL DEFAULT '0',
  `obs_campo` text NOT NULL,
  `usabilidade` char(1) NOT NULL DEFAULT 'A' COMMENT '||(P)ix / (B)oleto / (A)mbos',
  PRIMARY KEY (`codcampfc`),
  KEY `nro_ban` (`nro_ban`),
  KEY `codcart` (`codcart`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campo_forma_cob`
-- Table structure for table `consultas_publicas`
--

DROP TABLE IF EXISTS `consultas_publicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultas_publicas` (
  `codcpub` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `descri_cpub` varchar(50) NOT NULL,
  `limite` int(3) unsigned NOT NULL,
  `formato_padrao` char(1) NOT NULL,
  `salva_logs` char(1) NOT NULL DEFAULT 'N',
  `consulta_sql` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcpub`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultas_publicas`
-- Table structure for table `conf_retornos`
--

DROP TABLE IF EXISTS `conf_retornos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_retornos` (
  `codcret` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `quant_chart` int(3) NOT NULL DEFAULT '0',
  `cedente` varchar(15) NOT NULL,
  `ini_cedente` int(10) unsigned NOT NULL DEFAULT '0',
  `fin_cedente` int(10) unsigned NOT NULL DEFAULT '0',
  `carteira` varchar(7) NOT NULL,
  `ini_carteira` int(10) unsigned NOT NULL DEFAULT '0',
  `fin_carteira` int(10) unsigned NOT NULL DEFAULT '0',
  `ini_nro_arq` int(3) NOT NULL DEFAULT '0',
  `fin_nro_arq` int(3) NOT NULL DEFAULT '0',
  `ini_data_proc` int(3) NOT NULL DEFAULT '0',
  `fin_data_proc` int(3) NOT NULL DEFAULT '0',
  `ini_n_boleto` int(3) NOT NULL DEFAULT '0',
  `fin_n_boleto` int(4) NOT NULL DEFAULT '0',
  `ini_nro_doc` int(3) NOT NULL DEFAULT '0',
  `fin_nro_doc` int(3) NOT NULL DEFAULT '0',
  `ini_data_pag` int(3) NOT NULL DEFAULT '0',
  `fin_data_pag` int(3) NOT NULL DEFAULT '0',
  `tipo_data_pag` char(1) NOT NULL DEFAULT '',
  `ini_data_cre` int(3) NOT NULL DEFAULT '0',
  `fin_data_cre` int(3) NOT NULL DEFAULT '0',
  `ini_data_ven` int(10) unsigned NOT NULL DEFAULT '0',
  `fin_data_ven` int(10) unsigned NOT NULL DEFAULT '0',
  `ini_valor_lan` int(10) unsigned NOT NULL DEFAULT '0',
  `fin_valor_lan` int(10) unsigned NOT NULL DEFAULT '0',
  `ini_valor_pag` int(3) NOT NULL DEFAULT '0',
  `fin_valor_pag` int(3) NOT NULL DEFAULT '0',
  `ini_valor_multa` int(3) NOT NULL DEFAULT '0',
  `fin_valor_multa` int(3) NOT NULL DEFAULT '0',
  `ini_valor_juros` int(3) NOT NULL DEFAULT '0',
  `fin_valor_juros` int(3) NOT NULL DEFAULT '0',
  `ini_cod_oco` int(3) NOT NULL DEFAULT '0',
  `fin_cod_oco` int(3) NOT NULL DEFAULT '0',
  `ini_valor_tar` int(3) unsigned NOT NULL DEFAULT '0',
  `fin_valor_tar` int(3) unsigned NOT NULL DEFAULT '0',
  `ini_cod_rejeicao` int(10) unsigned NOT NULL DEFAULT '0',
  `fin_cod_rejeicao` int(10) unsigned NOT NULL DEFAULT '0',
  `ini_valor_des` int(10) unsigned NOT NULL DEFAULT '0',
  `fin_valor_des` int(10) unsigned NOT NULL DEFAULT '0',
  `somar_juros` char(1) NOT NULL DEFAULT 'N',
  `restar_desconto` char(1) NOT NULL,
  `ignora_cabe_lote` char(1) NOT NULL DEFAULT 'N',
  `valor_tarifa` float(10,2) NOT NULL,
  `ini_cod_identificador_da` int(11) NOT NULL DEFAULT '0',
  `fin_cod_identificador_da` int(11) NOT NULL DEFAULT '0',
  `ini_agencia` int(11) NOT NULL DEFAULT '0',
  `fin_agencia` int(11) NOT NULL DEFAULT '0',
  `ini_iden_cli_banco` int(11) NOT NULL DEFAULT '0',
  `fin_iden_cli_banco` int(11) NOT NULL DEFAULT '0',
  `ini_data_inclusao` int(11) NOT NULL DEFAULT '0',
  `fin_data_inclusao` int(11) NOT NULL DEFAULT '0',
  `ini_cod_movimento` int(11) NOT NULL DEFAULT '0',
  `fin_cod_movimento` int(11) NOT NULL DEFAULT '0',
  `ini_tipo_conta` int(11) NOT NULL DEFAULT '0',
  `fin_tipo_conta` int(11) NOT NULL DEFAULT '0',
  `ini_dv` int(11) NOT NULL DEFAULT '0',
  `fin_dv` int(11) NOT NULL DEFAULT '0',
  `ini_orpag` int(3) NOT NULL DEFAULT '0',
  `fin_orpag` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codcret`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_retornos`
-- Table structure for table `slot_olt`
--

DROP TABLE IF EXISTS `slot_olt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `slot_olt` (
  `codsolt` varchar(10) NOT NULL,
  `codolt` varchar(10) NOT NULL,
  `slotid` varchar(10) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `tecnologia` varchar(50) NOT NULL,
  PRIMARY KEY (`codsolt`),
  KEY `codolt` (`codolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slot_olt`
-- Table structure for table `indices`
--

DROP TABLE IF EXISTS `indices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `indices` (
  `codindc` varchar(10) NOT NULL,
  `descri_indice` varchar(50) NOT NULL,
  PRIMARY KEY (`codindc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indices`
-- Table structure for table `maparede_sinc`
--

DROP TABLE IF EXISTS `maparede_sinc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maparede_sinc` (
  `codmps` varchar(20) NOT NULL DEFAULT '',
  `descri_sinc` varchar(200) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codmps`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maparede_sinc`
-- Table structure for table `itens_apagados`
--

DROP TABLE IF EXISTS `itens_apagados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `itens_apagados` (
  `codi_a` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codtcom` char(1) NOT NULL DEFAULT '',
  `nome_i_a` varchar(50) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codsercliex` char(10) NOT NULL DEFAULT '',
  `nro_item` int(11) NOT NULL DEFAULT '0' COMMENT 'Numero do registro do serviço extra',
  `codserex` char(10) NOT NULL DEFAULT '',
  `codndis` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codi_a`),
  KEY `codsercli` (`codsercli`),
  KEY `codcli` (`codcli`),
  KEY `codndis` (`codndis`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itens_apagados`
-- Table structure for table `servidor_vod`
--

DROP TABLE IF EXISTS `servidor_vod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidor_vod` (
  `codvod` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `descri_vod` varchar(50) NOT NULL,
  `porta` int(5) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidor_vod`
-- Table structure for table `projeto_ind`
--

DROP TABLE IF EXISTS `projeto_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projeto_ind` (
  `codpji` varchar(10) NOT NULL,
  `codpar` char(10) NOT NULL,
  `nome_par` varchar(50) NOT NULL,
  PRIMARY KEY (`codpji`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_ind`
-- Table structure for table `tarefas_filhas_m`
--

DROP TABLE IF EXISTS `tarefas_filhas_m`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefas_filhas_m` (
  `codtfm` varchar(10) NOT NULL DEFAULT '',
  `codtarm` varchar(10) NOT NULL DEFAULT '',
  `codtarm_p` varchar(10) NOT NULL DEFAULT '',
  `codtarm_f` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtfm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefas_filhas_m`
-- Table structure for table `log_login`
--

DROP TABLE IF EXISTS `log_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_login` (
  `codllog` varchar(10) NOT NULL,
  `login` varchar(32) NOT NULL,
  `senha` varchar(25) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`codllog`),
  KEY `ip` (`ip`),
  KEY `data_hora` (`data_hora`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_login`
-- Table structure for table `equipamentos_rede`
--

DROP TABLE IF EXISTS `equipamentos_rede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipamentos_rede` (
  `codeqr` varchar(10) NOT NULL DEFAULT '',
  `codpat` varchar(10) DEFAULT NULL,
  `codosr` varchar(10) DEFAULT 'APROUTER',
  `codste` varchar(10) DEFAULT NULL,
  `host_name` varchar(50) DEFAULT NULL,
  `login` varchar(10) DEFAULT NULL,
  `senha` varchar(10) DEFAULT NULL,
  `porta` varchar(4) DEFAULT NULL,
  `obs` mediumtext,
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `posx` int(6) unsigned DEFAULT NULL,
  `posy` int(6) unsigned DEFAULT NULL,
  PRIMARY KEY (`codeqr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos_rede`
-- Table structure for table `consultas_tarefas`
--

DROP TABLE IF EXISTS `consultas_tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultas_tarefas` (
  `codctar` char(10) NOT NULL,
  `codextra` char(10) NOT NULL DEFAULT '',
  `tipo` varchar(20) NOT NULL,
  `versao` char(10) NOT NULL,
  `descri_ctar` varchar(100) NOT NULL,
  `titulo_ctar` char(10) NOT NULL,
  `padrao` char(1) NOT NULL,
  `data_hora_alt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `consulta_sql` mediumtext NOT NULL,
  `consulta_dados` mediumtext NOT NULL,
  `consulta_todos` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codctar`),
  KEY `codextra` (`codextra`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultas_tarefas`
-- Table structure for table `historia_kanban`
--

DROP TABLE IF EXISTS `historia_kanban`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historia_kanban` (
  `codhkb` char(10) NOT NULL DEFAULT '',
  `codcar` char(10) NOT NULL DEFAULT '',
  `n_hist` int(11) DEFAULT NULL,
  `data_lan` datetime DEFAULT NULL,
  `data_prev` datetime DEFAULT NULL,
  PRIMARY KEY (`codhkb`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historia_kanban`
-- Table structure for table `alteracoes_tabelas`
--

DROP TABLE IF EXISTS `alteracoes_tabelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alteracoes_tabelas` (
  `codatab` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `nome_campo` varchar(30) NOT NULL,
  `descri_campo` varchar(50) NOT NULL,
  `nome_codigo` varchar(30) NOT NULL,
  `nome_cursor` varchar(10) NOT NULL,
  `nome_tabela_pop` varchar(50) NOT NULL,
  `api` varchar(50) NOT NULL,
  `tipo_campo` varchar(1) NOT NULL,
  `sql_valores` mediumtext NOT NULL,
  `sql_cursor_ver` mediumtext NOT NULL,
  `macro_historico` mediumtext NOT NULL,
  PRIMARY KEY (`codatab`),
  KEY `codtab` (`codtab`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alteracoes_tabelas`
-- Table structure for table `tipo_acao_cobranca`
--

DROP TABLE IF EXISTS `tipo_acao_cobranca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_acao_cobranca` (
  `codtac` varchar(10) NOT NULL,
  `descri_tac` varchar(50) NOT NULL,
  PRIMARY KEY (`codtac`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_acao_cobranca`
-- Table structure for table `habilitacao_provisoria_velocidade`
--

DROP TABLE IF EXISTS `habilitacao_provisoria_velocidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `habilitacao_provisoria_velocidade` (
  `codhprovvel` char(10) NOT NULL,
  `codsercli` char(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_fim` date NOT NULL,
  PRIMARY KEY (`codhprovvel`),
  KEY `codsercli` (`codsercli`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habilitacao_provisoria_velocidade`
-- Table structure for table `pacotes_cdf`
--

DROP TABLE IF EXISTS `pacotes_cdf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pacotes_cdf` (
  `codpcdf` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  `codtcdf` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `quant` int(3) unsigned NOT NULL,
  `limite` int(3) unsigned NOT NULL,
  `valor_cdf_ex` float(10,2) NOT NULL,
  PRIMARY KEY (`codpcdf`),
  KEY `codpac` (`codpac`),
  KEY `codsad` (`codsad`),
  KEY `codtcdf` (`codtcdf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacotes_cdf`
-- Table structure for table `movimentos_pat`
--

DROP TABLE IF EXISTS `movimentos_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentos_pat` (
  `codmvp` varchar(10) NOT NULL DEFAULT '',
  `codpat` varchar(10) NOT NULL DEFAULT '',
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codaqs` varchar(10) NOT NULL DEFAULT '',
  `codvpat` varchar(10) NOT NULL,
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(4) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codords` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL DEFAULT '',
  `codcfop` varchar(10) NOT NULL,
  `quantidade` decimal(10,2) NOT NULL,
  `tipo_mov` char(1) NOT NULL DEFAULT 'E',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atual` char(1) NOT NULL DEFAULT 'N',
  `obs` mediumtext NOT NULL,
  `vl_venda` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tipo_conexao_p` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codmvp`),
  KEY `codpat` (`codpat`),
  KEY `codlmp` (`codlmp`),
  KEY `codcon` (`codcon`),
  KEY `codsercli` (`codsercli`),
  KEY `codadq` (`codaqs`),
  KEY `codfor` (`codfor`),
  KEY `codcmp` (`codcmp`),
  KEY `atual` (`atual`),
  KEY `codords` (`codords`),
  KEY `codprod` (`codprod`),
  KEY `codcfop` (`codcfop`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos_pat`
-- Table structure for table `log_inject`
--

DROP TABLE IF EXISTS `log_inject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_inject` (
  `codlgi` varchar(10) NOT NULL,
  `ip` varchar(30) NOT NULL,
  `data_hora` datetime NOT NULL,
  `parametro` mediumtext NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codlgi`),
  KEY `ip` (`ip`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_inject`
-- Table structure for table `servicos_ema`
--

DROP TABLE IF EXISTS `servicos_ema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_ema` (
  `codsema` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `quant_e` int(2) NOT NULL DEFAULT '0',
  `quota_e_p` int(6) NOT NULL DEFAULT '0',
  `quota_e_s` int(6) NOT NULL DEFAULT '0',
  `valor_e_adi` float(10,2) NOT NULL DEFAULT '0.00',
  `valor_antispam` float(10,2) NOT NULL DEFAULT '0.00',
  `valor_antispam_s` float(10,2) NOT NULL DEFAULT '0.00',
  `tipo_mta` char(1) NOT NULL DEFAULT 'Q',
  `sec_central` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codsema`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_ema`
-- Table structure for table `servicos_cnl`
--

DROP TABLE IF EXISTS `servicos_cnl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cnl` (
  `codscnl` varchar(10) NOT NULL,
  `codcnl` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `dias_trial` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codscnl`),
  KEY `codcnl` (`codcnl`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cnl`
-- Table structure for table `endereco_cli`
--

DROP TABLE IF EXISTS `endereco_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `endereco_cli` (
  `codecli` char(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codtend` char(10) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `apto` char(10) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` char(8) NOT NULL DEFAULT '',
  `cep` char(9) NOT NULL DEFAULT '',
  `latitude` varchar(20) NOT NULL DEFAULT '',
  `longitude` varchar(20) NOT NULL DEFAULT '',
  `codpros` char(10) NOT NULL,
  `referencia` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codecli`),
  KEY `codcli` (`codcli`),
  KEY `cidade` (`cidade`),
  KEY `codtend` (`codtend`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endereco_cli`
-- Table structure for table `det_pacotes`
--

DROP TABLE IF EXISTS `det_pacotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_pacotes` (
  `coddpac` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  `codcnl` varchar(10) NOT NULL,
  PRIMARY KEY (`coddpac`),
  KEY `codpac` (`codpac`),
  KEY `codcnl` (`codcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_pacotes`
-- Table structure for table `tipo_promocao`
--

DROP TABLE IF EXISTS `tipo_promocao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_promocao` (
  `codtprom` varchar(10) NOT NULL,
  `descri_tprom` varchar(70) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtprom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_promocao`
-- Table structure for table `relatorios`
--

DROP TABLE IF EXISTS `relatorios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relatorios` (
  `codrela` varchar(10) NOT NULL DEFAULT '',
  `codinf` varchar(10) NOT NULL DEFAULT '',
  `relatorio` varchar(30) NOT NULL DEFAULT '',
  `nombre` varchar(100) NOT NULL DEFAULT '',
  `ordenado` varchar(100) NOT NULL DEFAULT '',
  `agrupado` varchar(50) NOT NULL DEFAULT '',
  `filtro` varchar(100) NOT NULL DEFAULT '',
  `indice` int(2) unsigned NOT NULL DEFAULT '0',
  `etiqueta` char(1) NOT NULL DEFAULT 'N',
  `editavel` char(1) NOT NULL DEFAULT '',
  `ignorar_frx2any` char(1) NOT NULL DEFAULT 'N',
  `conteudo` text NOT NULL,
  `conteudo2` text NOT NULL,
  `variaveis` text NOT NULL,
  `teste` text NOT NULL,
  PRIMARY KEY (`codrela`),
  KEY `tela` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios`
-- Table structure for table `ocorrencias`
--

DROP TABLE IF EXISTS `ocorrencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocorrencias` (
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(11) NOT NULL DEFAULT '0',
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `codpros` varchar(10) NOT NULL,
  `codsto` varchar(10) NOT NULL DEFAULT '',
  `codoco_v` varchar(10) NOT NULL,
  `data_ua` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codco_cl` varchar(10) NOT NULL,
  `codmvis` varchar(10) NOT NULL,
  `codmfo` varchar(10) NOT NULL,
  `codigo_externo` varchar(10) NOT NULL,
  `codcatoco` varchar(10) NOT NULL,
  `data_lan` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_sol` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_prev` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_neg` datetime NOT NULL,
  `descri_oco` text NOT NULL,
  `script` text NOT NULL,
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codpint` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `codusu_d` char(2) NOT NULL DEFAULT '',
  `codocop` varchar(10) NOT NULL DEFAULT '',
  `codocop_sol` varchar(10) NOT NULL,
  `nivel` int(1) NOT NULL DEFAULT '0',
  `prioridade` char(1) NOT NULL DEFAULT '',
  `coddep` varchar(10) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `hora_lan` varchar(5) NOT NULL DEFAULT '',
  `hora_sol` varchar(5) NOT NULL DEFAULT '',
  `descri_oco_sol` text NOT NULL,
  `codusu_sol` char(2) NOT NULL DEFAULT '',
  `numero_oco` bigint(14) unsigned NOT NULL DEFAULT '0',
  `lida` char(1) NOT NULL DEFAULT 'N',
  `classificacao` char(1) NOT NULL,
  `ultimo_contato` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `script_atd` char(1) NOT NULL DEFAULT 'N',
  `atd_vinc` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codoco`),
  KEY `codcli` (`codcli`),
  KEY `codsercli` (`codsercli`),
  KEY `codsto` (`codsto`),
  KEY `codocop` (`codocop`),
  KEY `codpros` (`codpros`),
  KEY `codpint` (`codpint`),
  KEY `codcon` (`codcon`),
  KEY `codoco_v` (`codoco_v`),
  KEY `data_lan` (`data_lan`),
  KEY `data_sol` (`data_sol`),
  KEY `codusu_d` (`codusu_d`),
  KEY `codcar` (`codcar`),
  KEY `codmvis` (`codmvis`),
  KEY `codusu` (`codusu`),
  KEY `numero_oco` (`numero_oco`),
  KEY `codmfo` (`codmfo`),
  KEY `codigo_externo` (`codigo_externo`),
  KEY `lida` (`lida`),
  KEY `script_atd` (`script_atd`),
  KEY `atd_vinc` (`atd_vinc`),
  FULLTEXT KEY `descri_oco` (`descri_oco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocorrencias`
-- Table structure for table `banderias_cartoes`
--

DROP TABLE IF EXISTS `banderias_cartoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banderias_cartoes` (
  `codbanc` varchar(10) NOT NULL DEFAULT '',
  `codban` varchar(10) NOT NULL,
  `descri_banc` varchar(50) NOT NULL,
  `dias` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codbanc`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banderias_cartoes`
-- Table structure for table `bloquetos`
--

DROP TABLE IF EXISTS `bloquetos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bloquetos` (
  `codcamp` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `nome` varchar(50) NOT NULL DEFAULT '',
  `tamanho` varchar(10) NOT NULL DEFAULT '',
  `orden` int(11) NOT NULL DEFAULT '0',
  `conteudo` text NOT NULL,
  PRIMARY KEY (`codcamp`),
  KEY `codcob` (`codcob`),
  KEY `tipo` (`tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloquetos`
-- Table structure for table `troca_status`
--

DROP TABLE IF EXISTS `troca_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `troca_status` (
  `codtst` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `codest` varchar(10) NOT NULL,
  `codextra` varchar(10) NOT NULL,
  `ok` char(1) NOT NULL,
  `obs_int` mediumtext NOT NULL,
  PRIMARY KEY (`codtst`),
  KEY `codsercli` (`codsercli`),
  KEY `data_hora` (`data_hora`),
  KEY `codest` (`codest`),
  KEY `codextra` (`codextra`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `troca_status`
-- Table structure for table `config_central`
--

DROP TABLE IF EXISTS `config_central`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config_central` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codctr` char(10) NOT NULL,
  `name` varchar(40) NOT NULL,
  `value` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `codctr` (`codctr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config_central`
-- Table structure for table `script_tipo_comando`
--

DROP TABLE IF EXISTS `script_tipo_comando`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_tipo_comando` (
  `codstcom` char(10) NOT NULL COMMENT '||ScriptCommandType ID',
  `descri_tp_comando` varchar(50) NOT NULL DEFAULT '' COMMENT '||-',
  PRIMARY KEY (`codstcom`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=ScriptCommandType|Desc=|Grupo=OpticalFiber';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_tipo_comando`
-- Table structure for table `dados_pop`
--

DROP TABLE IF EXISTS `dados_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dados_pop` (
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `codima` varchar(15) NOT NULL,
  `codscp` varchar(10) NOT NULL,
  `nome_pop` varchar(50) NOT NULL DEFAULT '',
  `fone_acesso` varchar(10) NOT NULL DEFAULT '',
  `dns_primario` varchar(16) NOT NULL DEFAULT '',
  `dns_secundario` varchar(16) NOT NULL DEFAULT '',
  `dominio` varchar(50) NOT NULL DEFAULT '',
  `pop3` varchar(50) NOT NULL DEFAULT '',
  `smtp` varchar(50) NOT NULL DEFAULT '',
  `home_page` varchar(50) NOT NULL DEFAULT '',
  `codservp_p` varchar(10) NOT NULL DEFAULT '',
  `codservp_s` varchar(10) NOT NULL DEFAULT '',
  `codservp_e` varchar(10) NOT NULL DEFAULT '',
  `codservp_r` varchar(10) NOT NULL,
  `rateio` float(6,2) NOT NULL,
  `url_imagem` varchar(150) NOT NULL,
  PRIMARY KEY (`codpop`),
  KEY `codima` (`codima`),
  KEY `codscp` (`codscp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_pop`
-- Table structure for table `requisicao`
--

DROP TABLE IF EXISTS `requisicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requisicao` (
  `codrequis` varchar(10) NOT NULL DEFAULT '',
  `numero` bigint(12) NOT NULL AUTO_INCREMENT,
  `situacao` char(1) NOT NULL DEFAULT '',
  `previsaoentrega` date DEFAULT NULL,
  `obs` varchar(100) NOT NULL DEFAULT '',
  `geracaodata` datetime DEFAULT NULL,
  `geracaousuario` varchar(20) DEFAULT NULL,
  `autorizacaodata` datetime DEFAULT NULL,
  `autorizacaousuario` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`codrequis`),
  UNIQUE KEY `codrequis` (`codrequis`),
  KEY `Numero` (`numero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requisicao`
-- Table structure for table `detalhe_faturas`
--

DROP TABLE IF EXISTS `detalhe_faturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_faturas` (
  `coddfat` char(10) NOT NULL DEFAULT '',
  `codfat` char(10) NOT NULL DEFAULT '',
  `codcrec` char(10) NOT NULL DEFAULT '',
  `status_fat` char(1) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL DEFAULT '0.00',
  `valor_pag` decimal(10,2) NOT NULL DEFAULT '0.00',
  `codraz` char(10) NOT NULL DEFAULT '',
  `coddes` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddfat`),
  KEY `codcrec` (`codcrec`),
  KEY `codfat` (`codfat`),
  KEY `codraz` (`codraz`),
  KEY `status_fat` (`status_fat`),
  KEY `coddes` (`coddes`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_faturas`
-- Table structure for table `velocidades`
--

DROP TABLE IF EXISTS `velocidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `velocidades` (
  `codvel` varchar(10) NOT NULL DEFAULT '',
  `codvel_r` varchar(10) NOT NULL,
  `descri_vel` varchar(30) NOT NULL,
  `velocidade` int(6) unsigned NOT NULL DEFAULT '0',
  `unidade` varchar(4) NOT NULL DEFAULT 'Kbps',
  `upload` int(8) unsigned NOT NULL,
  `max_limit_up` int(8) unsigned NOT NULL,
  `burst_limit_up` int(8) unsigned NOT NULL,
  `burst_threshold_up` int(8) unsigned NOT NULL,
  `burst_time_up` int(6) unsigned NOT NULL,
  `download` int(8) unsigned NOT NULL,
  `max_limit_dw` int(8) unsigned NOT NULL,
  `burst_limit_dw` int(8) unsigned NOT NULL,
  `burst_threshold_dw` int(8) unsigned NOT NULL,
  `burst_time_dw` int(6) unsigned NOT NULL,
  `prioridade` int(2) unsigned NOT NULL,
  `profile_velocidade` varchar(50) NOT NULL,
  `profile_down` varchar(50) NOT NULL,
  `profile_up` varchar(50) NOT NULL,
  PRIMARY KEY (`codvel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `velocidades`
-- Table structure for table `franquia_ser_voz`
--

DROP TABLE IF EXISTS `franquia_ser_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franquia_ser_voz` (
  `codfsv` varchar(10) NOT NULL DEFAULT '',
  `codtter` varchar(10) NOT NULL DEFAULT '',
  `codsvoz` varchar(10) NOT NULL DEFAULT '',
  `descri_fsv` varchar(50) NOT NULL,
  `codcta` varchar(8) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `minutos_livres` int(6) unsigned NOT NULL DEFAULT '0',
  `valor_adicional` float(10,4) NOT NULL DEFAULT '0.0000',
  `valor_mensal` float(10,2) NOT NULL,
  `datas_venc` char(1) NOT NULL DEFAULT 'N',
  `valor_minutos_mvno` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codfsv`),
  KEY `codtter` (`codtter`),
  KEY `codsvoz` (`codsvoz`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `franquia_ser_voz`
-- Table structure for table `carga_impositiva`
--

DROP TABLE IF EXISTS `carga_impositiva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carga_impositiva` (
  `codcimp` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `codcomp` varchar(4) NOT NULL,
  `icms` float(7,3) NOT NULL,
  `iss` float(7,3) NOT NULL,
  `pis` float(7,3) NOT NULL,
  `cofins` float(7,3) NOT NULL,
  PRIMARY KEY (`codcimp`),
  KEY `codemp` (`codemp`),
  KEY `codcomp` (`codcomp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carga_impositiva`
-- Table structure for table `tipo_observacao`
--

DROP TABLE IF EXISTS `tipo_observacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_observacao` (
  `codtobs` varchar(10) NOT NULL DEFAULT '',
  `descri_tobs` varchar(50) NOT NULL DEFAULT '',
  `ordem` int(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codtobs`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_observacao`
-- Table structure for table `liberacao_canais`
--

DROP TABLE IF EXISTS `liberacao_canais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `liberacao_canais` (
  `codlcnl` varchar(10) NOT NULL,
  `codcnl` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `estado` char(2) NOT NULL,
  PRIMARY KEY (`codlcnl`),
  KEY `codcnl` (`codcnl`),
  KEY `cidade` (`cidade`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `liberacao_canais`
-- Table structure for table `filtros_cons_pub`
--

DROP TABLE IF EXISTS `filtros_cons_pub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filtros_cons_pub` (
  `codfcp` varchar(10) NOT NULL,
  `codcpub` varchar(10) NOT NULL,
  `titulo_fcp` varchar(50) NOT NULL,
  `alias` varchar(10) NOT NULL,
  `nome_campo` varchar(50) NOT NULL,
  `tipo_campo` char(1) NOT NULL,
  `operador` varchar(2) NOT NULL,
  `tamanho` int(3) unsigned NOT NULL,
  `obrigatorio` char(1) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codfcp`),
  KEY `codcpub` (`codcpub`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filtros_cons_pub`
-- Table structure for table `det_previsoes_mes`
--

DROP TABLE IF EXISTS `det_previsoes_mes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_previsoes_mes` (
  `coddpmes` varchar(10) NOT NULL,
  `codprev` varchar(10) NOT NULL,
  `compe` char(4) NOT NULL,
  `codban` varchar(10) NOT NULL,
  `valor` float(10,2) NOT NULL,
  `data` date NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`coddpmes`),
  KEY `codprev` (`codprev`),
  KEY `compe` (`compe`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_previsoes_mes`
-- Table structure for table `cidades_usuarios`
--

DROP TABLE IF EXISTS `cidades_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cidades_usuarios` (
  `codcusu` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `cidade` varchar(9) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidades_usuarios`
-- Table structure for table `virtual_number`
--

DROP TABLE IF EXISTS `virtual_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `virtual_number` (
  `codvnumber` varchar(10) NOT NULL,
  `virtual_number` double NOT NULL,
  `codtvoz` varchar(10) NOT NULL,
  PRIMARY KEY (`codvnumber`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `virtual_number`
-- Table structure for table `portabilidade`
--

DROP TABLE IF EXISTS `portabilidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `portabilidade` (
  `codport` char(10) NOT NULL COMMENT 'Chave primária',
  `data_cad` date NOT NULL DEFAULT '0000-00-00' COMMENT 'Data de Cadastro do número da ser portado',
  `data_portado` date NOT NULL DEFAULT '0000-00-00' COMMENT 'Data de Portabilidade do número',
  `codusu` char(2) NOT NULL COMMENT 'Código Usuário que solicitou a portabilidade',
  `ddd` varchar(3) NOT NULL DEFAULT '' COMMENT 'DDD do número a ser portado',
  `numero` varchar(12) NOT NULL DEFAULT '' COMMENT 'Número a ser portado',
  `status` char(1) NOT NULL DEFAULT '' COMMENT 'A- Aguardando Portabilidade, P - Número Portado',
  `codtvoz` char(10) NOT NULL COMMENT 'Chave primária tabela terminal_voz',
  `codopertel` char(10) NOT NULL COMMENT 'Chave primária tabela operadoras_telefonia',
  PRIMARY KEY (`codport`),
  KEY `codopertel` (`codopertel`),
  KEY `codtvoz` (`codtvoz`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portabilidade`
-- Table structure for table `tipo_contatos_cli`
--

DROP TABLE IF EXISTS `tipo_contatos_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_contatos_cli` (
  `codtco_cl` varchar(10) NOT NULL DEFAULT '',
  `descri_tco_cl` varchar(30) NOT NULL DEFAULT '',
  `ordem` int(2) unsigned NOT NULL DEFAULT '0',
  `obrigatorio_cliente` char(1) NOT NULL DEFAULT 'N',
  `obrigatorio_prospecto` char(1) NOT NULL DEFAULT 'N',
  `obrigatorio_pacesso` char(1) NOT NULL DEFAULT 'N',
  `tipo_contato_padrao` char(1) NOT NULL DEFAULT 'N',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codtco_cl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_contatos_cli`
-- Table structure for table `troca_status_fat`
--

DROP TABLE IF EXISTS `troca_status_fat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `troca_status_fat` (
  `codtsf` varchar(10) NOT NULL,
  `codfat` varchar(10) NOT NULL,
  `codsta_f` char(1) NOT NULL,
  `codrret` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  PRIMARY KEY (`codtsf`),
  KEY `codfat` (`codfat`),
  KEY `codsta_f` (`codsta_f`),
  KEY `codrret` (`codrret`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `troca_status_fat`
-- Table structure for table `opcoes_items_pos`
--

DROP TABLE IF EXISTS `opcoes_items_pos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes_items_pos` (
  `codopcip` varchar(10) NOT NULL,
  `codtfav` char(10) DEFAULT NULL,
  `codusu` varchar(3) DEFAULT NULL,
  `codopc` varchar(10) DEFAULT NULL,
  `posX` int(4) DEFAULT NULL,
  `posY` int(4) DEFAULT NULL,
  PRIMARY KEY (`codopcip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes_items_pos`
-- Table structure for table `det_fat_negociacao`
--

DROP TABLE IF EXISTS `det_fat_negociacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_fat_negociacao` (
  `codfat` char(10) NOT NULL,
  `codndeb` char(10) DEFAULT NULL,
  KEY `codfat` (`codfat`),
  KEY `codndeb` (`codndeb`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_fat_negociacao`
-- Table structure for table `emails_recebidos`
--

DROP TABLE IF EXISTS `emails_recebidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emails_recebidos` (
  `codemr` varchar(10) NOT NULL DEFAULT '',
  `codvis` varchar(10) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pasta` char(1) NOT NULL DEFAULT 'E',
  `id_mensagem` varchar(20) NOT NULL DEFAULT '',
  `destinatario` varchar(100) NOT NULL DEFAULT '',
  `remetente` varchar(100) NOT NULL DEFAULT '',
  `email_remetente` varchar(100) NOT NULL DEFAULT '',
  `copia` varchar(100) NOT NULL DEFAULT '',
  `email_copia` varchar(100) NOT NULL DEFAULT '',
  `assunto` varchar(100) NOT NULL DEFAULT '',
  `mensagem` mediumtext NOT NULL,
  `tipo_em_respons` varchar(10) NOT NULL,
  PRIMARY KEY (`codemr`),
  KEY `codvis` (`codvis`),
  KEY `data` (`data`),
  KEY `pasta` (`pasta`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_recebidos`
-- Table structure for table `servicos_cli_dici`
--

DROP TABLE IF EXISTS `servicos_cli_dici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_dici` (
  `codscdici` char(10) NOT NULL,
  `codsercli` char(10) DEFAULT NULL,
  `coddicita` char(10) DEFAULT NULL,
  `coddicitac` char(10) DEFAULT NULL,
  `coddicitec` char(10) DEFAULT NULL,
  `coddicitprod` char(10) DEFAULT NULL,
  `velocidade` decimal(15,5) NOT NULL DEFAULT '0.00000',
  `usu_proprio` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codscdici`),
  KEY `codsercli` (`codsercli`),
  KEY `usu_proprio` (`usu_proprio`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_dici`
-- Table structure for table `log_consulta_documento`
--

DROP TABLE IF EXISTS `log_consulta_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_consulta_documento` (
  `codlogdoc` varchar(20) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `documento` varchar(20) NOT NULL,
  `status` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codlogdoc`),
  KEY `codusu` (`codusu`),
  KEY `data_hora` (`data_hora`),
  KEY `documento` (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_consulta_documento`
-- Table structure for table `locais_mov_pat`
--

DROP TABLE IF EXISTS `locais_mov_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locais_mov_pat` (
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL,
  `codtlmp` varchar(10) NOT NULL,
  `descri_lmp` varchar(50) NOT NULL DEFAULT '',
  `fixo` char(1) NOT NULL DEFAULT 'N',
  `codusu_c` char(2) NOT NULL DEFAULT '',
  `codusu_conf` char(2) NOT NULL DEFAULT '',
  `deposito` varchar(1) NOT NULL DEFAULT 'N',
  `considera_mrp` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codlmp`),
  KEY `codpop` (`codpop`),
  KEY `codtlmp` (`codtlmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locais_mov_pat`
-- Table structure for table `imposto_retido`
--

DROP TABLE IF EXISTS `imposto_retido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imposto_retido` (
  `codimpret` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `codtcf` varchar(10) NOT NULL DEFAULT '',
  `coddtimret` varchar(10) NOT NULL DEFAULT '',
  `valor_ret` float(5,2) NOT NULL,
  `pis` float(5,2) NOT NULL DEFAULT '0.00',
  `cofins` float(5,2) NOT NULL DEFAULT '0.00',
  `csll` float(5,2) NOT NULL DEFAULT '0.00',
  `irrf` float(5,2) NOT NULL DEFAULT '0.00',
  `iss` float(5,3) NOT NULL,
  PRIMARY KEY (`codimpret`),
  KEY `codnf` (`codnf`),
  KEY `codcrec` (`codcrec`),
  KEY `codtcf` (`codtcf`),
  KEY `coddtmret` (`coddtimret`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imposto_retido`
-- Table structure for table `histo_comissoes`
--

DROP TABLE IF EXISTS `histo_comissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histo_comissoes` (
  `codhcomi` varchar(10) NOT NULL,
  `coddcp` varchar(10) NOT NULL,
  `codcomi` varchar(10) NOT NULL,
  `gerou_abatimento` varchar(1) NOT NULL,
  `codven` varchar(10) NOT NULL,
  PRIMARY KEY (`codhcomi`),
  KEY `coddcp` (`coddcp`),
  KEY `codcomi` (`codcomi`),
  KEY `gerou_abatimento` (`gerou_abatimento`),
  KEY `codven` (`codven`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `histo_comissoes`
-- Table structure for table `detalhe_regras_neg`
--

DROP TABLE IF EXISTS `detalhe_regras_neg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_regras_neg` (
  `coddtrng` varchar(10) NOT NULL DEFAULT '',
  `codrng` varchar(10) NOT NULL DEFAULT '',
  `campo` varchar(30) NOT NULL DEFAULT '',
  `valores` mediumtext NOT NULL,
  PRIMARY KEY (`coddtrng`),
  KEY `codrng` (`codrng`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_regras_neg`
-- Table structure for table `servicos_cli_imp`
--

DROP TABLE IF EXISTS `servicos_cli_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_imp` (
  `codscimp` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL,
  `codtnf` varchar(10) NOT NULL,
  `codcob` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codtser` varchar(10) NOT NULL,
  `codcif` char(4) NOT NULL DEFAULT '',
  `descri_simp` varchar(70) NOT NULL,
  `descri_nf` varchar(40) NOT NULL,
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `icms` float(5,2) NOT NULL DEFAULT '0.00',
  `iss` float(5,2) NOT NULL,
  `fust` float(5,2) NOT NULL DEFAULT '0.00',
  `funtel` float(5,2) NOT NULL DEFAULT '0.00',
  `pis` float(5,2) NOT NULL DEFAULT '0.00',
  `cofins` float(5,2) NOT NULL,
  `iva` float(5,2) NOT NULL,
  `codigo_fiscal` varchar(6) NOT NULL,
  `retem_imposto` char(1) NOT NULL DEFAULT 'N',
  `itemsgroupcode` char(3) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codscimp`),
  KEY `codsercli` (`codsercli`),
  KEY `codemp` (`codemp`),
  KEY `codtnf` (`codtnf`),
  KEY `codcob` (`codcob`),
  KEY `codcta` (`codcta`),
  KEY `codtser` (`codtser`),
  KEY `codcif` (`codcif`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_imp`
-- Table structure for table `tipo_cartao`
--

DROP TABLE IF EXISTS `tipo_cartao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cartao` (
  `codtct` varchar(10) NOT NULL DEFAULT '',
  `descri_tct` varchar(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtct`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cartao`
-- Table structure for table `logs_cobro_digital`
--

DROP TABLE IF EXISTS `logs_cobro_digital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_cobro_digital` (
  `codlcd` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `enviado` mediumtext NOT NULL,
  `resposta` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_cobro_digital`
-- Table structure for table `servicos_sici`
--

DROP TABLE IF EXISTS `servicos_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_sici` (
  `codssici` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL,
  `codtsici` varchar(10) NOT NULL,
  `codvsici` varchar(10) NOT NULL,
  `quant_megas` int(6) unsigned NOT NULL,
  `dedicado` char(1) NOT NULL,
  PRIMARY KEY (`codssici`),
  KEY `codser` (`codser`),
  KEY `codtsici` (`codtsici`),
  KEY `codvsici` (`codvsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_sici`
-- Table structure for table `conf_habilitacao_prov`
--

DROP TABLE IF EXISTS `conf_habilitacao_prov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_habilitacao_prov` (
  `codchprov` varchar(10) NOT NULL,
  `dias_central` int(2) unsigned NOT NULL DEFAULT '2',
  `dias_web` int(2) unsigned NOT NULL DEFAULT '2',
  `dias_desk` int(2) unsigned NOT NULL DEFAULT '2'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_habilitacao_prov`
-- Table structure for table `feriados_cid`
--

DROP TABLE IF EXISTS `feriados_cid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feriados_cid` (
  `codfcid` char(10) NOT NULL,
  `codfer` char(10) NOT NULL,
  `cidade` char(8) NOT NULL,
  PRIMARY KEY (`codfcid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feriados_cid`
-- Table structure for table `usu_indicadores`
--

DROP TABLE IF EXISTS `usu_indicadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_indicadores` (
  `codu_i` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codind` varchar(10) NOT NULL,
  PRIMARY KEY (`codu_i`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_indicadores`
-- Table structure for table `tipo_ponto_tv`
--

DROP TABLE IF EXISTS `tipo_ponto_tv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_ponto_tv` (
  `codtpt` varchar(10) NOT NULL,
  `descri_tpt` varchar(30) NOT NULL,
  PRIMARY KEY (`codtpt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_ponto_tv`
-- Table structure for table `tipo_scategoria`
--

DROP TABLE IF EXISTS `tipo_scategoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_scategoria` (
  `codtscat` char(10) NOT NULL,
  `nome_tscar` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtscat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_scategoria`
-- Table structure for table `emails_usuario`
--

DROP TABLE IF EXISTS `emails_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emails_usuario` (
  `codemusu` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `login` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(20) NOT NULL DEFAULT '',
  `pop3` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codemusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_usuario`
-- Table structure for table `det_saldos_sc`
--

DROP TABLE IF EXISTS `det_saldos_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_saldos_sc` (
  `codcrec` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codfat` varchar(10) NOT NULL,
  `status` char(1) NOT NULL,
  `data_ven` date NOT NULL,
  `saldo` float(10,2) NOT NULL,
  PRIMARY KEY (`codcrec`),
  KEY `codsercli` (`codsercli`),
  KEY `codfat` (`codfat`),
  KEY `status` (`status`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_saldos_sc`
-- Table structure for table `control_servicos`
--

DROP TABLE IF EXISTS `control_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_servicos` (
  `vg` char(3) NOT NULL DEFAULT '',
  `vf` char(3) NOT NULL DEFAULT '',
  `vr` char(3) NOT NULL DEFAULT '',
  `vp` char(3) NOT NULL DEFAULT '',
  `df` char(8) NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_servicos`
-- Table structure for table `planejamento_lactos`
--

DROP TABLE IF EXISTS `planejamento_lactos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `planejamento_lactos` (
  `codplalc` char(10) NOT NULL,
  `codplafin` char(10) NOT NULL,
  `codcta` char(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `periodo_ano` char(4) DEFAULT NULL,
  `periodo_mes` char(2) DEFAULT NULL,
  `valor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`codplalc`),
  UNIQUE KEY `identificacao` (`codplafin`,`codcta`,`codctc`,`periodo_ano`,`periodo_mes`),
  KEY `codplafin` (`codplafin`),
  KEY `codcta` (`codcta`),
  KEY `codctc` (`codctc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planejamento_lactos`
-- Table structure for table `campanhas_ligacoes_avc`
--

DROP TABLE IF EXISTS `campanhas_ligacoes_avc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campanhas_ligacoes_avc` (
  `codcla` varchar(10) NOT NULL,
  `coderc` varchar(10) NOT NULL,
  `codtco_cl` varchar(10) NOT NULL,
  `descri_cla` varchar(100) NOT NULL,
  `ativa` char(1) NOT NULL DEFAULT 'S',
  `inicia` datetime NOT NULL,
  `finaliza` datetime NOT NULL,
  `codigocampanha` varchar(20) NOT NULL DEFAULT '',
  `codigomailing` varchar(20) NOT NULL DEFAULT '',
  `codigo_portal_voz` varchar(20) NOT NULL DEFAULT '',
  `codigo_status_campanha` varchar(3) NOT NULL DEFAULT '',
  `codigo_canal_saida` varchar(20) NOT NULL DEFAULT '',
  `batedor` char(1) NOT NULL DEFAULT 'N',
  `processado` char(1) NOT NULL DEFAULT 'N',
  `data_processo` datetime NOT NULL,
  PRIMARY KEY (`codcla`),
  KEY `coderc` (`coderc`),
  KEY `codtco_cl` (`codtco_cl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campanhas_ligacoes_avc`
-- Table structure for table `grupo_clientes`
--

DROP TABLE IF EXISTS `grupo_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_clientes` (
  `codgcli` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `descri_gcli` varchar(100) NOT NULL DEFAULT '',
  `prioridade` char(1) NOT NULL DEFAULT 'M',
  `groupcode` char(10) NOT NULL DEFAULT '' COMMENT 'Campo de exportação para o SAP',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codgcli`),
  KEY `ativo` (`ativo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_clientes`
-- Table structure for table `host_dominio`
--

DROP TABLE IF EXISTS `host_dominio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_dominio` (
  `codhdom` varchar(10) NOT NULL DEFAULT '',
  `coddom` varchar(10) NOT NULL DEFAULT '',
  `nome_hdom` varchar(30) NOT NULL DEFAULT '',
  `valor` varchar(100) NOT NULL DEFAULT '',
  `arquivo_padrão` varchar(50) NOT NULL DEFAULT '',
  `tipo_host` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codhdom`),
  KEY `coddom` (`coddom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_dominio`
-- Table structure for table `acompanhamento_diario`
--

DROP TABLE IF EXISTS `acompanhamento_diario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acompanhamento_diario` (
  `codacd` varchar(10) NOT NULL,
  `descri_acd` varchar(50) NOT NULL,
  `titulo_acd` varchar(30) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT 'D',
  PRIMARY KEY (`codacd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acompanhamento_diario`
-- Table structure for table `bots_talkall`
--

DROP TABLE IF EXISTS `bots_talkall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bots_talkall` (
  `codbta` char(10) NOT NULL DEFAULT '',
  `plataforma` char(1) NOT NULL DEFAULT '',
  `id_bot` varchar(50) NOT NULL DEFAULT '',
  `senha_bot` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codbta`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bots_talkall`
-- Table structure for table `reserva_produto_imp`
--

DROP TABLE IF EXISTS `reserva_produto_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reserva_produto_imp` (
  `codrpl` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codlmp` varchar(10) NOT NULL,
  `codords` varchar(10) NOT NULL,
  `quant` float(8,2) unsigned NOT NULL,
  `codekit` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  PRIMARY KEY (`codrpl`),
  KEY `codprod` (`codprod`),
  KEY `codlmp` (`codlmp`),
  KEY `codords` (`codords`),
  KEY `codekit` (`codekit`),
  KEY `codpat` (`codpat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_produto_imp`
-- Table structure for table `contato_cli_ext`
--

DROP TABLE IF EXISTS `contato_cli_ext`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contato_cli_ext` (
  `codace` char(10) NOT NULL COMMENT '||CustomerContactExt ID',
  `descri_ace` varchar(45) NOT NULL DEFAULT '' COMMENT '||CustomerContactExt description',
  `ativo` char(1) NOT NULL DEFAULT 'S' COMMENT '||CustomerContactExt active flag',
  PRIMARY KEY (`codace`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=CustomerContactExt|Desc=|Grupo=Customer';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contato_cli_ext`
-- Table structure for table `servicos_tax`
--

DROP TABLE IF EXISTS `servicos_tax`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_tax` (
  `codstax` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `descri_stax` varchar(50) NOT NULL,
  `valor_tax` float(10,2) NOT NULL DEFAULT '0.00',
  `quant_parcelas` int(2) unsigned NOT NULL DEFAULT '1',
  `valor_avista` float(10,2) NOT NULL,
  `descri_crec` varchar(50) NOT NULL DEFAULT '',
  `aocriar` char(1) NOT NULL DEFAULT 'S',
  `quant_dias` int(2) unsigned NOT NULL,
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `dias_parcelas` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codstax`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_tax`
-- Table structure for table `servicos_prom`
--

DROP TABLE IF EXISTS `servicos_prom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_prom` (
  `codsprom` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codprom` varchar(10) NOT NULL,
  PRIMARY KEY (`codsprom`),
  KEY `codser` (`codser`),
  KEY `codprom` (`codprom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_prom`
-- Table structure for table `motivo_fechamento_oco`
--

DROP TABLE IF EXISTS `motivo_fechamento_oco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motivo_fechamento_oco` (
  `codmfo` varchar(10) NOT NULL,
  `codsto` varchar(10) NOT NULL,
  `descri_mfo` varchar(100) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codmfo`),
  KEY `codsto` (`codsto`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivo_fechamento_oco`
-- Table structure for table `usu_compromisos`
--

DROP TABLE IF EXISTS `usu_compromisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_compromisos` (
  `coducomp` varchar(10) NOT NULL DEFAULT '',
  `codcomp` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codsuc` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coducomp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_compromisos`
-- Table structure for table `debitos_rechazados`
--

DROP TABLE IF EXISTS `debitos_rechazados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `debitos_rechazados` (
  `codd_r` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codfat` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codoco` char(2) NOT NULL DEFAULT '',
  `processado` char(1) NOT NULL DEFAULT 'N',
  `email` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codd_r`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `debitos_rechazados`
-- Table structure for table `respostas_aten`
--

DROP TABLE IF EXISTS `respostas_aten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `respostas_aten` (
  `codr_a` varchar(10) NOT NULL DEFAULT '',
  `codo_a` varchar(10) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `valor` text NOT NULL,
  PRIMARY KEY (`codr_a`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respostas_aten`
-- Table structure for table `valor_campo_extra`
--

DROP TABLE IF EXISTS `valor_campo_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valor_campo_extra` (
  `codvcpx` varchar(10) NOT NULL DEFAULT '',
  `codcpx` varchar(10) NOT NULL DEFAULT '',
  `codigo` varchar(10) NOT NULL DEFAULT '',
  `valor` varchar(200) NOT NULL,
  PRIMARY KEY (`codvcpx`),
  KEY `codcpx` (`codcpx`),
  KEY `codigo` (`codigo`),
  KEY `valor` (`valor`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valor_campo_extra`
-- Table structure for table `tipo_comentario_atendimento`
--

DROP TABLE IF EXISTS `tipo_comentario_atendimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_comentario_atendimento` (
  `codtca` varchar(10) NOT NULL DEFAULT '',
  `descri_tca` varchar(50) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codtca`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_comentario_atendimento`
-- Table structure for table `nf_fatura_pdf`
--

DROP TABLE IF EXISTS `nf_fatura_pdf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nf_fatura_pdf` (
  `codnfp` varchar(10) NOT NULL,
  `nf_fatura` mediumtext NOT NULL,
  `nf_fatura_rosto` mediumtext NOT NULL,
  `nf_fatura_detalhe` mediumtext NOT NULL,
  `nro_paginas_detalhe` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codnfp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nf_fatura_pdf`
-- Table structure for table `parcela_cond_pagamento`
--

DROP TABLE IF EXISTS `parcela_cond_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parcela_cond_pagamento` (
  `codpcopgt` varchar(10) NOT NULL,
  `codcopgt` varchar(10) NOT NULL,
  `perc_min_entrada` float(8,2) NOT NULL,
  `dias_entre_venc` int(3) NOT NULL,
  `parcela` int(3) NOT NULL,
  `perc_desc_juros` float(8,2) NOT NULL,
  `perc_desc_divida` float(8,2) NOT NULL,
  PRIMARY KEY (`codpcopgt`),
  KEY `codcopgt` (`codcopgt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parcela_cond_pagamento`
-- Table structure for table `reajuste`
--

DROP TABLE IF EXISTS `reajuste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reajuste` (
  `codreajst` varchar(10) NOT NULL DEFAULT '',
  `codindc` varchar(10) NOT NULL DEFAULT '',
  `codmodc` varchar(10) NOT NULL DEFAULT '',
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codusu` varchar(2) NOT NULL DEFAULT '',
  `situacao` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codreajst`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reajuste`
-- Table structure for table `tipo_coluna_grd`
--

DROP TABLE IF EXISTS `tipo_coluna_grd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_coluna_grd` (
  `codtcg` varchar(10) NOT NULL,
  `codtgrd` varchar(10) NOT NULL,
  `descri_tcg` varchar(50) NOT NULL,
  `componente` varchar(30) NOT NULL,
  `valor` varchar(30) NOT NULL,
  `tipo_valor` char(1) NOT NULL,
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `fonte_titulo` varchar(50) NOT NULL,
  `fonte_coluna` varchar(50) NOT NULL,
  `propriedades` mediumtext NOT NULL,
  PRIMARY KEY (`codtcg`),
  KEY `codtgrd` (`codtgrd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_coluna_grd`
-- Table structure for table `creditos_navegacao`
--

DROP TABLE IF EXISTS `creditos_navegacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditos_navegacao` (
  `codcren` varchar(10) NOT NULL,
  `codcre` varchar(10) NOT NULL,
  `compe` char(4) NOT NULL,
  `data` datetime NOT NULL,
  `status` char(1) NOT NULL,
  `tipo_credito` char(1) NOT NULL DEFAULT 'N',
  `quant` int(6) NOT NULL,
  PRIMARY KEY (`codcren`),
  KEY `codcre` (`codcre`),
  KEY `compe` (`compe`),
  KEY `status` (`status`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creditos_navegacao`
-- Table structure for table `form_custom_command`
--

DROP TABLE IF EXISTS `form_custom_command`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `form_custom_command` (
  `codfrmcc` varchar(10) NOT NULL,
  `codfrmct` varchar(10) DEFAULT NULL,
  `comando` mediumtext,
  `c_comp_s` text,
  `tipo_comando` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`codfrmcc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_custom_command`
-- Table structure for table `transporte_nf`
--

DROP TABLE IF EXISTS `transporte_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transporte_nf` (
  `codtra` char(10) NOT NULL,
  `codnf` char(10) NOT NULL,
  `codfor` char(10) NOT NULL,
  `especie` varchar(20) NOT NULL DEFAULT '',
  `marca` varchar(50) NOT NULL DEFAULT '',
  `mod_frete` decimal(10,0) NOT NULL DEFAULT '0',
  `vlr_frete` decimal(10,2) NOT NULL DEFAULT '0.00',
  `quantidade` decimal(10,2) NOT NULL DEFAULT '0.00',
  `numeracao` decimal(10,0) NOT NULL DEFAULT '0',
  `peso_liq` decimal(10,2) NOT NULL DEFAULT '0.00',
  `peso_bruto` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codtra`),
  KEY `codfor` (`codfor`),
  KEY `codnf` (`codnf`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transporte_nf`
-- Table structure for table `tipo_documento`
--

DROP TABLE IF EXISTS `tipo_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_documento` (
  `tipo_doc` char(10) NOT NULL,
  `Descri_doc` varchar(45) NOT NULL DEFAULT '',
  `tipo_doc_p` char(10) NOT NULL DEFAULT '',
  `ordenacao` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tipo_doc`,`Descri_doc`),
  KEY `tipo_doc_p` (`tipo_doc_p`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_documento`
-- Table structure for table `relatorios_cubo`
--

DROP TABLE IF EXISTS `relatorios_cubo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relatorios_cubo` (
  `codrcb` char(10) NOT NULL,
  `codinf` char(10) NOT NULL DEFAULT '',
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `campo_codigo` varchar(30) NOT NULL DEFAULT '',
  `fonte` varchar(50) NOT NULL DEFAULT '',
  `cor_fundo` varchar(11) DEFAULT '',
  `degrade` char(1) NOT NULL DEFAULT 'N',
  `mostra_titulo` char(1) NOT NULL DEFAULT 'S',
  `borda` char(1) NOT NULL DEFAULT 'N',
  `area_nao_usada` char(1) NOT NULL DEFAULT 'N',
  `tree_horizontal` char(1) NOT NULL DEFAULT 'S',
  `tree_vertical` char(1) NOT NULL DEFAULT 'S',
  `degrade_dimensoes` char(1) NOT NULL DEFAULT 'N',
  `fundo_degrade` char(1) NOT NULL DEFAULT 'N',
  `step` int(3) unsigned NOT NULL,
  `minimizado_h` char(1) NOT NULL DEFAULT 'N',
  `minimizado_v` char(1) NOT NULL DEFAULT 'N',
  `permite_filtros` char(1) NOT NULL DEFAULT 'S',
  `permite_mudar_dim` char(1) NOT NULL DEFAULT 'S',
  `stilo_flat` int(1) unsigned NOT NULL DEFAULT '0',
  `com_titulos_f` char(1) NOT NULL DEFAULT 'S',
  `com_titulos_v` char(1) NOT NULL DEFAULT 'S',
  `com_titulos_h` char(1) NOT NULL DEFAULT 'S',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcar` char(10) NOT NULL DEFAULT '',
  `consulta_sql` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  `propriedades` mediumtext NOT NULL,
  `script_pos_sql` mediumtext NOT NULL,
  PRIMARY KEY (`codrcb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios_cubo`
-- Table structure for table `adquirente`
--

DROP TABLE IF EXISTS `adquirente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adquirente` (
  `codadq` varchar(10) NOT NULL COMMENT 'Codigo da Adquirente',
  `nome_adq` varchar(30) NOT NULL COMMENT 'Nome da Adquirente',
  `codadqext` varchar(30) NOT NULL COMMENT 'Codigo da Adquirente em outro sistema',
  `codemp` varchar(10) NOT NULL COMMENT 'Codigo da empresa no Integrator',
  `codusu` char(2) NOT NULL COMMENT 'Codigo do usuário que fez o cadastro',
  `status_adq` char(1) NOT NULL COMMENT 'Status da Aquirente (A Tivo;S usupenso;C ancelado)',
  `data_lan` datetime NOT NULL COMMENT 'Data de cadastro',
  `data_sus` datetime DEFAULT NULL COMMENT 'Data de suspensão',
  `data_can` datetime DEFAULT NULL COMMENT 'Data de Cancelamento',
  `codtplat` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codadq`),
  KEY `codemp` (`codemp`),
  KEY `codusu` (`codusu`),
  KEY `data_lan` (`data_lan`),
  KEY `data_sus` (`data_sus`),
  KEY `data_can` (`data_can`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adquirente`
-- Table structure for table `adquirente_cartao`
--

DROP TABLE IF EXISTS `adquirente_cartao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adquirente_cartao` (
  `codadqcar` varchar(10) NOT NULL COMMENT 'Chave primária',
  `codadq` varchar(10) NOT NULL COMMENT 'Codigo da Adquirente',
  `codcar` varchar(10) NOT NULL COMMENT 'Codigo do Cartão (Bandeira)',
  `codcontext` varchar(30) NOT NULL DEFAULT '' COMMENT 'Codigo do cartão em outro sistema',
  `float_cred` int(2) NOT NULL DEFAULT '30' COMMENT 'Float para o recebimento em caso de Credito',
  `float_deb` int(2) NOT NULL DEFAULT '1' COMMENT 'Float para o recebimento em caso de Débito',
  `tarifa_cred` decimal(5,2) NOT NULL DEFAULT '0.00' COMMENT 'Tarifa cobrada em pagamentos de Credito',
  `tarifa_deb` decimal(5,2) NOT NULL DEFAULT '0.00' COMMENT 'Tarifa cobrada em pagamentos de Débito',
  `status_adqcar` char(1) NOT NULL DEFAULT 'A',
  PRIMARY KEY (`codadqcar`),
  KEY `codcar` (`codcar`),
  KEY `codadq` (`codadq`),
  CONSTRAINT `codadq` FOREIGN KEY (`codadq`) REFERENCES `adquirente` (`codadq`),
  CONSTRAINT `codcar` FOREIGN KEY (`codcar`) REFERENCES `cartaocredito` (`codcar`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adquirente_cartao`
-- Table structure for table `detalhe_cancel_mov_pat`
--

DROP TABLE IF EXISTS `detalhe_cancel_mov_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_cancel_mov_pat` (
  `coddcmvp` varchar(10) NOT NULL DEFAULT '',
  `codpat` varchar(10) NOT NULL DEFAULT '',
  `codcmvp` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddcmvp`),
  KEY `codpat` (`codpat`),
  KEY `codcmvp` (`codcmvp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_cancel_mov_pat`
-- Table structure for table `script_onu`
--

DROP TABLE IF EXISTS `script_onu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_onu` (
  `codscp_onu` char(10) NOT NULL,
  `descricao_script` varchar(50) NOT NULL DEFAULT '',
  `script_cmd` mediumtext NOT NULL,
  `codtolt` char(10) NOT NULL,
  `codtexec` char(10) NOT NULL,
  `codtconu` char(10) NOT NULL,
  `tempo_espera` int(11) NOT NULL DEFAULT '0',
  `voz_tv` char(1) NOT NULL DEFAULT 'N',
  `codscnx` char(10) NOT NULL DEFAULT '01TELNET',
  `codstcom` char(10) NOT NULL DEFAULT '',
  `pppoe` char(1) NOT NULL DEFAULT 'N',
  `wireless` char(1) NOT NULL DEFAULT 'N',
  `lanport` int(2) NOT NULL DEFAULT '0',
  `voiceport` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codscp_onu`),
  KEY `codtolt` (`codtolt`),
  KEY `codtcmd` (`codtexec`),
  KEY `codtconu` (`codtconu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_onu`
-- Table structure for table `tipo_comissionado`
--

DROP TABLE IF EXISTS `tipo_comissionado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_comissionado` (
  `codtcs` varchar(10) NOT NULL,
  `codfcs` varchar(10) NOT NULL,
  `descri_tcs` varchar(50) NOT NULL,
  `ativo` char(1) NOT NULL,
  PRIMARY KEY (`codtcs`),
  KEY `codfcs` (`codfcs`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_comissionado`
-- Table structure for table `regras_negociacao`
--

DROP TABLE IF EXISTS `regras_negociacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_negociacao` (
  `codrneg` varchar(10) NOT NULL,
  `codrcob` varchar(10) NOT NULL,
  `valor_desde` float(10,2) NOT NULL DEFAULT '0.00',
  `valor_ate` float(10,2) NOT NULL DEFAULT '0.00',
  `ativa` char(1) NOT NULL,
  PRIMARY KEY (`codrneg`),
  KEY `codrcob` (`codrcob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_negociacao`
-- Table structure for table `compromisos`
--

DROP TABLE IF EXISTS `compromisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compromisos` (
  `codcomp` varchar(10) NOT NULL DEFAULT '',
  `coddono` char(2) NOT NULL DEFAULT '',
  `data_ini` date NOT NULL DEFAULT '0000-00-00',
  `data_fin` date NOT NULL DEFAULT '0000-00-00',
  `hora_ini` varchar(5) NOT NULL DEFAULT '',
  `hora_fin` varchar(5) NOT NULL DEFAULT '',
  `codscom` char(1) NOT NULL DEFAULT '',
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `tipo_comp` varchar(10) NOT NULL DEFAULT '',
  `descri_comp` text NOT NULL,
  `conclucao` text NOT NULL,
  `codigo_vin` varchar(10) NOT NULL DEFAULT '',
  `tipo_vin` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcomp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compromisos`
-- Table structure for table `log_troca_status`
--

DROP TABLE IF EXISTS `log_troca_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_troca_status` (
  `codlts` varchar(10) NOT NULL,
  `codtsp` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `log_execucao` mediumtext NOT NULL,
  PRIMARY KEY (`codlts`),
  KEY `codtsp` (`codtsp`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_troca_status`
-- Table structure for table `grupo_parceiros`
--

DROP TABLE IF EXISTS `grupo_parceiros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_parceiros` (
  `codgpar` varchar(10) NOT NULL,
  `descri_gpar` varchar(50) NOT NULL,
  PRIMARY KEY (`codgpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_parceiros`
-- Table structure for table `status_prospect`
--

DROP TABLE IF EXISTS `status_prospect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_prospect` (
  `codestp` varchar(10) NOT NULL DEFAULT '',
  `codemr` varchar(10) NOT NULL,
  `descri_estp` varchar(50) NOT NULL DEFAULT '',
  `tipo_prospect` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codestp`),
  KEY `codemr` (`codemr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_prospect`
-- Table structure for table `usuarios_cancelados`
--

DROP TABLE IF EXISTS `usuarios_cancelados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_cancelados` (
  `codusu` char(2) NOT NULL DEFAULT '',
  `data_lan` datetime NOT NULL,
  `data_can` datetime DEFAULT NULL,
  `codpar` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codcar_e` varchar(10) NOT NULL,
  `codtec` varchar(10) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `coddep` varchar(10) NOT NULL,
  `codigo_externo` varchar(20) DEFAULT NULL,
  `usuario_externo` varchar(50) DEFAULT NULL,
  `codtur` varchar(10) NOT NULL,
  `adm_sistema` char(1) NOT NULL DEFAULT 'N',
  `login` varchar(20) NOT NULL DEFAULT '',
  `senha` int(10) NOT NULL DEFAULT '0',
  `contrasenha` varchar(10) NOT NULL DEFAULT '',
  `nome_usu` varchar(30) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `ramal_ura` varchar(20) NOT NULL,
  `senha_ramal` varchar(30) NOT NULL,
  `endereco` varchar(30) NOT NULL DEFAULT '',
  `bairro` varchar(10) NOT NULL DEFAULT '',
  `cidade` varchar(15) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL,
  `fax` varchar(15) NOT NULL DEFAULT '',
  `bipper` char(3) NOT NULL DEFAULT '',
  `e_mail` varchar(60) NOT NULL,
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT '',
  `tecnico` char(1) NOT NULL DEFAULT '',
  `vendedor` char(1) NOT NULL DEFAULT '',
  `ver_cliente` char(1) NOT NULL DEFAULT 'T',
  `ver_prospect` char(1) NOT NULL DEFAULT 'T',
  `controla_email` char(1) NOT NULL DEFAULT '',
  `controla_oco_lem` char(1) NOT NULL DEFAULT '',
  `tempo_control` int(2) unsigned NOT NULL DEFAULT '0',
  `obs` text NOT NULL,
  `bloqueado` char(1) NOT NULL DEFAULT 'N',
  `codlmp` char(10) NOT NULL DEFAULT '',
  `data_troca_senha` date NOT NULL DEFAULT '0000-00-00',
  `id_funil` int(11) NOT NULL DEFAULT '0',
  `usu_img` mediumtext,
  KEY `codven` (`codven`),
  KEY `codpar` (`codpar`),
  KEY `codtec` (`codtec`),
  KEY `codcar_e` (`codcar_e`),
  KEY `codcar` (`codcar`),
  KEY `codigo_externo` (`codigo_externo`),
  KEY `usuario_externo` (`usuario_externo`),
  KEY `codlmp` (`codlmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_cancelados`
-- Table structure for table `det_aco_diario`
--

DROP TABLE IF EXISTS `det_aco_diario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_aco_diario` (
  `coddacd` varchar(10) NOT NULL,
  `codgacd` varchar(10) NOT NULL,
  `codind` varchar(10) NOT NULL,
  `codfmj` varchar(10) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `somatorio` char(1) NOT NULL DEFAULT 'N',
  `tipo` char(1) NOT NULL,
  `signo` char(1) NOT NULL DEFAULT '+',
  `ordem` int(2) NOT NULL,
  PRIMARY KEY (`coddacd`),
  KEY `codgacd` (`codgacd`),
  KEY `codind` (`codind`),
  KEY `codfmj` (`codfmj`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_aco_diario`
-- Table structure for table `favoritos`
--

DROP TABLE IF EXISTS `favoritos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favoritos` (
  `codfav` varchar(10) NOT NULL,
  `codusu` varchar(3) DEFAULT NULL,
  `codint` varchar(10) DEFAULT NULL,
  `codopc` varchar(10) DEFAULT NULL,
  `codmod` varchar(10) DEFAULT NULL,
  `codtfav` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codfav`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favoritos`
-- Table structure for table `cod_reg_retorno`
--

DROP TABLE IF EXISTS `cod_reg_retorno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cod_reg_retorno` (
  `codcrr` varchar(10) NOT NULL DEFAULT '',
  `numero_banco` char(3) NOT NULL DEFAULT '',
  `codigo` varchar(4) NOT NULL DEFAULT '',
  `descri_crr` varchar(40) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'D',
  PRIMARY KEY (`codcrr`),
  KEY `numero_banco` (`numero_banco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cod_reg_retorno`
-- Table structure for table `movimentos_hist_apagar`
--

DROP TABLE IF EXISTS `movimentos_hist_apagar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentos_hist_apagar` (
  `codmovex` char(10) NOT NULL DEFAULT '',
  `codmvp` char(10) NOT NULL DEFAULT '',
  `codlic` char(10) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de Início do Serviço',
  `quantidade` decimal(10,2) NOT NULL DEFAULT '0.00',
  `codmvp_origem` char(10) NOT NULL DEFAULT '' COMMENT 'Campo para informar o codmvp de origem do movimento',
  PRIMARY KEY (`codmovex`),
  KEY `codmvp` (`codmvp`),
  KEY `codlic` (`codlic`),
  KEY `quantidade` (`quantidade`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos_hist_apagar`
-- Table structure for table `respostas`
--

DROP TABLE IF EXISTS `respostas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `respostas` (
  `codresp` varchar(10) NOT NULL DEFAULT '',
  `codperg` varchar(10) NOT NULL DEFAULT '',
  `nome_resp` varchar(30) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  PRIMARY KEY (`codresp`),
  KEY `codperg` (`codperg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respostas`
-- Table structure for table `telas`
--

DROP TABLE IF EXISTS `telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `telas` (
  `codtel` varchar(10) NOT NULL,
  `codist` varchar(10) NOT NULL,
  `codmis` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `codidm` varchar(10) NOT NULL,
  `nome_tela` varchar(50) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `arquivo` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtel`),
  KEY `codist` (`codist`),
  KEY `codmis` (`codmis`),
  KEY `codtab` (`codtab`),
  KEY `codidm` (`codidm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telas`
-- Table structure for table `det_contas_pag`
--

DROP TABLE IF EXISTS `det_contas_pag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_contas_pag` (
  `coddcp` varchar(10) NOT NULL DEFAULT '',
  `codcpag` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `histo_dcp` varchar(100) NOT NULL DEFAULT '',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `valor_dcp` decimal(10,2) NOT NULL DEFAULT '0.00',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `codfcs` varchar(10) NOT NULL,
  PRIMARY KEY (`coddcp`),
  KEY `codcpag` (`codcpag`),
  KEY `codpop` (`codpop`),
  KEY `codcta` (`codcta`),
  KEY `codemp` (`codemp`),
  KEY `codctc` (`codctc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_contas_pag`
-- Table structure for table `execucao_manu_bd`
--

DROP TABLE IF EXISTS `execucao_manu_bd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `execucao_manu_bd` (
  `codembd` char(10) NOT NULL DEFAULT '',
  `codmbd` char(10) NOT NULL DEFAULT '',
  `codsercli` char(10) NOT NULL DEFAULT '',
  `ok` char(1) NOT NULL DEFAULT '',
  `data_hora` datetime NOT NULL,
  `resposta` mediumtext NOT NULL,
  PRIMARY KEY (`codembd`),
  KEY `codsercli` (`codsercli`),
  KEY `ok` (`ok`),
  KEY `codmbd` (`codmbd`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `execucao_manu_bd`
-- Table structure for table `nota_fiscal_n`
--

DROP TABLE IF EXISTS `nota_fiscal_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nota_fiscal_n` (
  `codnf` varchar(10) NOT NULL DEFAULT '',
  `codtnf` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `codraf` varchar(10) NOT NULL,
  `codrnf` varchar(10) NOT NULL,
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codmnf` varchar(10) NOT NULL DEFAULT '',
  `codfor` varchar(10) NOT NULL,
  `codemp_d` varchar(10) NOT NULL,
  `codigo_cnf` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `data_cad` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cfop` varchar(10) NOT NULL,
  `serie_nf` char(4) NOT NULL DEFAULT '',
  `numero_nf` int(9) NOT NULL DEFAULT '0',
  `data_lan` date NOT NULL,
  `data_can` date NOT NULL,
  `nro_protocolo` varchar(20) NOT NULL,
  `nro_recibo` varchar(20) NOT NULL,
  `valor_nf` float(10,2) NOT NULL DEFAULT '0.00',
  `base_icms` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_icms` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_fust` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_funtel` float(8,2) NOT NULL DEFAULT '0.00',
  `base_iss` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_iss` float(8,2) NOT NULL DEFAULT '0.00',
  `base_pis` float(8,2) NOT NULL,
  `valor_pis` float(8,2) NOT NULL DEFAULT '0.00',
  `base_cofins` float(8,2) NOT NULL,
  `valor_cofins` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_ipi` float(8,2) NOT NULL,
  `base_iva` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_iva` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_simp` float(8,2) NOT NULL DEFAULT '0.00',
  `identificacao` varchar(39) NOT NULL DEFAULT '',
  `cancelada` char(1) NOT NULL DEFAULT 'N',
  `xml` mediumtext NOT NULL,
  `nome_nf` varchar(100) NOT NULL,
  PRIMARY KEY (`codnf`),
  UNIQUE KEY `codigo_cnf` (`codigo_cnf`),
  KEY `codcli` (`codcli`),
  KEY `codmnf` (`codmnf`),
  KEY `codrnf` (`codrnf`),
  KEY `codraf` (`codraf`),
  KEY `codtnf` (`codtnf`),
  KEY `codemp` (`codemp`),
  KEY `data_cad` (`data_cad`),
  KEY `codfor` (`codfor`),
  KEY `codemp_d` (`codemp_d`)
) ENGINE=InnoDB AUTO_INCREMENT=6331 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_fiscal_n`
-- Table structure for table `sociedade_cota_participacao`
--

DROP TABLE IF EXISTS `sociedade_cota_participacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sociedade_cota_participacao` (
  `codscp` varchar(10) NOT NULL,
  `nome_scp` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codscp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sociedade_cota_participacao`
-- Table structure for table `tipo_indicador`
--

DROP TABLE IF EXISTS `tipo_indicador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_indicador` (
  `codtind` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `descri_tind` varchar(50) NOT NULL,
  `tipo` char(2) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtind`),
  KEY `codtab` (`codtab`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_indicador`
-- Table structure for table `tipo_conexao_onu`
--

DROP TABLE IF EXISTS `tipo_conexao_onu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_conexao_onu` (
  `codtconu` char(10) NOT NULL,
  `descri_tp_conexao` varchar(45) NOT NULL DEFAULT '',
  `tipo_conexao` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtconu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_conexao_onu`
-- Table structure for table `produtos_fornecedor`
--

DROP TABLE IF EXISTS `produtos_fornecedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produtos_fornecedor` (
  `codpdfr` varchar(10) NOT NULL,
  `codfor` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codigo_for` varchar(20) NOT NULL,
  `descri_for` varchar(120) NOT NULL,
  PRIMARY KEY (`codpdfr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos_fornecedor`
-- Table structure for table `filtros_ibi`
--

DROP TABLE IF EXISTS `filtros_ibi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filtros_ibi` (
  `codfibi` varchar(10) NOT NULL DEFAULT '',
  `codibi` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'F',
  `campo` varchar(100) NOT NULL DEFAULT '',
  `filtro_w` char(1) DEFAULT 'S',
  `operador` char(2) NOT NULL DEFAULT '',
  `data_padrao` date NOT NULL,
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `tamanho` int(4) unsigned NOT NULL,
  `ordem` int(2) NOT NULL,
  `consulta_sql` mediumtext NOT NULL,
  PRIMARY KEY (`codfibi`),
  KEY `codibi` (`codibi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filtros_ibi`
-- Table structure for table `regra_cond_pagamento`
--

DROP TABLE IF EXISTS `regra_cond_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regra_cond_pagamento` (
  `codrcopgt` varchar(10) NOT NULL,
  `codrcob` varchar(10) NOT NULL,
  `codcopgt` varchar(10) NOT NULL,
  PRIMARY KEY (`codrcopgt`),
  KEY `codrcob` (`codrcob`),
  KEY `codcopgt` (`codcopgt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regra_cond_pagamento`
-- Table structure for table `tipo_embalagem_prod`
--

DROP TABLE IF EXISTS `tipo_embalagem_prod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_embalagem_prod` (
  `codtep` varchar(10) NOT NULL,
  `descri_tep` varchar(30) NOT NULL,
  PRIMARY KEY (`codtep`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_embalagem_prod`
-- Table structure for table `tecnicos`
--

DROP TABLE IF EXISTS `tecnicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tecnicos` (
  `codtec` varchar(10) NOT NULL DEFAULT '',
  `nome_tec` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  PRIMARY KEY (`codtec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tecnicos`
-- Table structure for table `valor_campos_plataforma_pagamento`
--

DROP TABLE IF EXISTS `valor_campos_plataforma_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valor_campos_plataforma_pagamento` (
  `codvalplat` char(10) NOT NULL,
  `codcamplat` char(10) DEFAULT NULL,
  `codadq` char(10) NOT NULL DEFAULT '',
  `valor_plat` varchar(100) DEFAULT NULL,
  `codusu` char(2) DEFAULT NULL,
  PRIMARY KEY (`codvalplat`),
  KEY `codcamplat` (`codcamplat`),
  KEY `codadq` (`codadq`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valor_campos_plataforma_pagamento`
-- Table structure for table `usu_afiliados`
--

DROP TABLE IF EXISTS `usu_afiliados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_afiliados` (
  `codusua` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `coddep` varchar(10) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codusua`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_afiliados`
-- Table structure for table `observacoes_pat`
--

DROP TABLE IF EXISTS `observacoes_pat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `observacoes_pat` (
  `codopat` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codopat`),
  KEY `codpat` (`codpat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `observacoes_pat`
-- Table structure for table `sujestoes`
--

DROP TABLE IF EXISTS `sujestoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sujestoes` (
  `codsud` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codusu` char(2) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `estatus` char(1) NOT NULL DEFAULT '',
  `sujestao` text NOT NULL,
  `obs` text NOT NULL,
  PRIMARY KEY (`codsud`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sujestoes`
-- Table structure for table `bancos_unidades`
--

DROP TABLE IF EXISTS `bancos_unidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bancos_unidades` (
  `codp_b` varchar(10) NOT NULL,
  `codban` varchar(10) NOT NULL,
  `codpop` varchar(10) NOT NULL,
  PRIMARY KEY (`codp_b`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancos_unidades`
-- Table structure for table `cartoes_credito`
--

DROP TABLE IF EXISTS `cartoes_credito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cartoes_credito` (
  `codccd` varchar(10) NOT NULL,
  `codban` varchar(10) NOT NULL,
  `codbanc` varchar(10) NOT NULL DEFAULT '',
  `bandeira` varchar(20) NOT NULL,
  `final` varchar(3) NOT NULL,
  `vencimento` varchar(4) NOT NULL,
  PRIMARY KEY (`codccd`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartoes_credito`
-- Table structure for table `mvno`
--

DROP TABLE IF EXISTS `mvno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mvno` (
  `codmvno` char(10) NOT NULL DEFAULT '',
  `codpat` char(10) NOT NULL DEFAULT '',
  `codpref` char(10) NOT NULL DEFAULT '',
  `numero` char(9) NOT NULL DEFAULT '',
  `codtvoz` char(10) NOT NULL DEFAULT '',
  `codsercli` char(10) NOT NULL DEFAULT '',
  `plano_mvno` int(5) NOT NULL DEFAULT '0',
  `data_vinculo` date NOT NULL DEFAULT '0000-00-00',
  `data_bloq` date NOT NULL DEFAULT '0000-00-00',
  `data_troca` date NOT NULL DEFAULT '0000-00-00',
  `data_bloqparcial` date NOT NULL DEFAULT '0000-00-00',
  `data_desbloq` date NOT NULL DEFAULT '0000-00-00',
  `data_cancel` date NOT NULL DEFAULT '0000-00-00',
  `codmvno_a` char(10) NOT NULL DEFAULT '',
  `codmvno_p` char(10) NOT NULL DEFAULT '',
  `status` varchar(35) NOT NULL DEFAULT '',
  `portado` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codmvno`),
  KEY `codpref` (`codpref`),
  KEY `codtvoz` (`codtvoz`),
  KEY `codpat` (`codpat`),
  KEY `codsercli` (`codsercli`),
  KEY `codmvno_a` (`codmvno_a`),
  KEY `codmvno_p` (`codmvno_p`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mvno`
-- Table structure for table `int_xml`
--

DROP TABLE IF EXISTS `int_xml`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_xml` (
  `codxml` varchar(35) NOT NULL DEFAULT '0',
  `xml` mediumtext,
  `modo` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`codxml`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_xml`
-- Table structure for table `visitas`
--

DROP TABLE IF EXISTS `visitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visitas` (
  `codvis` varchar(10) NOT NULL DEFAULT '',
  `nro_vis` varchar(25) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `codtec` varchar(10) NOT NULL DEFAULT '',
  `codmvis` varchar(10) NOT NULL,
  `tipo_contato` char(1) NOT NULL DEFAULT 'T',
  `data_vis` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora` varchar(5) NOT NULL DEFAULT '',
  `minutos` int(3) unsigned NOT NULL DEFAULT '0',
  `data_fim` datetime NOT NULL,
  `descri_vis` text NOT NULL,
  `codocoi` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `nome_contato` varchar(100) NOT NULL DEFAULT '',
  `email_resposta` varchar(100) NOT NULL,
  `fone_resposta` varchar(10) NOT NULL,
  `celular_resposta` varchar(13) NOT NULL,
  PRIMARY KEY (`codvis`),
  KEY `codoco` (`codoco`),
  KEY `data_vis` (`data_vis`),
  KEY `codmvis` (`codmvis`),
  KEY `nro_vis` (`nro_vis`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitas`
-- Table structure for table `manager_cmd`
--

DROP TABLE IF EXISTS `manager_cmd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `manager_cmd` (
  `codcmd` varchar(10) NOT NULL DEFAULT '',
  `id` int(9) NOT NULL DEFAULT '0',
  `descricao` varchar(200) NOT NULL DEFAULT '',
  `comando` varchar(200) NOT NULL DEFAULT '',
  `tipoCMD` varchar(10) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `dtCriacao` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`codcmd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_cmd`
-- Table structure for table `tarefas_oco`
--

DROP TABLE IF EXISTS `tarefas_oco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefas_oco` (
  `codtaro` varchar(10) NOT NULL DEFAULT '',
  `codocop` varchar(10) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `codstto` varchar(10) NOT NULL DEFAULT '',
  `codtarm` varchar(10) NOT NULL,
  `data_lan` datetime NOT NULL,
  `data_lib` datetime NOT NULL,
  `data_ini` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `codusu_sol` char(2) NOT NULL,
  `titulo_taro` varchar(50) NOT NULL DEFAULT '',
  `descri_taro` mediumtext NOT NULL,
  `for_email` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  `posx` int(6) unsigned NOT NULL DEFAULT '0',
  `posy` int(6) unsigned NOT NULL DEFAULT '0',
  `width` int(6) unsigned NOT NULL DEFAULT '0',
  `height` int(6) unsigned NOT NULL DEFAULT '0',
  `obrigatorio` char(1) NOT NULL DEFAULT 'N',
  `tipo_o` char(1) NOT NULL DEFAULT '0',
  `obrigatrio` char(1) DEFAULT 'N',
  `nivel` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codtaro`),
  KEY `codoco` (`codoco`),
  KEY `codtarm` (`codtarm`),
  KEY `codstto` (`codstto`),
  KEY `codocop` (`codocop`),
  KEY `data_ini` (`data_ini`),
  KEY `data_fim` (`data_fim`),
  KEY `data_lib` (`data_lib`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefas_oco`
-- Table structure for table `alertas`
--

DROP TABLE IF EXISTS `alertas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alertas` (
  `codale` char(30) NOT NULL,
  `descri_ale` varchar(300) DEFAULT NULL,
  `severidade` char(3) DEFAULT NULL,
  `ativo` char(3) DEFAULT NULL,
  `codtale` int(3) DEFAULT NULL,
  `nome_per` varchar(150) DEFAULT NULL,
  `mensagem_a` longtext,
  `mensagem_f` longtext,
  PRIMARY KEY (`codale`),
  KEY `ativo` (`ativo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertas`
-- Table structure for table `envio_nfse`
--

DROP TABLE IF EXISTS `envio_nfse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `envio_nfse` (
  `codnfse` varchar(10) NOT NULL,
  `data_lan` datetime NOT NULL,
  `p_desde` date NOT NULL,
  `p_ate` date NOT NULL,
  `ultimo_rps` int(6) unsigned NOT NULL,
  `quant_nfs` int(6) unsigned NOT NULL,
  `total_nfs` float(10,2) NOT NULL,
  `chave_envio` varchar(80) NOT NULL,
  `arq_nfse` mediumtext NOT NULL,
  `ultimo_nro_rps` int(6) unsigned NOT NULL DEFAULT '0',
  `codemp` varchar(10) NOT NULL,
  PRIMARY KEY (`codnfse`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `envio_nfse`
-- Table structure for table `formatos_cond`
--

DROP TABLE IF EXISTS `formatos_cond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `formatos_cond` (
  `codfcnd` varchar(10) NOT NULL,
  `codtcg` varchar(10) NOT NULL,
  `descri_fcnd` varchar(50) NOT NULL,
  `fonte_formato` varchar(50) NOT NULL,
  PRIMARY KEY (`codfcnd`),
  KEY `codtcg` (`codtcg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formatos_cond`
-- Table structure for table `servicos_rad`
--

DROP TABLE IF EXISTS `servicos_rad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_rad` (
  `codsrad` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `quant_lr` int(2) unsigned NOT NULL DEFAULT '0',
  `vincula_rma` char(1) NOT NULL DEFAULT 'S',
  `horas_lr` int(4) unsigned NOT NULL DEFAULT '0',
  `valor_lr_adi` float(10,4) NOT NULL DEFAULT '0.0000',
  `salva_c_dominio` char(1) NOT NULL DEFAULT 'N',
  `codservp_r` varchar(10) NOT NULL DEFAULT '',
  `grupo` varchar(50) NOT NULL DEFAULT '',
  `valor_limite` float(10,2) NOT NULL,
  PRIMARY KEY (`codsrad`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_rad`
-- Table structure for table `logs_error`
--

DROP TABLE IF EXISTS `logs_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_error` (
  `Id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `datatime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `log` text NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=347 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_error`
-- Table structure for table `grupo_snmp_mib`
--

DROP TABLE IF EXISTS `grupo_snmp_mib`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_snmp_mib` (
  `codtblsnmpmib` varchar(10) NOT NULL,
  `mib_detalhe` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`codtblsnmpmib`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_snmp_mib`
-- Table structure for table `det_nota_fiscal`
--

DROP TABLE IF EXISTS `det_nota_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_nota_fiscal` (
  `coddnf` varchar(10) NOT NULL DEFAULT '',
  `codnf` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `coddes` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  `codrimp` varchar(10) NOT NULL,
  `codmvp` varchar(10) NOT NULL,
  `descri_nf` varchar(120) NOT NULL,
  `base_icms` float(10,2) NOT NULL,
  `valor_icms` float(7,2) NOT NULL,
  `valor_fust` float(7,2) NOT NULL,
  `valor_funtel` float(7,2) NOT NULL,
  `base_iss` float(10,2) NOT NULL,
  `valor_iss` float(7,2) NOT NULL,
  `valor_ipi` float(7,2) NOT NULL,
  `base_iva` float(10,2) NOT NULL,
  `valor_iva` float(10,2) NOT NULL,
  `valor_simp` float(10,2) NOT NULL,
  `codrtrib` char(10) NOT NULL COMMENT ' referente a tabela nova de registro_tributacao',
  `cfop` char(4) NOT NULL DEFAULT '' COMMENT 'Cfop',
  `valor_unitario` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor unitario',
  `quantidade` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'quantidade',
  `valor_total` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor total',
  `ncm` char(8) NOT NULL DEFAULT '' COMMENT 'Código NCM com 8 dígitos \nObrigatória informação do NCM completo (8 dígitos).\nNota: Em caso de item de serviço ou item que não tenham produto (ex. transferência de crédito, crédito do ativo imobilizado, etc.), informar o valor 00 (dois zeros). (NT 2014/00',
  `cst` char(4) NOT NULL DEFAULT '' COMMENT 'Código de Tributação do ICMS',
  `icms_origem` char(1) NOT NULL DEFAULT '' COMMENT 'origem do icms da mercadoria: 0 – Nacional; 1 – Estrangeira – Importação direta; 2 – Estrangeira – Adquirida no mercado interno.',
  `modbc` char(1) NOT NULL DEFAULT '' COMMENT 'Modalidade de determinação da BC do\nICMS\r',
  `pmvast` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual da margem de valor Adicionado\ndo ICMS ST',
  `picms` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Alíquota do imposto ICMS',
  `mod_bc_st` char(1) NOT NULL DEFAULT '' COMMENT 'Modalidade de determinação da BC do\nICMS ST',
  `base_icms_st` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor da BC do ICMS ST',
  `picms_st` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Alíquota do imposto do ICMS ST',
  `valor_icms_st` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do ICMS ST \n',
  `base_red_icms` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'base de reducao do icms',
  `pred_bc` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'percentual de reducao da base de calculo icms',
  `base_red_icms_st` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'base de reducao icms st',
  `pred_bc_st` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'percentual de reducao base de calculo icms st',
  `base_pis` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'base do pis',
  `p_pis` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'percentual pis',
  `valor_pis` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor do pis',
  `base_cofins` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'base cofins',
  `pcofins` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'percentual cofins',
  `valor_cofins` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor cofins',
  `base_ipi` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'base ipi',
  `p_ipi` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'percentual ipi',
  `cenq` char(3) NOT NULL DEFAULT '' COMMENT ' Código de Enquadramento Legal do IPI;',
  `cest` char(10) NOT NULL DEFAULT '' COMMENT 'Código Cest do produto',
  `coduprod` char(10) NOT NULL DEFAULT '' COMMENT 'Código Unidade Medida do produto',
  `codprod` char(10) NOT NULL DEFAULT '' COMMENT 'Código do produto',
  `codbeneficio` char(10) NOT NULL DEFAULT '' COMMENT 'Código do benefício fiscal',
  `pis_cst` char(2) NOT NULL DEFAULT '' COMMENT 'Código Situação Tributária PIS.',
  `cofins_cst` char(2) NOT NULL DEFAULT '' COMMENT 'Código Situação Tributária COFINS.',
  `ipi_cst` char(2) NOT NULL DEFAULT '' COMMENT 'Código da Situação Tributária IPI.',
  `pdif` decimal(10,4) NOT NULL DEFAULT '0.0000' COMMENT 'Percentual do Diferimento Parcial.',
  `adic_ipi` char(1) NOT NULL DEFAULT '' COMMENT 'Adiciona IPI a Base de Cálculo',
  `valor_dif` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do Diferimento Parcial.',
  `valor_icms_dif` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do ICMS do Diferimento Parcial.',
  `valor_frete` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do rateio do Frete.',
  `valor_seguro` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do rateio do Seguro.',
  `valor_outras_despesas` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do rateio das Outras Despesas.',
  `valor_desconto` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do rateio do Desconto.',
  `cancelada` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`coddnf`),
  KEY `codnf` (`codnf`),
  KEY `codcrec` (`codcrec`),
  KEY `codpat` (`codpat`),
  KEY `codrimp` (`codrimp`),
  KEY `coddes` (`coddes`),
  KEY `codmvp` (`codmvp`),
  KEY `codrtrib` (`codrtrib`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_nota_fiscal`
-- Table structure for table `resultado_ligacoes_avc`
--

DROP TABLE IF EXISTS `resultado_ligacoes_avc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resultado_ligacoes_avc` (
  `codrlu` varchar(10) NOT NULL,
  `codcla` varchar(10) NOT NULL,
  `idresultado` int(3) unsigned NOT NULL,
  `api_executar` varchar(100) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codrlu`),
  KEY `codcla` (`codcla`),
  KEY `idresultado` (`idresultado`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resultado_ligacoes_avc`
-- Table structure for table `gwp_webhook`
--

DROP TABLE IF EXISTS `gwp_webhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gwp_webhook` (
  `codgwpw` int(10) NOT NULL AUTO_INCREMENT,
  `codcob` varchar(10) NOT NULL,
  `processada` char(1) NOT NULL DEFAULT 'N',
  `ip` varchar(20) NOT NULL,
  `data_hora` datetime NOT NULL,
  `request_webhook` mediumtext NOT NULL,
  `msg_integrator` mediumtext NOT NULL,
  PRIMARY KEY (`codgwpw`),
  KEY `codcob` (`codcob`),
  KEY `processada` (`processada`)
) ENGINE=MyISAM AUTO_INCREMENT=5737 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gwp_webhook`
-- Table structure for table `paises`
--

DROP TABLE IF EXISTS `paises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paises` (
  `id_pais` int(11) NOT NULL AUTO_INCREMENT,
  `nome_pais` char(50) NOT NULL DEFAULT '',
  `codigo_onu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_pais`)
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paises`
-- Table structure for table `agenda_upd_arquivos`
--

DROP TABLE IF EXISTS `agenda_upd_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agenda_upd_arquivos` (
  `codaguarq` bigint(20) NOT NULL AUTO_INCREMENT,
  `codupdarq` char(10) DEFAULT NULL,
  `codagu` char(10) DEFAULT NULL,
  `versao` int(11) DEFAULT NULL,
  `md5` varchar(50) DEFAULT NULL,
  `data_upd` datetime DEFAULT NULL,
  PRIMARY KEY (`codaguarq`),
  KEY `codudparq` (`codupdarq`),
  KEY `codagu` (`codagu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda_upd_arquivos`
-- Table structure for table `status_login_radius`
--

DROP TABLE IF EXISTS `status_login_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_login_radius` (
  `codstl` varchar(10) NOT NULL,
  `descri_stl` varchar(50) NOT NULL,
  `desconectar` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codstl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_login_radius`
-- Table structure for table `tipo_pessoa`
--

DROP TABLE IF EXISTS `tipo_pessoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_pessoa` (
  `tipo_cliente` char(1) NOT NULL,
  `codtnf` varchar(10) NOT NULL,
  `descri_tp` varchar(50) NOT NULL,
  `gera_imposto` char(1) NOT NULL DEFAULT 'S',
  `gera_nota` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`tipo_cliente`),
  KEY `codtnf` (`codtnf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_pessoa`
-- Table structure for table `servicos_cli_combo`
--

DROP TABLE IF EXISTS `servicos_cli_combo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_combo` (
  `codserclicombo` char(10) NOT NULL,
  `codagrcombo` char(10) NOT NULL,
  `codsercli` char(10) NOT NULL,
  `codcombo` char(10) NOT NULL,
  `valor_multa` float(6,2) NOT NULL,
  `nro_combo` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codserclicombo`),
  KEY `codsercli` (`codsercli`,`codcombo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_combo`
-- Table structure for table `arquivo_bco`
--

DROP TABLE IF EXISTS `arquivo_bco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arquivo_bco` (
  `codarq` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_oco` date NOT NULL DEFAULT '0000-00-00',
  `nro_arq_ret` int(5) unsigned NOT NULL DEFAULT '0',
  `nro_arq_rem` int(5) unsigned NOT NULL DEFAULT '0',
  `nome_arq` varchar(150) NOT NULL DEFAULT '',
  `arquivo` mediumtext NOT NULL,
  `total_reg` int(5) unsigned NOT NULL DEFAULT '0',
  `valor_reg` float(10,2) NOT NULL DEFAULT '0.00',
  `valor_juros` float(10,2) NOT NULL DEFAULT '0.00',
  `inicio_nosso_nro` varchar(20) NOT NULL DEFAULT '',
  `final_nosso_nro` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codarq`),
  KEY `data` (`data`),
  KEY `nome_arq` (`nome_arq`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arquivo_bco`
-- Table structure for table `emails_recebidos_spam`
--

DROP TABLE IF EXISTS `emails_recebidos_spam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emails_recebidos_spam` (
  `codemrs` varchar(10) NOT NULL,
  `codemr` varchar(10) NOT NULL,
  `remetente` varchar(100) NOT NULL,
  `codusu` char(2) NOT NULL,
  PRIMARY KEY (`codemrs`),
  KEY `codemr` (`codemr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails_recebidos_spam`
-- Table structure for table `regiao_metropolitana`
--

DROP TABLE IF EXISTS `regiao_metropolitana`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regiao_metropolitana` (
  `codrgmt` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `descri_regmtp` varchar(70) NOT NULL,
  PRIMARY KEY (`codrgmt`),
  KEY `cidade` (`cidade`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regiao_metropolitana`
-- Table structure for table `consultas_servidores`
--

DROP TABLE IF EXISTS `consultas_servidores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultas_servidores` (
  `codcsvp` varchar(10) NOT NULL,
  `codcpub` varchar(10) NOT NULL,
  `id` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codcsvp`),
  KEY `codcpub` (`codcpub`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultas_servidores`
-- Table structure for table `tipo_nota_fiscal`
--

DROP TABLE IF EXISTS `tipo_nota_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_nota_fiscal` (
  `codtnf` varchar(10) NOT NULL,
  `coddoc` varchar(10) NOT NULL,
  `codrela` char(10) NOT NULL DEFAULT '',
  `descri_tnf` varchar(50) NOT NULL,
  PRIMARY KEY (`codtnf`),
  KEY `codrela` (`codrela`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_nota_fiscal`
-- Table structure for table `parcelas_neg`
--

DROP TABLE IF EXISTS `parcelas_neg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parcelas_neg` (
  `codpneg` varchar(10) NOT NULL,
  `codrneg` varchar(10) NOT NULL,
  `descri_pneg` varchar(100) NOT NULL,
  `nro_parcelas` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codpneg`),
  KEY `codrneg` (`codrneg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parcelas_neg`
-- Table structure for table `tipo_grid`
--

DROP TABLE IF EXISTS `tipo_grid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_grid` (
  `codtgrd` varchar(10) NOT NULL,
  `codist` varchar(10) NOT NULL,
  `descri_tgrd` varchar(30) NOT NULL,
  `classe` varchar(50) NOT NULL,
  `vcx` varchar(30) NOT NULL,
  `fonte_titulo` varchar(50) NOT NULL,
  `fonte_coluna` varchar(50) NOT NULL,
  `propriedades` mediumtext NOT NULL,
  PRIMARY KEY (`codtgrd`),
  KEY `codist` (`codist`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_grid`
-- Table structure for table `interfaces_bi`
--

DROP TABLE IF EXISTS `interfaces_bi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaces_bi` (
  `codibi` varchar(10) NOT NULL,
  `descri_ibi` varchar(30) NOT NULL,
  PRIMARY KEY (`codibi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interfaces_bi`
-- Table structure for table `eventos_faturamento`
--

DROP TABLE IF EXISTS `eventos_faturamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventos_faturamento` (
  `code_f` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL,
  `codftm` varchar(10) NOT NULL DEFAULT '',
  `codmvp` varchar(10) NOT NULL,
  `codcomp` varchar(4) NOT NULL DEFAULT '',
  `codmed` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `codtef` varchar(10) NOT NULL DEFAULT 'TIPEVEPADR',
  `codprom` varchar(10) NOT NULL,
  `codarq` varchar(10) NOT NULL,
  `p_desde` date NOT NULL DEFAULT '0000-00-00',
  `p_ate` date NOT NULL DEFAULT '0000-00-00',
  `descri_e_f` varchar(70) NOT NULL,
  `porcentagem` float(9,4) NOT NULL DEFAULT '0.0000',
  `valor` float(10,2) NOT NULL DEFAULT '0.00',
  `absoluto` char(1) NOT NULL DEFAULT 'S',
  `parcelas` int(2) unsigned NOT NULL DEFAULT '0',
  `promocional` char(1) NOT NULL DEFAULT 'N',
  `dias` int(2) NOT NULL,
  `nf_externa` varchar(13) NOT NULL,
  `codst_f` char(1) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`code_f`),
  KEY `codsercli` (`codsercli`),
  KEY `codftm` (`codftm`),
  KEY `codcomp` (`codcomp`),
  KEY `codmed` (`codmed`),
  KEY `codsad` (`codsad`),
  KEY `codtef` (`codtef`),
  KEY `codprom` (`codprom`),
  KEY `codarq` (`codarq`),
  KEY `codst_f` (`codst_f`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_faturamento`
-- Table structure for table `stilo_cond_rela_cubo`
--

DROP TABLE IF EXISTS `stilo_cond_rela_cubo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stilo_cond_rela_cubo` (
  `codscrc` varchar(10) NOT NULL,
  `coddrc` varchar(10) NOT NULL,
  `condicao` varchar(100) NOT NULL,
  `fonte` varchar(50) NOT NULL,
  PRIMARY KEY (`codscrc`),
  KEY `coddrc` (`coddrc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stilo_cond_rela_cubo`
-- Table structure for table `det_tarifas_un`
--

DROP TABLE IF EXISTS `det_tarifas_un`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_tarifas_un` (
  `coddtun` varchar(10) NOT NULL,
  `codtari` varchar(10) NOT NULL,
  `codpop` varchar(10) NOT NULL,
  `valor` float(10,2) DEFAULT NULL,
  `porcentagem` float(8,3) NOT NULL,
  PRIMARY KEY (`coddtun`),
  KEY `codtari` (`codtari`),
  KEY `codpop` (`codpop`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_tarifas_un`
-- Table structure for table `navegacao_fora_franquia`
--

DROP TABLE IF EXISTS `navegacao_fora_franquia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `navegacao_fora_franquia` (
  `codnff` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `compe` char(4) NOT NULL,
  `upload` int(8) unsigned NOT NULL,
  `download` int(8) unsigned NOT NULL,
  `tempo` int(8) unsigned NOT NULL,
  `data_med` datetime NOT NULL,
  PRIMARY KEY (`codnff`),
  KEY `codsercli` (`codsercli`),
  KEY `compe` (`compe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `navegacao_fora_franquia`
-- Table structure for table `numeros_promocao`
--

DROP TABLE IF EXISTS `numeros_promocao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `numeros_promocao` (
  `codfel` varchar(10) NOT NULL DEFAULT '',
  `numero` int(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codfel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `numeros_promocao`
-- Table structure for table `nf_fatura`
--

DROP TABLE IF EXISTS `nf_fatura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nf_fatura` (
  `codnffat` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `codfat` varchar(10) NOT NULL DEFAULT '',
  `codnfp` varchar(10) NOT NULL,
  `nome_nf_fatura` varchar(100) NOT NULL,
  `nf_fatura` mediumtext NOT NULL,
  PRIMARY KEY (`codnffat`),
  KEY `codnf` (`codnf`),
  KEY `codfat` (`codfat`),
  KEY `codnfp` (`codnfp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nf_fatura`
-- Table structure for table `filmes_sc`
--

DROP TABLE IF EXISTS `filmes_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filmes_sc` (
  `codflmsc` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codflm` varchar(10) NOT NULL,
  `code_f` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `data_hora_reg` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filmes_sc`
-- Table structure for table `usu_comissionados`
--

DROP TABLE IF EXISTS `usu_comissionados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_comissionados` (
  `codusc` varchar(10) NOT NULL,
  `codtcs` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codfcs` varchar(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_comissionados`
-- Table structure for table `det_financeiro_nf`
--

DROP TABLE IF EXISTS `det_financeiro_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_financeiro_nf` (
  `coddfnf` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `data_ven` date NOT NULL,
  `nro_doc` varchar(20) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`coddfnf`),
  KEY `codnf` (`codnf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_financeiro_nf`
-- Table structure for table `observacoes`
--

DROP TABLE IF EXISTS `observacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `observacoes` (
  `codobs` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcon` int(6) unsigned NOT NULL,
  `codtobs` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `mostra_ao_abrir` char(1) NOT NULL DEFAULT 'N',
  `obs` text NOT NULL,
  PRIMARY KEY (`codobs`),
  KEY `codcli` (`codcli`),
  KEY `codtobs` (`codtobs`),
  KEY `codcon` (`codcon`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `observacoes`
-- Table structure for table `servicos_radios`
--

DROP TABLE IF EXISTS `servicos_radios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_radios` (
  `codsrd` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codrad` varchar(10) NOT NULL,
  `id_servico` varchar(30) NOT NULL,
  PRIMARY KEY (`codsrd`),
  KEY `codser` (`codser`),
  KEY `codrad` (`codrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_radios`
-- Table structure for table `regras_negocio`
--

DROP TABLE IF EXISTS `regras_negocio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_negocio` (
  `codrng` varchar(10) NOT NULL DEFAULT '',
  `descri_rng` varchar(50) NOT NULL DEFAULT '',
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `valor` float(10,2) NOT NULL,
  `valor_instalacao` float(10,2) NOT NULL,
  `adiciona_multa` char(1) NOT NULL DEFAULT 'S',
  `tipo_regra` char(1) NOT NULL DEFAULT 'P',
  `obs` mediumtext NOT NULL,
  `desconto_debitosnaoacatado` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codrng`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_negocio`
-- Table structure for table `servicos_voz_redir`
--

DROP TABLE IF EXISTS `servicos_voz_redir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_voz_redir` (
  `codsvrd` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `sigame` char(1) NOT NULL,
  `criar_conta_rec` varchar(10) NOT NULL,
  `valor_sigame` float(10,4) NOT NULL,
  `cobra_mensal` char(1) NOT NULL,
  `parcelas` int(2) NOT NULL,
  PRIMARY KEY (`codsvrd`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_voz_redir`
-- Table structure for table `tipo_cep`
--

DROP TABLE IF EXISTS `tipo_cep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cep` (
  `codtcep` varchar(10) NOT NULL DEFAULT '',
  `nome_tcep` varchar(50) NOT NULL DEFAULT '',
  `nome_tcep_r` varchar(30) NOT NULL DEFAULT '',
  `ordem` int(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codtcep`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cep`
-- Table structure for table `telefone`
--

DROP TABLE IF EXISTS `telefone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `telefone` (
  `codfone` char(10) NOT NULL COMMENT '||ContactsTelephones',
  `ativo` char(1) NOT NULL DEFAULT 'S' COMMENT '||-',
  `ddi` char(4) NOT NULL DEFAULT '' COMMENT '||-',
  `ddd` char(5) NOT NULL DEFAULT '' COMMENT '||-',
  `numero_fone` char(10) NOT NULL DEFAULT '' COMMENT '||-',
  `codco_cl_p` char(10) NOT NULL DEFAULT '' COMMENT '||-',
  `mascara` varchar(45) NOT NULL DEFAULT '' COMMENT '||-',
  `principal` char(1) NOT NULL DEFAULT 'N' COMMENT '||-',
  `codcfone` char(10) NOT NULL DEFAULT '' COMMENT '||-',
  `ramal` char(10) NOT NULL DEFAULT '' COMMENT '||-',
  `codcli` int(6) NOT NULL DEFAULT '0' COMMENT '||-',
  `descricao` text COMMENT '||-',
  `codpros` char(10) NOT NULL DEFAULT '0' COMMENT '||-',
  PRIMARY KEY (`codfone`),
  KEY `ddi` (`ddi`),
  KEY `ddd` (`ddd`),
  KEY `numero_fone` (`numero_fone`),
  KEY `codco_cl_p` (`codco_cl_p`),
  KEY `principal` (`principal`),
  KEY `codcfone` (`codcfone`),
  KEY `codcli` (`codcli`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=ContactsTelephones|Desc=|Grupo=Customer';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telefone`
-- Table structure for table `crp_html`
--

DROP TABLE IF EXISTS `crp_html`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crp_html` (
  `codcrph` varchar(10) NOT NULL,
  `titulo` varchar(160) DEFAULT NULL,
  `imagem` varchar(45) NOT NULL,
  `html` text,
  `site` varchar(1) DEFAULT NULL,
  `fixo` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`codcrph`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crp_html`
-- Table structure for table `script_conexao`
--

DROP TABLE IF EXISTS `script_conexao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_conexao` (
  `codscnx` char(10) NOT NULL,
  `tipo_scnx` char(10) NOT NULL,
  PRIMARY KEY (`codscnx`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_conexao`
-- Table structure for table `layout_exportacao`
--

DROP TABLE IF EXISTS `layout_exportacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `layout_exportacao` (
  `codlexp` varchar(10) NOT NULL,
  `codtexp` varchar(10) NOT NULL,
  `codinf` varchar(10) NOT NULL,
  `nome_lexp` varchar(50) NOT NULL,
  `tipo_padrao` char(2) NOT NULL,
  `obs` mediumtext NOT NULL,
  `lay_padrao` char(1) NOT NULL DEFAULT 'N',
  `controlar_rps` char(1) NOT NULL DEFAULT 'N',
  `intercalado` char(1) NOT NULL DEFAULT 'N',
  `pos_script` mediumtext NOT NULL,
  PRIMARY KEY (`codlexp`),
  KEY `codtexp` (`codtexp`),
  KEY `codinf` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_exportacao`
-- Table structure for table `dias_semana_turno`
--

DROP TABLE IF EXISTS `dias_semana_turno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dias_semana_turno` (
  `coddstu` varchar(10) NOT NULL,
  `coddsem` int(1) NOT NULL,
  `codtur` varchar(10) NOT NULL,
  `hora_ini` char(8) NOT NULL DEFAULT '00:00:00',
  `hora_fim` char(8) NOT NULL DEFAULT '00:00:00',
  `tempo` char(8) NOT NULL DEFAULT '00:00:00',
  `intervalo` char(8) NOT NULL DEFAULT '00:00:00',
  PRIMARY KEY (`coddstu`),
  KEY `coddsem` (`coddsem`),
  KEY `codtur` (`codtur`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dias_semana_turno`
-- Table structure for table `codificadores`
--

DROP TABLE IF EXISTS `codificadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codificadores` (
  `codcdf` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codtcdf` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  `codlpt` varchar(10) NOT NULL,
  `codigo_interno` varchar(30) NOT NULL,
  `nro_serie` varchar(30) NOT NULL,
  `casn` varchar(15) NOT NULL,
  `status` char(1) NOT NULL DEFAULT 'I',
  `data_can` date NOT NULL,
  `senha` varchar(30) NOT NULL,
  PRIMARY KEY (`codcdf`),
  KEY `codsercli` (`codsercli`),
  KEY `codtcdf` (`codtcdf`),
  KEY `codpat` (`codpat`),
  KEY `codlpt` (`codlpt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codificadores`
-- Table structure for table `contas_emails`
--

DROP TABLE IF EXISTS `contas_emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_emails` (
  `codcemail` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `coddom` varchar(10) NOT NULL DEFAULT '',
  `login` varchar(100) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `quota` int(10) unsigned NOT NULL DEFAULT '0',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `foward` text NOT NULL,
  `central` char(1) NOT NULL DEFAULT 'S',
  `copia` char(1) NOT NULL DEFAULT '',
  `ok` char(1) NOT NULL DEFAULT '',
  `principal` char(1) NOT NULL DEFAULT '',
  `antispam` char(1) NOT NULL DEFAULT 'S',
  `antivirus` char(1) NOT NULL DEFAULT 'S',
  `alias` char(1) NOT NULL DEFAULT 'N',
  `autoresposta` text NOT NULL,
  PRIMARY KEY (`codcemail`),
  KEY `codsercli` (`codsercli`),
  KEY `coddom` (`coddom`),
  KEY `codcli` (`codcli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_emails`
-- Table structure for table `campos_exportar_inf`
--

DROP TABLE IF EXISTS `campos_exportar_inf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campos_exportar_inf` (
  `codcei` varchar(10) NOT NULL DEFAULT '',
  `codeinf` varchar(10) NOT NULL DEFAULT '',
  `nome` varchar(50) NOT NULL DEFAULT '',
  `tamanho` varchar(10) NOT NULL DEFAULT '',
  `descricao` varchar(150) NOT NULL DEFAULT '',
  `ordem` int(11) NOT NULL,
  `conteudo` mediumtext NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codcei`),
  KEY `codeinf` (`codeinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campos_exportar_inf`
-- Table structure for table `ocorencias_inst`
--

DROP TABLE IF EXISTS `ocorencias_inst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocorencias_inst` (
  `codocoi` char(3) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codsercli` char(3) NOT NULL DEFAULT '',
  `codsta` char(3) NOT NULL DEFAULT '',
  `data_ini` char(3) NOT NULL DEFAULT '',
  `data_fin` char(3) NOT NULL DEFAULT '',
  `obs` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`codocoi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocorencias_inst`
-- Table structure for table `telas_exportacao`
--

DROP TABLE IF EXISTS `telas_exportacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `telas_exportacao` (
  `codtexp` varchar(10) NOT NULL,
  `codinf` varchar(10) NOT NULL,
  `nome_texp` varchar(30) NOT NULL,
  `consulta_sql_r` mediumtext NOT NULL,
  `consulta_sql_c` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtexp`),
  KEY `codinf` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telas_exportacao`
-- Table structure for table `mensagem_empresa`
--

DROP TABLE IF EXISTS `mensagem_empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mensagem_empresa` (
  `codmen` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `prioridade` char(1) NOT NULL DEFAULT '',
  `url` varchar(100) NOT NULL DEFAULT '',
  `texto` text NOT NULL,
  PRIMARY KEY (`codmen`),
  UNIQUE KEY `codmen` (`codmen`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensagem_empresa`
-- Table structure for table `grids`
--

DROP TABLE IF EXISTS `grids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grids` (
  `codgrd` varchar(10) NOT NULL,
  `codtel` varchar(10) NOT NULL,
  `codtgrd` varchar(10) NOT NULL,
  `descri_grd` varchar(50) NOT NULL,
  `nome_ctl` varchar(50) NOT NULL,
  `campo_codigo` varchar(30) NOT NULL,
  `alias` varchar(10) NOT NULL,
  `codigo_formulario` varchar(10) NOT NULL,
  `consulta_sql` mediumtext NOT NULL,
  `script_post` mediumtext NOT NULL,
  `propriedades` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codgrd`),
  KEY `codtel` (`codtel`),
  KEY `codtgrd` (`codtgrd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grids`
-- Table structure for table `descontos_faturamento`
--

DROP TABLE IF EXISTS `descontos_faturamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `descontos_faturamento` (
  `codd_f` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL DEFAULT '0.00',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `descri_d_f` varchar(50) NOT NULL,
  PRIMARY KEY (`codd_f`),
  KEY `codcrec` (`codcrec`),
  KEY `data` (`data`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `descontos_faturamento`
-- Table structure for table `detalhe_mapas`
--

DROP TABLE IF EXISTS `detalhe_mapas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_mapas` (
  `coddmapa` varchar(10) NOT NULL DEFAULT '',
  `codmapa` varchar(10) DEFAULT NULL,
  `codbkn` varchar(10) DEFAULT NULL,
  `codcon` int(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`coddmapa`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_mapas`
-- Table structure for table `grupo_dre`
--

DROP TABLE IF EXISTS `grupo_dre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_dre` (
  `codgdre` varchar(10) NOT NULL,
  `coddre` varchar(10) NOT NULL,
  `descri_gdre` varchar(100) NOT NULL,
  `tipo` char(1) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `fixo` char(1) NOT NULL DEFAULT 'N',
  `valor` char(1) NOT NULL,
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `cor` int(8) NOT NULL,
  `ampliado` char(1) NOT NULL DEFAULT 'N',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codgdre`),
  KEY `coddre` (`coddre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_dre`
-- Table structure for table `versao_arquivos`
--

DROP TABLE IF EXISTS `versao_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `versao_arquivos` (
  `codvarq` varchar(10) NOT NULL DEFAULT '',
  `codarq` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `versao` int(3) unsigned NOT NULL,
  `comprimido` char(1) NOT NULL DEFAULT 'N',
  `data` datetime NOT NULL,
  `obs_versao` mediumtext NOT NULL,
  `arquivo` mediumtext NOT NULL,
  PRIMARY KEY (`codvarq`),
  KEY `codarq` (`codarq`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `versao_arquivos`
-- Table structure for table `servicos_cdf`
--

DROP TABLE IF EXISTS `servicos_cdf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cdf` (
  `codscdf` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL,
  `codtcdf` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `quant` int(2) NOT NULL,
  `valor_cdf_ex` float(10,2) NOT NULL,
  PRIMARY KEY (`codscdf`),
  KEY `codser` (`codser`),
  KEY `codtcdf` (`codtcdf`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cdf`
-- Table structure for table `telas_opc`
--

DROP TABLE IF EXISTS `telas_opc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `telas_opc` (
  `codtopc` varchar(10) NOT NULL COMMENT 'hasht',
  `nome_tela` varchar(45) NOT NULL,
  `codopc` char(3) DEFAULT NULL,
  PRIMARY KEY (`codtopc`),
  KEY `indice` (`codopc`),
  KEY `codopc` (`codopc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telas_opc`
-- Table structure for table `locais_saldo_prod`
--

DROP TABLE IF EXISTS `locais_saldo_prod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locais_saldo_prod` (
  `codlsp` varchar(10) NOT NULL DEFAULT '',
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `codprod` varchar(10) NOT NULL DEFAULT '',
  `qtde` int(11) NOT NULL DEFAULT '0',
  `qtde_minima` int(11) NOT NULL DEFAULT '0' COMMENT '||-',
  `qtde_maxima` int(11) NOT NULL DEFAULT '0' COMMENT '||-',
  PRIMARY KEY (`codlsp`),
  UNIQUE KEY `codlsp` (`codlsp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locais_saldo_prod`
-- Table structure for table `comissao_vendedor_ciclo2`
--

DROP TABLE IF EXISTS `comissao_vendedor_ciclo2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comissao_vendedor_ciclo2` (
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `nome_cli` varchar(50) NOT NULL,
  `seg_mensalidade` date NOT NULL DEFAULT '0000-00-00',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `descri_ser` varchar(50) NOT NULL DEFAULT '',
  `vendedor` varchar(30) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `valor_pag` float(8,2) NOT NULL DEFAULT '0.00',
  `comissao` double(12,6) DEFAULT NULL,
  `quant_comi` bigint(21) DEFAULT NULL,
  `ciclos` decimal(7,0) DEFAULT NULL,
  `Ciclos2` bigint(21) NOT NULL DEFAULT '0',
  `saldo` double(19,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissao_vendedor_ciclo2`
-- Table structure for table `usu_pgi`
--

DROP TABLE IF EXISTS `usu_pgi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_pgi` (
  `codusupgi` char(10) NOT NULL DEFAULT '',
  `codusu` char(10) NOT NULL DEFAULT '',
  `codpgi` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`codusupgi`),
  KEY `codusu` (`codusu`),
  KEY `codpgi` (`codpgi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_pgi`
-- Table structure for table `histo_fat`
--

DROP TABLE IF EXISTS `histo_fat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histo_fat` (
  `codhfat` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `codfat` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(5) unsigned NOT NULL DEFAULT '0',
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `n_boleto` varchar(10) NOT NULL DEFAULT '',
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `histo_fat` varchar(50) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL,
  PRIMARY KEY (`codhfat`),
  KEY `codfat` (`codfat`),
  KEY `n_boleto` (`n_boleto`),
  KEY `codcob` (`codcob`),
  KEY `codusu` (`codusu`),
  KEY `nro_doc` (`nro_doc`)
) ENGINE=MyISAM AUTO_INCREMENT=217147 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `histo_fat`
-- Table structure for table `tipo_interfaces_radio`
--

DROP TABLE IF EXISTS `tipo_interfaces_radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_interfaces_radio` (
  `codtintr` varchar(10) NOT NULL DEFAULT '',
  `descri_tintr` varchar(30) NOT NULL DEFAULT '',
  `editar` char(1) NOT NULL DEFAULT 'S',
  `multiplos` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codtintr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_interfaces_radio`
-- Table structure for table `usu_emails`
--

DROP TABLE IF EXISTS `usu_emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_emails` (
  `coduem` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `login` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`coduem`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_emails`
-- Table structure for table `feriados`
--

DROP TABLE IF EXISTS `feriados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feriados` (
  `codfer` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `desc_fer` varchar(30) NOT NULL DEFAULT '',
  `repete` char(1) NOT NULL DEFAULT 'S',
  `tipo` char(1) DEFAULT NULL,
  PRIMARY KEY (`codfer`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feriados`
-- Table structure for table `instalacoes`
--

DROP TABLE IF EXISTS `instalacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instalacoes` (
  `codinst` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codsta` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codinst`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instalacoes`
-- Table structure for table `valores_sici`
--

DROP TABLE IF EXISTS `valores_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_sici` (
  `codvlrsici` varchar(10) NOT NULL,
  `codsici` varchar(10) NOT NULL,
  `codisici` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `valor` float(10,2) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `tipo_cliente` char(1) NOT NULL,
  `tecno_item` char(1) NOT NULL,
  `faixa` int(3) NOT NULL,
  `estado` char(2) DEFAULT NULL,
  KEY `codsici` (`codsici`),
  KEY `codisici` (`codisici`),
  KEY `codsercli` (`codsercli`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_sici`
-- Table structure for table `log_tarefas`
--

DROP TABLE IF EXISTS `log_tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_tarefas` (
  `codltar` varchar(10) NOT NULL DEFAULT '',
  `codtar` varchar(10) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codeem` varchar(10) NOT NULL DEFAULT '',
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codltar`),
  KEY `codtar` (`codtar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_tarefas`
-- Table structure for table `equipamentos_rede_usuarios`
--

DROP TABLE IF EXISTS `equipamentos_rede_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipamentos_rede_usuarios` (
  `codeqrusu` varchar(10) NOT NULL,
  `codeqr` varchar(10) DEFAULT NULL,
  `usuario` varchar(30) DEFAULT NULL,
  `senha` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`codeqrusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos_rede_usuarios`
-- Table structure for table `campos_tela_exp`
--

DROP TABLE IF EXISTS `campos_tela_exp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campos_tela_exp` (
  `codctexp` varchar(10) NOT NULL,
  `codtexp` varchar(10) NOT NULL,
  `campo` varchar(50) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `tipo` char(1) NOT NULL,
  `tamanho` int(3) unsigned NOT NULL,
  `componente` varchar(30) NOT NULL,
  `visivel` char(1) NOT NULL DEFAULT 'S',
  `obs` mediumtext NOT NULL,
  `descricao` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codctexp`),
  KEY `codtexp` (`codtexp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campos_tela_exp`
-- Table structure for table `numeros_disponiveis`
--

DROP TABLE IF EXISTS `numeros_disponiveis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `numeros_disponiveis` (
  `codndis` char(10) NOT NULL,
  `codpref` char(10) NOT NULL,
  `numero` char(10) NOT NULL,
  `disponivel` char(1) NOT NULL,
  `tipo_ndis` char(4) NOT NULL,
  `codtvoz` char(10) NOT NULL DEFAULT '',
  `codigo_localidade` varchar(100) NOT NULL,
  `sigla_localidade` varchar(100) NOT NULL,
  `data_cancel` date NOT NULL DEFAULT '0000-00-00',
  `codsercli` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codndis`),
  KEY `codpref` (`codpref`),
  KEY `codtvoz` (`codtvoz`),
  KEY `numero` (`numero`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `numeros_disponiveis`
-- Table structure for table `acoes_regras_cob`
--

DROP TABLE IF EXISTS `acoes_regras_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acoes_regras_cob` (
  `codarc` varchar(10) NOT NULL,
  `codrcob` varchar(10) NOT NULL,
  `codacob` varchar(10) NOT NULL,
  `dias` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codarc`),
  KEY `codrcob` (`codrcob`),
  KEY `codacob` (`codacob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acoes_regras_cob`
-- Table structure for table `comandos_ass`
--

DROP TABLE IF EXISTS `comandos_ass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comandos_ass` (
  `codcass` varchar(10) NOT NULL,
  `codgass` varchar(10) NOT NULL,
  `codsca` varchar(10) NOT NULL,
  `codtcom` char(1) NOT NULL,
  `codpca` varchar(10) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `data_fim` datetime NOT NULL,
  `idError` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codcass`),
  KEY `codsca` (`codsca`),
  KEY `codtcom` (`codtcom`),
  KEY `codpca` (`codpca`),
  KEY `codgass` (`codgass`),
  KEY `ordem` (`ordem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comandos_ass`
-- Table structure for table `templates_doc`
--

DROP TABLE IF EXISTS `templates_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `templates_doc` (
  `codtdoc` varchar(10) NOT NULL DEFAULT '',
  `editavel` char(1) NOT NULL,
  `template` mediumtext NOT NULL,
  `descrição` text NOT NULL,
  PRIMARY KEY (`codtdoc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `templates_doc`
-- Table structure for table `produtos_interessados`
--

DROP TABLE IF EXISTS `produtos_interessados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produtos_interessados` (
  `codpint` varchar(10) NOT NULL DEFAULT '',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL,
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codvenc` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL,
  `codecli_i` char(10) NOT NULL,
  `codecli_c` char(10) NOT NULL,
  `codecli_n` char(10) NOT NULL,
  `codcon` int(3) NOT NULL DEFAULT '0',
  `codintr` char(10) NOT NULL,
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `taxa_inst` float(10,2) NOT NULL,
  `parcelas_inst` int(2) NOT NULL,
  `status` char(1) NOT NULL,
  `obs` text NOT NULL,
  `data_reserva` datetime NOT NULL,
  `id_etapa` int(11) NOT NULL DEFAULT '0',
  `qualificacao_interesse` int(11) NOT NULL DEFAULT '0',
  `status_negociacao` char(1) NOT NULL DEFAULT '',
  `id_perda` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codpint`),
  KEY `codprosp` (`codpros`),
  KEY `codser` (`codser`),
  KEY `codvenc` (`codvenc`),
  KEY `codcob` (`codcob`),
  KEY `codven` (`codven`),
  KEY `codsercli` (`codsercli`),
  KEY `codcli` (`codcli`),
  KEY `id_perda` (`id_perda`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos_interessados`
-- Table structure for table `ligacoes_reg_neg_voz`
--

DROP TABLE IF EXISTS `ligacoes_reg_neg_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ligacoes_reg_neg_voz` (
  `codlrnv` varchar(10) NOT NULL,
  `codrnv` varchar(10) NOT NULL,
  `codlig` varchar(10) NOT NULL,
  `valor_ant` float(8,2) NOT NULL,
  `valor_atual` float(8,2) NOT NULL,
  PRIMARY KEY (`codlrnv`),
  KEY `codrnv` (`codrnv`),
  KEY `codlig` (`codlig`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligacoes_reg_neg_voz`
-- Table structure for table `configuracoes_l_radius`
--

DROP TABLE IF EXISTS `configuracoes_l_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuracoes_l_radius` (
  `codclr` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codds` varchar(10) NOT NULL DEFAULT '',
  `valor` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codclr`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracoes_l_radius`
-- Table structure for table `status_debitos`
--

DROP TABLE IF EXISTS `status_debitos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_debitos` (
  `codedeb` varchar(10) NOT NULL DEFAULT '',
  `descri_edeb` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codedeb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_debitos`
-- Table structure for table `acoes_cobrancas`
--

DROP TABLE IF EXISTS `acoes_cobrancas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acoes_cobrancas` (
  `codacob` varchar(10) NOT NULL,
  `codtac` varchar(10) NOT NULL,
  `codtar` varchar(10) NOT NULL,
  `descri_acob` varchar(100) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codacob`),
  KEY `codtac` (`codtac`),
  KEY `codtar` (`codtar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acoes_cobrancas`
-- Table structure for table `usuarios_serv`
--

DROP TABLE IF EXISTS `usuarios_serv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_serv` (
  `coduserv` varchar(10) NOT NULL DEFAULT '',
  `codserv` varchar(10) NOT NULL DEFAULT '',
  `tipo_usu` char(2) NOT NULL DEFAULT '',
  `user` varchar(20) NOT NULL DEFAULT '',
  `senha` varchar(20) NOT NULL DEFAULT '',
  `porta` varchar(5) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  PRIMARY KEY (`coduserv`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_serv`
-- Table structure for table `projeto_oco`
--

DROP TABLE IF EXISTS `projeto_oco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projeto_oco` (
  `codocoprj` varchar(10) NOT NULL,
  `codprj` varchar(10) NOT NULL,
  `codoco` varchar(10) NOT NULL,
  `codigo_externo` char(10) NOT NULL,
  PRIMARY KEY (`codocoprj`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_oco`
-- Table structure for table `bancos_sici`
--

DROP TABLE IF EXISTS `bancos_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bancos_sici` (
  `codbsici` varchar(10) NOT NULL,
  `codban` varchar(10) NOT NULL,
  PRIMARY KEY (`codbsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancos_sici`
-- Table structure for table `servicos_blo`
--

DROP TABLE IF EXISTS `servicos_blo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_blo` (
  `codigo` int(10) NOT NULL AUTO_INCREMENT,
  `codsercli` varchar(10) DEFAULT NULL,
  `codser` varchar(10) DEFAULT NULL,
  `codcli` int(6) NOT NULL DEFAULT '0',
  `login` varchar(30) DEFAULT NULL,
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_blo` date NOT NULL DEFAULT '0000-00-00',
  `data_des` date NOT NULL DEFAULT '0000-00-00',
  `data_tol` date NOT NULL DEFAULT '0000-00-00',
  `competencia` varchar(6) DEFAULT NULL,
  `status` char(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codigo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Servicos bloquedos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_blo`
-- Table structure for table `interessados_prospect`
--

DROP TABLE IF EXISTS `interessados_prospect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interessados_prospect` (
  `codipros` varchar(10) NOT NULL DEFAULT '',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `nome_ipros` varchar(50) NOT NULL DEFAULT '',
  `fone_ipros` int(9) NOT NULL DEFAULT '0',
  `tipo_cliente` char(1) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codipros`),
  KEY `codpros` (`codpros`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interessados_prospect`
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `error` (
  `coderr` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `hora` varchar(10) NOT NULL DEFAULT '',
  `reporte` text NOT NULL,
  PRIMARY KEY (`coderr`),
  KEY `data` (`data`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `error`
-- Table structure for table `previsoes`
--

DROP TABLE IF EXISTS `previsoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `previsoes` (
  `codprev` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `codban` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT 'D',
  `descri_prev` varchar(100) NOT NULL,
  `valor_prev` float(10,2) NOT NULL,
  `so_codban` char(1) NOT NULL DEFAULT 'S',
  `se_feriado` char(1) NOT NULL DEFAULT 'M',
  `dia` int(2) unsigned NOT NULL,
  `codigo_dia` char(3) NOT NULL DEFAULT 'DFX',
  PRIMARY KEY (`codprev`),
  KEY `codemp` (`codemp`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `previsoes`
-- Table structure for table `filmes_dias`
--

DROP TABLE IF EXISTS `filmes_dias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filmes_dias` (
  `codfmd` varchar(10) NOT NULL,
  `codflm` varchar(10) NOT NULL,
  `codcnl` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  PRIMARY KEY (`codfmd`),
  KEY `codflm` (`codflm`),
  KEY `codcnl` (`codcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filmes_dias`
-- Table structure for table `detalhe_c_servicos`
--

DROP TABLE IF EXISTS `detalhe_c_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_c_servicos` (
  `coddser` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codaco` char(1) NOT NULL DEFAULT '',
  `codgcom` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddser`),
  KEY `codser` (`codser`),
  KEY `codaco` (`codaco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_c_servicos`
-- Table structure for table `relatorios_cube`
--

DROP TABLE IF EXISTS `relatorios_cube`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relatorios_cube` (
  `codcube` varchar(10) NOT NULL DEFAULT '',
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `filtro_data` char(1) NOT NULL DEFAULT '',
  `sql` text NOT NULL,
  PRIMARY KEY (`codcube`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios_cube`
-- Table structure for table `plano_cta`
--

DROP TABLE IF EXISTS `plano_cta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plano_cta` (
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codexterno` varchar(20) NOT NULL,
  `codtmr` varchar(10) NOT NULL,
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `descri_cta` varchar(50) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `natureza` char(1) NOT NULL DEFAULT '',
  `categoria` char(1) NOT NULL DEFAULT '',
  `nivel_acesso` char(1) NOT NULL DEFAULT '',
  `movimento` char(1) NOT NULL DEFAULT '',
  `iss` float(5,2) NOT NULL,
  PRIMARY KEY (`codcta`),
  KEY `codtmr` (`codtmr`),
  KEY `codexterno` (`codexterno`),
  KEY `codctc` (`codctc`),
  KEY `natureza` (`natureza`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plano_cta`
-- Table structure for table `composicao_protocolos`
--

DROP TABLE IF EXISTS `composicao_protocolos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `composicao_protocolos` (
  `codcpcan` varchar(10) NOT NULL,
  `codpcan` int(6) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  PRIMARY KEY (`codcpcan`),
  KEY `codcrec` (`codcrec`),
  KEY `codpcan` (`codpcan`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `composicao_protocolos`
-- Table structure for table `condicao_pagamento`
--

DROP TABLE IF EXISTS `condicao_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condicao_pagamento` (
  `codcopgt` varchar(10) NOT NULL,
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codcob_pag` varchar(10) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `nome_regra` varchar(100) NOT NULL DEFAULT '',
  `dia_prim_fat` int(3) NOT NULL,
  `valor_min` float(8,2) NOT NULL,
  `valor_max` float(8,2) NOT NULL,
  `prazo_min` int(3) NOT NULL,
  `prazo_max` int(3) NOT NULL,
  `percentual_multa` float(8,2) NOT NULL,
  `percentual_juros` float(8,2) NOT NULL,
  PRIMARY KEY (`codcopgt`),
  KEY `codcob` (`codcob`),
  KEY `codcob_pag` (`codcob_pag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condicao_pagamento`
-- Table structure for table `imagens_rela`
--

DROP TABLE IF EXISTS `imagens_rela`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imagens_rela` (
  `codirel` varchar(10) NOT NULL DEFAULT '',
  `codrel` varchar(10) NOT NULL DEFAULT '',
  `codima` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codirel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagens_rela`
-- Table structure for table `html_documentos`
--

DROP TABLE IF EXISTS `html_documentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_documentos` (
  `codhtmd` varchar(10) NOT NULL,
  `html` mediumtext NOT NULL,
  PRIMARY KEY (`codhtmd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_documentos`
-- Table structure for table `total_navegacao_nas`
--

DROP TABLE IF EXISTS `total_navegacao_nas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `total_navegacao_nas` (
  `codtnavnas` varchar(10) NOT NULL DEFAULT '',
  `codnr` varchar(10) NOT NULL DEFAULT '',
  `compe` varchar(4) NOT NULL DEFAULT '',
  `codmed` varchar(10) NOT NULL,
  `upload` bigint(20) unsigned NOT NULL DEFAULT '0',
  `download` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tempo` bigint(20) NOT NULL DEFAULT '0',
  `data_med` datetime NOT NULL,
  PRIMARY KEY (`codtnavnas`),
  KEY `codsercli` (`codnr`),
  KEY `compe` (`compe`),
  KEY `codmed` (`codmed`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `total_navegacao_nas`
-- Table structure for table `franquia_ser_terminacao`
--

DROP TABLE IF EXISTS `franquia_ser_terminacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franquia_ser_terminacao` (
  `codfster` varchar(10) NOT NULL,
  `codfsv` varchar(10) NOT NULL,
  `codtter` varchar(10) NOT NULL,
  PRIMARY KEY (`codfster`),
  KEY `codfsv` (`codfsv`),
  KEY `codtter` (`codtter`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `franquia_ser_terminacao`
-- Table structure for table `servicos_cli_sici`
--

DROP TABLE IF EXISTS `servicos_cli_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_sici` (
  `codscsici` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL,
  `codtsici` varchar(10) NOT NULL,
  `codvsici` varchar(10) NOT NULL,
  `quant_megas` int(6) unsigned NOT NULL,
  `dedicado` char(1) NOT NULL,
  PRIMARY KEY (`codscsici`),
  KEY `codsercli` (`codsercli`),
  KEY `codtsici` (`codtsici`),
  KEY `codvsici` (`codvsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_sici`
-- Table structure for table `mod_radio`
--

DROP TABLE IF EXISTS `mod_radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mod_radio` (
  `codmrad` varchar(10) NOT NULL DEFAULT '',
  `codtrad` varchar(10) NOT NULL DEFAULT '',
  `descri_mrad` varchar(50) NOT NULL DEFAULT '',
  `db` int(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codmrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mod_radio`
-- Table structure for table `det_mov_bancario`
--

DROP TABLE IF EXISTS `det_mov_bancario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_mov_bancario` (
  `coddmov` varchar(10) NOT NULL DEFAULT '',
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `coddrec` varchar(10) DEFAULT NULL,
  `numero_che` int(8) unsigned NOT NULL,
  `data_ven` date NOT NULL,
  `valor` float(8,2) NOT NULL,
  PRIMARY KEY (`coddmov`),
  KEY `codmov` (`codmov`),
  KEY `coddrec` (`coddrec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_mov_bancario`
-- Table structure for table `photo_temp`
--

DROP TABLE IF EXISTS `photo_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `photo_temp` (
  `codfot` varchar(10) DEFAULT NULL,
  `nome_foto` varchar(50) DEFAULT NULL,
  `foto` longtext,
  `codpros` varchar(10) DEFAULT NULL,
  `codcon` int(3) unsigned DEFAULT NULL,
  `codcli` int(6) unsigned DEFAULT NULL,
  `codcont` varchar(10) DEFAULT NULL,
  `codusu` char(2) DEFAULT NULL,
  `codtfot` varchar(10) DEFAULT NULL,
  `data` date DEFAULT NULL,
  `obs` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photo_temp`
-- Table structure for table `tipo_prospect`
--

DROP TABLE IF EXISTS `tipo_prospect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_prospect` (
  `codtpros` varchar(10) NOT NULL,
  `descri_tpros` varchar(50) NOT NULL,
  `tipo_prospect` char(1) NOT NULL,
  PRIMARY KEY (`codtpros`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_prospect`
-- Table structure for table `parceiros`
--

DROP TABLE IF EXISTS `parceiros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parceiros` (
  `codpar` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL,
  `codpop` varchar(10) NOT NULL,
  `codgpar` varchar(10) NOT NULL,
  `nome_par` varchar(50) NOT NULL DEFAULT '',
  `nome_fan` varchar(30) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `contato` varchar(50) NOT NULL DEFAULT '',
  `tipo_par` char(1) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `icm` varchar(15) NOT NULL DEFAULT '',
  `rg` varchar(11) NOT NULL DEFAULT '',
  `rg_emissor` varchar(10) NOT NULL,
  `cpf` varchar(14) NOT NULL DEFAULT '',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `obs` text NOT NULL,
  PRIMARY KEY (`codpar`),
  KEY `codsercli` (`codsercli`),
  KEY `codpop` (`codpop`),
  KEY `codgpar` (`codgpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parceiros`
-- Table structure for table `tipo_cobranca`
--

DROP TABLE IF EXISTS `tipo_cobranca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cobranca` (
  `tipo_cob` char(1) NOT NULL DEFAULT '',
  `descri_tcob` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`tipo_cob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cobranca`
-- Table structure for table `logs_cons_pub`
--

DROP TABLE IF EXISTS `logs_cons_pub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_cons_pub` (
  `codlcp` varchar(10) NOT NULL,
  `codcpub` varchar(10) NOT NULL,
  `id` int(3) unsigned NOT NULL,
  `data_hora` datetime NOT NULL,
  `ok` char(1) NOT NULL,
  `resposta` mediumtext NOT NULL,
  `xml_enviado` mediumtext NOT NULL,
  PRIMARY KEY (`codlcp`),
  KEY `codcpub` (`codcpub`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_cons_pub`
-- Table structure for table `grupos_servicos`
--

DROP TABLE IF EXISTS `grupos_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupos_servicos` (
  `codgser` varchar(10) NOT NULL DEFAULT '',
  `codtsici` varchar(10) NOT NULL,
  `descri_gser` varchar(30) NOT NULL DEFAULT '',
  `tipo_acesso` char(2) NOT NULL,
  `url_monitoramento` varchar(250) NOT NULL,
  `codsad_ip` varchar(10) NOT NULL,
  `valor_ip` float(10,2) NOT NULL,
  `comando_desconexao` varchar(100) NOT NULL,
  `retem_imposto` char(1) NOT NULL DEFAULT 'N',
  `altera_senha_radius` char(1) NOT NULL DEFAULT 'N',
  `servicegroup` char(10) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  PRIMARY KEY (`codgser`),
  KEY `codtsici` (`codtsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_servicos`
-- Table structure for table `historico_prospecto`
--

DROP TABLE IF EXISTS `historico_prospecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_prospecto` (
  `codhis` varchar(10) NOT NULL DEFAULT '',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `codpint` varchar(10) NOT NULL DEFAULT '',
  `tabela` varchar(30) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `usuario` char(2) NOT NULL DEFAULT '',
  `ip` varchar(50) NOT NULL DEFAULT '',
  `texto` text NOT NULL,
  PRIMARY KEY (`codhis`),
  KEY `codcli` (`codpros`),
  KEY `codsercli` (`codpint`),
  KEY `data` (`data`),
  KEY `usuario` (`usuario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_prospecto`
-- Table structure for table `login_ftp`
--

DROP TABLE IF EXISTS `login_ftp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_ftp` (
  `codlftp` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `coddom` varchar(10) NOT NULL DEFAULT '',
  `usuario` varchar(32) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `principal` char(1) NOT NULL DEFAULT 'N',
  `pasta` varchar(100) NOT NULL DEFAULT '',
  `pasta_v` varchar(100) NOT NULL DEFAULT '',
  `p_leitura` char(1) NOT NULL DEFAULT 'S',
  `p_escritura` char(1) NOT NULL DEFAULT 'S',
  `p_apagar` char(1) NOT NULL DEFAULT 'S',
  `p_listar` char(1) NOT NULL DEFAULT 'S',
  `p_apagar_d` char(1) NOT NULL DEFAULT 'S',
  `p_criar_d` char(1) NOT NULL DEFAULT 'S',
  `p_perm_r` char(1) NOT NULL DEFAULT 'S',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `quota_ftp` int(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codlftp`),
  KEY `codsercli` (`codsercli`),
  KEY `coddom` (`coddom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_ftp`
-- Table structure for table `modelos_contrato`
--

DROP TABLE IF EXISTS `modelos_contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modelos_contrato` (
  `codmodc` varchar(10) NOT NULL DEFAULT '',
  `codtcc` varchar(10) NOT NULL DEFAULT '',
  `coddoc` varchar(10) NOT NULL DEFAULT '',
  `codindc` varchar(10) NOT NULL,
  `codtrejcon` varchar(10) NOT NULL,
  `descri_modc` varchar(100) NOT NULL DEFAULT '',
  `validade` int(3) unsigned NOT NULL DEFAULT '0',
  `validade_reajuste` int(3) unsigned NOT NULL DEFAULT '0',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `nome_contato` varchar(100) NOT NULL DEFAULT '',
  `cpf` varchar(18) NOT NULL DEFAULT '',
  `celular` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `img_assinatura` mediumtext NOT NULL,
  `ext_img` char(4) NOT NULL DEFAULT '',
  PRIMARY KEY (`codmodc`),
  KEY `codtcc` (`codtcc`),
  KEY `coddoc` (`coddoc`),
  KEY `codindc` (`codindc`),
  KEY `codtrejcon` (`codtrejcon`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modelos_contrato`
-- Table structure for table `registro_tributacao_emp`
--

DROP TABLE IF EXISTS `registro_tributacao_emp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registro_tributacao_emp` (
  `codrtribemp` char(10) NOT NULL COMMENT 'Código Empresa que será utilizado o Regime de Tributação.',
  `codrtribdet` char(10) NOT NULL COMMENT 'Código Regime de Tributação Detalhado.',
  `codemp` char(10) NOT NULL COMMENT 'Código da Empresa.',
  PRIMARY KEY (`codrtribemp`),
  KEY `codrtribdet` (`codrtribdet`),
  KEY `codemp` (`codemp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_tributacao_emp`
-- Table structure for table `int_modules`
--

DROP TABLE IF EXISTS `int_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_modules` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `modulo` varchar(50) NOT NULL DEFAULT '',
  `descricao` tinytext NOT NULL,
  `status` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`,`modulo`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_modules`
-- Table structure for table `colunas_grids`
--

DROP TABLE IF EXISTS `colunas_grids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colunas_grids` (
  `codcgrd` varchar(10) NOT NULL,
  `codgrd` varchar(10) NOT NULL,
  `codtcg` varchar(10) NOT NULL,
  `campo` varchar(50) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `tamanho` int(4) unsigned NOT NULL,
  `formato` varchar(50) NOT NULL,
  `tooltips` varchar(200) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `oculto` char(1) NOT NULL DEFAULT 'N',
  `congelar` char(1) NOT NULL DEFAULT 'N',
  `somar` char(1) NOT NULL DEFAULT 'N',
  `fonte_titulo` varchar(50) NOT NULL,
  `fonte_coluna` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcgrd`),
  KEY `codgrd` (`codgrd`),
  KEY `codtcg` (`codtcg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colunas_grids`
-- Table structure for table `cidades_pop`
--

DROP TABLE IF EXISTS `cidades_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cidades_pop` (
  `codcidp` varchar(10) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `posx` int(6) unsigned NOT NULL,
  `posy` int(6) unsigned NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  PRIMARY KEY (`codcidp`),
  KEY `cidade` (`cidade`),
  KEY `codpop` (`codpop`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidades_pop`
-- Table structure for table `cobro_digital`
--

DROP TABLE IF EXISTS `cobro_digital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cobro_digital` (
  `codcli` int(6) unsigned NOT NULL,
  `sap_pmc19` varchar(19) NOT NULL,
  `sap_identificador` varchar(5) NOT NULL,
  `url_cod_barras` varchar(100) NOT NULL,
  `sap_barcode` varchar(30) NOT NULL,
  `imagem_cod_barras` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobro_digital`
-- Table structure for table `integrator_server_requests`
--

DROP TABLE IF EXISTS `integrator_server_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `integrator_server_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `method` varchar(100) NOT NULL,
  `submethod` varchar(100) NOT NULL,
  `ip` varchar(50) NOT NULL DEFAULT '',
  `log` mediumtext,
  PRIMARY KEY (`id`),
  KEY `data_hora` (`data_hora`),
  KEY `method` (`method`),
  KEY `submethod` (`submethod`),
  KEY `ip` (`ip`)
) ENGINE=MyISAM AUTO_INCREMENT=1767 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integrator_server_requests`
-- Table structure for table `status_recibo`
--

DROP TABLE IF EXISTS `status_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_recibo` (
  `status` char(1) NOT NULL,
  `descri_st` varchar(20) NOT NULL,
  PRIMARY KEY (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_recibo`
-- Table structure for table `crp_config`
--

DROP TABLE IF EXISTS `crp_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crp_config` (
  `codcrpc` varchar(10) NOT NULL,
  `descri_crpc` varchar(100) DEFAULT NULL,
  `variavel` varchar(100) DEFAULT NULL,
  `tipo` char(1) DEFAULT NULL,
  `tamanho` int(3) DEFAULT NULL,
  `valor` varchar(100) DEFAULT NULL,
  `site` char(1) DEFAULT '',
  PRIMARY KEY (`codcrpc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crp_config`
-- Table structure for table `f_cobrancas_pop`
--

DROP TABLE IF EXISTS `f_cobrancas_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `f_cobrancas_pop` (
  `codcobp` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcobp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `f_cobrancas_pop`
-- Table structure for table `dhcpcli`
--

DROP TABLE IF EXISTS `dhcpcli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcpcli` (
  `cod` int(8) unsigned NOT NULL DEFAULT '0',
  `codcli` int(8) unsigned NOT NULL DEFAULT '0',
  `ip` varchar(150) NOT NULL DEFAULT '',
  `mask` varchar(150) NOT NULL DEFAULT '',
  `mac` varchar(150) NOT NULL DEFAULT '',
  `email` varchar(150) NOT NULL DEFAULT '',
  `micro` blob NOT NULL,
  `pref` blob NOT NULL,
  `obs` blob NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcpcli`
-- Table structure for table `tipo_paginas_gi`
--

DROP TABLE IF EXISTS `tipo_paginas_gi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_paginas_gi` (
  `codtpgi` varchar(10) NOT NULL,
  `descri_tpgi` varchar(30) NOT NULL,
  `quant_ind` int(2) unsigned NOT NULL,
  `cor_fundo` varchar(11) NOT NULL,
  `fonte_titulo` varchar(50) NOT NULL,
  `matriz` varchar(10) NOT NULL,
  `layout_html` mediumtext NOT NULL,
  PRIMARY KEY (`codtpgi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_paginas_gi`
-- Table structure for table `profissoes`
--

DROP TABLE IF EXISTS `profissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profissoes` (
  `codprf` varchar(10) NOT NULL,
  `descri_prf` varchar(50) NOT NULL,
  PRIMARY KEY (`codprf`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profissoes`
-- Table structure for table `usuarios_conectados`
--

DROP TABLE IF EXISTS `usuarios_conectados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_conectados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` mediumtext NOT NULL,
  `codusu` char(2) NOT NULL,
  `status` char(1) NOT NULL,
  `ip_origem` varchar(20) NOT NULL,
  `data_hora_ini` datetime NOT NULL,
  `data_hora_ult` datetime NOT NULL,
  `data_hora_fim` datetime NOT NULL,
  `interface` char(1) NOT NULL,
  `tipo_desconexao` char(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM AUTO_INCREMENT=3645 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_conectados`
-- Table structure for table `modelo_contrato_servicos`
--

DROP TABLE IF EXISTS `modelo_contrato_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modelo_contrato_servicos` (
  `codmcs` char(10) NOT NULL,
  `codser` char(10) NOT NULL,
  `codmodc` char(10) NOT NULL,
  `validade` int(3) NOT NULL,
  PRIMARY KEY (`codmcs`),
  KEY `codser` (`codser`),
  KEY `codmodc` (`codmodc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modelo_contrato_servicos`
-- Table structure for table `usuarios_tarefas_o`
--

DROP TABLE IF EXISTS `usuarios_tarefas_o`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_tarefas_o` (
  `coduto` varchar(10) NOT NULL DEFAULT '0',
  `codtaro` varchar(10) NOT NULL DEFAULT '',
  `codusu` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`coduto`),
  KEY `codtaro` (`codtaro`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_tarefas_o`
-- Table structure for table `usu_horarios`
--

DROP TABLE IF EXISTS `usu_horarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_horarios` (
  `coduhor` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `dia` int(1) NOT NULL DEFAULT '0',
  `hora_ent` varchar(5) NOT NULL DEFAULT '',
  `hora_sai` varchar(5) NOT NULL DEFAULT '',
  PRIMARY KEY (`coduhor`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_horarios`
-- Table structure for table `negociacao_debito`
--

DROP TABLE IF EXISTS `negociacao_debito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `negociacao_debito` (
  `codndeb` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `status_neg` char(1) DEFAULT NULL,
  `data_lan` datetime DEFAULT NULL,
  `valor_divida` decimal(10,2) DEFAULT NULL,
  `valor_juros` decimal(10,2) DEFAULT NULL,
  `valor_desconto` decimal(10,2) DEFAULT NULL,
  `saldo_div` decimal(10,2) DEFAULT NULL,
  `data_can` datetime DEFAULT NULL,
  `codusu_can` char(2) DEFAULT NULL,
  `obs_can` mediumtext,
  PRIMARY KEY (`codndeb`),
  KEY `codusu` (`codusu`),
  KEY `data_lan` (`data_lan`),
  KEY `data_can` (`data_can`),
  KEY `status_neg` (`status_neg`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `negociacao_debito`
-- Table structure for table `servicos_lav`
--

DROP TABLE IF EXISTS `servicos_lav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_lav` (
  `codslav` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codtlav` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL DEFAULT '',
  `quantidade` int(2) unsigned NOT NULL,
  `valor_pri` float(8,2) NOT NULL,
  `valor_sec` float(8,2) NOT NULL,
  PRIMARY KEY (`codslav`),
  KEY `codser` (`codser`),
  KEY `codtlav` (`codtlav`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_lav`
-- Table structure for table `dados_gmaps`
--

DROP TABLE IF EXISTS `dados_gmaps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dados_gmaps` (
  `codgmp` varchar(10) NOT NULL,
  `zoom_inicial` int(3) unsigned NOT NULL,
  `lat_center` varchar(20) NOT NULL,
  `lon_center` varchar(20) NOT NULL,
  `chave` varchar(100) NOT NULL,
  `provider` int(2) NOT NULL,
  `id_here` varchar(20) NOT NULL,
  `key_here` varchar(20) NOT NULL,
  `id_bind` varchar(20) NOT NULL,
  `key_bind` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_gmaps`
-- Table structure for table `regras_negocios_telas`
--

DROP TABLE IF EXISTS `regras_negocios_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_negocios_telas` (
  `codrnt` varchar(10) NOT NULL,
  `codtel` varchar(10) NOT NULL,
  `descri_rnt` varchar(30) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `regras` mediumtext NOT NULL,
  `arquivo` mediumtext NOT NULL,
  PRIMARY KEY (`codrnt`),
  KEY `codtel` (`codtel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_negocios_telas`
-- Table structure for table `det_grupo_dre`
--

DROP TABLE IF EXISTS `det_grupo_dre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_grupo_dre` (
  `coddgd` varchar(10) NOT NULL,
  `codgdre` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  PRIMARY KEY (`coddgd`),
  KEY `codgdre` (`codgdre`),
  KEY `codcta` (`codcta`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_grupo_dre`
-- Table structure for table `moeda`
--

DROP TABLE IF EXISTS `moeda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moeda` (
  `codmoeda` varchar(10) NOT NULL,
  `descri_moeda` varchar(50) DEFAULT NULL,
  `pais` varchar(40) DEFAULT NULL,
  `simbolo` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codmoeda`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moeda`
-- Table structure for table `tipo_alertas`
--

DROP TABLE IF EXISTS `tipo_alertas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_alertas` (
  `codtale` int(3) DEFAULT NULL,
  `descri_ale` varchar(90) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_alertas`
-- Table structure for table `servicos_auto`
--

DROP TABLE IF EXISTS `servicos_auto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_auto` (
  `codsauto` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `valor` float(10,2) NOT NULL,
  PRIMARY KEY (`codsauto`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_auto`
-- Table structure for table `grupo_arquivos`
--

DROP TABLE IF EXISTS `grupo_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_arquivos` (
  `codgarq` varchar(10) NOT NULL DEFAULT '',
  `descri_garq` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codgarq`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_arquivos`
-- Table structure for table `servicos_adicionais`
--

DROP TABLE IF EXISTS `servicos_adicionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_adicionais` (
  `codsad` varchar(10) NOT NULL DEFAULT '',
  `codtser` varchar(10) NOT NULL,
  `codcob` varchar(10) NOT NULL,
  `descri_sad` varchar(70) NOT NULL DEFAULT '',
  `protocolo_cancel` char(1) NOT NULL DEFAULT 'N',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `valor_sad` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do Serviço Adicional',
  `qtde_parcelas` int(3) NOT NULL DEFAULT '0' COMMENT 'Quantidade de dias do Serviço Adicional',
  `dias_parcelas` int(3) NOT NULL DEFAULT '0' COMMENT 'Quantidade de dias Entre as Parcelas',
  PRIMARY KEY (`codsad`),
  KEY `codtser` (`codtser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_adicionais`
-- Table structure for table `equipamentos_rede_hosts`
--

DROP TABLE IF EXISTS `equipamentos_rede_hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipamentos_rede_hosts` (
  `codeqrhost` varchar(10) NOT NULL,
  `codeqr` varchar(10) DEFAULT NULL,
  `host_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`codeqrhost`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipamentos_rede_hosts`
-- Table structure for table `tipo_porcentagem_ind`
--

DROP TABLE IF EXISTS `tipo_porcentagem_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_porcentagem_ind` (
  `codtpi` varchar(10) NOT NULL,
  `descri_tpi` varchar(50) NOT NULL,
  `titulo_tpi` varchar(30) NOT NULL,
  PRIMARY KEY (`codtpi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_porcentagem_ind`
-- Table structure for table `locais_pontos_tv`
--

DROP TABLE IF EXISTS `locais_pontos_tv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locais_pontos_tv` (
  `codlpt` varchar(10) NOT NULL,
  `descri_lpt` varchar(30) NOT NULL,
  PRIMARY KEY (`codlpt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locais_pontos_tv`
-- Table structure for table `tipo_servico_extra`
--

DROP TABLE IF EXISTS `tipo_servico_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_servico_extra` (
  `codtserex` varchar(10) NOT NULL DEFAULT '' COMMENT 'Campo para informar o código do tipo do serviço extra',
  `descri_tserex` varchar(50) NOT NULL DEFAULT '' COMMENT 'Descrição do Tipo de Serviço Extra',
  `api_integracao` varchar(100) NOT NULL DEFAULT '' COMMENT 'Api a ser executada para Integração',
  PRIMARY KEY (`codtserex`),
  KEY `codtserex` (`codtserex`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_servico_extra`
-- Table structure for table `adquirente_plataforma_pagamento`
--

DROP TABLE IF EXISTS `adquirente_plataforma_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adquirente_plataforma_pagamento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codadq` char(10) NOT NULL DEFAULT '',
  `codtplat` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `codadq` (`codadq`),
  KEY `codtplat` (`codtplat`),
  KEY `codadq_codtplat` (`codadq`,`codtplat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adquirente_plataforma_pagamento`
-- Table structure for table `det_consulta_tarefas`
--

DROP TABLE IF EXISTS `det_consulta_tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_consulta_tarefas` (
  `coddct` char(10) NOT NULL DEFAULT '',
  `codctar` char(10) NOT NULL DEFAULT '',
  `ordem` char(3) NOT NULL,
  `descri_dct` varchar(100) NOT NULL,
  `titulo_dct` varchar(100) NOT NULL,
  `versao` char(10) NOT NULL,
  `padrao` char(1) NOT NULL DEFAULT 'S',
  `exclusao` char(1) NOT NULL,
  `ativo` char(1) NOT NULL,
  `data_hora_alt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `consulta_sql` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  `consulta_sql_heranca` mediumtext NOT NULL,
  `consulta_dados` mediumtext NOT NULL,
  `consulta_heranca` mediumtext NOT NULL,
  PRIMARY KEY (`coddct`),
  KEY `codctar` (`codctar`),
  KEY `ordem` (`ordem`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_consulta_tarefas`
-- Table structure for table `fornecedores`
--

DROP TABLE IF EXISTS `fornecedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fornecedores` (
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codexterno` varchar(20) NOT NULL,
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `nome_for` varchar(50) NOT NULL DEFAULT '',
  `nome_fan` varchar(30) NOT NULL DEFAULT '',
  `tipo_pesso` char(1) NOT NULL DEFAULT 'J',
  `contato` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `pais` varchar(30) NOT NULL DEFAULT '',
  `ddi` char(3) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `icm` varchar(15) NOT NULL DEFAULT '',
  `cpf` varchar(14) NOT NULL,
  `rg` varchar(20) NOT NULL,
  `rg_emissor` varchar(10) NOT NULL,
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `indicador_icm` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `obs` text NOT NULL,
  PRIMARY KEY (`codfor`),
  KEY `codexterno` (`codexterno`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedores`
-- Table structure for table `pool_ip`
--

DROP TABLE IF EXISTS `pool_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_ip` (
  `codpool` varchar(10) NOT NULL DEFAULT '',
  `codrad` varchar(10) NOT NULL DEFAULT '',
  `ip_inicio` varchar(15) NOT NULL DEFAULT '',
  `ip_fim` varchar(15) NOT NULL DEFAULT '',
  `formato` varchar(15) NOT NULL DEFAULT '',
  `octano` int(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codpool`),
  KEY `codrad` (`codrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pool_ip`
-- Table structure for table `cores_graficos`
--

DROP TABLE IF EXISTS `cores_graficos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cores_graficos` (
  `codcgr` varchar(10) NOT NULL,
  `nome_cor` varchar(30) NOT NULL,
  `codigo_desk` varchar(11) NOT NULL,
  `codigo_mobile` varchar(11) NOT NULL,
  `codigo_fc` varchar(11) NOT NULL,
  PRIMARY KEY (`codcgr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cores_graficos`
-- Table structure for table `tipo_servicos_imp`
--

DROP TABLE IF EXISTS `tipo_servicos_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_servicos_imp` (
  `codtser` varchar(10) NOT NULL,
  `descri_tser` varchar(50) NOT NULL,
  `tipo_utilizacao_nf` char(1) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_servicos_imp`
-- Table structure for table `graficos_indicadores`
--

DROP TABLE IF EXISTS `graficos_indicadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `graficos_indicadores` (
  `codgi` varchar(10) NOT NULL,
  `codcgr` varchar(10) NOT NULL,
  `codlgr` varchar(10) NOT NULL,
  `codtgi` varchar(10) NOT NULL,
  `codrcb` varchar(10) NOT NULL,
  `descri_gi` varchar(50) NOT NULL,
  `titulo_gi` varchar(30) NOT NULL,
  `subtitulo_gi` varchar(50) NOT NULL,
  `com_legendas` char(1) NOT NULL DEFAULT 'N',
  `com_indicadores` char(1) NOT NULL DEFAULT 'N',
  `com_axis` char(1) NOT NULL DEFAULT 'S',
  `com_scala` char(1) NOT NULL DEFAULT 'S',
  `com_metas` char(1) NOT NULL DEFAULT 'N',
  `mostrar_composicao` char(1) NOT NULL DEFAULT 'N',
  `pos_legenda` char(1) NOT NULL,
  `prof_3d` int(3) unsigned NOT NULL,
  `tamanho` int(3) NOT NULL,
  `transparencia` int(3) unsigned NOT NULL,
  `quant_limite_ind` int(2) unsigned NOT NULL,
  `titulo_axis_x` varchar(30) NOT NULL,
  `titulo_axis_y` varchar(30) NOT NULL,
  `imagem` varchar(100) DEFAULT NULL,
  `obs` mediumtext,
  PRIMARY KEY (`codgi`),
  KEY `codcgr` (`codcgr`),
  KEY `codlgr` (`codlgr`),
  KEY `codtgi` (`codtgi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graficos_indicadores`
-- Table structure for table `tipo_endereco`
--

DROP TABLE IF EXISTS `tipo_endereco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_endereco` (
  `codtend` varchar(10) NOT NULL DEFAULT '',
  `descri_tend` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtend`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_endereco`
-- Table structure for table `usuarios_aviso_atraso`
--

DROP TABLE IF EXISTS `usuarios_aviso_atraso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_aviso_atraso` (
  `coduaat` varchar(10) NOT NULL DEFAULT '',
  `codaat` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`coduaat`),
  KEY `codaat` (`codaat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_aviso_atraso`
-- Table structure for table `mov_bancario`
--

DROP TABLE IF EXISTS `mov_bancario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mov_bancario` (
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `codban` varchar(10) NOT NULL DEFAULT '',
  `codarq` varchar(10) NOT NULL,
  `nro_lan` int(10) unsigned NOT NULL DEFAULT '0',
  `conci` char(1) NOT NULL DEFAULT '',
  `codtmov` varchar(10) NOT NULL DEFAULT '',
  `cod_cta_transf` varchar(10) NOT NULL DEFAULT '',
  `codmov_t` varchar(10) NOT NULL DEFAULT '',
  `nro_doc` varchar(20) NOT NULL,
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_conci` date NOT NULL DEFAULT '0000-00-00',
  `valor_mov` double(11,2) NOT NULL DEFAULT '0.00',
  `histo_mov` varchar(254) NOT NULL,
  PRIMARY KEY (`codmov`),
  KEY `codban` (`codban`),
  KEY `data_ven` (`data_ven`),
  KEY `codtmov` (`codtmov`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mov_bancario`
-- Table structure for table `ligacoes_saida_avc`
--

DROP TABLE IF EXISTS `ligacoes_saida_avc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ligacoes_saida_avc` (
  `codlsu` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `codrlu` varchar(10) NOT NULL,
  `download` char(1) NOT NULL DEFAULT 'N',
  `data_hora_lig` datetime NOT NULL,
  `data_hora_exe` datetime NOT NULL,
  `data_agen_lig` datetime NOT NULL,
  `fone` varchar(13) NOT NULL,
  `nome_arq_lig` varchar(50) NOT NULL,
  PRIMARY KEY (`codlsu`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codrlu` (`codrlu`),
  KEY `download` (`download`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligacoes_saida_avc`
-- Table structure for table `registros_alterados_sincronismo`
--

DROP TABLE IF EXISTS `registros_alterados_sincronismo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registros_alterados_sincronismo` (
  `codtab` char(10) NOT NULL DEFAULT '',
  `data_proc` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codigo` char(10) NOT NULL DEFAULT '',
  `data_hora` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `codtab` (`codtab`),
  KEY `data_proc` (`data_proc`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros_alterados_sincronismo`
-- Table structure for table `servicos_cli_voz`
--

DROP TABLE IF EXISTS `servicos_cli_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_voz` (
  `codscvoz` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codvcre` varchar(10) NOT NULL,
  `simultaneas` int(3) NOT NULL DEFAULT '0',
  `franquia_proporcional` char(1) NOT NULL,
  PRIMARY KEY (`codscvoz`),
  KEY `codsercli` (`codsercli`),
  KEY `codvcre` (`codvcre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_voz`
-- Table structure for table `envio_email_pinteresse`
--

DROP TABLE IF EXISTS `envio_email_pinteresse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `envio_email_pinteresse` (
  `codeem` char(10) NOT NULL,
  `codpint` char(10) NOT NULL,
  KEY `codeem` (`codeem`),
  KEY `codpint` (`codpint`),
  KEY `codeem_codpint` (`codeem`,`codpint`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `envio_email_pinteresse`
-- Table structure for table `tipo_recibo`
--

DROP TABLE IF EXISTS `tipo_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_recibo` (
  `tipo` char(3) DEFAULT NULL,
  `descri_tipo` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_recibo`
-- Table structure for table `tabela_snmp`
--

DROP TABLE IF EXISTS `tabela_snmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabela_snmp` (
  `codtblsnmp` varchar(10) NOT NULL,
  `codtblsnmpmib` varchar(10) DEFAULT NULL,
  `snmp_oid` varchar(100) DEFAULT NULL,
  `snmp_objeto` varchar(100) DEFAULT NULL,
  `snmp_descricao` mediumtext,
  PRIMARY KEY (`codtblsnmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabela_snmp`
-- Table structure for table `grupo_aco_diario`
--

DROP TABLE IF EXISTS `grupo_aco_diario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_aco_diario` (
  `codgacd` varchar(10) NOT NULL,
  `codacd` varchar(10) NOT NULL,
  `codgi` varchar(10) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codgacd`),
  KEY `codacd` (`codacd`),
  KEY `codgi` (`codgi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_aco_diario`
-- Table structure for table `usu_inf`
--

DROP TABLE IF EXISTS `usu_inf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_inf` (
  `codu_i` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codinf` varchar(10) NOT NULL DEFAULT '',
  `p_exportar` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codu_i`),
  KEY `codusu` (`codusu`),
  KEY `codinf` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_inf`
-- Table structure for table `tipo_banco_dados`
--

DROP TABLE IF EXISTS `tipo_banco_dados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_banco_dados` (
  `codtbd` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `descri_tbd` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtbd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_banco_dados`
-- Table structure for table `faixas_ips`
--

DROP TABLE IF EXISTS `faixas_ips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faixas_ips` (
  `codfip` varchar(10) NOT NULL DEFAULT '',
  `codrad` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(6) unsigned NOT NULL DEFAULT '0',
  `ip_inicio` varchar(15) NOT NULL DEFAULT '',
  `ip_fim` varchar(15) NOT NULL DEFAULT '',
  `formato` varchar(13) NOT NULL DEFAULT '',
  PRIMARY KEY (`codfip`),
  KEY `codrad` (`codrad`),
  KEY `codcon` (`codcon`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faixas_ips`
-- Table structure for table `status_captura_ind`
--

DROP TABLE IF EXISTS `status_captura_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_captura_ind` (
  `codsind` varchar(10) NOT NULL,
  `descri_sind` varchar(50) NOT NULL,
  PRIMARY KEY (`codsind`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_captura_ind`
-- Table structure for table `faturas_negociacao`
--

DROP TABLE IF EXISTS `faturas_negociacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturas_negociacao` (
  `codftn` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_lan` datetime NOT NULL,
  `valor_base` decimal(10,2) NOT NULL,
  `valor_jr` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_multa` decimal(8,2) NOT NULL DEFAULT '0.00',
  `valor_lan` decimal(10,2) NOT NULL,
  `status` char(1) NOT NULL DEFAULT 'A',
  `data_can` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codusu_can` char(2) NOT NULL DEFAULT '',
  `valor_pag` decimal(10,2) NOT NULL DEFAULT '0.00',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codftn`),
  KEY `codusu` (`codusu`),
  KEY `data_lan` (`data_lan`),
  KEY `status` (`status`),
  KEY `data_can` (`data_can`),
  KEY `codusu_can` (`codusu_can`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturas_negociacao`
-- Table structure for table `desconto_filtro_aplicado`
--

DROP TABLE IF EXISTS `desconto_filtro_aplicado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `desconto_filtro_aplicado` (
  `coddesfilapl` char(10) NOT NULL,
  `codfiltro` char(10) NOT NULL,
  `codregradesconto` char(10) NOT NULL,
  `filtro_aplicado` text NOT NULL,
  PRIMARY KEY (`coddesfilapl`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `desconto_filtro_aplicado`
-- Table structure for table `imp_prod`
--

DROP TABLE IF EXISTS `imp_prod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imp_prod` (
  `codimprod` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codtcf` varchar(10) NOT NULL,
  `estado` char(2) NOT NULL,
  `base` float(10,4) NOT NULL,
  `aliquota` float(10,4) NOT NULL,
  `valor` float(10,4) NOT NULL,
  PRIMARY KEY (`codimprod`),
  KEY `codprod` (`codprod`),
  KEY `codtcf` (`codtcf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imp_prod`
-- Table structure for table `regra_cob_serasa`
--

DROP TABLE IF EXISTS `regra_cob_serasa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regra_cob_serasa` (
  `codrcobse` varchar(10) NOT NULL,
  `codcob` varchar(10) NOT NULL,
  `serasa` char(1) NOT NULL,
  PRIMARY KEY (`codrcobse`),
  KEY `codcob` (`codcob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regra_cob_serasa`
-- Table structure for table `movimentoconciliacao`
--

DROP TABLE IF EXISTS `movimentoconciliacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentoconciliacao` (
  `Id` bigint(18) NOT NULL AUTO_INCREMENT,
  `Arquivo` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `Banco` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `Conta` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `Data` date DEFAULT NULL,
  `Documento` varchar(18) CHARACTER SET latin1 DEFAULT NULL,
  `Historico` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `Valor` double(15,2) DEFAULT NULL,
  `SeqMov` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `Usuario` varchar(2) CHARACTER SET latin1 DEFAULT NULL,
  `Situacao` char(1) CHARACTER SET latin1 DEFAULT NULL,
  `Motivo` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `codarq` varchar(10) DEFAULT NULL,
  `codban` varchar(10) DEFAULT NULL,
  `codusu` char(2) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `SeqMov` (`SeqMov`),
  KEY `codarq` (`codarq`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentoconciliacao`
-- Table structure for table `protocolos_documentos`
--

DROP TABLE IF EXISTS `protocolos_documentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `protocolos_documentos` (
  `codprot` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `tipo` char(1) NOT NULL DEFAULT '',
  `arquivo` text NOT NULL,
  PRIMARY KEY (`codprot`),
  UNIQUE KEY `codprot` (`codprot`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocolos_documentos`
-- Table structure for table `meta_vendedor`
--

DROP TABLE IF EXISTS `meta_vendedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meta_vendedor` (
  `codmeta` varchar(10) NOT NULL DEFAULT '',
  `codcomp` varchar(4) NOT NULL DEFAULT '',
  `codven` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `meta` decimal(5,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codmeta`),
  KEY `codcomp` (`codcomp`),
  KEY `codven` (`codven`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meta_vendedor`
-- Table structure for table `det_combo_sc`
--

DROP TABLE IF EXISTS `det_combo_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_combo_sc` (
  `coddcombosc` char(10) NOT NULL,
  `codagrcombo` char(10) NOT NULL,
  `codsercli_r` char(10) NOT NULL COMMENT 'codsercli_r é responsalvel pela regra aplicado no codsercli_a',
  `codsercli_a` char(10) NOT NULL COMMENT 'codsercli_a recebeu a regra entregue pelo codsercli_r',
  `tipo_atribuicao` char(1) NOT NULL COMMENT 'I = taxa de instalação M = mensalidade\n A = taxa de adesao',
  `oderm` int(11) NOT NULL,
  `valor_plano_ser` decimal(10,2) NOT NULL,
  `valor_plano_sc` decimal(10,2) DEFAULT NULL,
  `valor_regra` decimal(10,2) NOT NULL DEFAULT '0.00',
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `periodo_desconto` char(1) NOT NULL COMMENT 'Vazio= Sem Conf. / P = Periodo de data',
  `data_ini_desconto` date NOT NULL,
  `data_fim_desconto` date NOT NULL,
  `valor_periodo_ciclo` int(11) NOT NULL,
  PRIMARY KEY (`coddcombosc`),
  KEY `codsercli_r` (`codsercli_r`),
  KEY `codsercli_a` (`codsercli_a`),
  KEY `oderm` (`oderm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_combo_sc`
-- Table structure for table `parametros_suspender`
--

DROP TABLE IF EXISTS `parametros_suspender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parametros_suspender` (
  `codpars` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `valor_minimo` float(10,2) NOT NULL DEFAULT '0.00',
  `quant_dias` int(3) unsigned NOT NULL DEFAULT '0',
  `quant_dias_aviso` int(3) unsigned NOT NULL,
  `quant_dias_reducao` int(3) unsigned NOT NULL,
  `dias_nao_gerar` int(3) unsigned NOT NULL DEFAULT '0',
  `dias_negociacao` int(3) unsigned NOT NULL,
  `data_inicio` date NOT NULL DEFAULT '0000-00-00',
  `porc_reducao` float(6,2) NOT NULL,
  PRIMARY KEY (`codpars`),
  KEY `codcob` (`codcob`),
  KEY `data_inicio` (`data_inicio`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_suspender`
-- Table structure for table `det_tabela_imp_ret`
--

DROP TABLE IF EXISTS `det_tabela_imp_ret`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_tabela_imp_ret` (
  `coddtimret` varchar(10) NOT NULL,
  `codtimret` varchar(10) NOT NULL DEFAULT '',
  `numero_faixa` int(4) NOT NULL,
  `valor_sup` double(10,2) NOT NULL,
  `valor_inf` double(10,2) NOT NULL,
  `pis_ret` float(5,2) NOT NULL,
  `cofins_ret` float(5,2) NOT NULL,
  `csll_ret` float(5,2) NOT NULL,
  `irrf_ret` float(5,2) NOT NULL,
  `retem_pis` char(1) NOT NULL DEFAULT 'N',
  `retem_cofins` char(1) NOT NULL DEFAULT 'N',
  `retem_csll` char(1) NOT NULL DEFAULT 'N',
  `retem_irrf` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`coddtimret`),
  KEY `codtimret` (`codtimret`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_tabela_imp_ret`
-- Table structure for table `versao`
--

DROP TABLE IF EXISTS `versao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `versao` (
  `codver` varchar(7) NOT NULL DEFAULT '',
  `status` varchar(40) NOT NULL,
  `data_prev` date NOT NULL,
  `desde` date NOT NULL DEFAULT '0000-00-00',
  `ate` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`codver`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `versao`
-- Table structure for table `syn_nota_fiscal`
--

DROP TABLE IF EXISTS `syn_nota_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syn_nota_fiscal` (
  `codsnf` bigint(20) NOT NULL AUTO_INCREMENT,
  `codnf` char(10) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  `data_ua` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sincronizado` char(1) NOT NULL DEFAULT 'N',
  `data_sincronismo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `resp_sincronismo` varchar(20) NOT NULL DEFAULT '',
  `data_erro` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tentativa` int(11) NOT NULL DEFAULT '0',
  `log_erro` mediumtext,
  `campos` mediumtext,
  `id_sap` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsnf`),
  KEY `codnf` (`codnf`),
  KEY `sincronizado` (`sincronizado`),
  KEY `acao` (`acao`),
  KEY `tentativa` (`tentativa`),
  KEY `data_ua` (`data_ua`),
  KEY `resp_sincronismo` (`resp_sincronismo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syn_nota_fiscal`
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes` (
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codexterno` varchar(20) NOT NULL DEFAULT '',
  `codgcli` varchar(10) NOT NULL DEFAULT '0120191003',
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `nome_cli` varchar(100) NOT NULL,
  `nome_fan` varchar(50) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT '',
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codigo_aut` varchar(10) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `referencia` varchar(100) NOT NULL,
  `apto` varchar(10) NOT NULL DEFAULT '',
  `sala` varchar(10) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `contato` varchar(50) NOT NULL DEFAULT '',
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `data_nac` date DEFAULT '0000-00-00',
  `tipo_cliente` char(1) NOT NULL DEFAULT '',
  `tipo_codigo` char(1) NOT NULL DEFAULT '',
  `endereco_cob` varchar(50) NOT NULL DEFAULT '',
  `bairro_cob` varchar(25) NOT NULL DEFAULT '',
  `cidade_cob` varchar(8) NOT NULL DEFAULT '',
  `cep_cob` varchar(9) NOT NULL DEFAULT '',
  `cnpj` varchar(18) NOT NULL DEFAULT '',
  `icm` varchar(16) NOT NULL DEFAULT '',
  `ic_mun` varchar(16) NOT NULL DEFAULT '',
  `rg` varchar(20) NOT NULL DEFAULT '',
  `rg_emissor` varchar(10) NOT NULL,
  `cpf` varchar(14) NOT NULL DEFAULT '',
  `codcfop` varchar(5) NOT NULL DEFAULT '',
  `data_cad` date NOT NULL DEFAULT '0000-00-00',
  `latitude` varchar(20) NOT NULL DEFAULT '',
  `longitude` varchar(20) NOT NULL DEFAULT '',
  `nunca_suspender` char(1) NOT NULL DEFAULT 'N',
  `cobrar_boleto` char(1) NOT NULL DEFAULT 'S',
  `cobrar_emails` char(1) NOT NULL DEFAULT 'S',
  `cobrar_franquia` char(1) NOT NULL DEFAULT 'S',
  `cobrar_multa` char(1) NOT NULL DEFAULT 'S',
  `dar_desconto` char(1) NOT NULL DEFAULT 'S',
  `dar_desc_prog` char(1) NOT NULL DEFAULT 'S',
  `imprime_nf` char(1) NOT NULL DEFAULT 'N',
  `enviar_nf` char(1) NOT NULL DEFAULT 'S',
  `enviar_boleto` char(1) NOT NULL DEFAULT 'S',
  `enviar_aviso` char(1) NOT NULL DEFAULT 'S',
  `nunca_imp_boleto` char(1) NOT NULL DEFAULT 'N',
  `nunca_reduzir_vel` char(1) NOT NULL DEFAULT 'N',
  `nunca_colocar_aviso` char(1) NOT NULL DEFAULT 'N',
  `nunca_avisar_franquia` char(1) NOT NULL DEFAULT 'N',
  `sla` char(1) NOT NULL DEFAULT 'N',
  `classif_contabil` varchar(20) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `saldo_atual` float(10,2) NOT NULL DEFAULT '0.00',
  `classificacao_tec` float(6,2) NOT NULL DEFAULT '0.00',
  `classificacao_fin` float(6,2) NOT NULL DEFAULT '0.00',
  `classificacao_cad` float(6,2) NOT NULL DEFAULT '0.00',
  `nunca_protestar_serasa` char(1) NOT NULL DEFAULT 'N',
  `funcionario` char(1) NOT NULL DEFAULT 'N',
  `sped_tipo_assinante` varchar(20) NOT NULL,
  `sped_classe_consumo` varchar(20) NOT NULL,
  `sped_tipo_servico` varchar(20) NOT NULL,
  `simples_nacional` char(1) NOT NULL DEFAULT 'S',
  `sub_tributario` char(1) NOT NULL DEFAULT 'N',
  `codcnae` varchar(8) NOT NULL,
  `indicador_icm` varchar(10) NOT NULL,
  `cod_identificador_da` varchar(15) NOT NULL DEFAULT '',
  `gerar_reajuste` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codcli`),
  KEY `cidade` (`cidade`),
  KEY `cidade_cob` (`cidade_cob`),
  KEY `nome_cli` (`nome_cli`),
  KEY `codexterno` (`codexterno`),
  KEY `ativo` (`ativo`),
  KEY `codgcli` (`codgcli`),
  KEY `enviar_nf` (`enviar_nf`),
  KEY `cnpj` (`cnpj`),
  KEY `cpf` (`cpf`),
  KEY `tipo_cliente` (`tipo_cliente`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
-- Table structure for table `conf_padrao_graficos`
--

DROP TABLE IF EXISTS `conf_padrao_graficos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_padrao_graficos` (
  `codcgraf` varchar(10) NOT NULL,
  `quant_itens_limit` int(2) unsigned NOT NULL,
  `cor_aleatoria` char(1) NOT NULL,
  `grafico_aleatorio` char(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_padrao_graficos`
-- Table structure for table `mensagem_telas`
--

DROP TABLE IF EXISTS `mensagem_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mensagem_telas` (
  `codmtel` varchar(10) NOT NULL,
  `codtel` varchar(10) NOT NULL,
  `tipo` char(1) NOT NULL,
  `mensagem` varchar(254) NOT NULL,
  `descricao` varchar(254) NOT NULL,
  PRIMARY KEY (`codmtel`),
  KEY `codtel` (`codtel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensagem_telas`
-- Table structure for table `status_cartoes`
--

DROP TABLE IF EXISTS `status_cartoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_cartoes` (
  `codstc` varchar(10) NOT NULL DEFAULT '',
  `descri_stc` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codstc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_cartoes`
-- Table structure for table `log_exc_bol`
--

DROP TABLE IF EXISTS `log_exc_bol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_exc_bol` (
  `codlexc` int(11) NOT NULL AUTO_INCREMENT,
  `codcli` int(6) NOT NULL,
  `codfat` char(10) NOT NULL,
  `codlogbol` char(10) NOT NULL,
  `data_lan` datetime NOT NULL,
  `dados_env` mediumtext NOT NULL,
  `dados_rec` mediumtext NOT NULL,
  PRIMARY KEY (`codlexc`),
  KEY `codcli` (`codcli`),
  KEY `codfat` (`codfat`),
  KEY `codlogbol` (`codlogbol`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_exc_bol`
-- Table structure for table `turnos_roteirizacao`
--

DROP TABLE IF EXISTS `turnos_roteirizacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnos_roteirizacao` (
  `codtrot` char(10) NOT NULL DEFAULT '',
  `descri_turno` varchar(40) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `hora_ini` char(5) NOT NULL DEFAULT '00:00',
  `hora_fim` char(5) NOT NULL DEFAULT '00:00',
  PRIMARY KEY (`codtrot`),
  KEY `ativo` (`ativo`),
  KEY `hora_ini` (`hora_ini`),
  KEY `hora_fim` (`hora_fim`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnos_roteirizacao`
-- Table structure for table `message_central`
--

DROP TABLE IF EXISTS `message_central`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message_central` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codctr` char(10) NOT NULL DEFAULT '',
  `message` mediumtext NOT NULL,
  `start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `active` char(1) NOT NULL DEFAULT '',
  `subject` varchar(254) DEFAULT NULL,
  `platform` char(1) NOT NULL DEFAULT 'W',
  PRIMARY KEY (`id`),
  KEY `codctr` (`codctr`),
  KEY `start_date` (`start_date`),
  KEY `end_date` (`end_date`),
  KEY `active` (`active`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_central`
-- Table structure for table `codigos_valores_ind`
--

DROP TABLE IF EXISTS `codigos_valores_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codigos_valores_ind` (
  `codcvi` varchar(10) NOT NULL,
  `codvind` varchar(10) NOT NULL,
  `codigos` mediumtext NOT NULL,
  PRIMARY KEY (`codcvi`),
  KEY `codvind` (`codvind`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos_valores_ind`
-- Table structure for table `status_nfe`
--

DROP TABLE IF EXISTS `status_nfe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_nfe` (
  `codstnfe` varchar(10) NOT NULL,
  `descri_stnfe` varchar(100) NOT NULL,
  `consulta` varchar(100) NOT NULL,
  PRIMARY KEY (`codstnfe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_nfe`
-- Table structure for table `item_er`
--

DROP TABLE IF EXISTS `item_er`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_er` (
  `codieb` varchar(10) NOT NULL DEFAULT '',
  `codeb` varchar(10) NOT NULL DEFAULT '',
  `coditem` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codieb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_er`
-- Table structure for table `maparede_portas`
--

DROP TABLE IF EXISTS `maparede_portas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maparede_portas` (
  `codmpp` varchar(20) NOT NULL DEFAULT '',
  `codmpeq` varchar(20) NOT NULL DEFAULT '',
  `codintr` char(10) DEFAULT '',
  `nro` int(3) NOT NULL DEFAULT '0',
  `integrator` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codmpp`),
  KEY `codgeoeq` (`codmpeq`),
  KEY `codintr` (`codintr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maparede_portas`
-- Table structure for table `contactos`
--

DROP TABLE IF EXISTS `contactos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contactos` (
  `codcont` varchar(10) NOT NULL DEFAULT '',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `codpint` char(10) NOT NULL DEFAULT '',
  `codco_cl_p` char(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codusu` char(2) NOT NULL DEFAULT '',
  `tipo_contato` char(1) NOT NULL DEFAULT '',
  `resposta` char(1) NOT NULL DEFAULT 'N',
  `obs` text NOT NULL,
  PRIMARY KEY (`codcont`),
  KEY `codpros` (`codpros`),
  KEY `data` (`data`),
  KEY `codusu` (`codusu`),
  KEY `resposta` (`resposta`),
  KEY `codpint` (`codpint`),
  KEY `codco_cl_p` (`codco_cl_p`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactos`
-- Table structure for table `conf_vendedores`
--

DROP TABLE IF EXISTS `conf_vendedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_vendedores` (
  `codven` varchar(10) NOT NULL DEFAULT '',
  `codfcs` varchar(10) NOT NULL,
  `mesalidade_paga` char(1) NOT NULL DEFAULT 'S',
  `servicos_adi` char(1) NOT NULL DEFAULT 'S',
  `porcentagem_adi` float(5,2) NOT NULL DEFAULT '0.00',
  `porcentagem_total` float(5,2) NOT NULL DEFAULT '0.00',
  `comissao_vendas` char(1) NOT NULL DEFAULT 'S',
  `primeira_mensalidade` varchar(1) NOT NULL DEFAULT 'N',
  `qtde_dias_abat` int(3) unsigned NOT NULL DEFAULT '0',
  `valor_evento` float(8,2) NOT NULL,
  `porcentagem_evento` float(5,2) NOT NULL,
  `evento_valor` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codven`),
  KEY `codfcs` (`codfcs`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_vendedores`
-- Table structure for table `servicos_vcre`
--

DROP TABLE IF EXISTS `servicos_vcre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_vcre` (
  `codsvcre` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codvcre` varchar(10) NOT NULL,
  PRIMARY KEY (`codsvcre`),
  KEY `codser` (`codser`),
  KEY `codvcre` (`codvcre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_vcre`
-- Table structure for table `cidades_codigos_externos`
--

DROP TABLE IF EXISTS `cidades_codigos_externos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cidades_codigos_externos` (
  `codcide` varchar(10) NOT NULL,
  `cidade` varchar(8) DEFAULT NULL,
  `codrad` varchar(10) DEFAULT NULL,
  `codexterno` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`codcide`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidades_codigos_externos`
-- Table structure for table `danfe_nota_fiscal`
--

DROP TABLE IF EXISTS `danfe_nota_fiscal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `danfe_nota_fiscal` (
  `coddanfe` varchar(10) NOT NULL,
  `codnf` varchar(10) DEFAULT NULL,
  `danfe` mediumtext,
  PRIMARY KEY (`coddanfe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danfe_nota_fiscal`
-- Table structure for table `valor_parametros_consulta`
--

DROP TABLE IF EXISTS `valor_parametros_consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valor_parametros_consulta` (
  `codvpcst` varchar(10) NOT NULL,
  `codcbe` varchar(10) DEFAULT NULL,
  `codpcst` varchar(10) DEFAULT NULL,
  `codatar` varchar(10) DEFAULT '',
  `valor` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`codvpcst`),
  KEY `codcbe` (`codcbe`),
  KEY `codpcst` (`codpcst`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valor_parametros_consulta`
-- Table structure for table `tipo_radio`
--

DROP TABLE IF EXISTS `tipo_radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_radio` (
  `codtrad` varchar(10) NOT NULL DEFAULT '',
  `descri_trad` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_radio`
-- Table structure for table `dominios`
--

DROP TABLE IF EXISTS `dominios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dominios` (
  `coddom` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codservp_h` varchar(10) NOT NULL DEFAULT '',
  `codservp_c` varchar(10) NOT NULL DEFAULT '',
  `nome_dom` varchar(50) NOT NULL DEFAULT '',
  `dns_primario` varchar(15) NOT NULL DEFAULT '',
  `dns_secundario` varchar(15) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `estatisticas` char(1) NOT NULL DEFAULT 'S',
  `data_reg` date NOT NULL DEFAULT '0000-00-00',
  `redirecionamento` varchar(50) NOT NULL DEFAULT '',
  `bancodados` varchar(15) NOT NULL DEFAULT '',
  `tipo_site` varchar(20) NOT NULL DEFAULT '',
  `desenvolvedor` varchar(50) NOT NULL DEFAULT '',
  `ddd` char(3) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `email_desen` varchar(50) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `quota` float(6,2) NOT NULL DEFAULT '0.00',
  `ftp` varchar(15) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `pasta` varchar(50) NOT NULL DEFAULT '',
  `email_adm` varchar(50) NOT NULL DEFAULT '',
  `nro_ip` varchar(15) NOT NULL DEFAULT '',
  `criado` char(1) NOT NULL DEFAULT 'S',
  `quota_atual` int(5) unsigned NOT NULL,
  PRIMARY KEY (`coddom`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dominios`
-- Table structure for table `dominios_padrao`
--

DROP TABLE IF EXISTS `dominios_padrao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dominios_padrao` (
  `coddomp` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `dominio` varchar(50) NOT NULL DEFAULT '',
  `quota` int(4) unsigned NOT NULL DEFAULT '0',
  `senha` varchar(10) NOT NULL DEFAULT '',
  `web` char(1) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`coddomp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dominios_padrao`
-- Table structure for table `saldos_sc`
--

DROP TABLE IF EXISTS `saldos_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `saldos_sc` (
  `codssc` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codcli` int(6) unsigned NOT NULL,
  `codepsc` varchar(10) NOT NULL,
  `ultima_alt_cr` datetime NOT NULL,
  `ultima_alt_saldo` datetime NOT NULL,
  `saldo_vencido` float(10,2) NOT NULL,
  `saldo_vencer` float(10,2) NOT NULL,
  `saldo_renegociado` float(10,2) NOT NULL,
  PRIMARY KEY (`codssc`),
  KEY `codcli` (`codcli`),
  KEY `ultima_alt_cr` (`ultima_alt_cr`),
  KEY `ultima_alt_saldo` (`ultima_alt_saldo`),
  KEY `saldo_vencido` (`saldo_vencido`),
  KEY `codsercli` (`codsercli`),
  KEY `codepsc` (`codepsc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saldos_sc`
-- Table structure for table `combo_grupo_comercial`
--

DROP TABLE IF EXISTS `combo_grupo_comercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combo_grupo_comercial` (
  `codcombocomercial` char(10) NOT NULL,
  `codgcom` char(10) NOT NULL,
  `codcombo` char(10) NOT NULL,
  `multa` char(1) NOT NULL COMMENT '''0 = não cobrar\\n1 = cobrar em função dos desconto \\n2 = cobrar valor fixo \\n''',
  `obrigatorio` char(1) NOT NULL COMMENT '''0 = não \\n1 = sim \\n''',
  `valor_fixo_multa` float(6,2) NOT NULL,
  PRIMARY KEY (`codcombocomercial`),
  KEY `codcombocomercial` (`codcombocomercial`,`codgcom`,`codcombo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo_grupo_comercial`
-- Table structure for table `servicos_extras`
--

DROP TABLE IF EXISTS `servicos_extras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_extras` (
  `codserex` char(10) NOT NULL COMMENT 'Chave primária',
  `codsad` char(10) NOT NULL COMMENT 'Codigo do Serviço Adicional',
  `ativo` char(1) NOT NULL DEFAULT 'S' COMMENT 'Serviço Ativo: S - Ativo, N - Inativo',
  `descri_serex` varchar(100) NOT NULL DEFAULT '' COMMENT 'Descrição do Serviço Extra',
  `valor_serex` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do Serviço Extra',
  `tipo_cob` char(1) NOT NULL DEFAULT 'U' COMMENT 'Tipo de Cobrança: U-Cobrança feita uma única vez, M - Cobrança Mensal',
  `tipo_cob_unica` char(1) NOT NULL DEFAULT 'C' COMMENT 'Tipo de Cobrança Unica: C-Contas a Receber, E - Evento de Faturamento',
  `qtde_diasvenc` int(3) NOT NULL DEFAULT '0' COMMENT 'Quantidade de dias para cobrança do contas a Receber',
  `qtde_parcelas` int(3) NOT NULL DEFAULT '0' COMMENT 'Quantidade de parcelas do evento de faturamento',
  `obs` text NOT NULL COMMENT 'Observação',
  `tipo_venc` char(1) NOT NULL DEFAULT 'P' COMMENT 'Tipo de Data de Vencimento: P-Data de Vencimento do Plano, D - Qtde de Dias para Vencimento',
  `codtserex` char(10) NOT NULL DEFAULT '0' COMMENT 'Campo para informar o código do tipo do serviço extra',
  `codigo_externo` char(10) NOT NULL DEFAULT '' COMMENT 'Campo para informar codigo externo de integração',
  `valor_externo` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codserex`),
  KEY `codsad` (`codsad`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_extras`
-- Table structure for table `servicos_cli_extras`
--

DROP TABLE IF EXISTS `servicos_cli_extras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_extras` (
  `codsercliex` char(10) NOT NULL COMMENT 'Chave primária',
  `codserex` char(10) NOT NULL COMMENT 'Codigo do Serviço Extra',
  `codsercli` char(10) NOT NULL COMMENT 'Codigo do Serviço do Cliente',
  `data_ini` date NOT NULL COMMENT 'Data de Início do Serviço',
  `valor` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Valor do Serviço Extra no Cliente',
  `complemento` varchar(30) NOT NULL DEFAULT '' COMMENT 'Complemento da Descrição do Serviço',
  `nro_serex` int(3) NOT NULL DEFAULT '0',
  `obs` text NOT NULL COMMENT 'Observação',
  `data_ven` date NOT NULL COMMENT 'Data do Primeiro Vencimento das parcelas (Contas a Receber)',
  `qtde_parcelas` int(3) NOT NULL DEFAULT '0' COMMENT 'Quantidade de parcelas (Contas a Receber ou Evento de Faturamento)',
  `nro_reg` int(11) NOT NULL DEFAULT '0' COMMENT 'Numero do registro do serviço extra',
  `codigo_externo` varchar(20) NOT NULL COMMENT 'Campo para informar código externo de integração',
  `codco_cl` char(10) NOT NULL DEFAULT '' COMMENT 'Campo do contato do cliente',
  PRIMARY KEY (`codsercliex`),
  KEY `codserex` (`codserex`),
  KEY `codsercli` (`codsercli`),
  CONSTRAINT `FK_codserex` FOREIGN KEY (`codserex`) REFERENCES `servicos_extras` (`codserex`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_extras`
-- Table structure for table `regras_atendimento`
--

DROP TABLE IF EXISTS `regras_atendimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_atendimento` (
  `codregatend` varchar(10) NOT NULL,
  `descri_regra` varchar(100) NOT NULL,
  PRIMARY KEY (`codregatend`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_atendimento`
-- Table structure for table `promocoes_sc`
--

DROP TABLE IF EXISTS `promocoes_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promocoes_sc` (
  `codpsc` varchar(10) NOT NULL,
  `codprom` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `quant_disponiveis` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codpsc`),
  KEY `codprom` (`codprom`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promocoes_sc`
-- Table structure for table `regras_negocios_voz`
--

DROP TABLE IF EXISTS `regras_negocios_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_negocios_voz` (
  `codrnv` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `descri_rnv` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codrnv`),
  KEY `codser` (`codser`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_negocios_voz`
-- Table structure for table `servicos_pop`
--

DROP TABLE IF EXISTS `servicos_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_pop` (
  `codserp` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codserp`),
  KEY `codser` (`codser`),
  KEY `codpop` (`codpop`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_pop`
-- Table structure for table `cidades_reg_metrop`
--

DROP TABLE IF EXISTS `cidades_reg_metrop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cidades_reg_metrop` (
  `codcrgmt` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `codrgmt` varchar(10) NOT NULL,
  PRIMARY KEY (`codcrgmt`),
  KEY `cidade` (`cidade`),
  KEY `codrgmt` (`codrgmt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidades_reg_metrop`
-- Table structure for table `remessa_nf`
--

DROP TABLE IF EXISTS `remessa_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `remessa_nf` (
  `codrnf` varchar(10) NOT NULL DEFAULT '',
  `mes` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`codrnf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remessa_nf`
-- Table structure for table `tarifas`
--

DROP TABLE IF EXISTS `tarifas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarifas` (
  `codtari` varchar(10) NOT NULL,
  `descri_tari` varchar(50) NOT NULL,
  `codban` varchar(10) NOT NULL,
  `valor` float(10,2) NOT NULL,
  `sacado` varchar(70) NOT NULL,
  PRIMARY KEY (`codtari`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarifas`
-- Table structure for table `dicionario_radius`
--

DROP TABLE IF EXISTS `dicionario_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dicionario_radius` (
  `coddr` varchar(10) NOT NULL DEFAULT '',
  `codosr` varchar(10) NOT NULL DEFAULT '',
  `atributo` varchar(50) NOT NULL DEFAULT '',
  `tabela` varchar(20) NOT NULL DEFAULT '',
  `descri_dr` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddr`),
  KEY `atributo` (`atributo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dicionario_radius`
-- Table structure for table `mensagem_usu`
--

DROP TABLE IF EXISTS `mensagem_usu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mensagem_usu` (
  `codmusu` char(10) NOT NULL,
  `codmsg` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `lido` char(1) NOT NULL DEFAULT 'N',
  `apagado` char(1) NOT NULL DEFAULT 'N',
  `codcar` char(10) NOT NULL DEFAULT '',
  `coddep` char(10) NOT NULL DEFAULT '',
  `codpas` char(10) NOT NULL DEFAULT '',
  `codmarc` char(1) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL,
  PRIMARY KEY (`codmusu`),
  KEY `codmsg` (`codmsg`),
  KEY `codusu_d` (`codusu`),
  KEY `apagado_d` (`apagado`),
  KEY `codcar` (`codcar`),
  KEY `coddep` (`coddep`),
  KEY `codpas_d` (`codpas`),
  KEY `codmarc_d` (`codmarc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensagem_usu`
-- Table structure for table `script_tipo_olt`
--

DROP TABLE IF EXISTS `script_tipo_olt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `script_tipo_olt` (
  `codstolt` varchar(10) NOT NULL,
  `codseq` varchar(10) NOT NULL,
  `codtolt` varchar(10) NOT NULL,
  PRIMARY KEY (`codstolt`),
  KEY `codseq` (`codseq`),
  KEY `codtolt` (`codtolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `script_tipo_olt`
-- Table structure for table `log_onu_fibra`
--

DROP TABLE IF EXISTS `log_onu_fibra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_onu_fibra` (
  `id_log` char(10) NOT NULL,
  `codpat` char(10) NOT NULL,
  `data_lan` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_fim` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codsercli` char(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codtexec` char(10) NOT NULL DEFAULT '',
  `codolt` char(10) NOT NULL,
  `log_onu` text NOT NULL,
  `status_exec` char(5) NOT NULL DEFAULT '',
  `msg_erro` text NOT NULL,
  KEY `codpat` (`codpat`),
  KEY `data_lan` (`data_lan`),
  KEY `codsercli` (`codsercli`),
  KEY `codusu` (`codusu`),
  KEY `codtexec` (`codtexec`),
  KEY `status_exec` (`status_exec`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_onu_fibra`
-- Table structure for table `pon_slot`
--

DROP TABLE IF EXISTS `pon_slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pon_slot` (
  `codpolt` varchar(10) NOT NULL,
  `codsolt` varchar(10) NOT NULL,
  `ponid` varchar(10) NOT NULL,
  `vlan` int(6) unsigned NOT NULL,
  `vlan_voz` int(6) unsigned NOT NULL,
  `vlan_tv` int(6) unsigned NOT NULL,
  `referencia` varchar(50) NOT NULL,
  PRIMARY KEY (`codpolt`),
  KEY `codsolt` (`codsolt`),
  KEY `ponid` (`ponid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pon_slot`
-- Table structure for table `logs_voip`
--

DROP TABLE IF EXISTS `logs_voip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_voip` (
  `codlgvp` varchar(10) NOT NULL DEFAULT '',
  `codlvp` varchar(10) NOT NULL DEFAULT '',
  `transid` varchar(36) NOT NULL DEFAULT '',
  `inicio` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `fin` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codpais` char(3) NOT NULL DEFAULT '',
  `codarea` varchar(5) NOT NULL DEFAULT '',
  `fone_destino` int(8) unsigned NOT NULL DEFAULT '0',
  `duracao` decimal(7,0) NOT NULL DEFAULT '2',
  `valor_minuto` decimal(5,3) NOT NULL DEFAULT '0.000',
  `valor_chamada` decimal(7,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codlgvp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_voip`
-- Table structure for table `sap_ret_mov`
--

DROP TABLE IF EXISTS `sap_ret_mov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sap_ret_mov` (
  `codmov` char(10) NOT NULL,
  `codnf` char(10) NOT NULL,
  `docentry` int(11) NOT NULL,
  KEY `codmov` (`codmov`),
  KEY `docentry` (`docentry`,`codnf`),
  KEY `codnf` (`codnf`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sap_ret_mov`
-- Table structure for table `status_ocorrencias`
--

DROP TABLE IF EXISTS `status_ocorrencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_ocorrencias` (
  `codsto` varchar(10) NOT NULL DEFAULT '',
  `descri_sto` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsto`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_ocorrencias`
-- Table structure for table `tipo_comandos`
--

DROP TABLE IF EXISTS `tipo_comandos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_comandos` (
  `codtcom` char(1) NOT NULL DEFAULT '',
  `descri_tcom` varchar(30) NOT NULL DEFAULT '',
  `timeout_ass` int(3) unsigned NOT NULL,
  PRIMARY KEY (`codtcom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_comandos`
-- Table structure for table `det_produtos_nf`
--

DROP TABLE IF EXISTS `det_produtos_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_produtos_nf` (
  `coddpnf` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `codigo_for` varchar(20) NOT NULL,
  `descri_for` varchar(100) NOT NULL,
  `unidade` varchar(6) NOT NULL,
  `quant` int(4) unsigned NOT NULL,
  `valor` float(10,2) NOT NULL,
  `base_icms` float(10,2) NOT NULL,
  `icms` float(5,2) NOT NULL,
  `base_pis` float(10,2) NOT NULL,
  `pis` float(5,2) NOT NULL,
  `base_cofins` float(10,2) NOT NULL,
  `cofins` float(5,2) NOT NULL,
  PRIMARY KEY (`coddpnf`),
  KEY `codprod` (`codprod`),
  KEY `codnf` (`codnf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_produtos_nf`
-- Table structure for table `form_custom`
--

DROP TABLE IF EXISTS `form_custom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `form_custom` (
  `codfrmct` varchar(10) NOT NULL,
  `form_name` varchar(100) DEFAULT NULL,
  `form_obj` varchar(255) DEFAULT NULL,
  `form_obj_event` varchar(150) DEFAULT NULL,
  `ativo` varchar(1) DEFAULT 'N',
  PRIMARY KEY (`codfrmct`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_custom`
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `codlog` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcomp` varchar(4) NOT NULL DEFAULT '',
  `id_session` bigint(21) NOT NULL DEFAULT '0',
  `user_name` varchar(32) NOT NULL DEFAULT '',
  `ip_entrada` varchar(15) NOT NULL DEFAULT '',
  `port` int(12) NOT NULL DEFAULT '0',
  `hora_ini` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `segundos` int(12) NOT NULL DEFAULT '0',
  `autenticacao` char(1) NOT NULL DEFAULT '',
  `input` int(12) NOT NULL DEFAULT '0',
  `output` int(12) NOT NULL DEFAULT '0',
  `estacao` varchar(10) NOT NULL DEFAULT '',
  `fone` varchar(10) NOT NULL DEFAULT '',
  `motivo_fin` char(1) NOT NULL DEFAULT '',
  `ip_dessignado` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`codlog`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
-- Table structure for table `ordemcompraitem`
--

DROP TABLE IF EXISTS `ordemcompraitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordemcompraitem` (
  `codordcompi` varchar(10) NOT NULL COMMENT 'Ordem de compra item',
  `ordemcompra` bigint(12) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  `codlmp` varchar(10) NOT NULL COMMENT 'Locaçao RBX',
  `quantidade` double(10,2) NOT NULL,
  `quantidade_rec` double(10,2) NOT NULL COMMENT 'Quant. Recebida do item',
  `custounitario` double(15,4) NOT NULL,
  PRIMARY KEY (`codordcompi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordemcompraitem`
-- Table structure for table `medicoes`
--

DROP TABLE IF EXISTS `medicoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicoes` (
  `codmed` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codflv` varchar(10) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL,
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `codunm` varchar(10) NOT NULL DEFAULT '',
  `quantidade` int(11) unsigned NOT NULL,
  `contratado` int(11) unsigned NOT NULL,
  PRIMARY KEY (`codmed`),
  KEY `codsercli` (`codsercli`),
  KEY `codflv` (`codflv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicoes`
-- Table structure for table `detalhe_deposito`
--

DROP TABLE IF EXISTS `detalhe_deposito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_deposito` (
  `codddep` varchar(10) NOT NULL DEFAULT '',
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `coddrec` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'D',
  PRIMARY KEY (`codddep`),
  KEY `codmov` (`codmov`),
  KEY `coddrec` (`coddrec`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_deposito`
-- Table structure for table `registro_tributacao`
--

DROP TABLE IF EXISTS `registro_tributacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registro_tributacao` (
  `codrtrib` char(10) NOT NULL COMMENT 'Código do Registro de Tributação.',
  `nome_reg_tri` varchar(30) NOT NULL DEFAULT ' ' COMMENT 'Nome do Registro de Tributação.',
  `descricao` varchar(100) NOT NULL DEFAULT ' ' COMMENT 'Descrição do Registro de Tributação, a critério do Provedor.',
  `cfop` char(4) NOT NULL DEFAULT '' COMMENT 'Codigo do CFOP.',
  `crt` char(1) NOT NULL DEFAULT '' COMMENT 'Especificação do Regime Tributário.',
  `obs_fiscal` mediumtext NOT NULL COMMENT 'Observação Fiscal',
  PRIMARY KEY (`codrtrib`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_tributacao`
-- Table structure for table `det_indice`
--

DROP TABLE IF EXISTS `det_indice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_indice` (
  `coddindc` varchar(10) NOT NULL DEFAULT '',
  `codindc` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'A',
  `mes` int(2) NOT NULL,
  `ano` varchar(4) NOT NULL,
  `porcentagem` float(8,2) NOT NULL,
  PRIMARY KEY (`coddindc`),
  KEY `codindc` (`codindc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_indice`
-- Table structure for table `usu_bots`
--

DROP TABLE IF EXISTS `usu_bots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_bots` (
  `codusub` char(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codbta` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codusub`),
  KEY `codusu` (`codusu`),
  KEY `codbta` (`codbta`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_bots`
-- Table structure for table `movimentos_hist`
--

DROP TABLE IF EXISTS `movimentos_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentos_hist` (
  `codmovex` varchar(10) NOT NULL COMMENT 'Chave primária',
  `codmvp` varchar(10) NOT NULL COMMENT 'Codigo da movimentos_pat',
  `codlic` varchar(10) NOT NULL COMMENT 'Codigo da logs_iclass',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de Início do Serviço',
  `quantidade` decimal(10,2) NOT NULL COMMENT 'Quantidade movimentada',
  `codmvp_origem` char(10) NOT NULL DEFAULT '' COMMENT 'Campo para informar o codmvp de origem do movimento',
  PRIMARY KEY (`codmovex`),
  KEY `codmvp` (`codmvp`),
  KEY `codlic` (`codlic`),
  KEY `quantidade` (`quantidade`),
  KEY `codmvp_origem` (`codmvp_origem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos_hist`
-- Table structure for table `tipo_grafico_ind`
--

DROP TABLE IF EXISTS `tipo_grafico_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_grafico_ind` (
  `codtgi` varchar(10) NOT NULL,
  `descri_tgi` varchar(50) NOT NULL,
  `codigo_desk` varchar(11) NOT NULL,
  `codigo_fc` varchar(11) NOT NULL,
  `codigo_mobile` varchar(255) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `tipo` char(2) NOT NULL,
  PRIMARY KEY (`codtgi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_grafico_ind`
-- Table structure for table `eventos_comissionados`
--

DROP TABLE IF EXISTS `eventos_comissionados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventos_comissionados` (
  `codecs` varchar(10) NOT NULL,
  `codtcs` varchar(10) NOT NULL,
  `codusc` varchar(10) NOT NULL,
  `valor_evento` float(8,2) NOT NULL,
  `porcentagem_evento` float(5,2) NOT NULL,
  PRIMARY KEY (`codecs`),
  KEY `codtcs` (`codtcs`),
  KEY `codusc` (`codusc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_comissionados`
-- Table structure for table `elementos_mapa_rede`
--

DROP TABLE IF EXISTS `elementos_mapa_rede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elementos_mapa_rede` (
  `codemr` varchar(10) NOT NULL,
  `codtemr` varchar(10) NOT NULL,
  `codimr` varchar(15) NOT NULL,
  `codgemr` varchar(10) NOT NULL,
  `descri_emr` varchar(50) NOT NULL,
  `titulo` varchar(20) NOT NULL,
  `classe_click_geral` varchar(30) NOT NULL,
  `classe_click_elemento` varchar(30) NOT NULL,
  `form_dblciclk` varchar(30) NOT NULL,
  `form_add` varchar(30) NOT NULL,
  `fonte_caption` varchar(30) NOT NULL,
  `cor` varchar(11) NOT NULL,
  `tool_tips` varchar(100) NOT NULL,
  `zoom_min` int(2) unsigned NOT NULL,
  `zoom_max` int(2) unsigned NOT NULL,
  `entra_marcado` char(1) NOT NULL,
  `tipo` char(1) NOT NULL,
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `icone` char(1) NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`codemr`),
  KEY `codtetr` (`codtemr`),
  KEY `codgetr` (`codgemr`),
  KEY `codimr` (`codimr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elementos_mapa_rede`
-- Table structure for table `operadoras`
--

DROP TABLE IF EXISTS `operadoras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operadoras` (
  `codope` varchar(10) NOT NULL,
  `nome_ope` varchar(50) NOT NULL,
  `nome_consultor` varchar(30) NOT NULL,
  `fone` varchar(10) NOT NULL,
  `e_mail` varchar(50) DEFAULT '0',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codope`),
  UNIQUE KEY `codope` (`codope`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operadoras`
-- Table structure for table `usu_mov`
--

DROP TABLE IF EXISTS `usu_mov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_mov` (
  `codu_m` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codban` varchar(10) NOT NULL DEFAULT '',
  `ver` char(1) NOT NULL DEFAULT 'N',
  `editar` char(1) NOT NULL DEFAULT 'N',
  `apagar` char(1) NOT NULL DEFAULT 'N',
  `data_ant` char(1) NOT NULL DEFAULT 'N',
  `editar_ant` char(1) NOT NULL DEFAULT 'N',
  `apagar_ant` char(1) NOT NULL DEFAULT 'N',
  `limite_mov` int(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codu_m`),
  KEY `codusu` (`codusu`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_mov`
-- Table structure for table `maparede_condominios`
--

DROP TABLE IF EXISTS `maparede_condominios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maparede_condominios` (
  `codmpcon` varchar(20) NOT NULL DEFAULT '',
  `codcon` int(11) NOT NULL DEFAULT '0',
  `descri_geocon` varchar(120) NOT NULL DEFAULT '',
  `latitude` varchar(20) NOT NULL DEFAULT '',
  `longitude` varchar(20) NOT NULL DEFAULT '',
  `integrator` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codmpcon`),
  KEY `codcon` (`codcon`),
  KEY `maparede_condominios_longitude_IDX` (`longitude`) USING BTREE,
  KEY `maparede_condominios_latitude_IDX` (`latitude`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maparede_condominios`
-- Table structure for table `ocorrencias_email`
--

DROP TABLE IF EXISTS `ocorrencias_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocorrencias_email` (
  `codocoe` varchar(10) NOT NULL,
  `codeem` varchar(10) DEFAULT NULL,
  `codoco` varchar(10) DEFAULT NULL,
  `codvis` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codocoe`),
  KEY `codoco` (`codoco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocorrencias_email`
-- Table structure for table `faturamentos`
--

DROP TABLE IF EXISTS `faturamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturamentos` (
  `codftm` varchar(10) NOT NULL DEFAULT '',
  `codvenc` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `p_desde_a` date NOT NULL DEFAULT '0000-00-00',
  `p_ate_a` date NOT NULL DEFAULT '0000-00-00',
  `p_desde` date NOT NULL DEFAULT '0000-00-00',
  `p_ate` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`codftm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturamentos`
-- Table structure for table `tarefas_programadas`
--

DROP TABLE IF EXISTS `tarefas_programadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefas_programadas` (
  `codtarp` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codusu` char(2) NOT NULL DEFAULT '',
  `tarefa` char(1) NOT NULL DEFAULT 'S',
  `codser` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `status` char(1) NOT NULL DEFAULT 'P',
  `valor_ser` float(10,2) NOT NULL,
  `codcan` varchar(10) NOT NULL DEFAULT '',
  `carne` char(1) NOT NULL,
  `codest` char(10) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `codcombo` char(10) NOT NULL DEFAULT '',
  `codagrcombo` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtarp`),
  KEY `codsercli` (`codsercli`),
  KEY `status` (`status`),
  KEY `data` (`data`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefas_programadas`
-- Table structure for table `traducao_mensagens`
--

DROP TABLE IF EXISTS `traducao_mensagens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `traducao_mensagens` (
  `codtmt` varchar(10) NOT NULL,
  `codmtel` varchar(10) NOT NULL,
  `codidm` varchar(10) NOT NULL,
  `mensagem` varchar(254) NOT NULL,
  PRIMARY KEY (`codtmt`),
  KEY `codmtel` (`codmtel`),
  KEY `codidm` (`codidm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `traducao_mensagens`
-- Table structure for table `combo`
--

DROP TABLE IF EXISTS `combo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combo` (
  `codcombo` char(10) NOT NULL,
  `descri_combo` varchar(45) NOT NULL,
  `valor_taxa` decimal(13,2) NOT NULL,
  `codsad` char(10) NOT NULL,
  `descri_instalacao` varchar(50) NOT NULL,
  `criar_instalacao` char(1) NOT NULL DEFAULT 'P' COMMENT 'P = criar plano \nE = evento',
  `dias_vencimento_instalacao` int(11) NOT NULL,
  `numero_parcelas_instalacao` int(11) NOT NULL,
  `valor_taxa_adesao` decimal(13,2) NOT NULL,
  `codsad_adesao` char(10) NOT NULL,
  `descri_adesao` varchar(50) NOT NULL,
  `criar_adesao` char(1) NOT NULL DEFAULT 'P' COMMENT 'P = criar plano \nE = evento',
  `dias_vencimento_adesao` int(11) NOT NULL,
  `numero_parcelas_adesao` int(11) NOT NULL,
  PRIMARY KEY (`codcombo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo`
-- Table structure for table `servicos_perg`
--

DROP TABLE IF EXISTS `servicos_perg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_perg` (
  `codsperg` varchar(10) NOT NULL DEFAULT '',
  `codperg` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsperg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_perg`
-- Table structure for table `logs_comandos`
--

DROP TABLE IF EXISTS `logs_comandos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_comandos` (
  `codlgc` varchar(10) NOT NULL DEFAULT '',
  `codlint` varchar(10) NOT NULL,
  `codcom` int(4) unsigned NOT NULL DEFAULT '0',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `data` datetime NOT NULL,
  `comando` mediumtext NOT NULL,
  `resposta` mediumtext NOT NULL,
  `log_inter` mediumtext NOT NULL,
  PRIMARY KEY (`codlgc`),
  KEY `codlint` (`codlint`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_comandos`
-- Table structure for table `banco_conf_recibo`
--

DROP TABLE IF EXISTS `banco_conf_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banco_conf_recibo` (
  `bancrec` char(10) NOT NULL,
  `codban` char(10) NOT NULL DEFAULT '',
  `pg_dinheiro` char(1) NOT NULL DEFAULT 'S',
  `pg_debito` char(1) NOT NULL DEFAULT 'S',
  `pg_credito` char(1) NOT NULL DEFAULT 'S',
  `pg_cheque` char(1) NOT NULL DEFAULT 'S',
  `permite_recibo` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`bancrec`),
  KEY `codban` (`codban`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banco_conf_recibo`
-- Table structure for table `classificacao_cli`
--

DROP TABLE IF EXISTS `classificacao_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classificacao_cli` (
  `codccli` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codtclc` varchar(10) NOT NULL DEFAULT '',
  `codoclc` varchar(10) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codccli`),
  KEY `codcli` (`codcli`),
  KEY `codtclc` (`codtclc`),
  KEY `codoclc` (`codoclc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classificacao_cli`
-- Table structure for table `combo_comercial_servicos`
--

DROP TABLE IF EXISTS `combo_comercial_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combo_comercial_servicos` (
  `codcomserv` char(10) NOT NULL,
  `codcombocomercial` char(10) NOT NULL,
  `codser` char(10) NOT NULL,
  `obrigatorio` char(1) NOT NULL,
  PRIMARY KEY (`codcomserv`),
  KEY `codcomserv` (`codcomserv`,`codcombocomercial`,`codser`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo_comercial_servicos`
-- Table structure for table `dici_tipo_atendimento`
--

DROP TABLE IF EXISTS `dici_tipo_atendimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dici_tipo_atendimento` (
  `coddicita` char(10) NOT NULL,
  `descricao` varchar(50) DEFAULT NULL,
  `ativo` char(1) DEFAULT 'S',
  PRIMARY KEY (`coddicita`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dici_tipo_atendimento`
-- Table structure for table `departamento`
--

DROP TABLE IF EXISTS `departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departamento` (
  `coddep` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `nome_dep` varchar(20) NOT NULL DEFAULT '',
  `padrao` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`coddep`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamento`
-- Table structure for table `tipo_troca_status`
--

DROP TABLE IF EXISTS `tipo_troca_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_troca_status` (
  `codextra` varchar(10) NOT NULL,
  `descri_extra` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codextra`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_troca_status`
-- Table structure for table `talkall_att`
--

DROP TABLE IF EXISTS `talkall_att`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `talkall_att` (
  `codtaa` char(10) NOT NULL DEFAULT '',
  `codtac` char(10) NOT NULL DEFAULT '',
  `codoco` char(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codco_cl` char(10) NOT NULL DEFAULT '',
  `codocop` char(10) NOT NULL DEFAULT '',
  `data_hora_ini` datetime DEFAULT NULL,
  `data_hora_fim` datetime DEFAULT NULL,
  `chat` mediumtext,
  `status` char(1) DEFAULT '',
  PRIMARY KEY (`codtaa`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `talkall_att`
-- Table structure for table `grupo_comandos_ass`
--

DROP TABLE IF EXISTS `grupo_comandos_ass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_comandos_ass` (
  `codgass` varchar(10) NOT NULL,
  `codsca` varchar(10) NOT NULL,
  `acao` char(1) NOT NULL,
  `data_cad` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `referencia` varchar(100) NOT NULL,
  PRIMARY KEY (`codgass`),
  KEY `codsca` (`codsca`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_comandos_ass`
-- Table structure for table `enlaces_bkp`
--

DROP TABLE IF EXISTS `enlaces_bkp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enlaces_bkp` (
  `codenl` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `tipo_enlace` varchar(5) NOT NULL DEFAULT '',
  `nome_res` varchar(30) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `modelo_r_b` int(2) unsigned NOT NULL DEFAULT '0',
  `mac_b` varchar(17) NOT NULL DEFAULT '',
  `serial_b` varchar(15) NOT NULL DEFAULT '',
  `frecuencia_b` decimal(8,2) NOT NULL DEFAULT '0.00',
  `tipo_r_b` int(1) unsigned NOT NULL DEFAULT '0',
  `amp_b` int(4) unsigned NOT NULL DEFAULT '0',
  `cumprimento_b` decimal(5,2) NOT NULL DEFAULT '0.00',
  `modelo_c_b` int(2) unsigned NOT NULL DEFAULT '0',
  `conectores_b` int(2) unsigned NOT NULL DEFAULT '0',
  `centelhador_b` char(1) NOT NULL DEFAULT '',
  `modelo_a_b` int(2) unsigned NOT NULL DEFAULT '0',
  `modelo_r_e` int(2) unsigned NOT NULL DEFAULT '0',
  `mac_e` varchar(17) NOT NULL DEFAULT '',
  `serial_e` varchar(15) NOT NULL DEFAULT '',
  `frecuencia_e` decimal(8,2) NOT NULL DEFAULT '0.00',
  `tipo_r_e` int(1) unsigned NOT NULL DEFAULT '0',
  `amp_e` int(4) unsigned NOT NULL DEFAULT '0',
  `cumprimento_e` decimal(5,2) NOT NULL DEFAULT '0.00',
  `modelo_c_e` int(2) unsigned NOT NULL DEFAULT '0',
  `conectores_e` int(2) unsigned NOT NULL DEFAULT '0',
  `centelhador_e` char(1) NOT NULL DEFAULT '',
  `modelo_a_e` int(2) unsigned NOT NULL DEFAULT '0',
  `lat_b` decimal(6,2) NOT NULL DEFAULT '0.00',
  `lon_b` decimal(6,2) NOT NULL DEFAULT '0.00',
  `alt_b` decimal(6,2) NOT NULL DEFAULT '0.00',
  `distancia` decimal(5,2) NOT NULL DEFAULT '0.00',
  `lat_e` decimal(6,2) NOT NULL DEFAULT '0.00',
  `lon_e` decimal(6,2) NOT NULL DEFAULT '0.00',
  `alt_e` decimal(5,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codenl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enlaces_bkp`
-- Table structure for table `det_exec_acao_ges`
--

DROP TABLE IF EXISTS `det_exec_acao_ges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_exec_acao_ges` (
  `coddeag` varchar(10) NOT NULL,
  `codeag` varchar(10) NOT NULL,
  `valor_codigo` varchar(10) NOT NULL,
  `campo` varchar(50) NOT NULL,
  `valor_ant` varchar(10) NOT NULL,
  `valor_novo` varchar(10) NOT NULL,
  PRIMARY KEY (`coddeag`),
  KEY `codeag` (`codeag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_exec_acao_ges`
-- Table structure for table `regras_cobrancas`
--

DROP TABLE IF EXISTS `regras_cobrancas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_cobrancas` (
  `codrcob` varchar(10) NOT NULL,
  `descri_rsus` varchar(100) NOT NULL,
  `geral` char(1) NOT NULL,
  `prioridade` int(2) unsigned NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `tempo_lig` int(3) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codrcob`),
  KEY `ativo` (`ativo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_cobrancas`
-- Table structure for table `conf_b_email`
--

DROP TABLE IF EXISTS `conf_b_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_b_email` (
  `codcbe` varchar(10) NOT NULL DEFAULT '',
  `codcst` varchar(10) DEFAULT NULL,
  `server` varchar(50) NOT NULL DEFAULT '',
  `sender` varchar(50) NOT NULL DEFAULT '',
  `e_mail_sender` varchar(50) NOT NULL DEFAULT '',
  `password_sender` varchar(50) NOT NULL DEFAULT '',
  `comcopia` varchar(50) NOT NULL,
  `assunto` varchar(100) NOT NULL DEFAULT '',
  `tipo_conf` char(1) NOT NULL DEFAULT '',
  `conteudo_mail` text NOT NULL,
  PRIMARY KEY (`codcbe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_b_email`
-- Table structure for table `tipo_integracao_servidor`
--

DROP TABLE IF EXISTS `tipo_integracao_servidor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_integracao_servidor` (
  `codintserv` char(10) NOT NULL,
  `tipo_integracao` char(10) NOT NULL,
  `servico` char(10) NOT NULL,
  PRIMARY KEY (`codintserv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_integracao_servidor`
-- Table structure for table `tipo_resultado_lig`
--

DROP TABLE IF EXISTS `tipo_resultado_lig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_resultado_lig` (
  `idresultado` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `codocop` varchar(10) NOT NULL,
  `descri_resultado` varchar(50) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`idresultado`)
) ENGINE=MyISAM AUTO_INCREMENT=823 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_resultado_lig`
-- Table structure for table `log_est`
--

DROP TABLE IF EXISTS `log_est`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_est` (
  `codlogest` int(11) NOT NULL AUTO_INCREMENT,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_est` varchar(15) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codesta` char(10) NOT NULL,
  `nome_estacao` varchar(45) DEFAULT NULL,
  `log_estcol` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`codlogest`),
  KEY `codesta` (`codesta`),
  KEY `ip_esta` (`ip_est`),
  KEY `data_hora` (`data_hora`)
) ENGINE=InnoDB AUTO_INCREMENT=3290 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_est`
-- Table structure for table `projeto_ords`
--

DROP TABLE IF EXISTS `projeto_ords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projeto_ords` (
  `codordsprj` char(10) NOT NULL DEFAULT '',
  `codprj` char(10) NOT NULL DEFAULT '',
  `codords` char(10) NOT NULL DEFAULT '',
  `codigo_externo` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codordsprj`),
  KEY `codoco` (`codords`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_ords`
-- Table structure for table `status_eqr`
--

DROP TABLE IF EXISTS `status_eqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_eqr` (
  `codste` varchar(10) NOT NULL DEFAULT '',
  `descri_ste` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`codste`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_eqr`
-- Table structure for table `login_bd`
--

DROP TABLE IF EXISTS `login_bd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_bd` (
  `codlbd` varchar(10) NOT NULL DEFAULT '',
  `codbd` varchar(10) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `host` varchar(15) NOT NULL DEFAULT '',
  `p_select` char(1) NOT NULL DEFAULT 'N',
  `p_insert` char(1) NOT NULL DEFAULT 'N',
  `p_update` char(1) NOT NULL DEFAULT 'N',
  `p_delete` char(1) NOT NULL DEFAULT 'N',
  `p_create` char(1) NOT NULL DEFAULT 'N',
  `p_drop` char(1) NOT NULL DEFAULT 'N',
  `p_alter` char(1) NOT NULL DEFAULT 'N',
  `p_index` char(1) NOT NULL DEFAULT 'N',
  `p_grant` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codlbd`),
  KEY `codbd` (`codbd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_bd`
-- Table structure for table `planejamento_fin`
--

DROP TABLE IF EXISTS `planejamento_fin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `planejamento_fin` (
  `codplafin` char(10) NOT NULL,
  `periodo_ini_ano` char(4) NOT NULL,
  `periodo_ini_mes` char(2) NOT NULL,
  `periodo_fim_ano` char(4) NOT NULL,
  `periodo_fim_mes` char(2) NOT NULL,
  `status_plan` char(1) NOT NULL DEFAULT 'A',
  `descri_plan` varchar(45) NOT NULL,
  `codusu` char(2) NOT NULL,
  PRIMARY KEY (`codplafin`),
  KEY `periodo_ini_ano` (`periodo_ini_ano`),
  KEY `periodo_fim_ano` (`periodo_fim_ano`),
  KEY `status_plan` (`status_plan`),
  KEY `periodo_fim_mes` (`periodo_fim_mes`),
  KEY `periodo_ini_mes` (`periodo_ini_mes`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planejamento_fin`
-- Table structure for table `unidades_tempo`
--

DROP TABLE IF EXISTS `unidades_tempo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades_tempo` (
  `codutmp` varchar(10) NOT NULL DEFAULT '',
  `descri_utmp` varchar(50) NOT NULL DEFAULT '0',
  `abreviado` char(4) NOT NULL DEFAULT '',
  `formula` varchar(100) NOT NULL DEFAULT '',
  `ordem` int(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codutmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_tempo`
-- Table structure for table `keycard`
--

DROP TABLE IF EXISTS `keycard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keycard` (
  `codkcd` varchar(10) NOT NULL,
  `codcdf` varchar(10) NOT NULL,
  `nro_kcd` varchar(30) NOT NULL,
  `chave` varchar(30) NOT NULL,
  PRIMARY KEY (`codkcd`),
  KEY `codcdf` (`codcdf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keycard`
-- Table structure for table `reducao_impostos`
--

DROP TABLE IF EXISTS `reducao_impostos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reducao_impostos` (
  `codrimp` varchar(10) NOT NULL DEFAULT '',
  `estado` char(2) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codtser` varchar(10) NOT NULL,
  `codtred` varchar(10) NOT NULL,
  `data_ini` date NOT NULL,
  `data_fim` date NOT NULL,
  `porc_baseicms` float(8,2) NOT NULL,
  `porc_icms` float(8,2) NOT NULL,
  `porc_baseiss` float(8,2) NOT NULL,
  `porc_iss` float(8,2) NOT NULL,
  `reducao` char(1) NOT NULL DEFAULT 'S',
  `local_reducao` char(1) NOT NULL DEFAULT 'I',
  PRIMARY KEY (`codrimp`),
  KEY `estado` (`estado`),
  KEY `codemp` (`codemp`),
  KEY `codser` (`codser`),
  KEY `codtser` (`codtser`),
  KEY `codtred` (`codtred`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reducao_impostos`
-- Table structure for table `banco_dados`
--

DROP TABLE IF EXISTS `banco_dados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banco_dados` (
  `codbd` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `coddom` varchar(10) NOT NULL DEFAULT '',
  `codtbd` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `nome_bd` varchar(15) NOT NULL DEFAULT '',
  `quota_bd` int(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codbd`),
  KEY `coddom` (`coddom`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banco_dados`
-- Table structure for table `patrimonio`
--

DROP TABLE IF EXISTS `patrimonio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patrimonio` (
  `codpat` varchar(10) NOT NULL DEFAULT '',
  `codprod` varchar(10) NOT NULL DEFAULT '',
  `imobilizado` char(1) NOT NULL DEFAULT 'S',
  `numero_pat` varchar(20) NOT NULL DEFAULT '0',
  `mac` varchar(17) NOT NULL DEFAULT '',
  `serial_number` varchar(35) NOT NULL,
  `serial_number2` varchar(35) NOT NULL DEFAULT '',
  PRIMARY KEY (`codpat`),
  KEY `codprod` (`codprod`),
  KEY `imobilizado` (`imobilizado`),
  KEY `numero_pat` (`numero_pat`),
  KEY `serial_number` (`serial_number`),
  KEY `mac` (`mac`),
  KEY `serial_number2` (`serial_number2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patrimonio`
-- Table structure for table `tabelas`
--

DROP TABLE IF EXISTS `tabelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabelas` (
  `codtab` varchar(10) NOT NULL DEFAULT '',
  `tabela` varchar(50) NOT NULL DEFAULT '',
  `codrcb` varchar(10) NOT NULL,
  `nome_tab` varchar(50) NOT NULL DEFAULT '',
  `visivel` char(1) NOT NULL DEFAULT 'N',
  `campo_codigo` varchar(30) NOT NULL,
  `campo_desc` varchar(30) NOT NULL,
  `modulo` varchar(20) NOT NULL,
  `formulario` varchar(50) NOT NULL,
  `campo_parametro` varchar(20) NOT NULL,
  `icone_gmaps` varchar(200) NOT NULL,
  `form_gmaps` varchar(100) NOT NULL,
  `obs` mediumtext NOT NULL,
  `consulta_gmaps` mediumtext NOT NULL,
  PRIMARY KEY (`codtab`),
  KEY `tabela` (`tabela`),
  KEY `codrcb` (`codrcb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelas`
-- Table structure for table `configuracao_parcelamentos`
--

DROP TABLE IF EXISTS `configuracao_parcelamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuracao_parcelamentos` (
  `codcfp` varchar(10) NOT NULL DEFAULT '',
  `multa` float(5,2) NOT NULL DEFAULT '0.00',
  `juros` float(5,2) NOT NULL DEFAULT '0.00',
  `quant_win` int(2) unsigned NOT NULL DEFAULT '0',
  `quant_web` int(2) unsigned NOT NULL DEFAULT '0',
  `dias_web` int(2) unsigned NOT NULL DEFAULT '0',
  `escolhe_cob` char(1) NOT NULL DEFAULT 'S',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcfp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracao_parcelamentos`
-- Table structure for table `vendedores`
--

DROP TABLE IF EXISTS `vendedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendedores` (
  `codven` varchar(10) NOT NULL DEFAULT '',
  `nome_ven` varchar(50) NOT NULL DEFAULT '',
  `endereco` varchar(50) NOT NULL DEFAULT '',
  `bairro` varchar(25) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `fone` int(8) unsigned NOT NULL DEFAULT '0',
  `fax` int(8) unsigned NOT NULL DEFAULT '0',
  `celular` varchar(13) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  `aniversario` varchar(5) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  PRIMARY KEY (`codven`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendedores`
-- Table structure for table `envio_emails`
--

DROP TABLE IF EXISTS `envio_emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `envio_emails` (
  `codeem` varchar(10) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora` varchar(5) DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codpros` varchar(10) NOT NULL,
  `enviado` char(1) NOT NULL DEFAULT 'S',
  `from_email` varchar(100) NOT NULL DEFAULT '',
  `from_alias` varchar(100) NOT NULL DEFAULT '',
  `for_email` text NOT NULL,
  `for_email_co` text NOT NULL,
  `subject` varchar(254) NOT NULL DEFAULT '',
  `codcbe` char(10) NOT NULL,
  `codpint` char(10) NOT NULL,
  `message` mediumtext NOT NULL,
  PRIMARY KEY (`codeem`),
  KEY `data` (`data`),
  KEY `codcli` (`codcli`),
  KEY `codpros` (`codpros`),
  KEY `codusu` (`codusu`),
  KEY `enviado` (`enviado`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `envio_emails`
-- Table structure for table `origem_comercial_externo`
--

DROP TABLE IF EXISTS `origem_comercial_externo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `origem_comercial_externo` (
  `codoce` varchar(10) NOT NULL,
  `codtocm` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL,
  `nome_oce` varchar(50) NOT NULL,
  PRIMARY KEY (`codoce`),
  KEY `codtocm` (`codtocm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `origem_comercial_externo`
-- Table structure for table `status_serasa`
--

DROP TABLE IF EXISTS `status_serasa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_serasa` (
  `codstse` varchar(10) NOT NULL,
  `permite_recibo` char(1) NOT NULL DEFAULT 'S',
  `descri_statserasa` varchar(30) NOT NULL,
  PRIMARY KEY (`codstse`),
  KEY `permite_recibo` (`permite_recibo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_serasa`
-- Table structure for table `registro_tributacao_uf`
--

DROP TABLE IF EXISTS `registro_tributacao_uf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registro_tributacao_uf` (
  `codrtribuf` char(10) NOT NULL COMMENT 'Chave Primária da Tabela registro_tributacao_uf.',
  `codrtribdet` char(10) NOT NULL COMMENT 'Código do Registro de Tributação Detalhado.',
  `estado` char(2) NOT NULL COMMENT 'Unidade Federativa.',
  PRIMARY KEY (`codrtribuf`),
  KEY `codrtribdet` (`codrtribdet`),
  KEY `estado` (`estado`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_tributacao_uf`
-- Table structure for table `tipo_canais`
--

DROP TABLE IF EXISTS `tipo_canais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_canais` (
  `codtcnl` varchar(10) NOT NULL,
  `descri_tcnl` varchar(50) NOT NULL,
  `hd` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codtcnl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_canais`
-- Table structure for table `grupo_campanha_lig`
--

DROP TABLE IF EXISTS `grupo_campanha_lig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_campanha_lig` (
  `codgcl` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `codcla` varchar(10) NOT NULL,
  `descri_gcl` varchar(50) NOT NULL,
  `valores` mediumtext NOT NULL,
  PRIMARY KEY (`codgcl`),
  KEY `codtab` (`codtab`),
  KEY `codcla` (`codcla`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_campanha_lig`
-- Table structure for table `componentes_telas`
--

DROP TABLE IF EXISTS `componentes_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `componentes_telas` (
  `codctl` varchar(10) NOT NULL,
  `codtel` varchar(10) NOT NULL,
  `codtct` varchar(10) NOT NULL,
  `codctl_p` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `parent` varchar(50) NOT NULL,
  `nome_ctl` varchar(50) NOT NULL,
  `ordem` int(3) unsigned NOT NULL,
  `caption` varchar(50) NOT NULL,
  `tooltips` varchar(100) NOT NULL,
  `value` varchar(254) NOT NULL,
  PRIMARY KEY (`codctl`),
  KEY `codtel` (`codtel`),
  KEY `codtct` (`codtct`),
  KEY `codctl_p` (`codctl_p`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `componentes_telas`
-- Table structure for table `servicos_cli_fec`
--

DROP TABLE IF EXISTS `servicos_cli_fec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_fec` (
  `competencia` char(4) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT 'E',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codest` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(5) unsigned NOT NULL DEFAULT '0',
  `valor_plano` float(8,2) NOT NULL DEFAULT '0.00',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_sus` date NOT NULL DEFAULT '0000-00-00',
  `data_can` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`competencia`,`codsercli`),
  KEY `competencia` (`competencia`),
  KEY `codsercli` (`codsercli`),
  KEY `acao` (`acao`),
  KEY `codcli` (`codcli`),
  KEY `data_lan` (`data_lan`),
  KEY `codest` (`codest`),
  KEY `data_sus` (`data_sus`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_fec`
-- Table structure for table `tipo_classificacao_assinante`
--

DROP TABLE IF EXISTS `tipo_classificacao_assinante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_classificacao_assinante` (
  `codtass` char(1) NOT NULL,
  `descri_tass` varchar(100) NOT NULL,
  PRIMARY KEY (`codtass`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_classificacao_assinante`
-- Table structure for table `mensagem_padrao_telas`
--

DROP TABLE IF EXISTS `mensagem_padrao_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mensagem_padrao_telas` (
  `codmpt` varchar(10) NOT NULL,
  `mensagem` varchar(254) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codmpt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensagem_padrao_telas`
-- Table structure for table `mov_items`
--

DROP TABLE IF EXISTS `mov_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mov_items` (
  `codmovi` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codeb` varchar(10) NOT NULL DEFAULT '',
  `numero_nf` varchar(10) NOT NULL DEFAULT '',
  `tipo_movi` char(1) NOT NULL DEFAULT '',
  `histo_movi` varchar(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`codmovi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mov_items`
-- Table structure for table `regra_ser_serasa`
--

DROP TABLE IF EXISTS `regra_ser_serasa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regra_ser_serasa` (
  `codregsese` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `serasa` char(1) NOT NULL,
  PRIMARY KEY (`codregsese`),
  KEY `codser` (`codser`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regra_ser_serasa`
-- Table structure for table `usu_regra_atendimento`
--

DROP TABLE IF EXISTS `usu_regra_atendimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_regra_atendimento` (
  `coduregat` varchar(10) NOT NULL,
  `codusu` varchar(2) NOT NULL,
  `codregatend` varchar(10) NOT NULL,
  PRIMARY KEY (`coduregat`),
  KEY `codusu` (`codusu`),
  KEY `codregatend` (`codregatend`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_regra_atendimento`
-- Table structure for table `necessidades_mercado`
--

DROP TABLE IF EXISTS `necessidades_mercado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `necessidades_mercado` (
  `codnm` varchar(10) NOT NULL,
  `codgcli` varchar(10) NOT NULL,
  `descri_nm` varchar(100) NOT NULL,
  `titulo_nm` varchar(20) NOT NULL,
  `ativo` char(1) NOT NULL,
  PRIMARY KEY (`codnm`),
  KEY `codgcli` (`codgcli`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `necessidades_mercado`
-- Table structure for table `padrao_comandos`
--

DROP TABLE IF EXISTS `padrao_comandos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `padrao_comandos` (
  `codpcom` varchar(10) NOT NULL DEFAULT '',
  `codtcom` char(1) NOT NULL DEFAULT '',
  `codaco` char(1) NOT NULL DEFAULT '',
  `codgcom` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codpcom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `padrao_comandos`
-- Table structure for table `oco_padrao`
--

DROP TABLE IF EXISTS `oco_padrao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oco_padrao` (
  `codocop` varchar(10) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `codpai` varchar(10) NOT NULL,
  `coddep` varchar(10) NOT NULL DEFAULT '',
  `codstc_p` varchar(10) NOT NULL,
  `nome_ocop` varchar(50) NOT NULL DEFAULT '',
  `codusu_d` char(2) NOT NULL,
  `codcar_d` varchar(10) NOT NULL,
  `zoom` int(10) unsigned NOT NULL,
  `tipo_oco` char(1) NOT NULL DEFAULT 'C',
  `vinculado` char(1) NOT NULL DEFAULT 'N',
  `qtde_horas_vin` int(2) unsigned NOT NULL,
  `alertar` char(1) NOT NULL DEFAULT 'N',
  `codutmp` varchar(10) NOT NULL,
  `valor_prazo` int(3) unsigned NOT NULL,
  `tempo_analise` int(4) unsigned NOT NULL,
  `tempo_resolucao` int(4) unsigned NOT NULL,
  `dias_reincidencia` int(6) unsigned NOT NULL,
  `prioridade` char(1) NOT NULL DEFAULT 'M',
  `tipo_ocop` char(1) NOT NULL,
  `permite_fechar_atend` char(1) DEFAULT 'N',
  `oco_criar_email` char(1) NOT NULL DEFAULT 'N',
  `oco_fechar_email` char(1) NOT NULL DEFAULT 'N',
  `codcbe_criar` char(10) NOT NULL,
  `codcbe_fechar` char(10) NOT NULL,
  `oco_criar_sms` char(1) NOT NULL DEFAULT 'N',
  `oco_fechar_sms` char(1) NOT NULL DEFAULT 'N',
  `codrsms_criar` char(10) NOT NULL,
  `codrsms_fechar` char(10) NOT NULL,
  PRIMARY KEY (`codocop`),
  KEY `codpai` (`codpai`),
  KEY `ativo` (`ativo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oco_padrao`
-- Table structure for table `sped_tipo_class`
--

DROP TABLE IF EXISTS `sped_tipo_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sped_tipo_class` (
  `codclas` char(2) NOT NULL,
  `codtass` char(1) NOT NULL,
  `descri_tass` varchar(100) NOT NULL,
  `valor_ini` float(8,2) NOT NULL,
  `valor_fim` float(8,2) NOT NULL,
  PRIMARY KEY (`codclas`),
  KEY `codtass` (`codtass`),
  KEY `vl_ini` (`valor_ini`),
  KEY `vl_fin` (`valor_fim`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sped_tipo_class`
-- Table structure for table `tipo_ata`
--

DROP TABLE IF EXISTS `tipo_ata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_ata` (
  `codtata` varchar(10) NOT NULL DEFAULT '',
  `descri_tata` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtata`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_ata`
-- Table structure for table `plataforma_pagamento`
--

DROP TABLE IF EXISTS `plataforma_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plataforma_pagamento` (
  `codtplat` char(10) NOT NULL,
  `descri_plataforma` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`codtplat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plataforma_pagamento`
-- Table structure for table `pool_ip_nova`
--

DROP TABLE IF EXISTS `pool_ip_nova`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_ip_nova` (
  `codpool` varchar(10) NOT NULL DEFAULT '',
  `codrad` varchar(10) NOT NULL DEFAULT '',
  `nome_pool` varchar(50) NOT NULL DEFAULT '',
  `network_address` varchar(31) NOT NULL DEFAULT '',
  `next_codpool` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codpool`),
  KEY `codrad` (`codrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pool_ip_nova`
-- Table structure for table `variaveis`
--

DROP TABLE IF EXISTS `variaveis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variaveis` (
  `codvar` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `descri_var` varchar(50) NOT NULL DEFAULT '',
  `valor` varchar(15) NOT NULL,
  `editavel` char(1) NOT NULL DEFAULT 'N',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codvar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variaveis`
-- Table structure for table `tipo_evento_faturamento`
--

DROP TABLE IF EXISTS `tipo_evento_faturamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_evento_faturamento` (
  `codtef` varchar(10) NOT NULL,
  `descr_tef` varchar(100) NOT NULL,
  `tipo_evento` char(1) NOT NULL DEFAULT 'N',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtef`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_evento_faturamento`
-- Table structure for table `tipo_os_router`
--

DROP TABLE IF EXISTS `tipo_os_router`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_os_router` (
  `codosr` varchar(10) NOT NULL DEFAULT '',
  `descri_osr` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codosr`),
  UNIQUE KEY `codosr` (`codosr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_os_router`
-- Table structure for table `funil_etapas`
--

DROP TABLE IF EXISTS `funil_etapas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `funil_etapas` (
  `id_etapa` int(11) NOT NULL AUTO_INCREMENT,
  `id_funil` int(11) NOT NULL,
  `nome_etapa` varchar(45) NOT NULL DEFAULT '',
  `ordenacao` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_etapa`),
  KEY `id_funil` (`id_funil`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funil_etapas`
-- Table structure for table `ordemcompra`
--

DROP TABLE IF EXISTS `ordemcompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordemcompra` (
  `codordcomp` varchar(10) NOT NULL COMMENT 'Chave Ordem de compra',
  `numero` bigint(12) NOT NULL AUTO_INCREMENT,
  `codfor` varchar(10) NOT NULL,
  `justificativa` varchar(50) NOT NULL,
  `locacao` varchar(50) NOT NULL,
  `previsaoentrega` date DEFAULT NULL,
  `condicaopagto` varchar(50) NOT NULL,
  `vlrtotal` double(15,2) NOT NULL,
  `fretemod` int(1) NOT NULL,
  `fretevlr` double(5,2) NOT NULL,
  `observacoes` varchar(100) NOT NULL,
  `geracaodata` datetime NOT NULL,
  `geracaousuario` varchar(20) NOT NULL,
  `autorizacaodata` datetime DEFAULT NULL,
  `autorizacaousuario` varchar(20) NOT NULL,
  `permiteexclusao` char(1) NOT NULL DEFAULT 'S',
  `situacao` char(1) NOT NULL,
  PRIMARY KEY (`codordcomp`),
  KEY `Fornecedor` (`codfor`),
  KEY `Numero` (`numero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordemcompra`
-- Table structure for table `debito_conta`
--

DROP TABLE IF EXISTS `debito_conta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `debito_conta` (
  `coddeb` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codedeb` varchar(10) NOT NULL DEFAULT '',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `nome_titular` varchar(50) NOT NULL,
  `cpf_titular` varchar(18) NOT NULL,
  `codtcta` varchar(10) NOT NULL,
  `agencia` varchar(4) NOT NULL DEFAULT '',
  `dig_agencia` char(1) NOT NULL DEFAULT '',
  `conta_cte` varchar(14) NOT NULL DEFAULT '',
  `dig_cta` char(1) NOT NULL DEFAULT '',
  `razao_conta` varchar(30) NOT NULL DEFAULT '' COMMENT '||PaymentDebitAccount BankRegistry number',
  `fddd` char(2) NOT NULL DEFAULT '',
  `fone` varchar(8) NOT NULL DEFAULT '',
  `fcont` varchar(10) NOT NULL DEFAULT '',
  `nro_cartao` varchar(16) NOT NULL DEFAULT '',
  `validade` varchar(4) NOT NULL DEFAULT '',
  `digito_seg` char(3) NOT NULL DEFAULT '',
  `codco_cl` varchar(10) NOT NULL,
  `tipo_car` char(1) NOT NULL,
  PRIMARY KEY (`coddeb`),
  KEY `codcli` (`codcli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `debito_conta`
-- Table structure for table `franquia_sc_voz`
--

DROP TABLE IF EXISTS `franquia_sc_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `franquia_sc_voz` (
  `codfscv` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codtter` varchar(10) NOT NULL DEFAULT '',
  `descri_fscv` varchar(50) NOT NULL DEFAULT '',
  `codcta` varchar(8) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `minutos_livres` int(9) unsigned NOT NULL DEFAULT '0',
  `valor_adicional` float(10,4) NOT NULL DEFAULT '0.0000',
  `valor_mensal` float(10,2) NOT NULL,
  `data_venc` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codfscv`),
  KEY `codsercli` (`codsercli`),
  KEY `codtter` (`codtter`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `franquia_sc_voz`
-- Table structure for table `regra_desconto`
--

DROP TABLE IF EXISTS `regra_desconto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regra_desconto` (
  `codregradesconto` char(10) NOT NULL,
  `codcombo` char(10) NOT NULL,
  `codgcom` char(10) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `ordem` int(11) NOT NULL DEFAULT '0',
  `valor_desconto` decimal(13,2) NOT NULL,
  `percentual_desconto` decimal(9,5) NOT NULL DEFAULT '0.00000',
  `tipo_atribuicao` char(1) NOT NULL COMMENT 'I = taxa de instalação M = mensalidade\n A = taxa de adesao',
  `periodo_desconto` char(1) NOT NULL DEFAULT '' COMMENT 'Vazio= Sem Conf. / P = Periodo de data',
  `data_ini_desconto` date NOT NULL,
  `data_fim_desconto` date NOT NULL,
  `valor_periodo_ciclo` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codregradesconto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regra_desconto`
-- Table structure for table `servidores_pop_integracoes`
--

DROP TABLE IF EXISTS `servidores_pop_integracoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidores_pop_integracoes` (
  `codservint` char(10) NOT NULL,
  `codservp` char(10) NOT NULL,
  `codintserv` char(10) NOT NULL,
  PRIMARY KEY (`codservint`),
  KEY `codservp` (`codservp`),
  KEY `codintserv` (`codintserv`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidores_pop_integracoes`
-- Table structure for table `teste_velocidade`
--

DROP TABLE IF EXISTS `teste_velocidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teste_velocidade` (
  `codtvel` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `data_ini` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `dias` int(10) unsigned NOT NULL,
  PRIMARY KEY (`codtvel`),
  KEY `codsercli` (`codsercli`),
  KEY `data_ini` (`data_ini`),
  KEY `data_fim` (`data_fim`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teste_velocidade`
-- Table structure for table `log_prov_desc`
--

DROP TABLE IF EXISTS `log_prov_desc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_prov_desc` (
  `codlpd` varchar(10) NOT NULL,
  `codprdc` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `log_execucao` mediumtext NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_prov_desc`
-- Table structure for table `syn_servicos_imp`
--

DROP TABLE IF EXISTS `syn_servicos_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syn_servicos_imp` (
  `codsyimp` bigint(20) NOT NULL AUTO_INCREMENT,
  `codsimp` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `tabela` varchar(20) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  `data_ua` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sincronizado` char(1) NOT NULL DEFAULT 'N',
  `data_sincronismo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `resp_sincronismo` varchar(20) NOT NULL DEFAULT '',
  `data_erro` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tentativa` int(11) NOT NULL DEFAULT '0',
  `log_erro` mediumtext,
  `campos` mediumtext,
  `id_sap` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsyimp`),
  KEY `sincronizado` (`sincronizado`),
  KEY `acao` (`acao`),
  KEY `data_sincronismo` (`data_sincronismo`),
  KEY `codsimp` (`codsimp`),
  KEY `codser` (`codser`),
  KEY `data_ua` (`data_ua`),
  KEY `tabela` (`tabela`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syn_servicos_imp`
-- Table structure for table `produtos_brt`
--

DROP TABLE IF EXISTS `produtos_brt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produtos_brt` (
  `codpbrt` varchar(10) NOT NULL DEFAULT '',
  `descri_pbrt` varchar(50) NOT NULL DEFAULT '',
  `dias_inst` int(3) unsigned NOT NULL DEFAULT '0',
  `comissao_n` decimal(6,3) NOT NULL DEFAULT '0.000',
  `comissao_v` decimal(6,3) NOT NULL DEFAULT '0.000',
  `valor` decimal(7,2) NOT NULL DEFAULT '0.00',
  `obs` text NOT NULL,
  PRIMARY KEY (`codpbrt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos_brt`
-- Table structure for table `contato_cli_per`
--

DROP TABLE IF EXISTS `contato_cli_per`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contato_cli_per` (
  `codccper` char(10) NOT NULL DEFAULT '' COMMENT '||CustomerContactRules ID',
  `codco_cl_p` char(10) NOT NULL DEFAULT '' COMMENT '||ContactCustomer ID',
  `p_insert` char(1) NOT NULL DEFAULT 'N' COMMENT '||CustomerContactRules insert grant',
  `p_delete` char(1) NOT NULL DEFAULT 'N' COMMENT '||CustomerContactRules delete grant',
  `p_update` char(1) NOT NULL DEFAULT 'N' COMMENT '||CustomerContactRules update grant',
  KEY `codccper` (`codccper`),
  KEY `codco_cl_p` (`codco_cl_p`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=CustomerContactRules|Desc=|Grupo=Customer';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contato_cli_per`
-- Table structure for table `pool_ip_radius`
--

DROP TABLE IF EXISTS `pool_ip_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_ip_radius` (
  `codpoolrad` varchar(10) NOT NULL,
  `codpool` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codpoolrad`),
  KEY `codpool` (`codpool`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pool_ip_radius`
-- Table structure for table `pacotes_stb`
--

DROP TABLE IF EXISTS `pacotes_stb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pacotes_stb` (
  `codpcod` varchar(10) NOT NULL,
  `codpsc` varchar(10) NOT NULL,
  `codcdf` varchar(10) NOT NULL,
  `idproduto` int(6) unsigned NOT NULL,
  PRIMARY KEY (`codpcod`),
  KEY `codpsc` (`codpsc`),
  KEY `codcdf` (`codcdf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacotes_stb`
-- Table structure for table `log_inter`
--

DROP TABLE IF EXISTS `log_inter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_inter` (
  `codlint` varchar(10) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codest` varchar(10) NOT NULL DEFAULT '',
  `coddom` varchar(10) NOT NULL DEFAULT '',
  `codextra` varchar(10) NOT NULL,
  `codservp_h` varchar(10) NOT NULL DEFAULT '',
  `codservp_c` varchar(10) NOT NULL DEFAULT '',
  `nro_ip` varchar(15) NOT NULL DEFAULT '',
  `nro_ip_v6` varchar(39) NOT NULL,
  `clase_ipv6` int(6) unsigned NOT NULL,
  `nro_ipv6_sec` varchar(45) NOT NULL,
  `clase_ipv6_sec` int(6) NOT NULL,
  `ip_secundario` varchar(15) NOT NULL,
  `vlan` varchar(30) NOT NULL,
  `vlan_voz` int(6) unsigned NOT NULL,
  `vlan_tv` int(6) unsigned NOT NULL,
  `tipo_conexao` char(1) NOT NULL,
  `nro_regra_fw` int(5) unsigned NOT NULL DEFAULT '0',
  `mac` varchar(18) NOT NULL DEFAULT '',
  `mac2` varchar(18) NOT NULL DEFAULT '',
  `hotspot` char(1) NOT NULL DEFAULT 'N',
  `wpa2` varchar(63) NOT NULL,
  `upload` int(6) unsigned NOT NULL DEFAULT '0',
  `download` int(6) unsigned NOT NULL DEFAULT '0',
  `upload_n` int(6) unsigned NOT NULL DEFAULT '0',
  `download_n` int(6) unsigned NOT NULL DEFAULT '0',
  `clase` int(3) unsigned NOT NULL DEFAULT '0',
  `clase_sec` int(3) unsigned NOT NULL,
  `gateway` varchar(15) NOT NULL DEFAULT '',
  `codpool` varchar(10) NOT NULL,
  `terminal_id` varchar(12) NOT NULL,
  `prefixo` char(13) NOT NULL DEFAULT '',
  `codip` varchar(10) NOT NULL DEFAULT '',
  `codcemail` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(2) unsigned NOT NULL DEFAULT '0',
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codintr` varchar(10) NOT NULL,
  `codonu` varchar(10) NOT NULL,
  `codcdf` varchar(10) NOT NULL,
  `codpsc` varchar(10) NOT NULL,
  `rede` char(1) NOT NULL DEFAULT 'N',
  `ip_publico` char(1) NOT NULL DEFAULT 'N',
  `mac_e_login` char(1) NOT NULL DEFAULT '',
  `submask` varchar(15) NOT NULL DEFAULT '',
  `proxy` char(1) NOT NULL DEFAULT 'S',
  `dhcp` char(1) NOT NULL DEFAULT 'N',
  `login_r` varchar(50) NOT NULL DEFAULT '',
  `login` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL,
  `senha` varchar(50) NOT NULL DEFAULT '',
  `codstl` varchar(10) NOT NULL,
  `dominio` varchar(50) NOT NULL DEFAULT '',
  `quota` int(7) NOT NULL DEFAULT '0',
  `quota_dom` int(7) NOT NULL DEFAULT '0',
  `quota_ftp` int(7) unsigned DEFAULT NULL,
  `forward` longtext,
  `comcopia` char(1) NOT NULL DEFAULT 'S',
  `antivirus` char(1) NOT NULL DEFAULT 'S',
  `antispam` char(1) NOT NULL DEFAULT 'N',
  `central` char(1) NOT NULL,
  `autoresposta` mediumtext NOT NULL,
  `alias` char(1) NOT NULL DEFAULT 'N',
  `status` char(1) NOT NULL DEFAULT '',
  `permisoes` varchar(10) NOT NULL DEFAULT '',
  `nome_bd` varchar(20) NOT NULL DEFAULT '',
  `estatisticas` char(1) NOT NULL DEFAULT '',
  `ip_hosting` varchar(15) NOT NULL DEFAULT '',
  `ip_mail` varchar(15) NOT NULL DEFAULT '',
  `redirecionamento` varchar(50) NOT NULL,
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `nome_cli` varchar(50) NOT NULL,
  `troca_plano` char(1) NOT NULL DEFAULT 'N',
  `cancel` char(1) NOT NULL DEFAULT 'N',
  `pasta` varchar(100) NOT NULL DEFAULT '',
  `pasta_v` varchar(100) NOT NULL DEFAULT '',
  `mensagem_ip` varchar(100) NOT NULL DEFAULT '',
  `suspender` char(1) NOT NULL DEFAULT 'N',
  `habilitar` char(1) NOT NULL DEFAULT 'N',
  `plano_novo` char(1) NOT NULL DEFAULT 'N',
  `tipo_tv` char(1) DEFAULT NULL,
  `codlav` mediumtext,
  `desconectar` char(1) NOT NULL DEFAULT 'N',
  `virtual_number` double NOT NULL DEFAULT '0',
  `credito` decimal(10,2) NOT NULL DEFAULT '0.00',
  `gateway_id` double NOT NULL DEFAULT '0',
  `routeplan_id` double NOT NULL DEFAULT '0',
  `costlist_id` double NOT NULL DEFAULT '0',
  `incoming_prefix` double NOT NULL DEFAULT '0',
  `carrier_id` double NOT NULL DEFAULT '0',
  `codwsale` varchar(10) NOT NULL,
  `login_web` varchar(50) NOT NULL,
  `senha_web` varchar(50) NOT NULL,
  `privacidade` char(1) NOT NULL DEFAULT 'N',
  `acobrar` char(1) NOT NULL DEFAULT 'N',
  `simultaneas` int(4) NOT NULL,
  `serial_number` varchar(30) NOT NULL,
  `codpat` char(10) NOT NULL DEFAULT '',
  `agora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`codlint`),
  KEY `codser` (`codser`),
  KEY `tipo` (`tipo`),
  KEY `acao` (`acao`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_inter`
-- Table structure for table `gadgets`
--

DROP TABLE IF EXISTS `gadgets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gadgets` (
  `codgdg` varchar(10) NOT NULL,
  `tipo_gdg` varchar(1) DEFAULT 'G',
  `codtgraf` varchar(10) DEFAULT '1',
  `qtde_campos` int(3) DEFAULT NULL,
  `nome_gdg` varchar(50) NOT NULL,
  `descri_gdg` varchar(200) NOT NULL,
  `consulta_grafico` mediumtext NOT NULL,
  `consulta_lista` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codgdg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gadgets`
-- Table structure for table `pacotes`
--

DROP TABLE IF EXISTS `pacotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pacotes` (
  `codpac` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `codcas` varchar(10) NOT NULL,
  `descri_pac` varchar(50) NOT NULL,
  `codigo_cas` varchar(50) NOT NULL,
  `valor` float(10,2) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `extra` char(1) NOT NULL DEFAULT 'N',
  `id_produto` varchar(50) NOT NULL,
  `eppv` char(1) NOT NULL DEFAULT 'N',
  `cobra_proporcional` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codpac`),
  KEY `codsad` (`codsad`),
  KEY `codcas` (`codcas`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacotes`
-- Table structure for table `site_survey`
--

DROP TABLE IF EXISTS `site_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_survey` (
  `codssur` varchar(10) NOT NULL DEFAULT '',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(6) unsigned NOT NULL DEFAULT '0',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codtec` varchar(10) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL,
  `codsss` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `numero_ss` int(6) unsigned NOT NULL,
  `falar_com` varchar(50) NOT NULL DEFAULT '',
  `ponto_referencia` varchar(50) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `hora` varchar(5) NOT NULL DEFAULT '',
  `unidade_t` int(1) unsigned NOT NULL DEFAULT '0',
  `data_r` date NOT NULL DEFAULT '0000-00-00',
  `hora_r` varchar(5) NOT NULL DEFAULT '',
  `unidade_t_r` int(1) unsigned NOT NULL DEFAULT '0',
  `comvisada` char(1) NOT NULL DEFAULT 'N',
  `pontos_visada` text NOT NULL,
  `medicao` mediumtext NOT NULL,
  `obs` text NOT NULL,
  PRIMARY KEY (`codssur`),
  KEY `codpros` (`codpros`),
  KEY `codtec` (`codtec`),
  KEY `codcar` (`codcar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='site_survey';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_survey`
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produtos` (
  `codprod` varchar(10) NOT NULL DEFAULT '',
  `codigo` varchar(15) NOT NULL,
  `codunm` varchar(10) NOT NULL,
  `codscat` varchar(10) NOT NULL DEFAULT '',
  `codigo_ncm` varchar(10) NOT NULL,
  `codigo_fiscal` varchar(10) NOT NULL,
  `codigo_cest` varchar(10) NOT NULL,
  `tipoitem` varchar(2) NOT NULL DEFAULT '00',
  `coduprod` varchar(10) NOT NULL,
  `codkit` varchar(10) NOT NULL,
  `descri_prod` varchar(120) NOT NULL,
  `fabricante` varchar(50) NOT NULL DEFAULT '',
  `preco_venda` float(8,2) NOT NULL DEFAULT '0.00',
  `quantidade` int(5) unsigned NOT NULL,
  `qtde_minima` int(5) unsigned NOT NULL,
  `qtde_maxima` int(5) unsigned NOT NULL,
  `lotecompra` double NOT NULL DEFAULT '0',
  `controleunidade` char(1) NOT NULL DEFAULT 'N',
  `basedesconto` char(1) NOT NULL DEFAULT 'N',
  `status` varchar(30) NOT NULL DEFAULT '',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `imobilizado` char(1) NOT NULL DEFAULT 'S',
  `consumo` char(1) NOT NULL DEFAULT 'N',
  `codigo_barras` varchar(30) NOT NULL,
  `EANtrib` varchar(14) NOT NULL,
  `EXTipi` varchar(3) NOT NULL,
  `homologacao` varchar(50) NOT NULL,
  `template` char(1) NOT NULL,
  `imprimir_qtde` char(1) NOT NULL DEFAULT 'N',
  `obs` text NOT NULL,
  `foto` mediumtext NOT NULL,
  `descri_adicional` mediumtext NOT NULL,
  `codigo_externo` char(20) NOT NULL DEFAULT '',
  `tipo_conexao_p` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codprod`),
  KEY `codscat` (`codscat`),
  KEY `codunm` (`codunm`),
  KEY `codigo_ncm` (`codigo_ncm`),
  KEY `consumo` (`consumo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
-- Table structure for table `pasta_msg`
--

DROP TABLE IF EXISTS `pasta_msg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pasta_msg` (
  `codpas` char(10) NOT NULL,
  `tipo` char(1) NOT NULL,
  `codusu` char(2) NOT NULL,
  `nome_pas` varchar(20) NOT NULL,
  `codpas_pai` char(10) NOT NULL DEFAULT '',
  `ordem` int(2) NOT NULL DEFAULT '99',
  PRIMARY KEY (`codpas`),
  KEY `codusu` (`codusu`),
  KEY `tipo` (`tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasta_msg`
-- Table structure for table `status_tarefas_oco`
--

DROP TABLE IF EXISTS `status_tarefas_oco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_tarefas_oco` (
  `codstto` varchar(10) NOT NULL,
  `descri_stto` varchar(30) NOT NULL,
  `cor` int(8) NOT NULL DEFAULT '0',
  `permite_fechar` char(1) NOT NULL DEFAULT 'S'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_tarefas_oco`
-- Table structure for table `eventos_ppv_sc`
--

DROP TABLE IF EXISTS `eventos_ppv_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventos_ppv_sc` (
  `codeppvsc` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codeppv` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  `code_f` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `data_hora_reg` datetime NOT NULL,
  PRIMARY KEY (`codeppvsc`),
  KEY `codsercli` (`codsercli`),
  KEY `codeppv` (`codeppv`),
  KEY `code_f` (`code_f`),
  KEY `codpac` (`codpac`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_ppv_sc`
-- Table structure for table `combo_pop`
--

DROP TABLE IF EXISTS `combo_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `combo_pop` (
  `codcombopop` char(10) NOT NULL,
  `codpop` char(10) NOT NULL,
  `codcombo` char(10) NOT NULL,
  PRIMARY KEY (`codcombopop`),
  KEY `codcombopop` (`codcombopop`,`codpop`,`codcombo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo_pop`
-- Table structure for table `unidades_medida`
--

DROP TABLE IF EXISTS `unidades_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades_medida` (
  `codunm` varchar(10) NOT NULL DEFAULT '',
  `descri_unm` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codunm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
-- Table structure for table `int_config`
--

DROP TABLE IF EXISTS `int_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_config` (
  `id_config` varchar(10) NOT NULL DEFAULT '',
  `modulo` varchar(50) NOT NULL DEFAULT '',
  `chave` varchar(50) NOT NULL DEFAULT '',
  `valor` varchar(255) NOT NULL DEFAULT '',
  `servidor` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_config`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_config`
-- Table structure for table `valores_cobrancas`
--

DROP TABLE IF EXISTS `valores_cobrancas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_cobrancas` (
  `codvcob` varchar(10) NOT NULL,
  `descri_vcob` varchar(100) NOT NULL,
  `tipo` char(1) NOT NULL,
  `tamanho` varchar(10) NOT NULL,
  `valor_padrao` char(10) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codvcob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_cobrancas`
-- Table structure for table `cotacao_moeda`
--

DROP TABLE IF EXISTS `cotacao_moeda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cotacao_moeda` (
  `codctmoeda` varchar(10) NOT NULL,
  `codmoeda` varchar(10) DEFAULT NULL,
  `valor` float(14,2) DEFAULT NULL,
  `data_hora` datetime DEFAULT NULL,
  PRIMARY KEY (`codctmoeda`),
  KEY `codmoeda` (`codmoeda`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotacao_moeda`
-- Table structure for table `ordem_servico`
--

DROP TABLE IF EXISTS `ordem_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordem_servico` (
  `codords` varchar(10) NOT NULL DEFAULT '',
  `codoco` varchar(10) NOT NULL DEFAULT '',
  `codtords` varchar(10) NOT NULL DEFAULT '',
  `codtords_ret` varchar(10) NOT NULL,
  `codtec` varchar(10) NOT NULL DEFAULT '',
  `codtec_ret` varchar(10) NOT NULL,
  `codmfos` varchar(10) NOT NULL,
  `data_ua` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codusu_sol` varchar(2) NOT NULL,
  `codcar` varchar(10) NOT NULL,
  `status_os` char(1) NOT NULL,
  `numero_os` int(6) unsigned NOT NULL DEFAULT '0',
  `codigo_externo` varchar(10) NOT NULL,
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora` varchar(5) NOT NULL DEFAULT '',
  `data_cad` datetime NOT NULL,
  `unidade_t` int(1) NOT NULL DEFAULT '0',
  `data_ret` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora_ret` varchar(5) NOT NULL DEFAULT '',
  `unidade_t_ret` int(1) unsigned NOT NULL,
  `tempo_ret` varchar(5) NOT NULL DEFAULT '',
  `valor_os` float(8,2) NOT NULL DEFAULT '0.00',
  `obs` text NOT NULL,
  `obs_ret` text NOT NULL,
  `agora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`codords`),
  KEY `codoco` (`codoco`),
  KEY `codtec` (`codtec`),
  KEY `data_ret` (`data_ret`),
  KEY `codtords` (`codtords`),
  KEY `data` (`data`),
  KEY `codigo_externo` (`codigo_externo`),
  KEY `codtec_ret` (`codtec_ret`),
  KEY `codmfos` (`codmfos`),
  KEY `codcar` (`codcar`),
  KEY `status_os` (`status_os`),
  KEY `codusu_sol` (`codusu_sol`),
  KEY `codusu` (`codusu`),
  KEY `codtords_ret` (`codtords_ret`),
  KEY `numero_os` (`numero_os`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordem_servico`
-- Table structure for table `cargos_mov`
--

DROP TABLE IF EXISTS `cargos_mov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargos_mov` (
  `codg_m` varchar(10) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `codban` varchar(10) NOT NULL DEFAULT '',
  `ver` char(1) NOT NULL DEFAULT 'N',
  `editar` char(1) NOT NULL DEFAULT 'N',
  `apagar` char(1) NOT NULL DEFAULT 'N',
  `data_ant` char(1) NOT NULL DEFAULT 'N',
  `editar_ant` char(1) NOT NULL DEFAULT 'N',
  `apagar_ant` char(1) NOT NULL DEFAULT 'N',
  `limite_mov` int(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codg_m`),
  KEY `codcar` (`codcar`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos_mov`
-- Table structure for table `eventos_contas_rec`
--

DROP TABLE IF EXISTS `eventos_contas_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventos_contas_rec` (
  `codefcr` varchar(10) NOT NULL DEFAULT '',
  `code_f` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL,
  PRIMARY KEY (`codefcr`),
  KEY `code_f` (`code_f`),
  KEY `codcrec` (`codcrec`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_contas_rec`
-- Table structure for table `planejamento_log`
--

DROP TABLE IF EXISTS `planejamento_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `planejamento_log` (
  `codplanlog` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codplafin` char(10) NOT NULL,
  `data_lan` datetime NOT NULL,
  `atividade` text NOT NULL,
  `codreg` char(10) NOT NULL,
  `obs` text,
  PRIMARY KEY (`codplanlog`),
  KEY `codusu` (`codusu`),
  KEY `data_lan` (`data_lan`),
  KEY `codreg` (`codreg`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planejamento_log`
-- Table structure for table `cod_trans_retorno`
--

DROP TABLE IF EXISTS `cod_trans_retorno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cod_trans_retorno` (
  `codctr` varchar(10) NOT NULL DEFAULT '',
  `numero_ban` char(3) NOT NULL DEFAULT '',
  `codigo` char(2) NOT NULL DEFAULT '',
  `descri_ctr` varchar(30) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT 'I',
  PRIMARY KEY (`codctr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cod_trans_retorno`
-- Table structure for table `consultas_inicio_mes`
--

DROP TABLE IF EXISTS `consultas_inicio_mes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultas_inicio_mes` (
  `codcim` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `ultima_execucao` datetime NOT NULL,
  `consulta_sql` mediumtext NOT NULL,
  `observacao` mediumtext NOT NULL,
  PRIMARY KEY (`codcim`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultas_inicio_mes`
-- Table structure for table `categoria_oco`
--

DROP TABLE IF EXISTS `categoria_oco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categoria_oco` (
  `codcatoco` varchar(10) NOT NULL,
  `descri_catoco` varchar(50) NOT NULL,
  PRIMARY KEY (`codcatoco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria_oco`
-- Table structure for table `status_condominio`
--

DROP TABLE IF EXISTS `status_condominio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_condominio` (
  `codstc` varchar(10) NOT NULL DEFAULT '',
  `descri_stc` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codstc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_condominio`
-- Table structure for table `usu_opc`
--

DROP TABLE IF EXISTS `usu_opc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_opc` (
  `coduopc` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codopc` char(3) NOT NULL DEFAULT '',
  `pn` char(1) NOT NULL DEFAULT 'N',
  `pa` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`coduopc`),
  KEY `codusu` (`codusu`),
  KEY `codopc` (`codopc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_opc`
-- Table structure for table `nas_radius`
--

DROP TABLE IF EXISTS `nas_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nas_radius` (
  `codnr` char(10) NOT NULL DEFAULT '',
  `codpat` char(10) NOT NULL DEFAULT '',
  `host` varchar(15) NOT NULL DEFAULT '',
  `shortname` varchar(50) NOT NULL DEFAULT '',
  `secret` varchar(40) NOT NULL DEFAULT '',
  `snmp` char(1) NOT NULL DEFAULT 'N',
  `community` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL,
  `nastype` varchar(30) NOT NULL,
  `smnp` char(1) NOT NULL DEFAULT 'N',
  `disconnect_port` int(4) NOT NULL DEFAULT '3779',
  PRIMARY KEY (`codnr`),
  KEY `codpat` (`codpat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nas_radius`
-- Table structure for table `wiki_telas`
--

DROP TABLE IF EXISTS `wiki_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wiki_telas` (
  `codwtl` varchar(10) NOT NULL,
  `codtel` varchar(10) NOT NULL,
  `descri_wtl` varchar(100) NOT NULL,
  `tipo` char(1) NOT NULL,
  `link` varchar(254) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codwtl`),
  KEY `codtel` (`codtel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wiki_telas`
-- Table structure for table `relatorios_tarefas`
--

DROP TABLE IF EXISTS `relatorios_tarefas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relatorios_tarefas` (
  `codrtar` varchar(10) NOT NULL,
  `codltar` varchar(10) NOT NULL,
  `codeem` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  `html` mediumtext NOT NULL,
  PRIMARY KEY (`codrtar`),
  KEY `codeem` (`codeem`),
  KEY `codltar` (`codltar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios_tarefas`
-- Table structure for table `tipo_fotografias`
--

DROP TABLE IF EXISTS `tipo_fotografias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_fotografias` (
  `codtfot` varchar(10) NOT NULL DEFAULT '',
  `descri_tfot` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtfot`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_fotografias`
-- Table structure for table `tipo_comp_telas`
--

DROP TABLE IF EXISTS `tipo_comp_telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_comp_telas` (
  `codtct` varchar(10) NOT NULL,
  `codist` varchar(10) NOT NULL,
  `codtct_p` varchar(10) NOT NULL,
  `descri_tct` varchar(30) NOT NULL,
  `classe_base` varchar(30) NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtct`),
  KEY `codist` (`codist`),
  KEY `codtct_p` (`codtct_p`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_comp_telas`
-- Table structure for table `clases_ip`
--

DROP TABLE IF EXISTS `clases_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clases_ip` (
  `codclip` varchar(10) NOT NULL DEFAULT '',
  `clase` int(3) NOT NULL DEFAULT '0',
  `quantidade` int(6) unsigned NOT NULL DEFAULT '0',
  `mascara` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`codclip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clases_ip`
-- Table structure for table `sped_tipo_servico`
--

DROP TABLE IF EXISTS `sped_tipo_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sped_tipo_servico` (
  `codsts` varchar(10) NOT NULL,
  `descri_sts` varchar(50) NOT NULL,
  `codigo_sped` char(1) NOT NULL,
  PRIMARY KEY (`codsts`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sped_tipo_servico`
-- Table structure for table `terminal_voz`
--

DROP TABLE IF EXISTS `terminal_voz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `terminal_voz` (
  `codtvoz` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `coddomp` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `prefixo` varchar(10) NOT NULL,
  `terminal_id` varchar(12) NOT NULL,
  `login` varchar(50) NOT NULL DEFAULT '',
  `senha` varchar(50) NOT NULL DEFAULT '',
  `principal` char(1) NOT NULL DEFAULT 'N',
  `privacidade` char(1) NOT NULL DEFAULT 'N',
  `chamada_cobrar` char(1) NOT NULL DEFAULT 'N',
  `account_code` varchar(50) NOT NULL,
  `simultaneas` int(3) unsigned NOT NULL,
  `data` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`codtvoz`),
  KEY `codsercli` (`codsercli`),
  KEY `codco_cl` (`codco_cl`),
  KEY `prefixo` (`prefixo`),
  KEY `terminal_id` (`terminal_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `terminal_voz`
-- Table structure for table `vencimentos`
--

DROP TABLE IF EXISTS `vencimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vencimentos` (
  `codvenc` varchar(10) NOT NULL DEFAULT '',
  `dia` int(2) NOT NULL DEFAULT '0',
  `dia_f` int(2) NOT NULL DEFAULT '0',
  `dia_f_n` int(2) unsigned NOT NULL,
  `dia_f_l` int(2) unsigned NOT NULL,
  `dia_ftm` int(2) unsigned NOT NULL,
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `mes_completo` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codvenc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vencimentos`
-- Table structure for table `atributos_dicionario_mikrotik`
--

DROP TABLE IF EXISTS `atributos_dicionario_mikrotik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `atributos_dicionario_mikrotik` (
  `codadcmkt` varchar(10) NOT NULL DEFAULT '',
  `coddcmkt` varchar(10) NOT NULL DEFAULT '',
  `atributo` varchar(30) NOT NULL DEFAULT '',
  `valor_padrao` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codadcmkt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atributos_dicionario_mikrotik`
-- Table structure for table `historico_cliente`
--

DROP TABLE IF EXISTS `historico_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_cliente` (
  `codhis` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `tabela` varchar(30) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `usuario` char(2) NOT NULL DEFAULT '',
  `ip` varchar(50) NOT NULL DEFAULT '',
  `texto` text NOT NULL,
  PRIMARY KEY (`codhis`),
  KEY `codcli` (`codcli`),
  KEY `codsercli` (`codsercli`),
  KEY `ip` (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_cliente`
-- Table structure for table `central_tipos_contato`
--

DROP TABLE IF EXISTS `central_tipos_contato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `central_tipos_contato` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codtco_cl` varchar(50) DEFAULT NULL,
  `obrigatorio` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `central_tipos_contato`
-- Table structure for table `log_upd_arquivos`
--

DROP TABLE IF EXISTS `log_upd_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_upd_arquivos` (
  `codlupdarq` bigint(20) NOT NULL AUTO_INCREMENT,
  `codupdarq` char(10) NOT NULL,
  `codagu` char(10) NOT NULL,
  `ip` varchar(50) NOT NULL,
  `bd` varchar(50) NOT NULL,
  `data_upd` datetime NOT NULL,
  `ok` char(1) NOT NULL,
  `log` mediumtext NOT NULL,
  `nro_lic` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codlupdarq`),
  KEY `ip` (`ip`),
  KEY `bd` (`bd`),
  KEY `ok` (`ok`),
  KEY `data_upd` (`data_upd`),
  KEY `codudparq` (`codupdarq`),
  KEY `codagu` (`codagu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_upd_arquivos`
-- Table structure for table `tipo_cancelamento_contrato`
--

DROP TABLE IF EXISTS `tipo_cancelamento_contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cancelamento_contrato` (
  `codtcc` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `descri_tcc` varchar(50) NOT NULL DEFAULT '',
  `descri_for` mediumtext NOT NULL,
  `formula_sql` text NOT NULL,
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codtcc`),
  KEY `codsad` (`codsad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cancelamento_contrato`
-- Table structure for table `motivo_perda_interesse`
--

DROP TABLE IF EXISTS `motivo_perda_interesse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motivo_perda_interesse` (
  `id_perda` int(11) NOT NULL AUTO_INCREMENT,
  `id_funil` int(11) NOT NULL DEFAULT '0',
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `motivo_perda` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_perda`),
  KEY `id_funil` (`id_funil`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivo_perda_interesse`
-- Table structure for table `det_tarifas_cta`
--

DROP TABLE IF EXISTS `det_tarifas_cta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_tarifas_cta` (
  `coddtct` varchar(10) NOT NULL,
  `codtari` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `valor` float NOT NULL,
  PRIMARY KEY (`coddtct`),
  KEY `codtari` (`codtari`),
  KEY `codcta` (`codcta`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_tarifas_cta`
-- Table structure for table `tipo_terminacao`
--

DROP TABLE IF EXISTS `tipo_terminacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_terminacao` (
  `codtter` varchar(10) NOT NULL DEFAULT '',
  `descri_tter` varchar(50) NOT NULL DEFAULT '',
  `valor` float(10,4) NOT NULL DEFAULT '0.0000',
  `ordem` int(2) unsigned NOT NULL,
  `disponivel` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codtter`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_terminacao`
-- Table structure for table `filtros_inf`
--

DROP TABLE IF EXISTS `filtros_inf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filtros_inf` (
  `codfil` varchar(10) NOT NULL DEFAULT '',
  `codinf` varchar(10) NOT NULL DEFAULT '',
  `grupo_filtro` varchar(30) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT 'F',
  `campo` varchar(100) NOT NULL,
  `filtro_w` char(1) NOT NULL DEFAULT 'S',
  `operador` char(2) NOT NULL DEFAULT '',
  `data_padrao` date NOT NULL DEFAULT '0000-00-00',
  `titulo` varchar(50) NOT NULL DEFAULT '',
  `tamanho` int(4) unsigned NOT NULL DEFAULT '180',
  `ordem` int(1) unsigned NOT NULL DEFAULT '0',
  `tabela` varchar(50) NOT NULL,
  `nome_exibe` varchar(50) NOT NULL,
  `campo_codigo` varchar(50) NOT NULL,
  `campo_like` varchar(50) NOT NULL,
  `nome_codigo` varchar(50) NOT NULL,
  `filtro_like` char(1) NOT NULL DEFAULT 'N',
  `consulta_sql` text NOT NULL,
  PRIMARY KEY (`codfil`),
  KEY `codinf` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filtros_inf`
-- Table structure for table `tipo_mov`
--

DROP TABLE IF EXISTS `tipo_mov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_mov` (
  `codtmov` varchar(10) NOT NULL DEFAULT '',
  `codban` varchar(10) NOT NULL,
  `codfor` varchar(10) NOT NULL,
  `descri_tmov` varchar(20) NOT NULL DEFAULT '',
  `gera_raz` char(1) NOT NULL DEFAULT '',
  `codcta` varchar(14) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `entrada` char(1) NOT NULL DEFAULT '',
  `valor` float(8,2) NOT NULL,
  `float_bank` char(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codtmov`),
  KEY `codban` (`codban`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_mov`
-- Table structure for table `regras_servicos_cli`
--

DROP TABLE IF EXISTS `regras_servicos_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regras_servicos_cli` (
  `codrsc` varchar(10) NOT NULL DEFAULT '',
  `titulo` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codrsc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regras_servicos_cli`
-- Table structure for table `cidade_tecnologia_sici`
--

DROP TABLE IF EXISTS `cidade_tecnologia_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cidade_tecnologia_sici` (
  `codtecsici` varchar(10) NOT NULL,
  `cidade` varchar(8) NOT NULL,
  `codtsici` varchar(10) NOT NULL,
  `capacidade` int(6) NOT NULL,
  PRIMARY KEY (`codtecsici`),
  KEY `cidade` (`cidade`),
  KEY `codtsici` (`codtsici`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidade_tecnologia_sici`
-- Table structure for table `det_ordemcompra_nf`
--

DROP TABLE IF EXISTS `det_ordemcompra_nf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_ordemcompra_nf` (
  `codorcnf` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `codordcomp` varchar(10) NOT NULL,
  `baixada` char(1) NOT NULL DEFAULT 'n',
  PRIMARY KEY (`codorcnf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_ordemcompra_nf`
-- Table structure for table `nota_fiscal_log_alter`
--

DROP TABLE IF EXISTS `nota_fiscal_log_alter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nota_fiscal_log_alter` (
  `codnfla` char(10) NOT NULL,
  `codnf` char(10) NOT NULL COMMENT 'codigo nota fiscal',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `codusu` char(2) NOT NULL COMMENT 'codigo do usuario',
  `campo` varchar(50) NOT NULL DEFAULT '' COMMENT 'ficará armazenado o nome do campo que sofreu alteração',
  `valor_ant` mediumtext NOT NULL COMMENT 'valor anterior da alteração',
  `valor_atu` mediumtext NOT NULL COMMENT 'valor atual',
  PRIMARY KEY (`codnfla`),
  KEY `codnf` (`codnf`),
  KEY `codusu` (`codusu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_fiscal_log_alter`
-- Table structure for table `painel_monitor_dados`
--

DROP TABLE IF EXISTS `painel_monitor_dados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `painel_monitor_dados` (
  `codpmdados` varchar(10) NOT NULL,
  `descricao` varchar(50) DEFAULT NULL,
  `consulta_grafico` text,
  `consulta_grid` text,
  PRIMARY KEY (`codpmdados`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `painel_monitor_dados`
-- Table structure for table `faturas_bco`
--

DROP TABLE IF EXISTS `faturas_bco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturas_bco` (
  `codfbco` char(10) NOT NULL,
  `codfat` char(10) NOT NULL,
  `codctr` char(10) NOT NULL,
  `codarq` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_lan` datetime NOT NULL,
  `codarq_e` char(10) NOT NULL DEFAULT '',
  `codarq_b` char(10) NOT NULL DEFAULT '',
  `n_boleto` varchar(20) NOT NULL,
  `nro_doc` char(10) NOT NULL,
  `id_externo` varchar(20) NOT NULL DEFAULT '',
  `link_fatura` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codfbco`),
  KEY `codfat` (`codfat`),
  KEY `codctr` (`codctr`),
  KEY `data_lan` (`data_lan`),
  KEY `codarq` (`codarq`),
  KEY `id_externo` (`id_externo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturas_bco`
-- Table structure for table `servicos_cli`
--

DROP TABLE IF EXISTS `servicos_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli` (
  `codsercli` char(10) NOT NULL DEFAULT '',
  `contrato` int(11) NOT NULL,
  `codser` char(10) NOT NULL DEFAULT '',
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codpop` char(10) NOT NULL DEFAULT '',
  `codvenc` char(10) NOT NULL DEFAULT '',
  `codcon` int(3) unsigned NOT NULL DEFAULT '0',
  `codextra` char(10) NOT NULL,
  `codven` char(10) NOT NULL DEFAULT '',
  `codigo_externo` char(20) NOT NULL,
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `coddeb` char(10) NOT NULL DEFAULT '',
  `codmodc` char(10) NOT NULL DEFAULT '',
  `codco_cl` char(10) NOT NULL,
  `codsercli_p` char(10) NOT NULL DEFAULT '',
  `codsercli_a` char(10) NOT NULL,
  `codsercli_v` char(10) NOT NULL DEFAULT '',
  `codecli_i` char(10) NOT NULL,
  `codecli_c` char(10) NOT NULL,
  `codecli_n` char(10) NOT NULL,
  `login` varchar(100) NOT NULL DEFAULT '',
  `codcob` char(10) NOT NULL DEFAULT '',
  `codrcob` char(10) NOT NULL,
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_fec` date NOT NULL DEFAULT '0000-00-00',
  `data_fec_a` date NOT NULL DEFAULT '0000-00-00',
  `data_sus` date NOT NULL DEFAULT '0000-00-00',
  `data_hab` date NOT NULL,
  `data_ini` date NOT NULL,
  `data_con` date NOT NULL,
  `codest` char(10) NOT NULL DEFAULT '',
  `valor_plano` decimal(10,2) NOT NULL DEFAULT '0.00',
  `desc_venc` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `desconto` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `q_dias_troca_plano` int(3) unsigned NOT NULL,
  `numero_con` int(11) NOT NULL DEFAULT '0',
  `boleto_separado` char(1) NOT NULL DEFAULT 'N',
  `nf_separado` char(1) NOT NULL DEFAULT 'N',
  `carne` char(1) NOT NULL DEFAULT 'N',
  `codintr` char(10) NOT NULL,
  `referencia_plano` varchar(50) NOT NULL,
  `obs` text NOT NULL,
  `obs_fiscal` mediumtext NOT NULL,
  `data_can` date NOT NULL DEFAULT '0000-00-00',
  `codcan` char(10) NOT NULL DEFAULT '',
  `dias_trail` int(3) unsigned NOT NULL DEFAULT '0',
  `senha` varchar(16) NOT NULL DEFAULT '',
  `pontos` int(3) unsigned NOT NULL DEFAULT '1',
  `codusu` char(2) NOT NULL DEFAULT '',
  `antecipada` char(1) NOT NULL DEFAULT 'N',
  `valor_taxa` decimal(10,2) NOT NULL DEFAULT '0.00',
  `parcelas_taxa` int(2) unsigned NOT NULL DEFAULT '0',
  `validade` int(3) unsigned NOT NULL DEFAULT '0',
  `competencia` char(4) NOT NULL,
  `nro_plano` int(3) DEFAULT NULL,
  `multa_contrato` decimal(10,2) NOT NULL,
  `cobrar_multa` char(1) NOT NULL DEFAULT 'S',
  `cod_identificador_da` varchar(15) NOT NULL DEFAULT '',
  `codco_cl_p_t1` char(10) NOT NULL DEFAULT '',
  `codco_cl_p_t2` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsercli`),
  KEY `codser` (`codser`),
  KEY `codcli` (`codcli`),
  KEY `codpop` (`codpop`),
  KEY `codvenc` (`codvenc`),
  KEY `codcon` (`codcon`),
  KEY `codcob` (`codcob`),
  KEY `codest` (`codest`),
  KEY `codven` (`codven`),
  KEY `codsercli_p` (`codsercli_p`),
  KEY `codextra` (`codextra`),
  KEY `codcan` (`codcan`),
  KEY `data_can` (`data_can`),
  KEY `codsercli_a` (`codsercli_a`),
  KEY `data_sus` (`data_sus`),
  KEY `codigo_externo` (`codigo_externo`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codecli_i` (`codecli_i`),
  KEY `coddeb` (`coddeb`),
  KEY `codco_cl_p_t1` (`codco_cl_p_t1`),
  KEY `codco_cl_p_t2` (`codco_cl_p_t2`),
  KEY `login` (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli`
-- Table structure for table `mysql_process_list`
--

DROP TABLE IF EXISTS `mysql_process_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mysql_process_list` (
  `codprolst` int(11) NOT NULL AUTO_INCREMENT,
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id` varchar(20) DEFAULT '',
  `user` varchar(50) DEFAULT NULL,
  `host` varchar(250) DEFAULT NULL,
  `db` varchar(250) DEFAULT NULL,
  `command` varchar(250) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `state` varchar(150) DEFAULT NULL,
  `info` mediumtext,
  PRIMARY KEY (`codprolst`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mysql_process_list`
-- Table structure for table `servidor_mw`
--

DROP TABLE IF EXISTS `servidor_mw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidor_mw` (
  `codmw` varchar(10) NOT NULL,
  `codservp` varchar(10) DEFAULT NULL,
  `descri_mw` varchar(50) DEFAULT NULL,
  `porta` char(6) DEFAULT NULL,
  PRIMARY KEY (`codmw`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidor_mw`
-- Table structure for table `valores_ind_sec`
--

DROP TABLE IF EXISTS `valores_ind_sec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_ind_sec` (
  `codvins` varchar(10) NOT NULL,
  `coddind` varchar(10) NOT NULL,
  `codigo_sec` varchar(10) NOT NULL,
  `descri_sec` varchar(50) NOT NULL,
  PRIMARY KEY (`codvins`),
  KEY `coddind` (`coddind`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_ind_sec`
-- Table structure for table `log_acesso`
--

DROP TABLE IF EXISTS `log_acesso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_acesso` (
  `codlog` char(10) NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `codopc` char(3) NOT NULL DEFAULT '',
  `data_log` datetime NOT NULL,
  `ip_log` varchar(45) NOT NULL DEFAULT '',
  `nome_estacao` varchar(45) NOT NULL DEFAULT '',
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codinf` char(10) NOT NULL DEFAULT '',
  `plataforma` char(1) NOT NULL DEFAULT 'D' COMMENT 'D_desk - W_eb - M_obile - C_entral',
  PRIMARY KEY (`codlog`),
  KEY `codusu` (`codusu`),
  KEY `codopc` (`codopc`),
  KEY `data_log` (`data_log`),
  KEY `codcli` (`codcli`),
  KEY `codinf` (`codinf`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_acesso`
-- Table structure for table `MovimentoConciliacao`
--

DROP TABLE IF EXISTS `MovimentoConciliacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MovimentoConciliacao` (
  `Id` bigint(18) NOT NULL AUTO_INCREMENT,
  `Arquivo` varchar(50) CHARACTER SET latin1 DEFAULT NULL COMMENT 'Nome do Arquivo',
  `Banco` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `Conta` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `Data` date DEFAULT NULL,
  `Documento` varchar(18) CHARACTER SET latin1 DEFAULT NULL,
  `Historico` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `Valor` double(15,2) DEFAULT NULL,
  `SeqMov` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `Usuario` varchar(2) CHARACTER SET latin1 DEFAULT NULL,
  `Situacao` char(1) CHARACTER SET latin1 DEFAULT NULL,
  `Motivo` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `codarq` varchar(10) DEFAULT NULL,
  `codban` varchar(10) DEFAULT NULL,
  `codusu` char(2) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `SeqMov` (`SeqMov`),
  KEY `codarq` (`codarq`),
  KEY `codban` (`codban`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MovimentoConciliacao`
-- Table structure for table `cartoes`
--

DROP TABLE IF EXISTS `cartoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cartoes` (
  `codcart` varchar(10) NOT NULL DEFAULT '',
  `codvcre` varchar(10) NOT NULL DEFAULT '',
  `codcre` varchar(10) NOT NULL DEFAULT '',
  `codstc` varchar(10) NOT NULL DEFAULT '',
  `codtct` varchar(10) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL,
  `data_lib` date NOT NULL,
  `data_ati` datetime NOT NULL,
  `numero_serie` int(8) NOT NULL,
  `senha` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcart`),
  KEY `codvcre` (`codvcre`),
  KEY `codstc` (`codstc`),
  KEY `codtct` (`codtct`),
  KEY `codcre` (`codcre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartoes`
-- Table structure for table `total_navegacao`
--

DROP TABLE IF EXISTS `total_navegacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `total_navegacao` (
  `codtnav` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `compe` varchar(4) NOT NULL DEFAULT '',
  `codmed` varchar(10) NOT NULL,
  `upload` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '||-',
  `download` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '||-',
  `tempo` bigint(20) NOT NULL DEFAULT '0' COMMENT '||-',
  `data_med` datetime NOT NULL,
  PRIMARY KEY (`codtnav`),
  KEY `codsercli` (`codsercli`),
  KEY `compe` (`compe`),
  KEY `codmed` (`codmed`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `total_navegacao`
-- Table structure for table `onu_fibra`
--

DROP TABLE IF EXISTS `onu_fibra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `onu_fibra` (
  `codonu` varchar(10) NOT NULL,
  `codpat` varchar(10) NOT NULL,
  `codpolt` varchar(10) NOT NULL,
  `ponid` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `codtonu` varchar(10) NOT NULL,
  `nro` int(3) unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  `onutype` varchar(50) NOT NULL,
  `authtype` varchar(10) NOT NULL,
  `mac` varchar(17) NOT NULL,
  `nro_serie` varchar(20) NOT NULL,
  `swver` varchar(10) NOT NULL,
  `onuport` int(5) unsigned NOT NULL,
  `vlan_port` int(5) unsigned NOT NULL,
  `vlan_voz` int(6) unsigned NOT NULL,
  `vlan_tv` int(6) unsigned NOT NULL,
  `senha_wrls` varchar(30) NOT NULL,
  `senha_wrls_5g` varchar(30) NOT NULL DEFAULT '',
  `ssid_wrls` varchar(50) NOT NULL,
  `ssid_wrls_5g` varchar(50) NOT NULL DEFAULT '',
  `senha_admin` varchar(50) NOT NULL,
  `lan_ip` varchar(15) NOT NULL,
  `lan_ip_start` varchar(15) NOT NULL,
  `lan_ip_end` varchar(15) NOT NULL,
  `lan_ip_mask` varchar(15) NOT NULL,
  `wan_ip` varchar(15) NOT NULL,
  `wan_mask` varchar(15) NOT NULL,
  `wan_gw` varchar(15) NOT NULL,
  `pppoe` char(1) NOT NULL,
  `tipo_conexao` char(1) NOT NULL,
  `ger_ip` varchar(50) NOT NULL,
  `ger_porta` int(5) unsigned NOT NULL,
  `ger_login` varchar(50) NOT NULL,
  `ger_senha` varchar(50) NOT NULL,
  `interface_ppp` varchar(50) NOT NULL,
  `etapa_provisionamento` int(11) NOT NULL,
  `ultima_sincronizacao` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sinal` decimal(10,2) NOT NULL DEFAULT '0.00',
  `ultima_leitura` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `data_cad` datetime DEFAULT NULL,
  PRIMARY KEY (`codonu`),
  KEY `codpat` (`codpat`),
  KEY `ponid` (`ponid`),
  KEY `codsercli` (`codsercli`),
  KEY `codpolt` (`codpolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `onu_fibra`
-- Table structure for table `det_juros_negociacao`
--

DROP TABLE IF EXISTS `det_juros_negociacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_juros_negociacao` (
  `codcrec` char(10) NOT NULL,
  `codndeb` char(10) DEFAULT NULL,
  KEY `codcrec` (`codcrec`),
  KEY `codndeb` (`codndeb`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_juros_negociacao`
-- Table structure for table `det_proposta`
--

DROP TABLE IF EXISTS `det_proposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_proposta` (
  `coddpcom` varchar(10) NOT NULL,
  `codpcom` varchar(10) NOT NULL,
  `codpint` varchar(10) NOT NULL,
  `taxa_inst` float(10,2) NOT NULL,
  `parcelas_inst` int(2) unsigned NOT NULL,
  `valor` float(10,2) NOT NULL,
  PRIMARY KEY (`coddpcom`),
  KEY `codpcom` (`codpcom`),
  KEY `codpint` (`codpint`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_proposta`
-- Table structure for table `detalhe_protocolo_c`
--

DROP TABLE IF EXISTS `detalhe_protocolo_c`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_protocolo_c` (
  `coddpcan` varchar(10) NOT NULL DEFAULT '',
  `codpcan` int(6) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `code_f` varchar(10) NOT NULL,
  `p_desde` date NOT NULL,
  `p_ate` date NOT NULL,
  `valor` float(10,2) NOT NULL,
  `valor_multa` float(10,2) NOT NULL,
  PRIMARY KEY (`coddpcan`),
  UNIQUE KEY `coddpcan` (`coddpcan`),
  KEY `codsercli` (`codsercli`),
  KEY `codpcan` (`codpcan`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_protocolo_c`
-- Table structure for table `servicos_cli_sta`
--

DROP TABLE IF EXISTS `servicos_cli_sta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_sta` (
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codest` varchar(10) NOT NULL DEFAULT '',
  `data` datetime NOT NULL,
  KEY `codsercli` (`codsercli`),
  KEY `codest` (`codest`),
  KEY `data` (`data`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_sta`
-- Table structure for table `olt_fibra`
--

DROP TABLE IF EXISTS `olt_fibra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `olt_fibra` (
  `codolt` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `codtolt` varchar(10) NOT NULL,
  `descri_olt` varchar(100) NOT NULL,
  `ativo` char(1) NOT NULL,
  `oltid` int(3) unsigned NOT NULL,
  `ip` varchar(15) NOT NULL,
  `login` varchar(30) NOT NULL,
  `senha` varchar(30) NOT NULL,
  `porta` int(5) unsigned NOT NULL,
  `dns_1` varchar(15) NOT NULL,
  `dns_2` varchar(15) NOT NULL,
  `lan_ip` varchar(15) NOT NULL,
  `lan_ip_start` varchar(15) NOT NULL,
  `lan_ip_end` varchar(15) NOT NULL,
  `lan_ip_mask` varchar(15) NOT NULL,
  `ip_teste_1` varchar(15) NOT NULL,
  `ip_teste_2` varchar(15) NOT NULL,
  `ger_ip` varchar(15) NOT NULL,
  `ger_mask` varchar(15) NOT NULL,
  `ger_porta` int(5) unsigned NOT NULL,
  `ger_login` varchar(50) NOT NULL,
  `ger_senha` varchar(50) NOT NULL,
  `ger_vlan` int(11) NOT NULL DEFAULT '0',
  `interface_ppp` varchar(50) NOT NULL,
  `sinal_minimo` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Campo para informar o sinal mínimo aceitável para a ONU',
  `sinal_maximo` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codolt`),
  KEY `codtolt` (`codtolt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `olt_fibra`
-- Table structure for table `dados_integrator`
--

DROP TABLE IF EXISTS `dados_integrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dados_integrator` (
  `coddint` char(10) NOT NULL DEFAULT '',
  `tipo` char(5) NOT NULL DEFAULT '',
  `host_serv` varchar(50) NOT NULL DEFAULT '',
  `host_web` varchar(100) NOT NULL DEFAULT '',
  `pasta_trabalho` varchar(50) NOT NULL DEFAULT '',
  `pasta_imagem` varchar(50) NOT NULL DEFAULT '',
  `moeda` char(10) NOT NULL,
  `certificado` char(1) NOT NULL DEFAULT 'N',
  `versao_server` char(1) NOT NULL DEFAULT '3',
  `versao_web` char(10) DEFAULT NULL,
  `versao` char(10) NOT NULL DEFAULT '',
  `versao_painel` char(10) NOT NULL,
  `versao_relatorio` char(10) NOT NULL,
  `versao_financeiro` char(10) NOT NULL,
  `versao_formularios` char(10) NOT NULL,
  `nro_lic` int(11) NOT NULL DEFAULT '0',
  `isp` mediumtext NOT NULL,
  PRIMARY KEY (`coddint`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_integrator`
-- Table structure for table `log_envio_email`
--

DROP TABLE IF EXISTS `log_envio_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_envio_email` (
  `codleem` varchar(10) NOT NULL,
  `codeem` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codleem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_envio_email`
-- Table structure for table `exportar_inf`
--

DROP TABLE IF EXISTS `exportar_inf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exportar_inf` (
  `codeinf` varchar(10) NOT NULL DEFAULT '',
  `codinf` varchar(10) NOT NULL DEFAULT '',
  `descri_einf` varchar(50) NOT NULL DEFAULT '',
  `ordem` int(2) unsigned NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT '',
  `campo_grupo` varchar(50) NOT NULL,
  `ativo` varchar(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`codeinf`),
  KEY `codinf` (`codinf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exportar_inf`
-- Table structure for table `int_modules_commands`
--

DROP TABLE IF EXISTS `int_modules_commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_modules_commands` (
  `modulo` int(2) NOT NULL DEFAULT '0',
  `comando` int(2) NOT NULL DEFAULT '0',
  `servidor` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`modulo`,`comando`,`servidor`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_modules_commands`
-- Table structure for table `ips_liberados`
--

DROP TABLE IF EXISTS `ips_liberados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips_liberados` (
  `codipl` varchar(10) NOT NULL DEFAULT '',
  `ip` varchar(16) NOT NULL DEFAULT '',
  `codpar` varchar(10) NOT NULL,
  `classe` int(2) unsigned NOT NULL,
  `aplicacao` char(1) NOT NULL,
  `obs` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codipl`),
  KEY `ip` (`ip`),
  KEY `codpar` (`codpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ips_liberados`
-- Table structure for table `servidores_liberados`
--

DROP TABLE IF EXISTS `servidores_liberados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidores_liberados` (
  `id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `host` varchar(50) NOT NULL,
  `user` varchar(30) NOT NULL,
  `passwd` varchar(30) NOT NULL,
  `obs` mediumtext NOT NULL,
  `codctr` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `HOST` (`host`),
  KEY `USER` (`user`),
  KEY `passwd` (`passwd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidores_liberados`
-- Table structure for table `logs_iclass`
--

DROP TABLE IF EXISTS `logs_iclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs_iclass` (
  `codlic` varchar(10) NOT NULL,
  `codords` varchar(10) NOT NULL,
  `codoco` varchar(10) NOT NULL,
  `data_hora` datetime DEFAULT NULL,
  `nome_api` varchar(50) NOT NULL,
  `tipo_retorno` varchar(10) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` varchar(100) NOT NULL,
  `xml` mediumtext NOT NULL,
  `xml_envio` mediumtext NOT NULL,
  `usuario_externo` varchar(50) DEFAULT NULL COMMENT 'Nome do usuário externo',
  `numero_os` int(11) unsigned DEFAULT NULL COMMENT 'Número da ordem de serviço',
  `codprod` char(10) DEFAULT NULL COMMENT 'Código do produto',
  `numero_pat` varchar(20) DEFAULT NULL COMMENT 'Número do patrimônio',
  `serial_number` varchar(35) DEFAULT NULL COMMENT 'Serial Number do Patrimônio',
  `mac` varchar(17) DEFAULT NULL COMMENT 'Mac do Patrimônio',
  `tipo` char(1) DEFAULT NULL COMMENT 'E - Logs recebidos do Iclass, S - Logs enviados para o Iclass',
  `ok` char(1) NOT NULL COMMENT 'Executado com sucesso Sim ou Não',
  PRIMARY KEY (`codlic`),
  KEY `codos` (`codords`),
  KEY `codoco` (`codoco`),
  KEY `usuario_externo` (`usuario_externo`),
  KEY `numero_os` (`numero_os`),
  KEY `codprod` (`codprod`),
  KEY `numero_pat` (`numero_pat`),
  KEY `serial_number` (`serial_number`),
  KEY `mac` (`mac`),
  KEY `ok` (`ok`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_iclass`
-- Table structure for table `int_xml_config`
--

DROP TABLE IF EXISTS `int_xml_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_xml_config` (
  `codxmlc` varchar(30) DEFAULT NULL,
  `titulo` varchar(150) DEFAULT NULL,
  `nome` varchar(90) DEFAULT NULL,
  `propriedade` varchar(90) DEFAULT NULL,
  `valor` varchar(90) DEFAULT NULL,
  `tipo` varchar(90) DEFAULT NULL,
  `codxml` varchar(150) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_xml_config`
-- Table structure for table `sici`
--

DROP TABLE IF EXISTS `sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sici` (
  `codsici` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `compe` varchar(4) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_lan` date NOT NULL,
  PRIMARY KEY (`codsici`),
  KEY `codemp` (`codemp`),
  KEY `compe` (`compe`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sici`
-- Table structure for table `perguntas`
--

DROP TABLE IF EXISTS `perguntas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perguntas` (
  `codperg` varchar(10) NOT NULL DEFAULT '',
  `nome_perg` varchar(50) NOT NULL DEFAULT '',
  `titulo_perg` varchar(50) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `obs` text NOT NULL,
  PRIMARY KEY (`codperg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perguntas`
-- Table structure for table `problemas_conexao_bd`
--

DROP TABLE IF EXISTS `problemas_conexao_bd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problemas_conexao_bd` (
  `codpcbd` char(10) NOT NULL DEFAULT '',
  `codsercli` char(10) NOT NULL DEFAULT '',
  `data` date NOT NULL,
  `data_base` varchar(30) NOT NULL DEFAULT '',
  `resposta` mediumtext NOT NULL,
  PRIMARY KEY (`codpcbd`),
  KEY `codsercli` (`codsercli`),
  KEY `data` (`data`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problemas_conexao_bd`
-- Table structure for table `dici_tecnologia`
--

DROP TABLE IF EXISTS `dici_tecnologia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dici_tecnologia` (
  `coddicitec` char(10) NOT NULL,
  `descricao` varchar(50) DEFAULT NULL,
  `ativo` char(1) DEFAULT 'S',
  PRIMARY KEY (`coddicitec`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dici_tecnologia`
-- Table structure for table `opcoes_grupo_items`
--

DROP TABLE IF EXISTS `opcoes_grupo_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes_grupo_items` (
  `codgrpopcitem` varchar(10) NOT NULL,
  `codgrp` varchar(10) DEFAULT NULL,
  `coditem` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codgrpopcitem`),
  KEY `codgrp` (`codgrp`),
  KEY `coditem` (`coditem`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes_grupo_items`
-- Table structure for table `servicos_cli_cob`
--

DROP TABLE IF EXISTS `servicos_cli_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_cob` (
  `codscc` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `coderc` varchar(10) NOT NULL,
  `saldo` float(10,2) NOT NULL,
  `data_exe` datetime NOT NULL,
  `ok` char(1) NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codscc`),
  KEY `codsercli` (`codsercli`),
  KEY `coderc` (`coderc`),
  KEY `saldo` (`saldo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_cob`
-- Table structure for table `empresas_conf_nfe`
--

DROP TABLE IF EXISTS `empresas_conf_nfe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresas_conf_nfe` (
  `codecn` char(10) NOT NULL,
  `codlmp` char(10) NOT NULL,
  `codrtrib` char(10) NOT NULL,
  `codemp` char(10) NOT NULL,
  PRIMARY KEY (`codecn`),
  KEY `codlmp` (`codlmp`),
  KEY `codrtrib` (`codrtrib`),
  KEY `codemp` (`codemp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas_conf_nfe`
-- Table structure for table `encaminhamentos`
--

DROP TABLE IF EXISTS `encaminhamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encaminhamentos` (
  `codenca` char(10) NOT NULL DEFAULT '',
  `codoco` char(10) NOT NULL DEFAULT '',
  `codusu_o` char(2) NOT NULL DEFAULT '',
  `codusu_d` char(2) NOT NULL DEFAULT '',
  `codcar` char(10) NOT NULL DEFAULT '',
  `codcar_o` char(10) NOT NULL DEFAULT '',
  `coddep` char(10) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `hora` char(5) NOT NULL DEFAULT '',
  `descri_enca` text NOT NULL,
  `local_origem_usu` char(2) DEFAULT NULL,
  `local_origem_car` char(10) DEFAULT NULL,
  PRIMARY KEY (`codenca`),
  KEY `codoco` (`codoco`),
  KEY `data` (`data`),
  KEY `codusu_o` (`codusu_o`),
  KEY `codusu_d` (`codusu_d`),
  KEY `codcar` (`codcar`),
  KEY `codcar_o` (`codcar_o`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encaminhamentos`
-- Table structure for table `unidades_produto`
--

DROP TABLE IF EXISTS `unidades_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades_produto` (
  `coduprod` varchar(10) NOT NULL,
  `id` int(5) NOT NULL AUTO_INCREMENT COMMENT 'Chave do routerbox',
  `codigo` varchar(6) NOT NULL DEFAULT '',
  `descricao` varchar(60) DEFAULT '',
  PRIMARY KEY (`coduprod`),
  KEY `id` (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_produto`
-- Table structure for table `valores_indicadores`
--

DROP TABLE IF EXISTS `valores_indicadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_indicadores` (
  `codvind` varchar(10) NOT NULL,
  `codind` varchar(10) NOT NULL,
  `codvins` varchar(10) NOT NULL,
  `data` datetime NOT NULL,
  `ano` char(4) NOT NULL DEFAULT '',
  `mes` char(2) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL,
  `codigos` mediumtext NOT NULL,
  `porcentagem` float(6,2) NOT NULL,
  PRIMARY KEY (`codvind`),
  KEY `codind` (`codind`),
  KEY `data` (`data`),
  KEY `codvins` (`codvins`),
  KEY `ano` (`ano`),
  KEY `mes` (`mes`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_indicadores`
-- Table structure for table `syn_clientes`
--

DROP TABLE IF EXISTS `syn_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `syn_clientes` (
  `codscli` bigint(20) NOT NULL AUTO_INCREMENT,
  `codcli` varchar(10) NOT NULL DEFAULT '',
  `acao` char(1) NOT NULL DEFAULT '',
  `data_ua` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sincronizado` char(1) NOT NULL DEFAULT 'N',
  `data_sincronismo` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `resp_sincronismo` varchar(20) NOT NULL DEFAULT '',
  `data_erro` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tentativa` int(11) NOT NULL DEFAULT '0',
  `log_erro` mediumtext,
  `campos` mediumtext,
  `id_sap` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codscli`),
  KEY `sincronizado` (`sincronizado`),
  KEY `acao` (`acao`),
  KEY `data_sincronismo` (`data_sincronismo`),
  KEY `codcli` (`codcli`),
  KEY `data_ua` (`data_ua`),
  KEY `resp_sincronismo` (`resp_sincronismo`),
  KEY `codcli_acao_resp_sincronismo` (`codcli`,`acao`,`resp_sincronismo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `syn_clientes`
-- Table structure for table `enlaces_novo`
--

DROP TABLE IF EXISTS `enlaces_novo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enlaces_novo` (
  `codenl` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcon` int(6) unsigned NOT NULL DEFAULT '0',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `coderb` varchar(10) NOT NULL DEFAULT '',
  `coderc` varchar(10) NOT NULL DEFAULT '',
  `distancia` decimal(8,3) NOT NULL DEFAULT '0.000',
  PRIMARY KEY (`codenl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enlaces_novo`
-- Table structure for table `exec_acao_gestores`
--

DROP TABLE IF EXISTS `exec_acao_gestores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exec_acao_gestores` (
  `codeag` varchar(10) NOT NULL,
  `codatab` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `codusu` char(2) NOT NULL,
  `tabela` varchar(50) NOT NULL,
  `motivo` mediumtext NOT NULL,
  PRIMARY KEY (`codeag`),
  KEY `codatab` (`codatab`),
  KEY `data_hora` (`data_hora`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exec_acao_gestores`
-- Table structure for table `login_radius`
--

DROP TABLE IF EXISTS `login_radius`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_radius` (
  `codlrad` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codcemail` varchar(10) NOT NULL DEFAULT '',
  `codstl` varchar(10) NOT NULL,
  `login` varchar(63) NOT NULL DEFAULT '',
  `senha` varchar(50) NOT NULL DEFAULT '',
  `status` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codlrad`),
  KEY `login` (`login`),
  KEY `codcemail` (`codcemail`),
  KEY `codsercli` (`codsercli`),
  KEY `codstl` (`codstl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_radius`
-- Table structure for table `ligacoes_atendimentos`
--

DROP TABLE IF EXISTS `ligacoes_atendimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ligacoes_atendimentos` (
  `codliga` varchar(10) NOT NULL DEFAULT '',
  `codvis` varchar(10) NOT NULL DEFAULT '',
  `callingstationid` varchar(12) NOT NULL DEFAULT '',
  `calledstationid` varchar(12) NOT NULL DEFAULT '',
  `username` varchar(30) NOT NULL DEFAULT '',
  `starttime` datetime NOT NULL,
  `sessiontime` int(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`codliga`),
  KEY `codvis` (`codvis`),
  KEY `starttime` (`starttime`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligacoes_atendimentos`
-- Table structure for table `servicos_adi_imp`
--

DROP TABLE IF EXISTS `servicos_adi_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_adi_imp` (
  `codsai` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codemp` varchar(10) NOT NULL DEFAULT '',
  `codtnf` varchar(10) NOT NULL DEFAULT '',
  `codtser` varchar(10) NOT NULL,
  `codcif` char(4) NOT NULL DEFAULT '',
  `descri_adi` varchar(70) NOT NULL DEFAULT '',
  `descri_nf` varchar(40) NOT NULL,
  `porcentagem` float(6,2) NOT NULL,
  `icms` float(5,2) NOT NULL,
  `iss` float(5,2) NOT NULL,
  `fust` float(5,2) NOT NULL,
  `funtel` float(5,2) NOT NULL,
  `pis` float(5,2) NOT NULL,
  `cofins` float(5,2) NOT NULL,
  `iva` float(5,2) NOT NULL,
  `codigo_fiscal` varchar(5) NOT NULL,
  `retem_imposto` char(1) NOT NULL,
  `itemsgroupcode` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsai`),
  KEY `codsad` (`codsad`),
  KEY `codcta` (`codcta`),
  KEY `codemp` (`codemp`),
  KEY `codtnf` (`codtnf`),
  KEY `codtser` (`codtser`),
  KEY `codcif` (`codcif`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_adi_imp`
-- Table structure for table `tipo_metas_ind`
--

DROP TABLE IF EXISTS `tipo_metas_ind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_metas_ind` (
  `codtmi` varchar(10) NOT NULL,
  `codtgraf` varchar(10) NOT NULL,
  `descri_tmi` varchar(50) NOT NULL,
  `titulo_tmi` varchar(30) NOT NULL,
  PRIMARY KEY (`codtmi`),
  KEY `codtgraf` (`codtgraf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_metas_ind`
-- Table structure for table `transacoes_cielo`
--

DROP TABLE IF EXISTS `transacoes_cielo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transacoes_cielo` (
  `tid` varchar(20) NOT NULL COMMENT 'Código da transação cielo.',
  `codfat` varchar(200) NOT NULL COMMENT 'Codigo da fatura integrator.',
  `status_trans` varchar(2) NOT NULL COMMENT 'Status do pagamento.',
  `valor` int(11) NOT NULL COMMENT 'Valor do pagamento 1,00 = 100.',
  `data_hora` datetime NOT NULL,
  `erro` varchar(10) NOT NULL,
  `bandeira` varchar(15) NOT NULL DEFAULT '' COMMENT 'Bandeira.',
  `tipo_cartao` varchar(20) NOT NULL DEFAULT '1' COMMENT 'Credito ou debito.',
  `parcelas` int(11) NOT NULL DEFAULT '1' COMMENT 'Parcelas',
  `codemp` varchar(12) DEFAULT NULL COMMENT 'Empresa que vai créditar no integrator.',
  `codcli` int(11) DEFAULT NULL COMMENT 'Codigo do cliente.',
  `nome_cli` varchar(200) DEFAULT NULL COMMENT 'Nome do cliente do cliente.',
  `credito` varchar(20) DEFAULT NULL COMMENT 'codvcre compra de crédito.',
  `codsercli` varchar(10) DEFAULT NULL COMMENT 'Plano que vai o credito comprado.',
  `return_cielo` text COMMENT 'Retorno da cielo.',
  `paymentid` varchar(40) DEFAULT NULL COMMENT 'Id do pagamento.',
  `recurrencyId` varchar(36) NOT NULL DEFAULT '',
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Vincula o codigo da transação com o codfat.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacoes_cielo`
-- Table structure for table `chat_atendimentos`
--

DROP TABLE IF EXISTS `chat_atendimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_atendimentos` (
  `codcha` varchar(10) NOT NULL DEFAULT '',
  `codvis` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `login` varchar(30) NOT NULL DEFAULT '',
  `chat` mediumtext NOT NULL,
  PRIMARY KEY (`codcha`),
  KEY `codvis` (`codvis`),
  KEY `codusu` (`codusu`),
  KEY `data` (`data`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_atendimentos`
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(191) NOT NULL,
  `email` varchar(191) NOT NULL,
  `email_verified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `password` varchar(191) NOT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `gauth` varchar(16) DEFAULT '',
  `codesta` varchar(10) DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_unique` (`email`),
  KEY `codesta` (`codesta`),
  KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
-- Table structure for table `sms_incidentes`
--

DROP TABLE IF EXISTS `sms_incidentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_incidentes` (
  `codsin` int(10) NOT NULL AUTO_INCREMENT,
  `codicon` varchar(10) NOT NULL,
  `codcli` int(6) unsigned NOT NULL,
  `codesms` varchar(10) NOT NULL,
  `numero` char(12) NOT NULL,
  `data_hora` datetime NOT NULL,
  PRIMARY KEY (`codsin`),
  KEY `codicon` (`codicon`),
  KEY `codcli` (`codcli`),
  KEY `codesms` (`codesms`)
) ENGINE=MyISAM AUTO_INCREMENT=12129 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_incidentes`
-- Table structure for table `incidentes_condominios`
--

DROP TABLE IF EXISTS `incidentes_condominios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incidentes_condominios` (
  `codicon` varchar(10) NOT NULL,
  `codcon` int(4) unsigned NOT NULL,
  `codrep` varchar(10) NOT NULL,
  `data_ini` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `ura` char(1) NOT NULL DEFAULT 'S',
  `descri_icon` varchar(100) NOT NULL,
  `obs` mediumtext NOT NULL,
  `codicon_p` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codicon`),
  KEY `codcon` (`codcon`),
  KEY `data_ini` (`data_ini`),
  KEY `data_fim` (`data_fim`),
  KEY `ura` (`ura`),
  KEY `codicon_p` (`codicon_p`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incidentes_condominios`
-- Table structure for table `plano_cta_sici`
--

DROP TABLE IF EXISTS `plano_cta_sici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plano_cta_sici` (
  `codcsici` varchar(10) NOT NULL,
  `codemp` varchar(10) NOT NULL,
  `codcta` varchar(9) NOT NULL,
  `codctc` char(8) NOT NULL,
  `tipo` char(1) NOT NULL,
  `codisici` varchar(10) NOT NULL,
  `reduz_fat_liq` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codcsici`),
  KEY `codemp` (`codemp`),
  KEY `codcta` (`codcta`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plano_cta_sici`
-- Table structure for table `pastas`
--

DROP TABLE IF EXISTS `pastas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pastas` (
  `codpas` varchar(10) NOT NULL DEFAULT '',
  `nome_pas` varchar(50) NOT NULL DEFAULT '',
  `data` datetime NOT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codpas`),
  KEY `nome_pas` (`nome_pas`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pastas`
-- Table structure for table `venda_patrimonio`
--

DROP TABLE IF EXISTS `venda_patrimonio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venda_patrimonio` (
  `codvpat` varchar(10) NOT NULL DEFAULT '',
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `code_f` varchar(10) NOT NULL DEFAULT '',
  `valor_lan` float(10,2) NOT NULL,
  `parcelas` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codvpat`),
  KEY `codcmp` (`codcmp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda_patrimonio`
-- Table structure for table `status_inst`
--

DROP TABLE IF EXISTS `status_inst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_inst` (
  `codsta` char(3) NOT NULL DEFAULT '',
  `descri_sta` varchar(30) NOT NULL DEFAULT '',
  `nome_sta` char(3) NOT NULL DEFAULT '',
  `reporte` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsta`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_inst`
-- Table structure for table `usu_mapa`
--

DROP TABLE IF EXISTS `usu_mapa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_mapa` (
  `codu_m` varchar(10) NOT NULL,
  `codmapa` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_mapa`
-- Table structure for table `tipo_vinculo_arquivos`
--

DROP TABLE IF EXISTS `tipo_vinculo_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_vinculo_arquivos` (
  `codvin` varchar(10) NOT NULL DEFAULT '',
  `descri_vin` varchar(50) NOT NULL DEFAULT '',
  `nome_tabela` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codvin`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_vinculo_arquivos`
-- Table structure for table `regra_serasa`
--

DROP TABLE IF EXISTS `regra_serasa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regra_serasa` (
  `codrgserasa` varchar(10) NOT NULL,
  `nome` varchar(50) NOT NULL DEFAULT '',
  `dias_vencido` smallint(6) NOT NULL DEFAULT '0',
  `dias_vencido_neg` smallint(6) NOT NULL DEFAULT '0',
  `email_resp` varchar(200) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codrgserasa`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regra_serasa`
-- Table structure for table `campos_plataforma_pagamento`
--

DROP TABLE IF EXISTS `campos_plataforma_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campos_plataforma_pagamento` (
  `codcamplat` char(10) NOT NULL,
  `codtplat` char(10) DEFAULT NULL,
  `descri_campo` varchar(50) DEFAULT NULL,
  `tipo_campo` char(1) DEFAULT NULL,
  `tamanho` int(3) DEFAULT NULL,
  `soleitura` char(1) DEFAULT NULL,
  `nome_campo` varchar(50) DEFAULT NULL,
  `consulta_sql` mediumtext,
  PRIMARY KEY (`codcamplat`),
  KEY `codtplat` (`codtplat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campos_plataforma_pagamento`
-- Table structure for table `categoria_fone`
--

DROP TABLE IF EXISTS `categoria_fone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categoria_fone` (
  `codcfone` char(10) NOT NULL COMMENT '||PhoneCategory ID',
  `descri_catf` varchar(45) NOT NULL DEFAULT '' COMMENT '||PhoneCategory description',
  `ativo` char(1) NOT NULL DEFAULT 'S' COMMENT '||PhoneCategory status',
  `tipo` char(1) DEFAULT 'C' COMMENT '||PhoneCategory type (C-elular ou F-ixo)',
  `obs` mediumtext NOT NULL COMMENT '||PhoneCategory obs',
  PRIMARY KEY (`codcfone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=PhoneCategory|Desc=|Grupo=Phone';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria_fone`
-- Table structure for table `creditos_voip`
--

DROP TABLE IF EXISTS `creditos_voip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditos_voip` (
  `codcvp` varchar(10) NOT NULL DEFAULT '',
  `codlvp` varchar(10) NOT NULL DEFAULT '',
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `valor` float(8,2) NOT NULL DEFAULT '0.00',
  `status` char(1) NOT NULL DEFAULT 'P',
  PRIMARY KEY (`codcvp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creditos_voip`
-- Table structure for table `usu_equipe`
--

DROP TABLE IF EXISTS `usu_equipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_equipe` (
  `codusueqp` varchar(10) NOT NULL,
  `codusu` varchar(2) DEFAULT NULL,
  `codeqp` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codusueqp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_equipe`
-- Table structure for table `suspensao_programada`
--

DROP TABLE IF EXISTS `suspensao_programada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suspensao_programada` (
  `codsusprog` char(10) NOT NULL,
  `codcli` int(6) NOT NULL,
  `codsercli` char(10) NOT NULL,
  `suspender` char(1) NOT NULL,
  `reduzir` char(1) NOT NULL,
  `data_sus` date NOT NULL,
  `status` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codsusprog`),
  KEY `codcli` (`codcli`),
  KEY `codsercli` (`codsercli`),
  KEY `data_sus` (`data_sus`),
  KEY `reduzir` (`reduzir`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suspensao_programada`
-- Table structure for table `radios`
--

DROP TABLE IF EXISTS `radios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radios` (
  `codrad` varchar(10) NOT NULL DEFAULT '',
  `codpat` varchar(10) NOT NULL DEFAULT '',
  `codosr` varchar(10) NOT NULL DEFAULT '',
  `router` char(1) NOT NULL DEFAULT 'N',
  `host_name` varchar(50) NOT NULL DEFAULT '',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `porta` int(5) NOT NULL,
  `mac` varchar(30) NOT NULL DEFAULT '',
  `semsenha` char(1) NOT NULL DEFAULT 'S',
  `nas` varchar(1) NOT NULL DEFAULT 'N',
  `porta_api_mkt` int(5) unsigned NOT NULL,
  `nome_backup` varchar(40) NOT NULL,
  `guarda_backup` char(1) NOT NULL DEFAULT 'S',
  `api_teste` char(1) NOT NULL DEFAULT 'N',
  `api_qnt_teste` int(2) NOT NULL,
  `codigo_externo` char(20) NOT NULL,
  `tipo_equi` char(1) NOT NULL DEFAULT 'C' COMMENT '(C)liente - (E)nlace - (A)mbos',
  `obs` text NOT NULL,
  `backup` text NOT NULL,
  PRIMARY KEY (`codrad`),
  KEY `codpat` (`codpat`),
  KEY `codosr` (`codosr`),
  KEY `router` (`router`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radios`
-- Table structure for table `descontos_regras_neg`
--

DROP TABLE IF EXISTS `descontos_regras_neg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `descontos_regras_neg` (
  `coddrng` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codrng` varchar(10) NOT NULL DEFAULT '',
  `codftm` varchar(10) NOT NULL DEFAULT '',
  `valor` float(10,2) NOT NULL,
  `data` date NOT NULL,
  PRIMARY KEY (`coddrng`),
  KEY `codsercli` (`codsercli`),
  KEY `codrng` (`codrng`),
  KEY `codftm` (`codftm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `descontos_regras_neg`
-- Table structure for table `usu_gadgets`
--

DROP TABLE IF EXISTS `usu_gadgets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_gadgets` (
  `codugdg` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codgdg` varchar(10) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  PRIMARY KEY (`codugdg`),
  KEY `codusu` (`codusu`),
  KEY `codgdg` (`codgdg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_gadgets`
-- Table structure for table `login_web`
--

DROP TABLE IF EXISTS `login_web`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_web` (
  `codlgw` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `login` varchar(50) NOT NULL,
  `senha` varchar(30) NOT NULL,
  PRIMARY KEY (`codlgw`),
  KEY `codsercli` (`codsercli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_web`
-- Table structure for table `accesos`
--

DROP TABLE IF EXISTS `accesos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accesos` (
  `indice` int(2) NOT NULL DEFAULT '0',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `coddep` varchar(10) NOT NULL DEFAULT '',
  `menu` int(1) unsigned NOT NULL DEFAULT '0',
  `edita` int(1) unsigned NOT NULL DEFAULT '0',
  `lanza` int(1) unsigned NOT NULL DEFAULT '0',
  `apaga` int(1) unsigned NOT NULL DEFAULT '0',
  `relatorios` int(1) unsigned NOT NULL DEFAULT '0',
  `nusuario` char(2) NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accesos`
-- Table structure for table `tabelas_segmentadas`
--

DROP TABLE IF EXISTS `tabelas_segmentadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabelas_segmentadas` (
  `codtabseg` varchar(10) NOT NULL,
  `tabela` varchar(50) NOT NULL,
  `nome_tabseg` varchar(100) NOT NULL DEFAULT '',
  `primeira_data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ultima_data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`codtabseg`),
  KEY `tabela` (`tabela`),
  KEY `nome_tabseg` (`nome_tabseg`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelas_segmentadas`
-- Table structure for table `faturas_a`
--

DROP TABLE IF EXISTS `faturas_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faturas_a` (
  `codfat` varchar(10) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codcob` varchar(10) NOT NULL DEFAULT '',
  `n_boleto` varchar(20) NOT NULL DEFAULT '',
  `codarq` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `status` char(1) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `data_bai` date NOT NULL DEFAULT '0000-00-00',
  `valor_lan` float(8,2) NOT NULL DEFAULT '2.00',
  `histo_fat` varchar(70) NOT NULL DEFAULT '',
  PRIMARY KEY (`codfat`),
  KEY `n_boleto` (`n_boleto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faturas_a`
-- Table structure for table `update_arquivos`
--

DROP TABLE IF EXISTS `update_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `update_arquivos` (
  `codupdf` varchar(10) NOT NULL,
  `nome` varchar(30) DEFAULT NULL,
  `tamanho` varchar(15) DEFAULT NULL,
  `arquivo` varchar(50) DEFAULT NULL,
  `destino` varchar(100) DEFAULT NULL,
  `tamanho_c` int(15) DEFAULT NULL,
  `temporario` varchar(100) DEFAULT NULL,
  `data_l` datetime DEFAULT NULL,
  `data_s` datetime DEFAULT NULL,
  `semext` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`codupdf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `update_arquivos`
-- Table structure for table `redirecionamento_numero`
--

DROP TABLE IF EXISTS `redirecionamento_numero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redirecionamento_numero` (
  `codredirn` varchar(10) NOT NULL,
  `codndis` varchar(10) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `valor` float(9,4) NOT NULL,
  `parcelas` int(3) NOT NULL,
  `num_redi` varchar(10) NOT NULL,
  PRIMARY KEY (`codredirn`),
  KEY `codndis` (`codndis`),
  KEY `codco_cl` (`codco_cl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `redirecionamento_numero`
-- Table structure for table `usu_ggi`
--

DROP TABLE IF EXISTS `usu_ggi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_ggi` (
  `coduggi` varchar(10) NOT NULL,
  `codggi` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  PRIMARY KEY (`coduggi`),
  KEY `codggi` (`codggi`),
  KEY `codusu` (`codusu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_ggi`
-- Table structure for table `sentencia_historico`
--

DROP TABLE IF EXISTS `sentencia_historico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sentencia_historico` (
  `tabela` varchar(30) NOT NULL DEFAULT '',
  `alias_tabela` varchar(30) NOT NULL DEFAULT '',
  `alias_titulo` varchar(30) NOT NULL DEFAULT '',
  `consulta_sql` text NOT NULL,
  PRIMARY KEY (`tabela`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sentencia_historico`
-- Table structure for table `usu_exesu`
--

DROP TABLE IF EXISTS `usu_exesu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usu_exesu` (
  `codexesu` varchar(10) NOT NULL,
  `host` varchar(15) DEFAULT NULL,
  `host_name` varchar(50) DEFAULT NULL,
  `usuario` varchar(20) DEFAULT NULL,
  `ativo` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`codexesu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usu_exesu`
-- Table structure for table `login_liberados`
--

DROP TABLE IF EXISTS `login_liberados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_liberados` (
  `codl_l` varchar(10) NOT NULL DEFAULT '',
  `codlrad` varchar(10) NOT NULL DEFAULT '',
  `mac` varchar(17) NOT NULL DEFAULT '',
  PRIMARY KEY (`codl_l`),
  KEY `codlrad` (`codlrad`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_liberados`
-- Table structure for table `layout_impressao`
--

DROP TABLE IF EXISTS `layout_impressao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `layout_impressao` (
  `layout_imp_l` varchar(10) NOT NULL DEFAULT '',
  `descri_lay` varchar(30) NOT NULL DEFAULT '',
  `parametros` varchar(100) NOT NULL DEFAULT '',
  `nosso_nro_a` varchar(150) NOT NULL DEFAULT '',
  `nosso_nro_d` varchar(150) NOT NULL DEFAULT '',
  `campo_livre` varchar(255) NOT NULL DEFAULT '',
  `calculo_dig_cob` varchar(100) NOT NULL DEFAULT '',
  `codrela` varchar(10) NOT NULL DEFAULT '',
  `codrela_v` varchar(10) NOT NULL,
  `codrela_e` varchar(10) NOT NULL,
  `codigos` text NOT NULL,
  `funcao` text NOT NULL,
  `relatorio` text NOT NULL,
  `grafico` text NOT NULL,
  PRIMARY KEY (`layout_imp_l`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_impressao`
-- Table structure for table `razao_cartao`
--

DROP TABLE IF EXISTS `razao_cartao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `razao_cartao` (
  `codraz` varchar(10) NOT NULL COMMENT 'Codigo da conta no Razão',
  `codadqcar` varchar(10) NOT NULL COMMENT 'Codigo do Cartão usado nesse pagamento',
  `valor_tar` decimal(8,2) NOT NULL COMMENT 'Valor da Tarifa cobrando nessa transação',
  `tarifa_perc` decimal(5,2) NOT NULL COMMENT 'Percentual aplicado nessa transação',
  `id_transacao` varchar(30) NOT NULL DEFAULT '' COMMENT 'Id do cartão',
  `obs` mediumtext COMMENT 'Resposta do Gateway',
  PRIMARY KEY (`codraz`),
  KEY `codadqcar` (`codadqcar`),
  CONSTRAINT `codadqcar` FOREIGN KEY (`codadqcar`) REFERENCES `adquirente_cartao` (`codadqcar`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `razao_cartao`
-- Table structure for table `servicos_tv`
--

DROP TABLE IF EXISTS `servicos_tv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_tv` (
  `codstv` varchar(10) NOT NULL,
  `codser` varchar(10) NOT NULL,
  `codsad` varchar(10) NOT NULL,
  `codpac` varchar(10) NOT NULL,
  `codtpt` varchar(10) NOT NULL,
  PRIMARY KEY (`codstv`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`),
  KEY `codpac` (`codpac`),
  KEY `codtpt` (`codtpt`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_tv`
-- Table structure for table `indicadores`
--

DROP TABLE IF EXISTS `indicadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `indicadores` (
  `codind` varchar(10) NOT NULL,
  `codtui` varchar(10) NOT NULL,
  `codtind` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `codtpi` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL DEFAULT 'S',
  `codtci` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `codsind` varchar(10) NOT NULL,
  `ultima_leitura` datetime NOT NULL,
  `tela_ind` char(2) NOT NULL,
  `ordem_leitura` int(3) unsigned NOT NULL,
  `tempo_captura` int(6) NOT NULL,
  `descri_ind` varchar(50) NOT NULL,
  `titulo_ind` varchar(50) NOT NULL,
  `nome_abrev` varchar(12) NOT NULL,
  `codigo_externo` varchar(20) NOT NULL,
  `orientacao` char(1) NOT NULL DEFAULT 'P',
  `decimais` int(2) unsigned NOT NULL,
  `captura` int(6) unsigned NOT NULL,
  `frequencia` char(1) NOT NULL,
  `totalizador` char(1) NOT NULL,
  `padrao` char(1) NOT NULL DEFAULT 'N',
  `quant_frente` int(2) unsigned NOT NULL,
  `quant_atras` int(2) unsigned NOT NULL,
  `api_indicadores` varchar(100) NOT NULL,
  `api_dados` varchar(100) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `codigo_group` varchar(10) NOT NULL,
  `limite` int(2) unsigned NOT NULL,
  `mobile` char(1) NOT NULL DEFAULT 'S',
  `projeto_ind` char(1) NOT NULL,
  `consulta_valor` mediumtext NOT NULL,
  `consulta_vl_ot` mediumtext NOT NULL,
  `consulta_codigos` mediumtext NOT NULL,
  `consulta_dados` mediumtext NOT NULL,
  `consulta_cubo` mediumtext NOT NULL,
  `consulta_porcentagem` mediumtext NOT NULL,
  `consulta_parametros` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  `log_captura` mediumtext NOT NULL,
  PRIMARY KEY (`codind`),
  KEY `codtui` (`codtui`),
  KEY `codtind` (`codtind`),
  KEY `codservp` (`codservp`),
  KEY `codtpi` (`codtpi`),
  KEY `ativo` (`ativo`),
  KEY `codtci` (`codtci`),
  KEY `ultima_leitura` (`ultima_leitura`),
  KEY `codtab` (`codtab`),
  KEY `codsind` (`codsind`),
  KEY `tela_ind` (`tela_ind`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indicadores`
-- Table structure for table `servicos_ivr`
--

DROP TABLE IF EXISTS `servicos_ivr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_ivr` (
  `codsivr` varchar(10) NOT NULL DEFAULT '',
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codsad` varchar(10) NOT NULL,
  `clase` int(3) unsigned NOT NULL DEFAULT '0',
  `codvel` varchar(10) NOT NULL,
  `codvel_r` varchar(10) NOT NULL,
  `upload` int(6) unsigned NOT NULL DEFAULT '0',
  `max_limit_up` int(4) unsigned NOT NULL,
  `burst_limit_up` int(4) unsigned NOT NULL,
  `burst_threshold_up` int(4) unsigned NOT NULL,
  `burst_time_up` int(3) unsigned NOT NULL,
  `download` int(6) unsigned NOT NULL DEFAULT '0',
  `max_limit_dw` int(4) unsigned NOT NULL,
  `burst_limit_dw` int(4) unsigned NOT NULL,
  `burst_threshold_dw` int(4) unsigned NOT NULL,
  `burst_time_dw` int(3) unsigned NOT NULL,
  `upload_n` int(6) NOT NULL DEFAULT '0',
  `download_n` int(6) unsigned NOT NULL DEFAULT '0',
  `quant_ip` int(2) NOT NULL DEFAULT '1',
  `uni_medida` char(1) NOT NULL DEFAULT 'M',
  `quant_mensal` int(6) unsigned NOT NULL DEFAULT '0',
  `franquia_nav` char(1) NOT NULL DEFAULT 'N',
  `valor_adi_i` float(8,3) NOT NULL DEFAULT '0.000',
  `valor_limite` float(10,2) NOT NULL,
  `autenticacao` char(1) NOT NULL DEFAULT 'N',
  `acrescenta_ip` char(1) NOT NULL DEFAULT 'N',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `quant_livr` int(1) unsigned NOT NULL DEFAULT '0',
  `grupo_horario` varchar(30) NOT NULL DEFAULT '',
  `ip_publico` char(1) NOT NULL DEFAULT 'N',
  `ip_fixo` char(1) NOT NULL DEFAULT 'N',
  `prioridade` int(2) unsigned NOT NULL,
  `sessoes` int(4) unsigned NOT NULL,
  PRIMARY KEY (`codsivr`),
  KEY `codser` (`codser`),
  KEY `codsad` (`codsad`),
  KEY `codvel` (`codvel`),
  KEY `codvel_r` (`codvel_r`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_ivr`
-- Table structure for table `conf_remetentes_sms`
--

DROP TABLE IF EXISTS `conf_remetentes_sms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_remetentes_sms` (
  `codrsms` varchar(10) NOT NULL,
  `codcbe` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  PRIMARY KEY (`codrsms`),
  KEY `codcbe` (`codcbe`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_remetentes_sms`
-- Table structure for table `carta_correcao_nfe`
--

DROP TABLE IF EXISTS `carta_correcao_nfe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carta_correcao_nfe` (
  `codcartac` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `numero` int(6) NOT NULL,
  `carta_correcao` mediumtext NOT NULL,
  `protocolo` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcartac`),
  KEY `codnf` (`codnf`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carta_correcao_nfe`
-- Table structure for table `tipo_base_conhecimento`
--

DROP TABLE IF EXISTS `tipo_base_conhecimento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_base_conhecimento` (
  `codtbacon` varchar(10) NOT NULL,
  `descri_tbacon` varchar(50) NOT NULL,
  PRIMARY KEY (`codtbacon`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_base_conhecimento`
-- Table structure for table `arq_pas`
--

DROP TABLE IF EXISTS `arq_pas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arq_pas` (
  `codapas` varchar(10) NOT NULL DEFAULT '',
  `codarq` varchar(10) NOT NULL DEFAULT '',
  `codpas` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codapas`),
  KEY `codarq` (`codarq`),
  KEY `codpas` (`codpas`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arq_pas`
-- Table structure for table `item_produtos`
--

DROP TABLE IF EXISTS `item_produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_produtos` (
  `coditempro` varchar(10) NOT NULL DEFAULT '',
  `codprod` varchar(10) NOT NULL DEFAULT '',
  `coditem` varchar(10) NOT NULL DEFAULT '',
  `quant` int(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`coditempro`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_produtos`
-- Table structure for table `filtro_desconto`
--

DROP TABLE IF EXISTS `filtro_desconto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filtro_desconto` (
  `codfiltro` char(10) NOT NULL,
  `descri_regra` varchar(100) NOT NULL,
  `tabela` varchar(45) NOT NULL,
  `coluna_filtro` varchar(45) NOT NULL,
  `coluna_descri_filtro` varchar(45) NOT NULL,
  `seleciona` char(1) NOT NULL DEFAULT 'N' COMMENT 'N = pode selecionar 1 item para o filtro\\n S = pode selecionar varios ',
  PRIMARY KEY (`codfiltro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filtro_desconto`
-- Table structure for table `upd_arquivos`
--

DROP TABLE IF EXISTS `upd_arquivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `upd_arquivos` (
  `codupdarq` char(10) NOT NULL,
  `nome_arq` varchar(100) NOT NULL,
  `versao` int(11) NOT NULL,
  `local` varchar(200) NOT NULL,
  `atualizar` char(1) NOT NULL DEFAULT 'N',
  `obrigatorio` char(1) NOT NULL DEFAULT 'N',
  `md5` varchar(50) DEFAULT NULL,
  `data_upd` datetime DEFAULT NULL,
  PRIMARY KEY (`codupdarq`),
  KEY `nome_arq` (`nome_arq`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `upd_arquivos`
-- Table structure for table `log_tarefa_cob`
--

DROP TABLE IF EXISTS `log_tarefa_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_tarefa_cob` (
  `codltc` varchar(10) NOT NULL,
  `codtar` varchar(10) NOT NULL,
  `coderc` varchar(10) NOT NULL,
  `data_hora` datetime NOT NULL,
  `ok` char(1) NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codltc`),
  KEY `codtar` (`codtar`),
  KEY `coderc` (`coderc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_tarefa_cob`
-- Table structure for table `lista_campos_fc`
--

DROP TABLE IF EXISTS `lista_campos_fc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lista_campos_fc` (
  `idlcdc` int(11) NOT NULL AUTO_INCREMENT,
  `codlcfc` char(10) NOT NULL DEFAULT '',
  `codcampfc` char(10) NOT NULL DEFAULT '',
  `valor` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`idlcdc`),
  KEY `codcampfc` (`codcampfc`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lista_campos_fc`
-- Table structure for table `agendar_contato`
--

DROP TABLE IF EXISTS `agendar_contato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agendar_contato` (
  `codacon` varchar(10) NOT NULL,
  `codoco` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `codco_cl` varchar(10) NOT NULL,
  `status` char(1) NOT NULL DEFAULT 'P',
  `data` datetime NOT NULL,
  `data_fim` datetime NOT NULL,
  `descri_acon` mediumtext NOT NULL,
  `tipo_contato` char(1) NOT NULL DEFAULT 'T',
  PRIMARY KEY (`codacon`),
  KEY `codoco` (`codoco`),
  KEY `codusu` (`codusu`),
  KEY `codco_cl` (`codco_cl`),
  KEY `status` (`status`),
  KEY `data` (`data`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendar_contato`
-- Table structure for table `tarefas_modelo`
--

DROP TABLE IF EXISTS `tarefas_modelo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tarefas_modelo` (
  `codtarm` varchar(10) NOT NULL DEFAULT '',
  `codocop` varchar(10) NOT NULL DEFAULT '',
  `titulo_tarm` varchar(50) NOT NULL DEFAULT '',
  `codutmp` varchar(10) NOT NULL DEFAULT '',
  `tempo` int(4) unsigned NOT NULL DEFAULT '0',
  `descri_tarm` mediumtext NOT NULL,
  `for_email` mediumtext NOT NULL,
  `obs` mediumtext NOT NULL,
  `posx` int(6) unsigned NOT NULL DEFAULT '0',
  `posy` int(6) unsigned NOT NULL DEFAULT '0',
  `width` int(6) unsigned NOT NULL DEFAULT '0',
  `height` int(6) unsigned NOT NULL DEFAULT '0',
  `criar_atendimento` char(1) DEFAULT NULL,
  `obrigatorio` char(1) DEFAULT 'N',
  `tipo_m` char(1) DEFAULT '0',
  PRIMARY KEY (`codtarm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarefas_modelo`
-- Table structure for table `contas_rec`
--

DROP TABLE IF EXISTS `contas_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contas_rec` (
  `codcrec` varchar(10) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `codcomp` varchar(4) NOT NULL DEFAULT '',
  `codmov` varchar(10) NOT NULL DEFAULT '',
  `codbol` varchar(10) NOT NULL DEFAULT '',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL DEFAULT '',
  `codcli` int(6) NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL,
  `codcob` varchar(10) NOT NULL,
  `codmed` varchar(10) NOT NULL,
  `codftm` varchar(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL,
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codadi` varchar(10) NOT NULL DEFAULT '',
  `nro_nta_fiscal` varchar(10) NOT NULL DEFAULT '',
  `codicr` varchar(10) NOT NULL,
  `codnf` varchar(10) NOT NULL,
  `codacob` char(10) NOT NULL DEFAULT '',
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `periodo` varchar(19) NOT NULL DEFAULT '',
  `p_desde` date NOT NULL DEFAULT '0000-00-00',
  `p_ate` date NOT NULL DEFAULT '0000-00-00',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `data_ven` date NOT NULL DEFAULT '0000-00-00',
  `parcela` varchar(5) NOT NULL DEFAULT '',
  `data_bai` date NOT NULL DEFAULT '0000-00-00',
  `histo_rec` varchar(70) NOT NULL DEFAULT '',
  `valor_lan` float(8,2) NOT NULL DEFAULT '0.00',
  `valor_pag` float(8,2) NOT NULL DEFAULT '0.00',
  `n_boleto` varchar(20) NOT NULL DEFAULT '',
  `juros` float(8,2) NOT NULL DEFAULT '0.00',
  `data_trans` date NOT NULL DEFAULT '0000-00-00',
  `recebido` char(1) NOT NULL DEFAULT '',
  `arq_ret` varchar(15) NOT NULL DEFAULT '',
  `codstse` varchar(10) NOT NULL,
  `protocolo_can` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`codcrec`),
  KEY `codcomp` (`codcomp`),
  KEY `codafi` (`codpop`),
  KEY `codbol` (`codbol`),
  KEY `codmov` (`codmov`),
  KEY `codcli` (`codcli`),
  KEY `codftm` (`codftm`),
  KEY `data_ven` (`data_ven`),
  KEY `codicr` (`codicr`),
  KEY `codsercli` (`codsercli`),
  KEY `codcob` (`codcob`),
  KEY `codemp` (`codemp`),
  KEY `codmed` (`codmed`),
  KEY `data_lan` (`data_lan`),
  KEY `codctc` (`codctc`),
  KEY `codadi` (`codadi`),
  KEY `arq_ret` (`arq_ret`),
  KEY `codacob` (`codacob`),
  KEY `codstse` (`codstse`),
  KEY `ix_codcrec_codsercli_codcob_codicr` (`codcrec`,`codsercli`,`codcob`,`codicr`),
  KEY `codftm_codadi_data_ven_codsercli_valor_lan` (`codsercli`,`codftm`,`codadi`,`data_ven`,`valor_lan`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_rec`
-- Table structure for table `servicos_interfaces`
--

DROP TABLE IF EXISTS `servicos_interfaces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_interfaces` (
  `codservint` varchar(10) NOT NULL,
  `codinte` varchar(10) DEFAULT NULL,
  `codtservint` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codservint`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_interfaces`
-- Table structure for table `pendencias`
--

DROP TABLE IF EXISTS `pendencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pendencias` (
  `codpend` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `tipo_p` char(2) NOT NULL DEFAULT '',
  `mensagem` varchar(100) NOT NULL DEFAULT '',
  `proxima_tela` varchar(50) NOT NULL DEFAULT '',
  `comando` varchar(50) NOT NULL DEFAULT '',
  `status` char(1) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_pro` date NOT NULL DEFAULT '0000-00-00',
  `obs` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codpend`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pendencias`
-- Table structure for table `tipo_ppv`
--

DROP TABLE IF EXISTS `tipo_ppv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_ppv` (
  `codtppv` varchar(10) NOT NULL,
  `descri_tppv` varchar(30) NOT NULL,
  `pacote` char(1) NOT NULL,
  PRIMARY KEY (`codtppv`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_ppv`
-- Table structure for table `colunas_cond`
--

DROP TABLE IF EXISTS `colunas_cond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colunas_cond` (
  `codccnd` varchar(10) NOT NULL,
  `codcgrd` varchar(10) NOT NULL,
  `codgrd` varchar(10) NOT NULL,
  `codima` varchar(15) NOT NULL,
  `codfcnd` varchar(10) NOT NULL,
  `fonte_condicao` varchar(50) NOT NULL,
  `condicao` varchar(200) NOT NULL,
  `codcgrd_cond` varchar(10) NOT NULL,
  `operador` char(2) NOT NULL,
  `valor` varchar(100) NOT NULL,
  `tipo_valor` char(1) NOT NULL,
  PRIMARY KEY (`codccnd`),
  KEY `codcgrd` (`codcgrd`),
  KEY `codima` (`codima`),
  KEY `codfcnd` (`codfcnd`),
  KEY `codgrd` (`codgrd`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colunas_cond`
-- Table structure for table `lembretes`
--

DROP TABLE IF EXISTS `lembretes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lembretes` (
  `codlem` varchar(10) NOT NULL DEFAULT '',
  `codusu` char(2) NOT NULL DEFAULT '',
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `desktop` char(1) NOT NULL DEFAULT 'N',
  `codlem_r` varchar(10) NOT NULL DEFAULT '',
  `data_lan` date NOT NULL DEFAULT '0000-00-00',
  `hora_lan` varchar(5) NOT NULL DEFAULT '',
  `data_lem` datetime NOT NULL,
  `codusu_g` char(2) NOT NULL DEFAULT '',
  `status` char(2) NOT NULL DEFAULT '',
  `codcli` int(6) unsigned NOT NULL DEFAULT '0',
  `codpros` varchar(10) NOT NULL DEFAULT '',
  `asunto` varchar(30) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `leido` char(1) NOT NULL DEFAULT '',
  `posx` int(4) unsigned DEFAULT NULL,
  `posy` int(4) unsigned DEFAULT NULL,
  `largura` int(4) unsigned DEFAULT NULL,
  `altura` int(4) unsigned DEFAULT NULL,
  `aviso_lembrete` int(1) unsigned DEFAULT NULL,
  `cod_cor` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codlem`),
  KEY `codusu` (`codusu`),
  KEY `desktop` (`desktop`),
  KEY `codcli` (`codcli`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lembretes`
-- Table structure for table `nota_fiscal_transporte`
--

DROP TABLE IF EXISTS `nota_fiscal_transporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nota_fiscal_transporte` (
  `codnftra` char(10) NOT NULL,
  `codnf` char(10) NOT NULL COMMENT 'codigo nota_fiscal',
  `codfor` char(10) NOT NULL COMMENT 'codigo fornecedor',
  `adic_valor_bc_icms` char(1) NOT NULL DEFAULT '' COMMENT 'adicionar valor base de calculo icms',
  `mod_frete` char(1) NOT NULL DEFAULT '0' COMMENT 'Modalidade do frete',
  `valor_frete` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'valor do frete',
  `quant_volumes` int(15) NOT NULL DEFAULT '0' COMMENT 'Quantidade volumes transportados',
  `especie` varchar(60) NOT NULL DEFAULT '' COMMENT 'Espécie volumes transportados',
  `marca` varchar(60) NOT NULL DEFAULT '' COMMENT 'Marca volumes transportados',
  `numeracao` varchar(60) NOT NULL DEFAULT '' COMMENT 'Numeração volumes transportados',
  `peso_liquido` decimal(12,3) NOT NULL DEFAULT '0.000' COMMENT 'Peso Liquido em Kg',
  `peso_bruto` decimal(12,3) NOT NULL DEFAULT '0.000' COMMENT 'Peso Bruto em Kg',
  PRIMARY KEY (`codnftra`),
  KEY `codnf` (`codnf`),
  KEY `codfor` (`codfor`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_fiscal_transporte`
-- Table structure for table `dados_dispositivo`
--

DROP TABLE IF EXISTS `dados_dispositivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dados_dispositivo` (
  `coddisp` int(11) NOT NULL AUTO_INCREMENT,
  `id_dispositivo` int(11) NOT NULL DEFAULT '0',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `latitude` varchar(20) NOT NULL DEFAULT '',
  `longitude` varchar(20) NOT NULL DEFAULT '',
  `status_iclass` varchar(20) NOT NULL DEFAULT '',
  `usuario` varchar(20) NOT NULL DEFAULT '',
  `codtec` varchar(20) NOT NULL DEFAULT '',
  `status_bateria` varchar(20) NOT NULL DEFAULT '',
  `dados` text,
  PRIMARY KEY (`coddisp`),
  UNIQUE KEY `coddisp` (`coddisp`),
  KEY `codtec` (`codtec`),
  KEY `usuario` (`usuario`),
  KEY `data_hora` (`data_hora`),
  KEY `id_dispositivo` (`id_dispositivo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dados_dispositivo`
-- Table structure for table `informacoes_bi`
--

DROP TABLE IF EXISTS `informacoes_bi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `informacoes_bi` (
  `codibi` varchar(10) NOT NULL DEFAULT '',
  `menu` char(1) NOT NULL DEFAULT '',
  `nome_ibi` varchar(50) NOT NULL DEFAULT '',
  `formulario` varchar(30) NOT NULL DEFAULT '',
  `codigo` varchar(30) NOT NULL DEFAULT '',
  `tabela` varchar(50) NOT NULL DEFAULT '',
  `origem` char(1) NOT NULL DEFAULT '',
  `destino` char(2) NOT NULL DEFAULT '',
  `consulta_sql` mediumtext NOT NULL,
  `script_pos` mediumtext NOT NULL,
  PRIMARY KEY (`codibi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informacoes_bi`
-- Table structure for table `carteiras`
--

DROP TABLE IF EXISTS `carteiras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carteiras` (
  `codcart` varchar(10) NOT NULL DEFAULT '',
  `codu_f` char(3) NOT NULL DEFAULT '',
  `descri_cart` varchar(20) NOT NULL DEFAULT '',
  `carteira` char(2) NOT NULL DEFAULT '',
  `f_agencia` varchar(7) NOT NULL DEFAULT '',
  `f_conta` varchar(10) NOT NULL DEFAULT '',
  `f_cedente` varchar(15) NOT NULL DEFAULT '',
  `f_nosso_nro` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcart`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carteiras`
-- Table structure for table `dre`
--

DROP TABLE IF EXISTS `dre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dre` (
  `coddre` varchar(10) NOT NULL,
  `descri_dre` varchar(50) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  PRIMARY KEY (`coddre`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dre`
-- Table structure for table `traducao_componentes`
--

DROP TABLE IF EXISTS `traducao_componentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `traducao_componentes` (
  `codtct` varchar(10) NOT NULL,
  `codctl` varchar(10) NOT NULL,
  `codidm` varchar(10) NOT NULL,
  `caption` varchar(100) NOT NULL,
  `tooltips` varchar(254) NOT NULL,
  `value` varchar(100) NOT NULL,
  PRIMARY KEY (`codtct`),
  KEY `codctl` (`codctl`),
  KEY `codidm` (`codidm`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `traducao_componentes`
-- Table structure for table `detalhe_regras_sc`
--

DROP TABLE IF EXISTS `detalhe_regras_sc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detalhe_regras_sc` (
  `coddrsc` varchar(10) NOT NULL DEFAULT '',
  `codrsc` varchar(10) NOT NULL DEFAULT '',
  `campo` varchar(50) NOT NULL DEFAULT '',
  `valores` text NOT NULL,
  PRIMARY KEY (`coddrsc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalhe_regras_sc`
-- Table structure for table `valor_campo_fc`
--

DROP TABLE IF EXISTS `valor_campo_fc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valor_campo_fc` (
  `codvalcfc` char(10) NOT NULL,
  `codcampfc` char(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `valor_cfc` text NOT NULL,
  `codcob` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codvalcfc`),
  KEY `codcampfc` (`codcampfc`),
  KEY `codusu` (`codusu`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valor_campo_fc`
-- Table structure for table `integrator`
--

DROP TABLE IF EXISTS `integrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `integrator` (
  `codpar` char(1) NOT NULL DEFAULT '',
  `nome` varchar(20) NOT NULL DEFAULT '',
  `ddd` char(2) NOT NULL DEFAULT '',
  `cidade` varchar(8) NOT NULL DEFAULT '',
  `cep` varchar(9) NOT NULL DEFAULT '',
  `estado1` char(2) NOT NULL DEFAULT '',
  `estado2` char(3) NOT NULL DEFAULT '',
  `imagem` varchar(100) NOT NULL DEFAULT '',
  `ci` int(11) NOT NULL DEFAULT '0',
  `li` int(11) NOT NULL DEFAULT '0',
  `cor1` int(11) NOT NULL DEFAULT '0',
  `cor2` int(11) NOT NULL DEFAULT '0',
  `cor3` int(11) NOT NULL DEFAULT '0',
  `pasta_trabalho` varchar(100) NOT NULL DEFAULT '',
  `pasta_dados` varchar(100) NOT NULL DEFAULT '',
  `recurso` varchar(100) NOT NULL DEFAULT '',
  `quant_reg` int(11) NOT NULL DEFAULT '0',
  `remota` char(1) NOT NULL DEFAULT '',
  `dia_venc` varchar(10) NOT NULL DEFAULT '',
  `ultima_versao` date NOT NULL DEFAULT '0000-00-00',
  `dominio` varchar(20) NOT NULL DEFAULT '',
  `nro_ocorrencia` int(9) unsigned NOT NULL DEFAULT '0',
  `e_mail_teste` text NOT NULL,
  `ultima_nota_fiscal` int(8) NOT NULL DEFAULT '0',
  `unidade_tempo` char(1) NOT NULL DEFAULT 'H',
  PRIMARY KEY (`codpar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integrator`
-- Table structure for table `talkall_chat`
--

DROP TABLE IF EXISTS `talkall_chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `talkall_chat` (
  `codtac` char(10) NOT NULL DEFAULT '',
  `codcli` int(11) DEFAULT NULL,
  `chatid` int(11) DEFAULT NULL,
  `codusu` char(2) NOT NULL DEFAULT '',
  `data_hora_ini` datetime DEFAULT NULL,
  `data_hora_fim` datetime DEFAULT NULL,
  `chat` mediumtext,
  `status` char(1) DEFAULT '',
  `plataforma` char(1) NOT NULL DEFAULT '',
  `tipo` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`codtac`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `talkall_chat`
-- Table structure for table `nas_servers`
--

DROP TABLE IF EXISTS `nas_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nas_servers` (
  `codn_s` varchar(10) NOT NULL DEFAULT '',
  `codnr` varchar(10) NOT NULL DEFAULT '',
  `codservp` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codn_s`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nas_servers`
-- Table structure for table `movimentos_pat_bkp`
--

DROP TABLE IF EXISTS `movimentos_pat_bkp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movimentos_pat_bkp` (
  `codmvp` varchar(10) NOT NULL DEFAULT '',
  `codpat` varchar(10) NOT NULL DEFAULT '',
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codaqs` varchar(10) NOT NULL DEFAULT '',
  `codvpat` char(10) NOT NULL DEFAULT '',
  `codlmp` varchar(10) NOT NULL DEFAULT '',
  `codcon` int(4) unsigned NOT NULL DEFAULT '0',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codfor` varchar(10) NOT NULL DEFAULT '',
  `codords` char(10) NOT NULL DEFAULT '',
  `codprod` char(10) NOT NULL DEFAULT '',
  `codemp` varchar(10) NOT NULL DEFAULT '',
  `codcfop` char(10) NOT NULL DEFAULT '',
  `quantidade` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tipo_mov` char(1) NOT NULL DEFAULT '',
  `data` date NOT NULL DEFAULT '0000-00-00',
  `data_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atual` char(1) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  `vl_venda` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`codmvp`),
  KEY `codpat` (`codpat`),
  KEY `codlmp` (`codlmp`),
  KEY `codcon` (`codcon`),
  KEY `codsercli` (`codsercli`),
  KEY `codadq` (`codaqs`),
  KEY `codfor` (`codfor`),
  KEY `codcmp` (`codcmp`),
  KEY `atual` (`atual`),
  KEY `codords` (`codords`),
  KEY `codprod` (`codprod`),
  KEY `codcfop` (`codcfop`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentos_pat_bkp`
-- Table structure for table `tipo_cdf_produtos`
--

DROP TABLE IF EXISTS `tipo_cdf_produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cdf_produtos` (
  `codtcp` varchar(10) NOT NULL,
  `codtcdf` varchar(10) NOT NULL,
  `codprod` varchar(10) NOT NULL,
  PRIMARY KEY (`codtcp`),
  KEY `codtcdf` (`codtcdf`),
  KEY `codprod` (`codprod`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_cdf_produtos`
-- Table structure for table `webhook_talkall`
--

DROP TABLE IF EXISTS `webhook_talkall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webhook_talkall` (
  `codwta` int(11) NOT NULL AUTO_INCREMENT,
  `log` mediumtext,
  `data_hora` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id` int(11) DEFAULT NULL,
  `message` mediumtext,
  `plataforma` int(11) DEFAULT NULL,
  `tipo` char(1) NOT NULL DEFAULT '',
  `codtac` char(10) NOT NULL DEFAULT '',
  `codtaa` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codwta`),
  UNIQUE KEY `codwbtkall` (`codwta`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webhook_talkall`
-- Table structure for table `login_ivr`
--

DROP TABLE IF EXISTS `login_ivr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_ivr` (
  `codlivr` varchar(10) NOT NULL DEFAULT '',
  `codip` varchar(10) NOT NULL DEFAULT '',
  `codcemail` varchar(10) NOT NULL DEFAULT '',
  `login` varchar(30) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codlivr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_ivr`
-- Table structure for table `juros_razao`
--

DROP TABLE IF EXISTS `juros_razao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `juros_razao` (
  `codjraz` varchar(10) NOT NULL,
  `codraz` varchar(10) NOT NULL,
  `codcrec` varchar(10) NOT NULL,
  `valor_juros` float(10,2) NOT NULL,
  PRIMARY KEY (`codjraz`),
  KEY `codraz` (`codraz`),
  KEY `codcrec` (`codcrec`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juros_razao`
-- Table structure for table `int_commands`
--

DROP TABLE IF EXISTS `int_commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `int_commands` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `comando` varchar(50) NOT NULL DEFAULT '',
  `descricao` text NOT NULL,
  `status` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `int_commands`
-- Table structure for table `cargos_pgi`
--

DROP TABLE IF EXISTS `cargos_pgi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargos_pgi` (
  `codcarpgi` char(10) NOT NULL DEFAULT '',
  `codcar` char(10) NOT NULL DEFAULT '',
  `codgi` char(10) NOT NULL DEFAULT '',
  `ordem` int(11) NOT NULL DEFAULT '0',
  `codpgi` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`codcarpgi`),
  KEY `codcar` (`codcar`),
  KEY `codpgi` (`codpgi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos_pgi`
-- Table structure for table `tipo_servico_interface`
--

DROP TABLE IF EXISTS `tipo_servico_interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_servico_interface` (
  `codtservint` varchar(10) NOT NULL,
  `descri_tservint` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`codtservint`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_servico_interface`
-- Table structure for table `sub_categorias`
--

DROP TABLE IF EXISTS `sub_categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sub_categorias` (
  `codscat` varchar(10) NOT NULL DEFAULT '',
  `codcat` varchar(10) NOT NULL DEFAULT '',
  `descri_scat` varchar(50) NOT NULL DEFAULT '',
  `permite_mac` char(1) NOT NULL DEFAULT 'S',
  `obs` text NOT NULL,
  `codtscat` char(10) NOT NULL DEFAULT '01PADRAO',
  PRIMARY KEY (`codscat`),
  KEY `codcat` (`codcat`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_categorias`
-- Table structure for table `logins`
--

DROP TABLE IF EXISTS `logins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logins` (
  `ip` varchar(15) NOT NULL DEFAULT '',
  `login` varchar(20) NOT NULL DEFAULT '',
  `senha` varchar(30) NOT NULL DEFAULT '',
  `motivo` varchar(250) NOT NULL DEFAULT '',
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logins`
-- Table structure for table `linhas_voip`
--

DROP TABLE IF EXISTS `linhas_voip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linhas_voip` (
  `codlvp` varchar(10) NOT NULL DEFAULT '',
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `codtvp` varchar(10) NOT NULL DEFAULT '',
  `line_number` int(8) unsigned NOT NULL DEFAULT '0',
  `login` varchar(15) NOT NULL DEFAULT '',
  `senha` varchar(10) NOT NULL DEFAULT '',
  `e_mail` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codlvp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linhas_voip`
-- Table structure for table `status_tarefa`
--

DROP TABLE IF EXISTS `status_tarefa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status_tarefa` (
  `codstar` varchar(10) NOT NULL,
  `descri_star` varchar(50) NOT NULL DEFAULT '',
  `permite_execucao` char(1) DEFAULT 'N',
  PRIMARY KEY (`codstar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_tarefa`
-- Table structure for table `controle_mov_pat_apagar`
--

DROP TABLE IF EXISTS `controle_mov_pat_apagar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controle_mov_pat_apagar` (
  `codcmp` varchar(10) NOT NULL DEFAULT '',
  `codusu_g` char(2) NOT NULL DEFAULT '',
  `codusu_t` char(2) NOT NULL DEFAULT '',
  `codusu_c` char(2) NOT NULL DEFAULT '',
  `codlmp_o` char(10) NOT NULL DEFAULT '',
  `confirmado` char(1) NOT NULL DEFAULT '',
  `numero` int(6) NOT NULL DEFAULT '0',
  `code_f` varchar(10) NOT NULL DEFAULT '',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codcmp`),
  KEY `codusu_t` (`codusu_t`),
  KEY `codusu_c` (`codusu_c`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controle_mov_pat_apagar`
-- Table structure for table `tipo_acao`
--

DROP TABLE IF EXISTS `tipo_acao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_acao` (
  `codaco` char(1) NOT NULL DEFAULT '',
  `Descri_aco` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`codaco`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_acao`
-- Table structure for table `opcoes_cla_cli`
--

DROP TABLE IF EXISTS `opcoes_cla_cli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opcoes_cla_cli` (
  `codoclc` varchar(10) NOT NULL DEFAULT '',
  `codtclc` varchar(10) NOT NULL DEFAULT '',
  `descri_oclc` varchar(50) NOT NULL DEFAULT '',
  `porcentagem` float(5,2) NOT NULL DEFAULT '0.00',
  `obs` mediumtext NOT NULL,
  PRIMARY KEY (`codoclc`),
  KEY `codtclc` (`codtclc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opcoes_cla_cli`
-- Table structure for table `sacados`
--

DROP TABLE IF EXISTS `sacados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sacados` (
  `codsac` varchar(10) NOT NULL,
  `nome_sac` varchar(100) NOT NULL,
  PRIMARY KEY (`codsac`),
  KEY `nome_sac` (`nome_sac`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sacados`
-- Table structure for table `servidores_pop`
--

DROP TABLE IF EXISTS `servidores_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidores_pop` (
  `codservp` varchar(10) NOT NULL DEFAULT '',
  `id` int(3) unsigned NOT NULL DEFAULT '0',
  `host` varchar(50) NOT NULL DEFAULT '',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `data_base` varchar(20) NOT NULL DEFAULT '',
  `login` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `porta` varchar(5) NOT NULL DEFAULT '',
  `ip_valido` varchar(15) NOT NULL DEFAULT '',
  `senha_adm` varchar(10) NOT NULL DEFAULT '',
  `pasta` varchar(50) NOT NULL DEFAULT '',
  `url_rrdtool` varchar(100) NOT NULL DEFAULT 'admin/rrdtool/',
  `tipo` varchar(5) NOT NULL DEFAULT 'http',
  `codtservp` varchar(10) NOT NULL DEFAULT '',
  `codcrad` varchar(10) NOT NULL DEFAULT '',
  `isp` char(1) NOT NULL DEFAULT '',
  `ssh_ip` varchar(15) NOT NULL DEFAULT '',
  `ssh_ac` varchar(20) NOT NULL DEFAULT '',
  `ssh_sa` varchar(50) NOT NULL DEFAULT '',
  `ssh_p` varchar(20) NOT NULL DEFAULT '',
  `ssh_sr` varchar(20) NOT NULL DEFAULT '',
  `obs` text NOT NULL,
  `cripto` char(1) NOT NULL DEFAULT 'N',
  `c_ssl` char(1) NOT NULL DEFAULT 'S',
  `mac` varchar(12) NOT NULL DEFAULT '',
  `semintegrador` char(1) NOT NULL DEFAULT 'N',
  `ssh_key_path` varchar(100) NOT NULL,
  `padrao_elite` char(1) NOT NULL DEFAULT 'S',
  `ssh_private_key` varchar(256) NOT NULL,
  `ssh_public_key` varchar(256) NOT NULL,
  `colaborador` varchar(50) NOT NULL,
  `sgbd` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`codservp`),
  KEY `codtservp` (`codtservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidores_pop`
-- Table structure for table `servicos`
--

DROP TABLE IF EXISTS `servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos` (
  `codser` varchar(10) NOT NULL DEFAULT '',
  `codafi` varchar(10) NOT NULL DEFAULT '',
  `codgser` varchar(10) NOT NULL DEFAULT '',
  `codcob` char(10) NOT NULL DEFAULT '',
  `codcfps` varchar(4) NOT NULL,
  `codsts` varchar(10) NOT NULL,
  `data_ua` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `codigo_externo` varchar(20) NOT NULL,
  `descri_ser` varchar(100) NOT NULL,
  `formula` text NOT NULL,
  `data_cad` date NOT NULL,
  `tipo_pag` char(1) NOT NULL DEFAULT '',
  `carne` char(1) NOT NULL DEFAULT 'N',
  `codcta` varchar(9) NOT NULL DEFAULT '',
  `codctc` char(8) NOT NULL,
  `codest` varchar(10) NOT NULL DEFAULT '',
  `codmodc` varchar(10) NOT NULL DEFAULT '',
  `codgcom` char(10) NOT NULL,
  `cobra_taxa` char(1) NOT NULL DEFAULT 'N',
  `horas` int(6) unsigned NOT NULL DEFAULT '0',
  `d_trail` int(3) unsigned NOT NULL DEFAULT '0',
  `trial_proporcional` char(1) NOT NULL DEFAULT 'N',
  `q_dias_troca_plano` int(3) unsigned NOT NULL,
  `com_contrato` char(1) NOT NULL DEFAULT 'S',
  `obs` text NOT NULL,
  `quant_emails` int(2) unsigned NOT NULL DEFAULT '0',
  `valor_excedente` decimal(7,4) NOT NULL DEFAULT '0.0000',
  `valor_email_adicional` decimal(5,2) NOT NULL DEFAULT '0.00',
  `quota_email` decimal(5,2) NOT NULL DEFAULT '0.00',
  `permite_email` char(1) NOT NULL DEFAULT '',
  `permite_circuito` char(1) NOT NULL DEFAULT 'N',
  `permite_automacao` char(1) NOT NULL,
  `permite_onu` char(1) NOT NULL DEFAULT 'N',
  `permite_cir` char(1) NOT NULL DEFAULT 'N',
  `codservp_e` varchar(10) NOT NULL DEFAULT '',
  `permite_creditos` char(1) DEFAULT 'N',
  `autentica_radius` char(1) NOT NULL DEFAULT '',
  `codservp_r` varchar(10) NOT NULL DEFAULT '',
  `salva_c_dominio` char(1) NOT NULL DEFAULT 'N',
  `grupo_radius` varchar(15) NOT NULL DEFAULT '',
  `altera_senha_radius` char(1) NOT NULL DEFAULT 'N',
  `permite_dominio` char(1) NOT NULL DEFAULT '',
  `codservp_w` varchar(10) NOT NULL DEFAULT '',
  `servico_ivr` char(1) NOT NULL DEFAULT 'N',
  `ivr_down` int(6) NOT NULL DEFAULT '0',
  `ivr_up` int(6) unsigned NOT NULL DEFAULT '0',
  `comissao_vendedor` float(7,2) NOT NULL DEFAULT '0.00',
  `valor_fixo_comissao` char(1) NOT NULL DEFAULT '',
  `grafico` varchar(20) NOT NULL DEFAULT '',
  `web` char(1) NOT NULL DEFAULT '',
  `codpop` varchar(10) NOT NULL DEFAULT '',
  `cob_adiantada` char(1) NOT NULL DEFAULT 'N',
  `prop_cancel` char(1) NOT NULL DEFAULT 'S',
  `pontos_ser` decimal(5,2) NOT NULL DEFAULT '0.00',
  `obs_web` text NOT NULL,
  `valor_web` float(8,2) NOT NULL DEFAULT '0.00',
  `habi_web` decimal(7,5) NOT NULL DEFAULT '0.00000',
  `desconto_prorata` char(1) NOT NULL DEFAULT '',
  `permite_bd` char(1) NOT NULL DEFAULT '',
  `permite_voz` char(1) NOT NULL DEFAULT 'N',
  `permite_lav` char(1) NOT NULL DEFAULT 'N',
  `permite_tv` char(1) NOT NULL DEFAULT 'N',
  `desconto` float(8,5) NOT NULL DEFAULT '0.00000',
  `dias_desc` int(2) unsigned NOT NULL DEFAULT '0',
  `plano_vinculado` char(1) NOT NULL DEFAULT 'N',
  `permite_protestar` char(1) NOT NULL DEFAULT 'N',
  `permite_comodato` char(1) NOT NULL DEFAULT 'S',
  `precisa_autorizacao` char(1) NOT NULL DEFAULT 'N',
  `permite_stream` char(1) DEFAULT NULL COMMENT 'Disponibilizar o a opção Streaming Sim ou Nao',
  `codgrcom` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`codser`),
  KEY `codgser` (`codgser`),
  KEY `codsts` (`codsts`),
  KEY `codctc` (`codctc`),
  KEY `codgrcom` (`codgrcom`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos`
-- Table structure for table `codigo_api_bol`
--

DROP TABLE IF EXISTS `codigo_api_bol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codigo_api_bol` (
  `codlogbol` char(10) NOT NULL,
  `nro_ban` char(3) NOT NULL DEFAULT '',
  `codigo_api` char(10) NOT NULL DEFAULT '',
  `mensagem` text NOT NULL,
  `carteira` char(10) NOT NULL DEFAULT '',
  `descricao` text NOT NULL,
  `metodo` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codlogbol`),
  KEY `nro_ban` (`nro_ban`),
  KEY `carteira` (`carteira`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigo_api_bol`
-- Table structure for table `wholesale`
--

DROP TABLE IF EXISTS `wholesale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wholesale` (
  `codwsale` varchar(10) NOT NULL,
  `codsercli` varchar(10) NOT NULL,
  `carrier_id` double NOT NULL,
  `routeplan_id` double NOT NULL,
  `gateway_id` double NOT NULL,
  `costlist_id` double NOT NULL,
  `incoming_prefix` varchar(50) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `numero_a` varchar(20) NOT NULL,
  PRIMARY KEY (`codwsale`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wholesale`
-- Table structure for table `servicos_cli_new`
--

DROP TABLE IF EXISTS `servicos_cli_new`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicos_cli_new` (
  `codsercli` varchar(10) NOT NULL DEFAULT '',
  `data_new` date NOT NULL,
  PRIMARY KEY (`codsercli`),
  KEY `codsercli` (`codsercli`),
  KEY `data_new` (`data_new`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos_cli_new`
-- Table structure for table `valores_regras_cob`
--

DROP TABLE IF EXISTS `valores_regras_cob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_regras_cob` (
  `codvrc` varchar(10) NOT NULL,
  `codvcob` varchar(10) NOT NULL,
  `codrcob` varchar(10) NOT NULL,
  `valor` varchar(10) NOT NULL,
  PRIMARY KEY (`codvrc`),
  KEY `codvcob` (`codvcob`),
  KEY `codrcob` (`codrcob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_regras_cob`
-- Table structure for table `servidor_cas`
--

DROP TABLE IF EXISTS `servidor_cas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servidor_cas` (
  `codcas` varchar(10) NOT NULL,
  `codservp` varchar(10) NOT NULL,
  `descri_cas` varchar(50) NOT NULL,
  `porta` char(6) NOT NULL,
  PRIMARY KEY (`codcas`),
  KEY `codservp` (`codservp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidor_cas`
-- Table structure for table `log_elitesign`
--

DROP TABLE IF EXISTS `log_elitesign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_elitesign` (
  `codles` varchar(10) NOT NULL,
  `codcli` int(11) DEFAULT NULL,
  `codco_cl` varchar(10) DEFAULT NULL,
  `tipo_envio` char(1) DEFAULT 'E',
  `ip` varchar(100) DEFAULT NULL,
  `ip_reverso` varchar(100) DEFAULT NULL,
  `data_hora` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tipo_pessoa` char(1) DEFAULT 'C',
  `celular` varchar(100) DEFAULT NULL,
  `codsercli` varchar(10) DEFAULT NULL,
  `codmodc` varchar(10) DEFAULT NULL,
  `codsms` varchar(10) DEFAULT NULL,
  `codeem` varchar(10) DEFAULT NULL,
  `codace` varchar(10) DEFAULT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `cpf` varchar(18) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `status_ac` char(1) DEFAULT NULL,
  `obs_rejeicao` varchar(100) DEFAULT NULL,
  `tipo_contato` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`codles`),
  KEY `codco_cl` (`codco_cl`),
  KEY `codmodc` (`codmodc`),
  KEY `codsercli` (`codsercli`),
  KEY `codace` (`codace`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_elitesign`
-- Table structure for table `det_lacto_padrao`
--

DROP TABLE IF EXISTS `det_lacto_padrao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_lacto_padrao` (
  `coddetpad` char(10) NOT NULL,
  `codpadban` int(11) DEFAULT NULL COMMENT 'Codigo do Lancamento Padrao',
  `codpop` varchar(10) DEFAULT NULL COMMENT 'Codigo da Unidade de negocio',
  `codcta` varchar(10) DEFAULT NULL COMMENT 'Codigo da conta de demonstrativo',
  `codctc` char(8) NOT NULL,
  `valor_rat` double(10,2) DEFAULT NULL COMMENT 'Percentual do rateio',
  PRIMARY KEY (`coddetpad`),
  KEY `codctc` (`codctc`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `det_lacto_padrao`
-- Table structure for table `imp_contas_rec`
--

DROP TABLE IF EXISTS `imp_contas_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imp_contas_rec` (
  `codicr` varchar(10) NOT NULL DEFAULT '',
  `codtnf` varchar(10) NOT NULL,
  `codsimp` varchar(10) NOT NULL,
  `codscimp` varchar(10) NOT NULL,
  `codsai` varchar(10) NOT NULL,
  `codigo_fiscal` varchar(6) NOT NULL DEFAULT '',
  `iss` float(5,2) NOT NULL DEFAULT '0.00',
  `icms` float(5,2) NOT NULL DEFAULT '0.00',
  `fust` float(5,2) NOT NULL DEFAULT '0.00',
  `funtel` float(5,2) NOT NULL DEFAULT '0.00',
  `pis` float(5,2) NOT NULL DEFAULT '0.00',
  `cofins` float(5,2) NOT NULL DEFAULT '0.00',
  `ipi` float(5,2) NOT NULL DEFAULT '0.00',
  `iva` float(5,2) NOT NULL,
  PRIMARY KEY (`codicr`),
  KEY `codtnf` (`codtnf`),
  KEY `codsimp` (`codsimp`),
  KEY `codscimp` (`codscimp`),
  KEY `codsai` (`codsai`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imp_contas_rec`
-- Table structure for table `cargos`
--

DROP TABLE IF EXISTS `cargos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargos` (
  `codcar` varchar(10) NOT NULL DEFAULT '',
  `coddep` varchar(10) NOT NULL DEFAULT '',
  `nome_car` varchar(30) NOT NULL DEFAULT '',
  `nivel` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codcar`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos`
-- Table structure for table `registros_retorno`
--

DROP TABLE IF EXISTS `registros_retorno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registros_retorno` (
  `codrret` varchar(10) NOT NULL DEFAULT '',
  `codarq` varchar(10) NOT NULL DEFAULT '',
  `codfat` varchar(10) NOT NULL,
  `codraz` varchar(10) NOT NULL,
  `status` char(2) NOT NULL,
  `codcrr` varchar(10) NOT NULL,
  `nosso_numero` varchar(20) NOT NULL DEFAULT '',
  `nro_doc` varchar(10) NOT NULL DEFAULT '',
  `codigo_ctr` char(3) NOT NULL DEFAULT '',
  `motivos_oco` varchar(50) NOT NULL DEFAULT '',
  `data_oco` date NOT NULL DEFAULT '0000-00-00',
  `valor_doc` float(10,2) NOT NULL DEFAULT '0.00',
  `valor_juros` float(10,2) NOT NULL,
  `tipo` char(1) NOT NULL DEFAULT '',
  `codigo_crr` varchar(4) NOT NULL DEFAULT '',
  PRIMARY KEY (`codrret`),
  KEY `codarq` (`codarq`),
  KEY `codfat` (`codfat`),
  KEY `codraz` (`codraz`),
  KEY `status` (`status`),
  KEY `codcrr` (`codcrr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros_retorno`
-- Table structure for table `estoque_kit`
--

DROP TABLE IF EXISTS `estoque_kit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estoque_kit` (
  `codekit` varchar(10) NOT NULL,
  `id` bigint(12) NOT NULL AUTO_INCREMENT COMMENT 'ID estoquekit RBX',
  `descricao` varchar(50) NOT NULL COMMENT 'Descricao do kit',
  PRIMARY KEY (`codekit`),
  KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque_kit`
-- Table structure for table `centrais`
--

DROP TABLE IF EXISTS `centrais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `centrais` (
  `codctr` char(10) DEFAULT NULL COMMENT '||Centrals ID',
  `host` varchar(100) DEFAULT NULL COMMENT '||Centrals host',
  `uri` varchar(100) DEFAULT NULL COMMENT '||Centrals endpoint',
  `descri_ctr` varchar(100) DEFAULT NULL COMMENT '||Centrals  description',
  `versao` int(11) DEFAULT '5'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Rota=Centrals|Desc=|Grupo=CentralCustomer';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `centrais`
-- Table structure for table `historico_cpag`
--

DROP TABLE IF EXISTS `historico_cpag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_cpag` (
  `codhcpag` varchar(10) NOT NULL,
  `codcpag` varchar(10) NOT NULL,
  `codusu` char(2) NOT NULL,
  `data_hora` datetime NOT NULL,
  `ip` varchar(50) NOT NULL,
  `log` mediumtext NOT NULL,
  PRIMARY KEY (`codhcpag`),
  KEY `codcpag` (`codcpag`),
  KEY `codusu` (`codusu`),
  KEY `data_hora` (`data_hora`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_cpag`
-- Table structure for table `metas_indicadores`
--

DROP TABLE IF EXISTS `metas_indicadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metas_indicadores` (
  `codmind` varchar(10) NOT NULL,
  `codind` varchar(10) NOT NULL,
  `codtmi` varchar(10) NOT NULL,
  `descri_mind` varchar(50) NOT NULL,
  `tipo_meta` char(2) NOT NULL,
  `valor` float(10,2) NOT NULL,
  PRIMARY KEY (`codmind`),
  KEY `codind` (`codind`),
  KEY `codtmi` (`codtmi`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metas_indicadores`
-- Table structure for table `lista_campos_extra`
--

DROP TABLE IF EXISTS `lista_campos_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lista_campos_extra` (
  `codlcpx` varchar(10) NOT NULL DEFAULT '',
  `codcpx` varchar(10) NOT NULL DEFAULT '',
  `valor` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`codlcpx`),
  KEY `codcpx` (`codcpx`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lista_campos_extra`
-- Table structure for table `valores_parcelas_neg`
--

DROP TABLE IF EXISTS `valores_parcelas_neg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `valores_parcelas_neg` (
  `codvpn` varchar(10) NOT NULL,
  `codpneg` varchar(10) NOT NULL,
  `codvcob` varchar(10) NOT NULL,
  `valor` varchar(20) NOT NULL,
  PRIMARY KEY (`codvpn`),
  KEY `codpneg` (`codpneg`),
  KEY `codvcob` (`codvcob`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valores_parcelas_neg`
-- Table structure for table `tipo_recibo_doc`
--

DROP TABLE IF EXISTS `tipo_recibo_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_recibo_doc` (
  `codrdoc` varchar(10) NOT NULL,
  `coddoc` varchar(10) DEFAULT '',
  `descri_rec` varchar(25) NOT NULL,
  PRIMARY KEY (`codrdoc`),
  KEY `coddoc` (`coddoc`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_recibo_doc`
-- Table structure for table `tipo_origem_comercial`
--

DROP TABLE IF EXISTS `tipo_origem_comercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_origem_comercial` (
  `codtocm` varchar(10) NOT NULL,
  `codtab` varchar(10) NOT NULL,
  `ativo` char(1) NOT NULL,
  `descri_tocm` varchar(50) NOT NULL,
  `ordem` int(2) unsigned NOT NULL,
  `consulta_sql` mediumtext NOT NULL,
  PRIMARY KEY (`codtocm`),
  KEY `codtab` (`codtab`),
  KEY `ativo` (`ativo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_origem_comercial`
-- Table structure for table `tipo_conf_b_email`
--

DROP TABLE IF EXISTS `tipo_conf_b_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_conf_b_email` (
  `codtcbe` varchar(1) DEFAULT NULL,
  `descri_tcbe` varchar(60) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_conf_b_email`
