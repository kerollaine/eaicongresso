# coding=utf-8
__author__ = 'kerollaine'

import requests
import xml.etree.ElementTree as ET
import logging

class ImportarTipoProposicao(object):

    @staticmethod
    def executa(c):
        try:
            #Faz a requisicao para o ListarSiglasTipoProposicao
            r = requests.get("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSiglasTipoProposicao")
            logging.info('Requisição para o WS de listar tipos de proposições efetuada.')
        except Exception:
            logging.exception('Falha ao tentar conectar no WS.')
            quit()

        #Pega a string recebida e transforma em XML, e cria uma estrutura de acordo com as tags do arquivo
        root = ET.fromstring(r.content)
        c.execute('SELECT id FROM tipo_proposicao')
        logging.info('Iniciando rotina de sincronização do ListarSiglasTipoProposicao com a aplicação.')
        tiposSigla = map(lambda x: x[0],c.fetchall())
        if not tiposSigla:
            logging.warning('A rotina será executada para esta tabela pela primeira vez.')

        #Percorre o XML
        for tiposProposicao in root.findall('sigla'):
            id = tiposProposicao.get('tipoSigla')
            descricao = tiposProposicao.get('descricao')
            ativa = tiposProposicao.get('ativa')
            genero = tiposProposicao.get('genero')

            if int(id) not in tiposSigla:
                logging.debug('Inserção realizada, id: ' +id)
                sql = 'INSERT INTO situacao (id, descricao, ativa) VALUES (%(id)s, %(descricao)s, %(ativa)s, %(genero)s)'
                param = {'id': int(id), 'descricao': descricao, 'ativa': ativa, 'genero': genero}
                c.execute(sql, param)