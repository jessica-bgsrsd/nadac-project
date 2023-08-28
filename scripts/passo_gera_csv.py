# encoding: ISO8859-1

import os
import glob
import sqlite3
import pandas as pd

class PassoGeraCsv:

    def __init__(self, output, base, quantidade):
        self.DirOutput = output
        self.BaseFile = base
        self.Qtde = quantidade
    
    def gera_csv(self):
        try:
            print(f'Iniciando o {self.__class__.__name__}')
            
            exec_ok = True

            # Verificando se a pasta de saida existe (onde será gerado o csv final)
            if not os.path.isdir(self.DirOutput):
                os.makedirs(self.DirOutput)
            else:
                for doc in glob.glob(os.path.join(self.DirOutput, f'*.*')):
                    os.remove(doc)
            
            # Abrindo conexão com o banco, filtrando tabela e gerando csv
            try:
                conn = sqlite3.connect(self.BaseFile)

                # Filtrando os 100 medicamentos mais caros
                colunas = f"ndc_description,ndc,nadac_per_unit,effective_date,pricing_unit,pharmacy_type_indicator,otc,explanation_code,classification_rate_setting,generic_drug_per_unit,generic_drug_effective_date,MAX(as_of_date) as as_of_date"
                query = f"SELECT {colunas} FROM medicamentos GROUP BY ndc_description ORDER BY nadac_per_unit DESC LIMIT {self.Qtde}"
            
                df_query = pd.read_sql(query, conn)
                df_query['effective_date'] = pd.to_datetime(df_query['effective_date']).dt.date
                df_query['generic_drug_effective_date'] = pd.to_datetime(df_query['generic_drug_effective_date']).dt.date
                df_query['as_of_date'] = pd.to_datetime(df_query['as_of_date']).dt.date

                # Gerando o csv na pasta de saida
                nome_csv = f'nadac-{len(df_query)}-most-expensive-drugs.csv'
                df_query.to_csv (os.path.join(self.DirOutput, nome_csv),sep = '|', index = False)

            except sqlite3.Error as error:
                print(f'ERRO ao filtrar dados no banco')
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