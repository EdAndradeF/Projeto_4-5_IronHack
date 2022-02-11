import os

import pandas
import logging
import pandas as pd

logger = logging.getLogger('Tratament')
log = logger.info


def filtro(filtro, filename):
    if filtro in filename:
        return True
    return False


def dtframe(pasta, filename):
    try:
        df = pd.read_csv(f'{pasta}/{filename}', encoding='latin 1', sep=';')
        log('df feito')
    except Exception as e:
        logger.warning(e)
    else:
        return df


class EleitorDf:

    def __init__(self, pasta, arqs=None):
        self.pasta = pasta

        # self.perfilnacional = []
        self.ufdf = []

        self.comdeficiencia = []

        self.local = ()
        self.localname = 'local'


        self.arquivos = arqs
        if not arqs:
            self.arquivos = os.listdir(pasta)

        log('mapping')
        list(map(self.organi, self.arquivos))
        s = 'stop'

    def organi(self, filename):

        # EXEMPLO DE MODELO DAS TABELAS POR ESTADO
        if filtro('perfil_eleitorado_ATUAL', filename):
            pass


        # TABELAS DOS ESTADOS
        elif filtro('secao', filename):
            df = dtframe(self.pasta, filename)
            dropcolum = df.drop(columns=['DS_MUN_SIT_BIOMETRIA', 'HH_GERACAO',
                                         'CD_MUN_SIT_BIOMETRIA', 'QT_ELEITORES_INC_NM_SOCIAL'])
            dropcolum['ANO_ELEICAO'] = dropcolum['ANO_ELEICAO'].apply(lambda x: x - (x - 2022))
            dropcolum.columns = ['data', 'ano_eleicao', 'uf', 'id_municipio', 'nome_municipio',
                                 'numero_zona', 'numero_secao', 'id_genero', 'genero', 'id_estado_civil',
                                 'estado_civil', 'id_faixa_etaria', 'faixa_etaria', 'id_escolaridade',
                                 'escolaridade', 'quantidade_eleitores', 'quantidade_biometria', 'deficientes']
            self.ufdf.append(('eleitorado_2022', dropcolum))
            log('secao')

        # LOCAIS DE VOTAÇÃO
        elif filtro('local', filename):
            df = dtframe(self.pasta, filename).drop(columns=['DT_ELEICAO', 'HH_GERACAO',
                                                             'DS_ELEICAO', 'CD_TIPO_SECAO_AGREGADA',
                                                             'DS_TIPO_SECAO_AGREGADA', 'CD_TIPO_LOCAL',
                                                             'DS_TIPO_LOCAL', 'QT_ELEITOR_ELEICAO'])
            df['AA_ELEICAO'] = df['AA_ELEICAO'].apply(lambda x: x - (x - 2022))
            df.columns = ['data', 'ano', 'uf', 'id_municipio', 'nome_municipio', 'numero_zona', 'numero_secao',
                'numero_local', 'nome_local', 'endereco', 'bairro', 'cep', 'numero', 'latitude', 'longitude',
                'id_situacao_local', 'situacao_local', 'id_situacao_zona', 'situacao_zona', 'id_situacao_secao',
                'situacao_secao', 'id_situacao_localidade','situacao_localidade', 'quantidade_eleitores']

            self.local = ('local', df)
            log('local')



        # todo projeto 0.2
        # TABELA PCDs
        # elif filtro('deficiencia', filename):
        #     log('deficiencia')
        #     self.comdeficiencia.append(dtframe(self.pasta, filename))




if __name__ == '__main__':
    from ..pipeline import setlog

    setlog()

    s = EleitorDf('../csvs/csv_eleitor')

    print()