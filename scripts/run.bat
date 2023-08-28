@echo off

cd C:\GitHub\rpa\nadac_proj\
set PYTHONPATH=C:\GitHub\rpa\nadac_proj\

set UrlNadac=https://data.medicaid.gov/dataset/4a00010a-132b-4e4d-a611-543c9521280f
set ChromeDriver=C:\GitHub\chrome_driver\chromedriver.exe
set DirInput=C:\Testes\nadac_proj\input
set DirOutput=C:\Testes\nadac_proj\output
set BaseFile=C:\BD\nadac_proj\nadac.db
set Qtde=100

taskkill /IM python.exe /f

python scripts\main.py
