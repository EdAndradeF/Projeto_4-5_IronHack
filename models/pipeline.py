import logging

from nodes.extractor import Eleitorado
from nodes.loador import DBQuerie
from nodes.transformactor import EleitorDf
from params import Config as conf
from db_conect import DBConn


def setlog():

    '''
    Configuracao do resgistro de log
    '''

    logging.basicConfig(filename=conf.log_name,
                        filemode='a',
                        format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)


def processo(config):
    setlog()

    connbd = DBConn('eleitoral')
    getelei = Eleitorado()
    df = EleitorDf(getelei.pasta, getelei.arq_exist)
    sql = DBQuerie(connbd.conn, df)
    sql.todb()
    connbd.conn.close()



if __name__ == "__main__":
    processo(conf)
