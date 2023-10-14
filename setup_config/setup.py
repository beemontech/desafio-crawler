from setup_config.settings import *
from abc import ABC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime




class Setup():
    '''
    Class com setup do service e chromeOptions
    '''
    def __init__(self) -> None:       
        self.service = Service(ChromeDriverManager().install())  
        self.opt = ChromeOptions()
        prefs = {
            "download.default_directory" : os.getcwd(),         
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1, 
            "safebrowsing.disable_download_protection": True,
            }
        self.opt.add_experimental_option("excludeSwitches", ["enable-logging"])        
        self.opt.add_experimental_option("prefs", prefs)

class PageElements(ABC):

    '''
    Class com os Métodos responsaveis por manipular o Browser atraves do Selenium
    '''
    def __init__(self, webdriver):       
        self.webdriver = webdriver       
        self.webdriver.maximize_window()        
        self.start_time = datetime.today()     
  

    def wait_(self, t=60):
        '''
        aguarda por t segundos
        '''
        return WebDriverWait(self.webdriver, t)
        
    def wait_element(self, locator, t=60, el_type='presence'):      
        '''
        aguarda elemento por t segundos de acordo com e expect conditions definido
        '''
        if el_type == 'presence':
            return self.wait_(t).until(EC.presence_of_element_located(locator))
        elif el_type == 'clickable':
            return self.wait_(t).until(EC.element_to_be_clickable(locator))
        elif el_type == 'visibility':
            return self.wait_(t).until(EC.visibility_of_element_located(locator))
    
    def find(self, locator, t=60, el_type='presence'): 
        '''
        retorna o elemento
        '''       
        self.wait_element(locator, t, el_type)
        return self.webdriver.find_element(*locator)
    
    def finds(self, locator, t=60, el_type='presence'):  
        '''
        retorna os elementos
        '''      
        self.wait_element(locator, t, el_type)
        return self.webdriver.find_elements(*locator)    
        
    def open_url(self, url):        
        '''
        abre a url
        '''
        print_log(f"[INFO] Abrindo a URL..")
        self.webdriver.get(url)
        return     

    def click_in_element(self, locator, t=60, el_type='presence'):     
        '''
        clica no elemento
        '''   
        self.find(locator, t, el_type).click()    
    
    def click_in_elements(self, locator, i, t=60, el_type='presence'):    
        '''
        encontra os elementos e clica no elemento posicionado no index
        '''    
        elements = self.finds(locator, t, el_type)
        elements[i].click()

    def rename(self, dic):
        '''
        Recebe a url, de acordo com a url retorna o nome para salvar os dados
        '''
        if dic == 'URL_250':
            name = '250_melhores_filmes_imdb'
        elif dic == 'PIOR_AVALI':
            name = 'Filmes_pior_avaliacao'
        elif dic == 'PRINCI_BILHETERIAS':
            name = 'Principais_bilheterias'
        elif dic == 'MAIS_POPULARES':
            name = 'Filmes_mais_populares'
        return name

    