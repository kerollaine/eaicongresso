# coding=utf-8
__author__ = 'kerollaine'

import psycopg2
import logging
from subrotinas.importar_situacao import ImportarSituacao
from subrotinas.contador_proposicao import ContadorProposicao

try:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='rotina_importacao.log',
                        filemode='a')
    logging.info('Rotina de importação iniciada.')

    #Faz a conexao com o banco de dados
    try:
        con = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
        c = con.cursor()
        logging.info('Conexão com o banco de dados estabelecida.')
    except Exception:
        logging.exception('Erro ao tentar conectar com o banco de dados.')
        quit()

#    ImportarSituacao.executa(c)
    ContadorProposicao.executa(c)

    con.commit()
    logging.info('Rotina de importação finalizada.')

except Exception:
    logging.exception('Ocorreu um erro.')