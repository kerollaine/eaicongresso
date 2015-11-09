# coding=utf-8
__author__ = 'kerollaine'

import re
import nltk
from nltk.corpus import stopwords
from unicodedata import normalize
import logging

logging.info('Definindo conjuntos a substituir e stopwords sem acentuação.')
stopwords_sem_acentuacao = [normalize('NFKD', palavra).encode('ASCII','ignore') for palavra in stopwords.words('portuguese')]
conjunto_caracteres_a_substituir = '[\\!\\"\\#\\$\\%\\&\\\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\]\\^\\_\\`\\{\\|\\}\\~\\º\\ª]'

def processa_palavras(caracteres, cursor):

    logging.info('Decodifica o texto recebido - utf8.')
    caracteres = caracteres.decode('utf8')
    palavras = caracteres.lower()
    logging.info('Lowercase em todos os caracteres.')
    palavras = re.sub(conjunto_caracteres_a_substituir, ' ', palavras)

    logging.info('Processa tozekine.')
    palavras = nltk.word_tokenize(palavras, language='portuguese')
    palavras = [normalize('NFKD', palavra).encode('ASCII','ignore') for palavra in palavras]
    palavras = [palavra for palavra in palavras if palavra not in stopwords_sem_acentuacao]
    palavras = [palavra for palavra in palavras if len(palavra) > 2]

    ids_palavras = []

    logging.info('Processa a palavra no banco de dados.')
    for palavra in palavras:
        #palavra = normalize('NFKD', palavra).encode('ASCII','ignore')
        sql = 'SELECT id FROM palavra where descricao = %(palavra)s'
        param = {'palavra': palavra}

        cursor.execute(sql, param)
        tupla_retorno = cursor.fetchone()

        if tupla_retorno is not None:
            ids_palavras.append(tupla_retorno[0])

        else:
            sql = 'INSERT INTO palavra(descricao) VALUES (%(palavra)s) RETURNING id'
            cursor.execute(sql, param)
            id_retorno = cursor.fetchone()[0]
            ids_palavras.append(id_retorno)

    return ids_palavras


class ProcessarPalavras(object):

    @staticmethod
    def executa(connection):
        c_proposicoes = connection.cursor()
        c_temas = connection.cursor()
        c_persistencia = connection.cursor()

        c_proposicoes.execute('SELECT id, ementa FROM proposicao WHERE indexada = false')
        proposicao = c_proposicoes.fetchone()

        while proposicao is not None:
            id = proposicao[0]
            ementa = proposicao[1]
            ids_palavras = []

            ids_palavras += processa_palavras(ementa, c_persistencia)

            c_temas.execute('SELECT descricao FROM tema JOIN tema_proposicao on id = id_tema where id_proposicao = ' + str(id))
            tema = c_temas.fetchone()

            while tema is not None:
                ids_palavras += processa_palavras(tema[0], c_persistencia)
                tema = c_temas.fetchone()

            c_persistencia.execute('DELETE FROM palavra_proposicao WHERE id_proposicao = ' + str(id))

            for id_palavra in ids_palavras:
                sql = """INSERT INTO palavra_proposicao (id_palavra, id_proposicao)
                        VALUES (%(id_palavra)s, %(id_proposicao)s)"""

                params = {'id_palavra': id_palavra, 'id_proposicao': id}
                c_persistencia.execute(sql, params)
                c_persistencia.execute('UPDATE proposicao SET indexada = true WHERE id ='+ str(id))

            proposicao = c_proposicoes.fetchone()

            logging.info('Commita indexação da proposição, id '+ str(id))
            connection.commit()
