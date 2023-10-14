import os, logging


def print_log(msg):
    '''
    escreve o log no cmd e no log
    '''
    print(msg)
    logging.info(msg)

def setup_log():     
    '''
    Setup do log, salva com data horário e outras informaçoes que forem adicionadas no cod.
    '''   
    log_filename = os.path.join(os.getcwd(), "movies.log")
    
    # Configuração básica do logger
    logging.basicConfig(level=logging.INFO)
    
    # Cria um handler de arquivo com a codificação desejada
    file_handler = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
    
    # Define o formato do log
    formatter = logging.Formatter('%(asctime)s :: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    file_handler.setFormatter(formatter)
    
    # Adiciona o handler ao logger
    logging.getLogger('').addHandler(file_handler)

DICT_URLS = {'URL_250':'https://www.imdb.com/chart/top/?ref_=nv_mv_250',
             'PIOR_AVALI':'https://www.imdb.com/chart/bottom/?ref_=chttp_ql_7',
             'MAIS_POPULARES':'https://www.imdb.com/chart/moviemeter/?ref_=chttp_ql_2',
             'PRINCI_BILHETERIAS':'https://www.imdb.com/chart/boxoffice/?ref_=chtbtm_ql_1'}

COLUMNS = ['Titulo', 
           'Ano', 
           'Duracao', 
           'Classificacao_Indicativa', 
           'Classificação_no_IMDb', 
           'Qtd_Avaliacoes',
           'Direcao',
           'Atores',
           'Legenda',
           'Prime_Video']

COLUMNS_P = ['Titulo', 
           'Fim_de_semana_bruto', 
           'Total_bruto', 
           'Lançamento_de_semanas', 
           'Classificação_no_IMDb', 
           'Qtd_Avaliacoes',
           'Direcao',
           'Atores',
           'Legenda',
           'Prime_Video']