# coding=utf-8
__author__ = 'kerollaine'

import psycopg2
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import time
from random import randint
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

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


if __name__ == '__main__':
    app.run(debug=True)