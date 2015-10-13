# coding=utf-8
__author__ = 'kerollaine'

import requests
import xml.etree.ElementTree as ET
import logging

class ImportarSituacao(object):

    @staticmethod
    def executa(c):
        try:
            #Faz a requisicao para o ListarSituacoesProposicao
            r = requests.get("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSituacoesProposicao")
            logging.info('Requisição para o WS de listar situações efetuada.')
        except Exception:
            logging.exception('Falha ao tentar conectar no WS.')
            quit()

        #Pega a string recebida e transforma em XML, e cria uma estrutura de acordo com as tags do arquivo
        root = ET.fromstring(r.content)
        c.execute('SELECT id FROM situacao')
        logging.info('Iniciando rotina de sincronização do ListarSituacoesProposicao com a aplicação.')
        ids_situacao = map(lambda x: x[0],c.fetchall())
        if not ids_situacao:
            logging.warning('A rotina será executada para esta tabela pela primeira vez.')

        #Percorre o XML
        for situacaoProposicao in root.findall('situacaoProposicao'):
            id = situacaoProposicao.get('id')
            descricao = situacaoProposicao.get('descricao')
            ativa = situacaoProposicao.get('ativa')

            if int(id) not in ids_situacao:
                logging.debug('Inserção realizada, id: ' +id)
                sql = 'INSERT INTO situacao (id, descricao, ativa) VALUES (%(id)s, %(descricao)s, %(ativa)s)'
                param = {'id': int(id), 'descricao': descricao, 'ativa': ativa}
                c.execute(sql, param)