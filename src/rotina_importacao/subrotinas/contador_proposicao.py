# coding=utf-8
__author__ = 'kerollaine'

import requests
import xml.etree.ElementTree as ET
import logging

class ContadorProposicao(object):

    @staticmethod
    def executa(c):
        try:
            #Faz a requisicao para o ListarSiglasTipoProposicao
            r = requests.get("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSiglasTipoProposicao")
            logging.info('Requisição para o WS de listar tipos de proposições efetuada.')
        except Exception:
            logging.exception('Falha ao tentar conectar no WS.')
            quit()

        #Pega a string recebida e transforma em XML
        root = ET.fromstring(r.content)
        siglas = set()
        #Percorre o XML

        for siglaProposicao in root.findall('sigla'):
            siglas.add(siglaProposicao.get('tipoSigla').rstrip())

        logging.info('Criado conjunto de siglas de de tipo de proposição')

        try:
            total = 0
            #Faz a requisicao para o ListarProposicoes
            for sigla in siglas:
                payload = {'sigla': sigla, 'numero': '', 'ano': '2015', 'datApresentacaoIni': '', 'datApresentacaoFim': '', 'idTipoAutor': '', 'parteNomeAutor': '', 'siglaPartidoAutor': '', 'siglaUFAutor': '', 'generoAutor': '', 'codEstado': '', 'codOrgaoEstado' : '', 'emTramitacao': ''}
                r = requests.get("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes", params = payload)
                root = ET.fromstring(r.content)
                total += len(root.findall('proposicao'))
                print("Subtotal: " + str(total) + " - Sigla: " +sigla)

            print total

            quit()
            logging.info('Requisição para o WS de listar proposições efetuada.')
        except Exception:
            logging.exception('Falha ao tentar conectar no WS.')
            quit()
