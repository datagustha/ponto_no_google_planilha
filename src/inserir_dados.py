
#%%

# 📚 bibliotecas
#------------------------------------------------

#%%

# 📚 bibliotecas
#------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

import time


# inserir_dados.py
import pandas as pd

#%%

# 📚 bibliotecas
#------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

import time


# inserir_dados.py
import pandas as pd
import os


def inserir_dados_ponto(service, spreadsheet_id, df_ponto, nome_aba, limpar_ate_linha=38):
    """Versão corrigida - formatação condicional (Git vs Local)"""
    
    print(f"\n📤 Salvando dados na aba: '{nome_aba}'")
    print(f"📊 DataFrame com {len(df_ponto)} linhas")
    
    # Verificar se o DataFrame não está vazio
    if df_ponto.empty:
        print(f"⚠️  DataFrame vazio para {nome_aba}. Nada para salvar.")
        return None
    
    # Verificar colunas disponíveis
    colunas_disponiveis = list(df_ponto.columns)
    print(f"📋 Colunas no DataFrame: {colunas_disponiveis}")
    
    # 👉 DETECTAR SE ESTÁ RODANDO NO GITHUB ACTIONS
    MODO_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'
    
    print(f"\n🔍 DADOS ORIGINAIS DO DATAFRAME (últimas 5 linhas):")
    print(df_ponto.tail().to_string(index=False))
    
    # 📅 DICIONÁRIO PARA TRADUZIR DIAS DA SEMANA
    dias_traducao = {
        'Mon': 'Seg',
        'Tue': 'Ter',
        'Wed': 'Qua',
        'Thu': 'Qui',
        'Fri': 'Sex',
        'Sat': 'Sáb',
        'Sun': 'Dom'
    }
    
    # Preparar dados
    dados_preparados = []
    
    for idx, row in df_ponto.iterrows():
        # Extrair cada valor, com tratamento para valores nulos/vazios
        data = str(row.get('Data', '')).strip()
        BSaldo = row.get('BSaldo', '')
        BTotal = row.get('BTotal', '')
        
        # 🔥 CONVERSÃO CONDICIONAL: SÓ APLICA SE ESTIVER NO GITHUB
        if MODO_GITHUB and data and ' - ' in data:
            partes_data = data.split(' - ')
            if len(partes_data) == 2:
                data_numero = partes_data[0]  # Ex: "02/01/2026"
                dia_ingles = partes_data[1]    # Ex: "Sun"
                
                # TRADUZIR O DIA DA SEMANA
                dia_portugues = dias_traducao.get(dia_ingles, dia_ingles)
                
                # CONVERTER DATA DE US PARA BR (se estiver no formato MM/DD/YYYY)
                if '/' in data_numero:
                    partes_data_num = data_numero.split('/')
                    if len(partes_data_num) == 3:
                        # Formato US: MM/DD/YYYY → BR: DD/MM/YYYY
                        mes_us = partes_data_num[0]
                        dia_us = partes_data_num[1]
                        ano = partes_data_num[2]
                        
                        # Reorganizar para formato BR
                        data_br = f"{dia_us}/{mes_us}/{ano}"
                        print(f"   🔄 (GitHub) Convertendo data: {data_numero} (US) → {data_br} (BR)")
                        
                        # Remontar a data completa com dia em português
                        data = f"{data_br} - {dia_portugues}"
                        print(f"   🔄 Data final: {data}")
        else:
            if MODO_GITHUB:
                print(f"   ℹ️ (GitHub) Data já está no formato correto: {data}")
            else:
                print(f"   ℹ️ (Local) Mantendo data original: {data}")
        
        # Converter para string
        if isinstance(BSaldo, (list, tuple)):
            BSaldo = str(BSaldo[0]) if BSaldo else ''
        else:
            BSaldo = str(BSaldo)

        if isinstance(BTotal, (list, tuple)):
            BTotal = str(BTotal[0]) if BTotal else ''
        else:
            BTotal = str(BTotal)

        # Limpar espaços e apóstrofe
        BSaldo = BSaldo.strip()
        BTotal = BTotal.strip()
        
        # Remover apóstrofe no início (se tiver)
        if BSaldo.startswith("'"):
            BSaldo = BSaldo[1:].strip()
        
        if BTotal.startswith("'"):
            BTotal = BTotal[1:].strip()

        # Tratamento de sinais
        if BSaldo:
            if BSaldo.startswith('+'):
                BSaldo = BSaldo[1:]  # Remove o '+'
            elif BSaldo.lower() in ['nan', 'nat', 'none', '']:
                BSaldo = ''
        
        if BTotal:
            if BTotal.startswith('+'):
                BTotal = BTotal[1:]  # Remove o '+'
            elif BTotal.lower() in ['nan', 'nat', 'none', '']:
                BTotal = ''
        
        dados_preparados.append([data, BSaldo, BTotal])
    
    print(f"\n📝 Dados preparados: {len(dados_preparados)} linhas")
    
    # 🔥 ALTERAÇÃO PRINCIPAL: Limpar até linha fixa
    linha_inicio = 6
    linha_fim_dados = linha_inicio + len(dados_preparados) - 1
    
    # Define dois ranges diferentes:
    range_limpar = f"{nome_aba}!A{linha_inicio}:C{limpar_ate_linha}"
    range_inserir = f"{nome_aba}!A{linha_inicio}:C{linha_fim_dados}"
    
    print(f"\n📍 Range para limpar: {range_limpar}")
    print(f"📍 Range para inserir: {range_inserir}")
    
    # Inserir dados no Google Sheets
    try:
        body = {'values': dados_preparados}
        
        # 🔥 PRIMEIRO: Limpar até a linha 38
        print(f"🧹 Limpando de A6 até C{limpar_ate_linha}...")
        try:
            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_limpar,
                body={}
            ).execute()
            print(f"✅ Dados antigos limpos até linha {limpar_ate_linha}")
        except Exception as e:
            print(f"⚠️  Não foi possível limpar completamente: {e}")
        
        # 🔥 SEGUNDO: Inserir os novos dados
        print(f"📝 Inserindo {len(dados_preparados)} linhas de dados...")
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_inserir,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        
        updated_cells = result.get('updatedCells', 0)
        print(f"✅ {nome_aba}: {updated_cells} células atualizadas")
        print(f"   Dados inseridos nas linhas {linha_inicio} a {linha_fim_dados}")
        
        # 🔥 Limpar sobra entre os dados e linha 38
        if linha_fim_dados < limpar_ate_linha:
            range_sobra = f"{nome_aba}!A{linha_fim_dados + 1}:C{limpar_ate_linha}"
            try:
                service.spreadsheets().values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=range_sobra,
                    body={}
                ).execute()
                print(f"🧹 Limpando sobra: linhas {linha_fim_dados + 1} a {limpar_ate_linha}")
            except:
                pass
        
        return result
        
    except Exception as e:
        print(f"❌ Erro ao salvar dados de {nome_aba}:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {str(e)}")
        
        return None



# dicionario = {
#     'BSaldo'    : ['+00:58'],
#     'BTotal' : ['+00:40']
# }


# df = pd.DataFrame(dicionario)
# df

# from api_gs import * 

# autentcar = autenticar_google_sheets()
# autentcar

# try:
#     enviar = inserir_dados_ponto(
#         service        = autentcar,
#         spreadsheet_id = '186TDcqEU_eAagw96QuwwLvTEDmouyTye2KwMI63ZVik',
#         df_ponto       = df,
#         nome_aba       = 'ANA LUISA ALVES DA SILVA'
#     )
#     print('dados enviados! ')

# except Exception:
#     print('error não consegui enviar')