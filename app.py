import schedule
import time
from setup_config.settings import *
from crawler.crawler import *
from setup_config.setup import Setup
from selenium.webdriver import Chrome
from crawler.crawler import Collect



class Main():
    def __init__(self): 
        '''
        Classe principal da aplicação. 
        '''
        self.first_run = True  # Flag para controlar a primeira execução
        
    def run_script(self):
        '''
        Neste método serão instanciadas as classes Setup e webdriver 
        que são necessários para manipulação do browser e inicio da coleta, além 
        da class Collect responsável pela coleta dos dados
        '''
        self.setup = Setup()
        self.webdriver = Chrome(service=self.setup.service, options=self.setup.opt)
        self.crawler = Collect(self.webdriver)
        self.crawler.to_collect_movies()
        self.webdriver.close()
        self.crawler.time_exec()
        
    def start_scheduler(self):
        '''
        Método responsável por controlar o fluxo de execuções,
        Atrvés da vaiavel self.first_run que inicia como True,
        O método sempre irá executar a primeira vez quando chamado,
        após a 1 excecução, a variavel self.first_run recebe False,
        e cai no modulo schedule, responsável por realizar a execução conforme necessário.
        '''
        if self.first_run:
            self.run_script()
            self.first_run = False

        # Agende a execução a cada hora (ajuste conforme necessário)
        schedule.every(1).hour.do(self.run_script)
        # Agende a execução todos os dias às 3:00 AM (ajuste conforme necessário)
        #schedule.every().day.at("03:00").do(self.run_script)
        
        while True:
            #loop infinito para garantir os agendamentos de execução.
            schedule.run_pending()
            time.sleep(1)
        
        
if __name__ == "__main__":
    setup_log()
    main_instance = Main()
    main_instance.start_scheduler()
