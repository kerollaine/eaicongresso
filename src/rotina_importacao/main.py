# coding=utf-8
__author__ = 'kerollaine'

import psycopg2
import logging
from threading import Thread
import time
from subrotinas.importar_situacao import ImportarSituacao
from subrotinas.contador_proposicao import ContadorProposicao
from subrotinas.importar_tramitacao import ImportarTramitacao
from subrotinas.importar_proposicao import ImportarProposicao

try:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='rotina_importacao.log',
                        filemode='a')
    logging.info('Rotina de importação iniciada.')

    #Faz a conexao com o banco de dados, utilizado em outras rotinas como a importação de tramitações
    try:
        con = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
        c = con.cursor()
        logging.info('Conexão com o banco de dados estabelecida.')
    except Exception:
        logging.exception('Erro ao tentar conectar com o banco de dados.')
        quit()

    # ImportarSituacao.executa(c)
    # ContadorProposicao.executa(c)

    #Já foi executado uma vez, de 2010 até 2015. Tramitação não pode ser importada duas vezes.
    for i in range(2010,2016):
        anoImportacao = i;
        ImportarTramitacao.executa(c, anoImportacao)

    con.commit()

    def obterproposicao(offset):
        try:
            conexao = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
            logging.info('Conexão com o banco de dados estabelecida.')
        except Exception:
            logging.exception('Erro ao tentar conectar com o banco de dados.')
            quit()

        ImportarProposicao.executa(conexao, offset)

    threads = []

    while c.execute('SELECT count(id_proposicao) FROM importacao_proposicao WHERE desatualizada=true') >= 1:
        for x in range(0, 7):
            t = Thread(target=obterproposicao, args=(x*10, ))
            t.start()
            time.sleep(1)
            threads.append(t)

        for t in threads:
            t.join()

    logging.info('Rotina de importação finalizada.')

except Exception:
    logging.exception('Ocorreu um erro. Exceção abaixo.')
    quit()