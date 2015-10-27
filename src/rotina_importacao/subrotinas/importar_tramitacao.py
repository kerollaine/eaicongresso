# coding=utf-8
__author__ = 'kerollaine'

import requests
import xml.etree.ElementTree as ET
import logging
import datetime
from datetime import date


def intervaloDatas(inicio, fim, dias):
    while inicio <= fim:
        yield inicio
        inicio += datetime.timedelta(days=dias)


class ImportarTramitacao(object):

    @staticmethod
    def executa(c,ano):
        try:
            if (ano == 2015):
                mes = 10
                dia = 26
            else:
                mes = 12
                dia = 31

            for dia in intervaloDatas(date(ano, 1, 1), date(ano, mes, dia), 7):
                diaFinal = dia + datetime.timedelta(days=6)
                #Faz a requisicao para o listarProposicoesTramitadasNoPeriodo
                payload = {'dtInicio': dia.strftime('%d/%m/%Y'), 'dtFim': diaFinal.strftime('%d/%m/%Y')}
                r = requests.get("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesTramitadasNoPeriodo", params=payload)
                logging.info('Requisição para o WS de listar proposições tramitadas no período efetuada.')

                if (r.text.find('Dados n&#227;o encontrados.') != -1):
                    logging.info("Dados nao encontrados para o intervalo de datas: "+ str (dia) +" | " + str(diaFinal) )
                    continue

                #Verificar o que consta na pagina e depois importar
                root = ET.fromstring(r.content)

                for tramitacao in root.findall('proposicao'):
                    idProposicao = int(tramitacao.find('codProposicao').text)
                    data = tramitacao.find('dataTramitacao').text

                    sql = 'SELECT importar_tramitacao (%(id_proposicao)s, %(data)s)'
                    param = {'id_proposicao': idProposicao, 'data': data}
                    c.execute(sql, param)
                    logging.debug('Função importar_tramitacao executada para o id: ' + str(idProposicao) + ' e para o intervalo de datas: '+ str (dia) +' | ' + str(diaFinal))

        except Exception:
            logging.exception('Falha ao importar a tramitação.')
            quit()
