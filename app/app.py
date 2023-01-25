from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import json

def setup_browser():

    options = webdriver.ChromeOptions()

    options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(options=options, service=service)

    return browser

def create_json_file(dictionary):
    with open("movies.json", "w") as outfile:
        json.dump(dictionary, outfile, indent = 4)

def main():
    
    #definindo url
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    
    #iniciando dict dos dados
    data = dict()
    
    # acessando a pagina
    r = requests.get(url)
    
    # return early caso houver algum problema para acessar a URL
    if r.status_code != 200:
        print('URL não acessivel')
        return
    
    # selecionando tabela a ser trabalhada
    content = r.content
        
    soup = BeautifulSoup(content, 'html.parser')
        
    table = soup.find('tbody', {'class': 'lister-list'})
        
    all_movies = table.find_all('tr')
        
    for row in all_movies:
            
        # pegando valores da linha
        movie_data = row.find_all('td')
            
        # ranking do filme pegando o index da linha + 1
        movie_rank = all_movies.index(row) + 1
            
        # nome do filme
        movie_name = movie_data[1].find('a').text
            
        # avaliação imdb
        movie_imdb_rating = movie_data[2].text.replace('\n', '')
            
        # pegando o scr do poster do filme
        movie_img_scr = movie_data[0].find('img')['src']

        # Removendo acentuação e letras maiusculas para ser a chave do dicionario
        movie_key = unidecode(movie_name.lower())
            
        # criando um dict com os dados do filme
        data[movie_key] = {
                
            'movie_rank': movie_rank,
                
            'movie_name': movie_name,
                
            'movie_imdb_rating': movie_imdb_rating,
                
            'movie_img_scr': movie_img_scr
                
        }
        

    print("Todos os dados recebido!")
        
    # Criação do DataFrame com os dados do dicionario    
    df = pd.DataFrame(data).transpose().set_index('movie_rank')           
    print(df)


    # Criação do arquivo JSON
    create_json_file(data)
    
    
if __name__ == "__main__":
    main()
    