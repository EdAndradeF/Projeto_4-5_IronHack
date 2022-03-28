import functools
import requests
import logging
import os
# from multiprocessing import Pool
from bs4 import BeautifulSoup
from zipfile import ZipFile

from params import Config as conf


#   todo tratar excepts indiviualmente



logger = logging.getLogger('Extract')
log = logger.info
bad = logger.warning


def downzipfeito(url, pasta):
    arqzip = url.split('/')[-1]
    list_arq = os.listdir(pasta)
    nozip = [x[:-4] for x in list_arq]
    if arqzip in list_arq:
        os.remove(pasta+'/'+arqzip)
        return False
    elif arqzip[:-4] in nozip:
        return True
    return False


def down( url, pasta):

    '''
        DOWNLOAD DE ARQUIVOS VIA ENDEREÇO HTML
    :param url: str com endereço do download
    :param pasta: nome do repositorio a savar o download
    :return: o nome do arquivo (salva arquivos em pastas especifica INPLACE)
    '''

    arqlink = requests.get(url)
    if pasta.split('/')[-1] not in os.listdir('../../data/csvs'):
        os.mkdir(pasta)
        log('pasta criada')

    try:
        arq = url.split("/")[-1]
        log('abrindo o zip')

        with open(pasta + '/' + arq, 'wb') as a:
            for ar in arqlink.iter_content(chunk_size=None):
                if a:
                    a.write(ar)
                    log(f'arquivo {arq} salvo')
    except Exception as ex:
        bad(f'download nao concluido {url}: \n {ex} ')
    else:
        return url.split("/")[-1]


def deszip(arq, pasta):
    try:
        with ZipFile(pasta + '/' + arq, 'r') as arq_zip:
            arq_ext = [x for x in arq_zip.namelist() if x.endswith('.csv') or x.endswith('.txt')]
            arq_zip.extractall(members=arq_ext, path=pasta)
            log('extaction complete :P')
    except Exception as e:
        bad(f'arquivo nao extraido {e}')


def ziptodata(url, pasta):
    if not downzipfeito(url, pasta):
        arqzip = down(url, pasta)
        deszip(arqzip, pasta)
        try:
            os.remove(pasta + '/' + arqzip)
        except Exception as e:
            bad(f'arquivo {arqzip}nao quer ser apagado')
    else:
        log('nada pra fazer')


class TSEget:

    '''
    classe pai
    possui os atributos padroes como:
                url principal do site
                e configuracao fenix
    '''

    site = 'https://dadosabertos.tse.jus.br/'

    def __init__(self, modo_fenix=False):

        '''
            url: url do site de dados abertos do TRIBUNAL SUPERIOR ELEITORAL
            sopa: retorno da funcao panela
            _fenix (padrao = false): se True abilita restruturacao total, sem verificacao para processos
        '''

        self.url = self.site
        self.sopa = self.panela(self.url)
        self._fenix = modo_fenix

    def req(self, url):
        '''
        recebe endereco para request e retorna response objeto se code 200
        se qualquer outro resultado retorna none
        '''

        # todo criar excecao para status code

        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                log(f'YAHOOOWW... STATUS CODE {resposta.status_code}')
                return resposta.content
            else:
                log(f'aaa nao STATUS CODE = {resposta.status_code}')
        except Exception as e:
            log(f'XP, Erro no requerimento {e}')

    def panela(self, content):

        '''

        recebe string (url) ou conteudo de objeto (<response 200>) e retorna uma linda sopa

        '''
        if isinstance(content, str):
            try:
                content = self.req(content).content
                log('link requerido com sucesso')
            except BaseException as ex:
                log(ex, '\n nao era link')
        try:
            caldo = BeautifulSoup(content, 'lxml')
            log('preparando caldo, humm......')
            return caldo
        except:
            log('problema na sopa')


class AGELget(TSEget):

    '''
    Assessoria de Gestão Eleitoral
    '''

    def __init__(self):
        super().__init__()
        self.url = self.site+'dataset/?organization=tse-agel'
        self.sopa = self.panela(self.url)


class Eleitorado(AGELget):

    # repositorio o qual serao salvos os arquivos de dados
    pasta = r'C:\Users\eandr\Meu Drive\IronHack\Work\modolo 2\Projetos\data_visualization\data\csvs\csv_eleitor'

    def __init__(self, ano='atual'):
        if 'data' in  os.listdir('../'):
            self.arq_exist = os.listdir(self.pasta)

        super().__init__()
        self.url = self.url+'&groups=eleitorado'

        self.sopa = self.panela(self.url)
        self.link = self.linkatual(ano)
        self.csv_novo = self.lista_csvs()

    def linkatual(self, ano):
        for tag in self.sopa.findAll('h2', 'dataset-heading'):
            if ano in tag.contents[1].attrs['href']:
                return [self.url + tag.contents[1].attrs['href']]


    # opção de metodo para todos os anos separados por tipo de eleição
    # FOI TRABALHOSO NAO APAGAR ;p!
    # def list_anos(self):
    #     nacio = munic = []
    #     atual = ''
    #     try:
    #         for tag in self.sopa.findAll('h2', 'dataset-heading'):
    #             link = self.url+tag.contents[1].attrs['href']
    #             try:
    #                 ano = int(link[-4:])
    #                 pos_real = ano >= 1994
    #                 if pos_real:
    #                     if ano % 4:
    #                         nacio.append(link)
    #                     else:
    #                         munic.append(link)
    #             except ValueError:
    #                 if 'atual' in link:
    #                     atual = link
    #         retorno = {'municipal': munic, 'nacional': nacio, 'atual': atual}
    #         log(f'retornado links: minicipal>{len(munic)} | nacional>{len(nacio)} | atual>{len(atual)}')
    #         return retorno
    #
    #     except Exception as ex:
    #         log(f'problema list_link em Eleitorado {ex}')


    # FOI TRABALHOSO NAO APAGAR ;p!


    def lista_csvs(self):
        lista = []
        # links = self.link['municipal']+[self.link['atual']]+self.link['nacional']
        links = self.link
        # pool = Pool(processes=3)
        for x in links:
            sopa = self.panela(x).findAll('a', 'resource-url-analytics')
            listxt = list(map((lambda x: x.attrs['href'] if x.text else None), sopa))
            # testando imap map imap_unordered
            l = list(map(functools.partial(ziptodata, pasta=self.pasta), listxt))
            # l = list(pool.imap(functools.partial(ziptodata, pasta=self._pasta), listxt))
            lista.append(l)
        # pool.terminate()
        return lista


if __name__ == '__main__':
    logging.root.handlers = []
    logging.basicConfig(filename='../../log/loginho.log',
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # s = AGELget()
    # t = TSEget()
    e = Eleitorado()

    print()















