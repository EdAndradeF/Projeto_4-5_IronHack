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

    def __init__(self, nome):

        '''

        nome recebe o nome do banco de dados a ser conectado

        parametros de senha e usuario, utilizados para criação da classe de conexão com Banco de dados
        configurados noo arquivo .env do repositorio

        '''

        self.server = 'postgresql'
        self.host = 'localhost'
        self.db_name = nome
        # seguranca e privacidade esses atributos sao usados de maneira direta e por instancia
        # self.senha = os.getenv("postgre_senha")
        # self.uer = os.getenv("postgre_user")


        try:
            self.eng = db.create_engine(f'{self.server}://{os.getenv("postgre_user")}:{os.getenv("postgre_senha")}@{self.host}/{self.db_name}')
            self.conn = self.eng.connect()

            info(f'postgreSQL conectado')
        except Exception as e:
            warning(f'sem conexão com banco {e}')

