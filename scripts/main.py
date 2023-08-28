# encoding: ISO8859-1

import os
import subprocess

from scripts.passo_download_csv import PassoDownloadCsv
from scripts.passo_insert_db import PassoInsertDB
from scripts.passo_gera_csv import PassoGeraCsv

class Main:

    def __init__(self):
        self.UrlNadac = os.environ.get('UrlNadac')
        self.ChromeDriver = os.environ.get('ChromeDriver')
        self.DirInput = os.environ.get('DirInput')
        self.DirOutput = os.environ.get('DirOutput')
        self.BaseFile = os.environ.get('BaseFile')
        self.Qtde = os.environ.get('Qtde')

    def run(self):
        try:
            print(f'Iniciando o {self.__class__.__name__}')

            executavel = os.path.split(self.ChromeDriver)[1]
            subprocess.run(f"taskkill /IM {executavel} /f")
            subprocess.run(f"taskkill /IM chrome.exe /f")

            passo_download_csv = PassoDownloadCsv(self.ChromeDriver, self.UrlNadac, self.DirInput)
            executa_proximo_passo = passo_download_csv.extrai_arquivo()
            if executa_proximo_passo:
                passo_insert_db = PassoInsertDB(self.DirInput, self.BaseFile)
                executa_proximo_passo = passo_insert_db.insere_dados_db()
            if executa_proximo_passo:
                passo_gera_csv = PassoGeraCsv(self.DirOutput, self.BaseFile, self.Qtde)
                executa_proximo_passo = passo_gera_csv.gera_csv()
            
            print(f'Finalizando o {self.__class__.__name__}')

        except Exception as e:
            print(f'ERRO no {self.__class__.__name__}')
            print(f'{str(e)}')


if __name__ == "__main__":
    Main().run()