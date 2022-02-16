import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from models.db_conect import DBConn


def latlong(linhas):
    try:
        uf = linhas['uf']
        cidade = linhas['nome_municipio'].capitalize().replace(' ', '_')
        url = f'https://www.apolo11.com/latlon.php?uf={uf}&cidade={cidade}'
        req = requests.get(url).content
        sopa = BeautifulSoup(req, 'lxml')
    except Exception as e:
        print(e, 'REQUESTS / SOPA')
    else:
        try:
            lati, long= sopa.find_all(style="margin-top:10px;font-family:courier")[0].text.split('\n')[1:3]
            long = re.findall('[-]?\d{1,2}', long)
            long = '.'.join(long[:2]) + long[2]
            lati = re.findall('[-]?\d{1,2}', lati)
            lati = '.'.join(lati[:2]) + lati[2]
        except Exception as e:
            print(e, 'get modify')

    linhas['latitude'] = lati
    linhas['longitude'] = long





conex = DBConn()
conn = conex.conn
query = pd.read_csv('data/cidades.csv')


query.to_sql("mapa", conn, if_exists='replace', index=False)



# query2 = query.apply(latlong, axis=1)

po=3