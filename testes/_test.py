import os
import unittest


def contar_arquivos(caminho):
    '''
    Método para contar arquivos em um caminho
    '''
    try:
        lista_arquivos = os.listdir(caminho)
        return len(lista_arquivos)
    except OSError:
        print(f"Não foi possível acessar o caminho: {caminho}")
        return None



class TestContagemArquivos(unittest.TestCase):
    '''
    Classe principal de testes que herda de unittest.TestCase
    '''
    def test_cont_arq_screenshots(self):
        '''
        Teste para a contagem de arquivos na pasta de screenshots
        '''
        path = os.path.join(os.getcwd(), 'screenshots')
        qtd_esperada = 4
        qtd_arquivos = contar_arquivos(path)
        self.assertEqual(qtd_arquivos, qtd_esperada,
                         f"A quantidade de arquivos é {qtd_arquivos}, esperado {qtd_esperada}")

    def test_db(self):
        '''
        Teste para a contagem de arquivos na pasta de db_sqlite
        '''
        path = os.path.join(os.getcwd(), 'db_sqlite')
        qtd_esperada = 1
        qtd_arquivos = contar_arquivos(path)
        self.assertEqual(qtd_arquivos, qtd_esperada,
                         f"A quantidade de arquivos é {qtd_arquivos}, esperado {qtd_esperada}")

    def test_arq_df(self):
        '''
        Teste para a contagem de arquivos na pasta de arquivos
        '''
        path = os.path.join(os.getcwd(), 'arquivos')
        qtd_esperada = 4
        qtd_arquivos = contar_arquivos(path)
        self.assertEqual(qtd_arquivos, qtd_esperada,
                         f"A quantidade de arquivos é {qtd_arquivos}, esperado {qtd_esperada}")



def run_tests(test_class):
    '''
    Método para executar os testes
    '''
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_tests(TestContagemArquivos)