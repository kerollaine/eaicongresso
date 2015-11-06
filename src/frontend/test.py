__author__ = 'kerollaine'
import psycopg2

class Teste:
    def __init__(self):
        try:
            con = psycopg2.connect(host='localhost', user='eaicongresso', password='eai2015cong', dbname='eaicongresso')
            c = con.cursor()
        except Exception:
            quit()

        c.execute('SELECT id_tema, COUNT(id_tema) FROM tema_proposicao GROUP BY id_tema')
        qtdProposicoes = [id[0][0] for id in c]

        for i in range(len(qtdProposicoes[0])):
            for item in qtdProposicoes:
                print(item[i])