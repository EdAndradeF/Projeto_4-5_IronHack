import logging
import pandas
import psycopg2
import sqlalchemy



logger = logging.getLogger('sqlizer')
log = logger.info
warn = logger.warning


def appenddf(df, conect):
    name, df = df
    try:
        df.to_sql(name, conect, if_exists='append', index=False)
        log(msg=f'Tabela UF criada {name}')
    except Exception as e:
        warn(e, 'NAO NAO NAO NAO')


class DBQuerie:

    def __init__(self, conn, obj):

        self.conect = conn
        self.local = obj.local
        self.dfs = obj.ufdf

    def todb(self, so_local=False, so_eleitor=False):
        if not so_local:
            list(map(lambda x: appenddf(x, self.conect), self.dfs))
        if not so_eleitor:
            try:
                self.local[1].to_sql(self.local[0], self.conect, if_exists='replace', index=False)
                log(f'Tabela UF criada {self.local[0]}')
            except Exception as e:
                warn(e, 'NAO NAO NAO NAO')




if __name__ == '__main__':
    from ..db_conect import DBConn
    from ..params import Config as conf
    from .transformactor import EleitorDf


    conn = DBConn(conf())
    dfs = EleitorDf()
    query = DBQuerie(conn)

    stop = 'pots'