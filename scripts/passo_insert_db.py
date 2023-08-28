# encoding: ISO8859-1

import os
import glob
import sqlite3
import pandas as pd

class PassoInsertDB:

    PADRAO_LISTA_COLUNAS = ['ndc_description', 'ndc','nadac_per_unit', 'effective_date','pricing_unit', 'pharmacy_type_indicator','otc', 'explanation_code','classification_rate_setting', 'generic_drug_per_unit','generic_drug_effective_date', 'as_of_date']

    def __init__(self, input, base):
        self.DirInput = input
        self.BaseFile = base
    
    def insere_dados_db(self):
        try:
            print(f'Iniciando o {self.__class__.__name__}')

            exec_ok = True

            # Pegando o arquivo baixado
            doc_input = glob.glob(os.path.join(self.DirInput, f'*.*'))
            doc_input = doc_input[0]

            # Lendo o arquivo e armazenando em um DataFrame
            try:
                df = pd.read_csv(doc_input)
                if len(df) == 0:
                    print(f'ERRO: Arquivo csv vazio')
                    print(f'Finalizando o {self.__class__.__name__}')
                    return False
            except:
                print(f'ERRO: Não foi possivel ler o csv')
                print(f'Finalizando o {self.__class__.__name__}')
                return False
            
            # Verificando se a quantidade de colunas no csv ainda é a mesma
            if len(df.columns) != len(self.PADRAO_LISTA_COLUNAS):
                print(f'ERRO: Arquivo csv com quantidade de colunas diferente do padrão')
                print(f'Finalizando o {self.__class__.__name__}')
                return False

            # Renomeando as colunas para estarem no mesmo padrão do banco
            df.columns = self.PADRAO_LISTA_COLUNAS

            # Removendo linhas duplicadas, caso existam
            df=df.drop_duplicates()

            # Convertendo as colunas de data em datetime
            df['effective_date'] = pd.to_datetime(df['effective_date'], format='%m/%d/%Y')
            df['generic_drug_effective_date'] = pd.to_datetime(df['generic_drug_effective_date'], format='%m/%d/%Y')
            df['as_of_date'] = pd.to_datetime(df['as_of_date'], format='%m/%d/%Y')
            
            # Verificando se a pasta do banco existe
            dir_base = os.path.split(self.BaseFile)[0]
            if not os.path.isdir(dir_base):
                os.makedirs(dir_base)
            
            # Abrindo conexão com o banco, criando a tabela e inserindo os dados do DataFrame
            try:
                conn = sqlite3.connect(self.BaseFile)
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS medicamentos
                                (ndc_description TEXT NOT NULL,
                                ndc INTEGER NOT NULL,
                                nadac_per_unit REAL NOT NULL,
                                effective_date DATE NOT NULL,
                                pricing_unit TEXT NOT NULL,
                                pharmacy_type_indicator TEXT NOT NULL,
                                otc TEXT NOT NULL,
                                explanation_code TEXT NOT NULL,
                                classification_rate_setting TEXT NOT NULL,
                                generic_drug_per_unit REAL,
                                generic_drug_effective_date DATE,
                                as_of_date DATE NOT NULL)
                            """)

                df.to_sql(name = 'medicamentos', con = conn, if_exists = 'replace', index = False)

                cursor.close()

            except sqlite3.Error as error:
                print(f'ERRO ao inserir dados no banco')
                print(f'{str(error)}')
                if conn:
                    conn.close()
                exec_ok = False
            
            if exec_ok:
                print(f'Finalizando o {self.__class__.__name__}')
                return True
            else:
                print(f'Finalizando o {self.__class__.__name__}')
                return False

        except Exception as e:
            print(f'ERRO no {self.__class__.__name__}')
            print(f'{str(e)}')
            return False