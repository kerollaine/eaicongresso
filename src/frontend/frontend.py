# coding=utf-8
__author__ = 'kerollaine'

import string
import re
import nltk
from nltk.corpus import stopwords
from unicodedata import normalize
import psycopg2
from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

def processa_palavras(caracteres, cursor):

    stopwords_sem_acentuacao = [normalize('NFKD', palavra).encode('ASCII','ignore') for palavra in stopwords.words('portuguese')]
    conjunto_caracteres_a_substituir = '[\\!\\"\\#\\$\\%\\&\\\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\]\\^\\_\\`\\{\\|\\}\\~\\º\\ª]'

    caracteres = caracteres
    palavras = caracteres.lower()
    palavras = re.sub(conjunto_caracteres_a_substituir, ' ', palavras)
    palavras = nltk.word_tokenize(palavras, language='portuguese')
    palavras = [normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII') for palavra in palavras]
    palavras = [palavra for palavra in palavras if palavra not in stopwords_sem_acentuacao]
    palavras = [palavra for palavra in palavras if len(palavra) > 2]

    ids_palavras = []
    resultados = []

    for palavra in palavras:
        sql = 'SELECT id FROM palavra where descricao = %(palavra)s'
        param = {'palavra': palavra}

        cursor.execute(sql, param)
        tupla_retorno = cursor.fetchone()

        if tupla_retorno is not None:
            ids_palavras.append(tupla_retorno[0])

    if len(ids_palavras):
        sql = """SELECT nome, ementa, link_teor, data_apresentacao, count(*) AS ranking
                FROM proposicao
                    JOIN palavra_proposicao on id = id_proposicao
                WHERE id_palavra IN %(ids_palavra)s
                GROUP BY id
                ORDER BY ranking DESC
                LIMIT 50
        """
        param = {'ids_palavra': tuple(ids_palavras)}
        cursor.execute(sql, param)

        resultados = cursor.fetchall()

    return resultados


@app.route('/_get_tema')
def get_tema():
    try:
        con = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
        c = con.cursor()
    except Exception:
        quit()

    c.execute("""

        SELECT maiores.nome, maiores.contador
        FROM (
            SELECT t.descricao as nome, count(tp.id_tema) as contador
            FROM tema as t JOIN tema_proposicao as tp ON t.id = tp.id_tema
            WHERE id_tema <> 49
            GROUP BY id_tema, t.descricao
            ORDER BY contador DESC
            LIMIT 10
        ) maiores

        UNION

        SELECT 'Outros', SUM(menores.contador)::int
        FROM (
            SELECT count(tp.id_tema) as contador
            FROM tema as t JOIN tema_proposicao as tp ON t.id = tp.id_tema
            WHERE id_tema <> 49
            GROUP BY id_tema, t.descricao
            ORDER BY contador DESC
            OFFSET 10
        ) menores;

    """)

    temas = [tema for tema in c];

    return jsonify(output=temas)

@app.route('/_get_mes')
def get_mes():
    try:
        con = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
        c = con.cursor()
    except Exception:
        quit()

    c.execute("""SELECT EXTRACT ('Month' FROM data_apresentacao) as mes,
                    count(id)
                    FROM proposicao
                    WHERE data_apresentacao >= '2015-01-01' GROUP BY mes

    """)

    mes = [mes for mes in c];

    return jsonify(output=mes)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/temas')
def tema():
    return render_template('temas.html')


@app.route('/proposicaopormes')
def proposicaopormes():
    return render_template('mes.html')

@app.route('/indexacao', methods=['GET'])
def indexacao():

    try:
        con = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
        c = con.cursor()
    except Exception:
        quit()


    if 'palavras' in request.args:
        palavras = request.args['palavras']
        resultados = processa_palavras(palavras, c)

    else:
        palavras = None
        resultados = None

    return render_template('indexacao.html', palavras=palavras, resultados=resultados)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

