from setup_config.settings import *
from setup_config.locators import *
from selenium.webdriver.common.by import By
from setup_config.setup import PageElements
import pandas as pd
import sqlite3, time, shutil
from datetime import datetime
import unittest


class Collect(PageElements):
    '''
    Class principal de coleta dos Movies, através do Método collect_movies
    será coletado os Filmes e suas caracteristicas salvando em um dataframe temporário,
    onde posteriormente será possível salvar no tipo de arquivo escolhido "" CSV, XLSX, JSON""
    '''
    def to_collect_movies(self):
        '''
        Método responsável por direcionar a coleta dos Filmes.
        Fara um loop do dicionario de urls para coletar os dados de cada página.
        '''
        self.remove_arq()
        for dic in DICT_URLS:
            self.open_url(DICT_URLS.get(dic))
            print_log(f"[INFO] Criando o DataFrame..")
            self.df = pd.DataFrame(columns=COLUMNS)
            self.dfs = []
            self.collect_movies(dic)
            self.save_format(dic, 'csv')
            self.save_in_db(dic)
        print_log(f"[INFO] Coleta Concluida!..")  

    def collect_movies(self, dic):
        '''
        Para cada url os dados a serem coletados estao em formatos diferentes,
        entao o método faz um depara, e de acordo com a url, é direcionado um método de coleta.
        '''
        if dic == 'URL_250' or dic == 'PIOR_AVALI' or dic == 'MAIS_POPULARES':
            self.collect_movies_m_p(dic)
        else:
            self.collect_princip(dic)

    def collect_princip(self, dic):
        self.log(dic)
        for i, mov in enumerate(self.finds(MOVIES_ALL)):
            try:
                title = mov.find_element(By.CSS_SELECTOR, "a[class='ipc-title-link-wrapper']").text[3:].replace(".", "").lstrip()
                print_log(f"[INFO] Coletando Filme: {title}")
                fds = mov.find_elements(By.CSS_SELECTOR, "li[class*=' lkUVhM']")[0].text.split('US$')[-1].lstrip().split()[0]
                tot_bruto =  mov.find_elements(By.CSS_SELECTOR, "li[class*=' lkUVhM']")[1].text.split('US$')[-1].lstrip().split()[0]
                Lan_sem =  mov.find_elements(By.CSS_SELECTOR, "li[class*=' lkUVhM']")[2].text.split(':')[-1].lstrip()
                stars = mov.find_element(By.CSS_SELECTOR, "span[class='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating']").get_attribute('aria-label').split(":")[-1].strip()
                qtd_aval = mov.find_element(By.CSS_SELECTOR, "span[class='ipc-rating-star--voteCount").text.replace("(", "").replace(")", "").lstrip()
                dir, art, desc, prime = self.more_infos(i, dic, title)
                new_row = pd.DataFrame([[title, float(fds.replace(',','.')), float(tot_bruto.replace(',','.')), int(Lan_sem), stars, qtd_aval, dir, art, desc, prime]], columns=COLUMNS_P)
                self.dfs.append(new_row)
                self.df = pd.concat(self.dfs, ignore_index=True)
            except:
                print_log(f"[INFO] Não consegui coletar os dados do filme {title}")


    def collect_movies_m_p(self, dic):
        self.log(dic)
        for i, mov in enumerate(self.finds(MOVIES_ALL)):
            try:
                if dic == 'MAIS_POPULARES':
                    title = mov.find_element(By.CSS_SELECTOR, "a[class='ipc-title-link-wrapper']").text
                else:     
                    title = mov.find_element(By.CSS_SELECTOR, "a[class='ipc-title-link-wrapper']").text[3:].replace(".", "").lstrip()
                print_log(f"[INFO] Coletando Filme: {title}")
                
                ano = mov.find_elements(By.CSS_SELECTOR, "span[class*=' cli-title-metadata-item']")[0].text
                duracao = mov.find_elements(By.CSS_SELECTOR, "span[class*=' cli-title-metadata-item']")[1].text
                try:
                    class_indi = mov.find_elements(By.CSS_SELECTOR, "span[class*=' cli-title-metadata-item']")[-1].text
                except:
                    class_indi = ''
                try:
                    stars = mov.find_element(By.CSS_SELECTOR, "span[class='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating']").get_attribute('aria-label').split(":")[-1].strip()
                    qtd_aval = mov.find_element(By.CSS_SELECTOR, "span[class='ipc-rating-star--voteCount").text.replace("(", "").replace(")", "").lstrip()
                except:
                    stars = ''
                    qtd_aval = ''
                dir, art, desc, prime = self.more_infos(i, dic, title)
                new_row = pd.DataFrame([[title, ano, duracao, class_indi, stars, qtd_aval, dir, art, desc, prime]], columns=COLUMNS)
                self.dfs.append(new_row)
                self.df = pd.concat(self.dfs, ignore_index=True)
            except:
                print_log(f"[INFO] Não consegui coletar os dados do filme {title}")

    def more_infos(self,i, nome, title):
        '''
        Coleta os itens apos clicar em mais informações
        '''
        self.webdriver.execute_script(f'window.scrollBy(0, 115)')
        try:
            button_mais = self.finds(MAIS_INFOS)
            self.webdriver.execute_script("arguments[0].click();", button_mais[i])
            dir = self.finds(DIR)[0].text
            artists = self.finds(DIR_ART)
            art1 = artists[0].text
            art2 = artists[1].text
            art3 = artists[2].text
            art = art1 + ', '+art2+ ', '+art3
            desc = self.find(DESC).text
            try:
                prime = self.find(PRIME, t=0.5).get_attribute("href")
            except:
                prime = "Sem link Prime"
            self.webdriver.save_screenshot(os.path.join(os.getcwd(), 'screenshots', f'SCREENSHOT_{nome}.png'))
            self.find(CLOSE).click()
            time.sleep(0.5)
        except:
            print_log(f"[INFO] Não consegui coletar mais informações do filme {title}")
        return dir, art, desc, prime

    def save_format(self, dic, formato):
        '''
        Recebe como parametro o nome que deseja salvar o aqrquivo e 
        o tipo de arquivo escolhido csv, xlsx, json
        '''
        name = self.rename(dic)
        print_log(f"[INFO] Salvando no Formato {formato}..")
        if str(formato) == 'csv':
            self.df.to_csv(os.path.join(os.getcwd(), 'arquivos', f"{name}.csv"), index=False)
        elif str(formato) == 'xlsx':
            self.df.to_excel(os.path.join(os.getcwd(), 'arquivos', f"{name}.xlsx"), index=False)
        elif str(formato) =='json':
            self.df.to_json(os.path.join(os.getcwd(), 'arquivos', f"{name}.json"), orient="records", force_ascii=False)
        
    def save_in_db(self, dic):
        '''
        Salva a coleta no Banco de dados Sqlite.
        '''
        name = self.rename(dic) + '_' + str(int(time.time()))
        caminho_db = os.path.join(os.getcwd(), 'db_sqlite', 'movies.db')
        print_log(f"[INFO] Abrindo a conexão..")
        conn = sqlite3.connect(caminho_db)
        print_log(f"[INFO] Salvando no DB Sqlite..")
        self.df.to_sql(f'{name}', conn, if_exists='replace', index=False)
        print_log(f"[INFO] Fechando a conexão..")
        conn.close()
    
    def time_exec(self):
        '''
        Calcula o tempo de execução..
        '''
        now = datetime.now()
        time_ex = now-self.start_time
        print_log(f"[INFO] Tempo de execução {time_ex}..")

    def log(self, dic):
        '''
        printa e registra no log conforme a url.
        '''
        if dic == 'URL_250':
            print_log(f"[INFO] Coletando os 250 melhores Filmes do Imdb")
        elif dic == 'PIOR_AVALI':
            print_log(f"[INFO] Coletando os 100 piores Filmes do Imdb")
        elif dic == 'PRINCI_BILHETERIAS':
            print_log(f"[INFO] Coletando Principais Bilheterias..")
        else:
            print_log(f"[INFO] Coletando Filmes mais Populares..")
    
    def run_tests(self):
        '''
        Método para executar os testes.
        '''
        time.sleep(5)
        path = os.path.join(os.getcwd(), "testes")
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(start_dir=path, pattern='*_test.py')
        test_runner = unittest.TextTestRunner()
        test_runner.run(test_suite)
    
    def remove_arq(self):
        '''
        Método remove os arquivos das pastas
        '''
        pastas = ['arquivos', 'db_sqlite', 'screenshots']
        for pasta in pastas:
            path = os.path.join(os.getcwd(), pasta)

            try:
                shutil.rmtree(path)
                os.makedirs(path)  # Recria a pasta vazia
                print_log(f"Conteúdo de {pasta} removido com sucesso.")
            except Exception as e:
                print_log(f"Ocorreu um erro ao limpar {pasta}: {e}")