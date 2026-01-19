
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

def inserir_dados_ponto(service, spreadsheet_id, df_ponto, nome_aba):
    """Versão corrigida - lida com nomes e DataFrames separados"""
    
    print(f"\n📤 Salvando dados na aba: '{nome_aba}'")
    print(f"📊 DataFrame com {len(df_ponto)} linhas")
    
    # Verificar se o DataFrame não está vazio
    if df_ponto.empty:
        print(f"⚠️  DataFrame vazio para {nome_aba}. Nada para salvar.")
        return None
    
    # Verificar colunas disponíveis
    colunas_disponiveis = list(df_ponto.columns)
    print(f"📋 Colunas no DataFrame: {colunas_disponiveis}")
    
    # 👉 ADICIONE ESTA LINHA PARA VER OS DADOS ORIGINAIS
    print(f"\n🔍 DADOS ORIGINAIS DO DATAFRAME (primeiras 5 linhas):")
    print(df_ponto.head().to_dict())
    
    # Preparar dados
    dados_preparados = []
    
    for idx, row in df_ponto.iterrows():  # 👉 Adicione idx para depuração
        # 👉 ADICIONE DEPURAÇÃO PARA CADA LINHA
        print(f"\n--- Processando linha {idx} ---")
        
        # Extrair cada valor, com tratamento para valores nulos/vazios
        data = str(row.get('Data', '')).strip()

        BSaldo = row.get('BSaldo', '')
        BTotal = row.get('BTotal', '')
        
        # 👉 MOSTRAR VALORES ORIGINAIS
        print(f"BSaldo original (tipo: {type(BSaldo)}): {repr(BSaldo)}")
        print(f"BTotal original (tipo: {type(BTotal)}): {repr(BTotal)}")
        
        # Converter para string
        if isinstance(BSaldo, (list, tuple)):
            BSaldo = str(BSaldo[0]) if BSaldo else ''
        else:
            BSaldo = str(BSaldo)

        if isinstance(BTotal, (list, tuple)):
            BTotal = str(BTotal[0]) if BTotal else ''
        else:
            BTotal = str(BTotal)
        
        print(f"Depois de converter para string:")
        print(f"BSaldo: {repr(BSaldo)}")
        print(f"BTotal: {repr(BTotal)}")

        # Limpar espaços E REMOVER APÓSTROFE se existir!
        BSaldo = BSaldo.strip()
        BTotal = BTotal.strip()
        
        print(f"Depois de strip():")
        print(f"BSaldo: {repr(BSaldo)}")
        print(f"BTotal: {repr(BTotal)}")
        
        # 👉 REMOVER APÓSTROFE no início (se tiver)
        if BSaldo.startswith("'"):
            BSaldo = BSaldo[1:].strip()
            print(f"Depois de remover apóstrofe BSaldo: {repr(BSaldo)}")
        
        if BTotal.startswith("'"):
            BTotal = BTotal[1:].strip()
            print(f"Depois de remover apóstrofe BTotal: {repr(BTotal)}")

        # CORREÇÃO PRINCIPAL: Para valores negativos de tempo
        # Se o valor começar com '-', manter como está
        # Se começar com '+', remover o sinal
        
        if BSaldo:
            if BSaldo.startswith('+'):
                BSaldo = BSaldo[1:]  # Remove o '+'
                print(f"Depois de remover + BSaldo: {repr(BSaldo)}")
            elif BSaldo.startswith('-'):
                # Mantém o '-' 
                print(f"BSaldo tem sinal negativo: {repr(BSaldo)}")
                pass
            # Limpar valores 'nan' ou 'NaT'
            elif BSaldo.lower() in ['nan', 'nat', 'none', '']:
                BSaldo = ''
                print(f"BSaldo era nan, agora: {repr(BSaldo)}")
        
        if BTotal:
            if BTotal.startswith('+'):
                BTotal = BTotal[1:]  # Remove o '+'
                print(f"Depois de remover + BTotal: {repr(BTotal)}")
            elif BTotal.startswith('-'):
                # Mantém o '-'
                print(f"BTotal tem sinal negativo: {repr(BTotal)}")
                pass
            # Limpar valores 'nan' ou 'NaT'
            elif BTotal.lower() in ['nan', 'nat', 'none', '']:
                BTotal = ''
                print(f"BTotal era nan, agora: {repr(BTotal)}")
        
        # 👉 VERIFICAR SE AINDA TEM APÓSTROFE
        if "'" in BSaldo:
            print(f"⚠️  ATENÇÃO: BSaldo ainda contém apóstrofe!")
        if "'" in BTotal:
            print(f"⚠️  ATENÇÃO: BTotal ainda contém apóstrofe!")
        
        dados_preparados.append([data, BSaldo, BTotal])
        
        print(f"Valores finais para esta linha:")
        print(f"data: {repr(data)}")
        print(f"BSaldo: {repr(BSaldo)}")
        print(f"BTotal: {repr(BTotal)}")
    
    print(f"\n📝 Dados preparados: {len(dados_preparados)} linhas")
    
    # Definir range (começa na linha 6)
    linha_inicio = 6
    if len(dados_preparados) > 0:
        linha_fim = linha_inicio + len(dados_preparados) - 1
        range_name = f"{nome_aba}!A{linha_inicio}:C{linha_fim}"
        
        print(f"\n🔍 Valores que serão enviados para o Google Sheets:")
        for i, linha in enumerate(dados_preparados):
            print(f"  Linha {linha_inicio + i}: {linha}")
    else:
        print("⚠️  Nenhum dado para inserir")
        return None
    
    print(f"📍 Range: {range_name}")
    
    # Inserir dados no Google Sheets
    try:
        body = {'values': dados_preparados}
        
        # Primeiro limpar o range existente (opcional)
        try:
            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                body={}
            ).execute()
            print("🧹 Range limpo antes da inserção")
        except:
            print("ℹ️  Não foi possível limpar range (pode ser novo)")
        
        # Mude de volta para USER_ENTERED para interpretar tempo corretamente!
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",  # 👈 VOLTE para USER_ENTERED!
            body=body
        ).execute()
        
        updated_cells = result.get('updatedCells', 0)
        print(f"✅ {nome_aba}: {updated_cells} células atualizadas")
        print(f"   Linhas {linha_inicio} a {linha_fim} preenchidas")
        
        return result
        
    except Exception as e:
        print(f"❌ Erro ao salvar dados de {nome_aba}:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {str(e)}")
        
        if "Unable to parse range" in str(e):
            print(f"\n💡 DICA: A aba '{nome_aba}' não existe na planilha!")
            print(f"   Verifique se o nome da aba está correto.")
        elif "PERMISSION_DENIED" in str(e):
            print(f"\n💡 DICA: Problema de permissão no Google Sheets!")
            print(f"   Verifique se o token.json tem acesso à planilha.")
        
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