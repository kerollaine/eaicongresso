# coding=utf-8
__author__ = 'kerollaine'

import requests
import xml.etree.ElementTree as ET
import logging
import datetime

def string_para_inteiro_ou_null(param):
    if not param:
        return None
    else:
        return int(param)

def string_para_data_ou_null(param):
    if not param:
        return None
    else:
        return datetime.datetime.strptime(param, '%d/%m/%Y').date()

class ImportarProposicao(object):

    @staticmethod
    def executa(conexao, offset):
        c = conexao.cursor()

        logging.info('Busca por todas as proposições desatualizadas.')

        sql = 'SELECT id_proposicao FROM importacao_proposicao WHERE desatualizada = true OFFSET ' + str(offset) + ' LIMIT 10'
        c.execute(sql)
        ids_proposicao = [id[0] for id in c]

        if not ids_proposicao:
            logging.info('Nenhuma proposição está desatualizada.')
            quit()

        try:

            for id in ids_proposicao:
                payload = {'idProp': id}
                r = requests.get("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID", params=payload)
                logging.info('Requisição para o WS de obter proposição por id efetuada.')

                # Pega a string recebida e transforma em XML, e cria uma estrutura de acordo com as tags do arquivo
                proposicao = ET.fromstring(r.content)
                logging.info('Percorrendo o XML')
                # Percorre o XML
                id = proposicao.find('idProposicao').text.strip()
                nome = proposicao.find('nomeProposicao').text.strip()
                numero = proposicao.get('numero').strip()
                ano = proposicao.get('ano').strip()
                data_ap = proposicao.find('DataApresentacao').text.strip()
                data_desp = proposicao.find('UltimoDespacho').get('Data').strip()
                ementa = proposicao.find('Ementa').text.strip()
                exp_ementa = proposicao.find('ExplicacaoEmenta').text.strip()
                indexacao = proposicao.find('Indexacao').text.strip()
                link = proposicao.find('LinkInteiroTeor').text.strip()
                autor = proposicao.find('Autor').text.strip()
                uf_autor = proposicao.find('ufAutor').text.strip()
                partido_autor = proposicao.find('partidoAutor').text.strip()
                sigla_tipo_proposicao = proposicao.get('tipo').strip()
                descricao_tipo_proposicao = proposicao.find('tipoProposicao').text.strip()
                situacao_proposicao = proposicao.find('Situacao').text.strip()
                tema = proposicao.find('tema').text.strip()

                logging.info('Chamando function obter_proposicao')

                sql = 'SELECT obter_proposicao(%(p_id)s, %(p_nome)s, %(p_numero)s, %(p_ano)s, %(p_data_ap)s, %(p_data_despacho)s, %(p_ementa)s, '
                sql = sql + '%(p_explicacao_ementa)s, %(p_indexacao)s, %(p_link)s, %(p_autor)s, %(p_autoruf)s, '
                sql = sql + '%(p_autorpartido)s, %(p_tipo)s, %(p_tiposigla)s, %(p_situacao)s, %(p_tema)s)'

                param = {'p_id': string_para_inteiro_ou_null(id), 'p_nome': nome, 'p_numero': string_para_inteiro_ou_null(numero), 'p_ano': string_para_inteiro_ou_null(ano),
                         'p_data_ap': string_para_data_ou_null(data_ap), 'p_data_despacho': string_para_data_ou_null(data_desp),
                         'p_ementa': ementa, 'p_explicacao_ementa': exp_ementa, 'p_indexacao': indexacao, 'p_link': link, 'p_autor': autor,
                         'p_autoruf': uf_autor, 'p_autorpartido': partido_autor, 'p_tipo': descricao_tipo_proposicao, 'p_tiposigla': sigla_tipo_proposicao,
                         'p_situacao': situacao_proposicao, 'p_tema': tema
                         }
                c.execute(sql, param)
                conexao.commit()
                logging.debug('Função obter_proposicao executada para o id: ' + str(id))

        except Exception:
            logging.exception('Ocorreu um erro, veja detalhes abaixo.')
            quit()
