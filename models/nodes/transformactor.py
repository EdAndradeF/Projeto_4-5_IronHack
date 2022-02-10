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

        # self.perfilnacional = []      # todo padrao de colunas
        self.ufdf = []                  # todo {'ano': {'UF': ['nome arquivo', ...], ...}, ...}

        self.comdeficiencia = []        # todo {'ano': {'UF': ['nome arquivo', ...], ...}, ...

        self.local = ()                 # todo {'ano': ['nome arquivo', ...], ...}
        self.localname = 'local'


        self.arquivos = arqs
        if not arqs:
            self.arquivos = os.listdir(pasta)

        log('mapping')
        list(map(self.organi, self.arquivos))
        'stop'

    def organi(self, filename):

        # EXEMPLO DE MODELO DAS TABELAS POR ESTADO
        if filtro('perfil_eleitorado_ATUAL', filename):
            pass


        # TABELAS DOS ESTADOS
        elif filtro('secao', filename):
            df = dtframe(self.pasta, filename)
            dropcolum = df.drop(columns=['DS_MUN_SIT_BIOMETRIA',
                                         'CD_MUN_SIT_BIOMETRIA'])
            # df['ANO_ELEICAO'] = df['ANO_ELEICAO'].str.replace('2022', '9999')
            self.ufdf.append((filename[-6:-4] ,dropcolum))
            log('secao')

        # LOCAIS DE VOTAÇÃO
        elif filtro('local', filename):
            df = dtframe(self.pasta, filename).drop(columns=['DT_ELEICAO',
                                                             'DS_ELEICAO', 'CD_TIPO_SECAO_AGREGADA',
                                                             'DS_TIPO_SECAO_AGREGADA', 'CD_TIPO_LOCAL',
                                                             'DS_TIPO_LOCAL', 'QT_ELEITOR_ELEICAO'])
            # df['AA_ELEICAO'] = df['AA_ELEICAO'].str.replace('2022', '9999')
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