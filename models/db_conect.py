from logging import getLogger
from os.path import abspath

import sqlalchemy as db
import psycopg2 as psy
import os
from dotenv import load_dotenv


env = load_dotenv('./.env')

logg = getLogger('db connect')
info = logg.info
warning = logg.warning


class DBConn:

    '''
    Conexão com banco de dados
    referenciado para PostgreSQL
    '''

    def __init__(self):

        '''
        parametros utilizados para criação da classe de conexão com Banco de dados
        ver parametros em ETL.params

        '''

        self.server = 'postgresql'
        self.user = os.getenv('postgre_user')
        self.password = os.getenv('postgre_senha')
        self.host = 'localhost'
        self.db_name = 'eleitoral'
        self.conector()

    def conector(self):
        try:
            self.eng = db.create_engine(f'{self.server}://{self.user}:{self.password}@{self.host}/{self.db_name}')
            self.conn = self.eng.connect()

            info(f'Conexão concluida')
        except Exception as e:
            warning(f'sem conexão {e}')

