import os
from os.path import abspath
from dotenv import load_dotenv, find_dotenv



class Config:


    env = load_dotenv(abspath('../.env'))


    # LOCAL DO ARQUIVO DE LOG
    log_name = abspath('../log/log.log')


    # LOCAIS DE ARQUIVOS EXTRAIDOS E TRANSFORMADOS
    csvs_pasta = abspath('../data/csvs/')
    csv_eleitor = abspath(f'{csvs_pasta}/csv_eleitor/')
    external_data = abspath('../data/external/')
    processed_data = abspath('../data/processed/')
    intermediate_data = abspath('../data/intermediate/')




