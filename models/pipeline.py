import logging

from models.nodes.extractor import Eleitorado
from models.nodes.loador import DBQuerie
from models.nodes.transformactor import EleitorDf
from params import Config as conf
from db_conect import DBConn


def setlog():
    logging.basicConfig(filename=conf.log_name,
                        filemode='a',
                        format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)


def processo(con, arg):
    ...





if __name__ == "__main__":
    setlog()
    connbd = DBConn(conf)

    getelei = Eleitorado()
    df = EleitorDf(getelei.pasta, getelei.arq_exist)
    sql = DBQuerie(connbd.conn, df)

    sql.todb()

    connbd.conn.close()
