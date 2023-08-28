# encoding: ISO8859-1

import os
import subprocess
import autoit
import glob
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PassoDownloadCsv:

    JANELA_NADAC = "[REGEXPTITLE:(?i)(NADAC.*);CLASS:Chrome_WidgetWin_1]"
    XPATH_CSV = '//*[@id="main-content"]/section/div/div[2]/div[1]/ul/li/a'

    def __init__(self, chrome_driver, url, input):
        self.ChromeDriver = chrome_driver
        self.UrlNadac = url
        self.DirInput = input

    def extrai_arquivo(self):
        try:
            print(f'Iniciando o {self.__class__.__name__}')

            # Verificando se a pasta de entrada existe (onde será baixado o csv)
            if not os.path.isdir(self.DirInput):
                os.makedirs(self.DirInput)
            else:
                for doc in glob.glob(os.path.join(self.DirInput, f'*.*')):
                    os.remove(doc)

            #  Carregando o site (3 tentativas)
            for tentativa in range(1, 4):
                service = Service(executable_path=self.ChromeDriver)
                opt = webdriver.ChromeOptions()
                opt.add_argument('--sillent')
                opt.add_argument('--log-level=3')
                opt.add_argument('--disable-extensions')
                opt.add_experimental_option('excludeSwitches', ['enable-logging'])
                opt.add_experimental_option('prefs', {'download.default_directory':self.DirInput})
                driver = webdriver.Chrome(service=service, options=opt)

                driver.maximize_window()
                driver.get(self.UrlNadac)

                try:
                    autoit.win_wait(self.JANELA_NADAC, 5)
                    break
                except:
                    self.kill_chrome(driver)
            
            if tentativa == 3:
                print(f'Finalizando o {self.__class__.__name__}')
                return False
            
            #  Baixando o csv
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.XPATH_CSV))).click()

                #  Aguardando o csv ser baixado
                arquivo = glob.glob(os.path.join(self.DirInput, f'*.csv'))
                timeout = 60
                while len(arquivo) < 1 and timeout:
                    time.sleep(1)
                    timeout -= 1
                    arquivo = glob.glob(os.path.join(self.DirInput, f'*.csv'))
                
                try:
                    self.kill_chrome(driver)
                except:
                    pass

                print(f'Finalizando o {self.__class__.__name__}')
                return True
            except:
                print(f'Finalizando o {self.__class__.__name__}')
                return False

        except Exception as e:
            print(f'ERRO no {self.__class__.__name__}')
            print(f'{str(e)}')
            self.kill_chrome(driver)
            return False
    
    def kill_chrome(self, driver):
        driver.quit()
        executavel = os.path.split(self.ChromeDriver)[1]
        subprocess.run(f"taskkill /IM {executavel} /f")
        subprocess.run(f"taskkill /IM chrome.exe /f")
