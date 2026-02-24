
#%%

# 📚 bibliotecas
#------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# inserir_dados.py
import pandas as pd

def inserir_dados_ponto(service, spreadsheet_id, df_ponto, nome_aba, limpar_ate_linha=38):
    """Versão final - Remove apenas o dia da semana, mantém a data original"""
    
    print(f"\n📤 Salvando dados na aba: '{nome_aba}'")
    print(f"📊 DataFrame com {len(df_ponto)} linhas")
    
    # Verificar se o DataFrame não está vazio
    if df_ponto.empty:
        print(f"⚠️  DataFrame vazio para {nome_aba}. Nada para salvar.")
        return None
    
    # Verificar colunas disponíveis
    colunas_disponiveis = list(df_ponto.columns)
    print(f"📋 Colunas no DataFrame: {colunas_disponiveis}")
    
    # 👉 VER DADOS ORIGINAIS ANTES DA FORMATAÇÃO
    print(f"\n🔍 DADOS ORIGINAIS DO DATAFRAME (primeiras 5 linhas):")
    print(df_ponto.head().to_string(index=False))
    
    # ====================================================
    # 🔥 REMOVER APENAS O DIA DA SEMANA - MANTER DATA ORIGINAL
    # ====================================================
    if 'Data' in df_ponto.columns:
        # Criar uma cópia para não modificar o original
        df_ponto = df_ponto.copy()
        
        # Função para remover apenas o dia da semana
        def remover_dia_semana(data):
            if pd.isna(data) or data == '':
                return ''
            
            data_str = str(data).strip()
            
            # Se tiver formato "02/01/2026 - Sun", remove o " - Sun"
            if ' - ' in data_str:
                partes = data_str.split(' - ')
                if len(partes) > 1 and partes[1] in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                    return partes[0]  # Retorna só a data
            
            return data_str  # Se não tiver dia da semana, mantém original
        
        # Aplicar a remoção
        df_ponto['Data'] = df_ponto['Data'].apply(remover_dia_semana)
        
        print(f"\n✅ DIAS DA SEMANA REMOVIDOS (data original mantida):")
        print(df_ponto['Data'].head().to_string(index=False))
    # ====================================================
    
    # Preparar dados
    dados_preparados = []
    
    for idx, row in df_ponto.iterrows():
        # Extrair cada valor, com tratamento para valores nulos/vazios
        data = str(row.get('Data', '')).strip()
        BSaldo = row.get('BSaldo', '')
        BTotal = row.get('BTotal', '')
        
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
    print(f"\n🔍 PRIMEIRAS 5 LINHAS PREPARADAS (para conferir):")
    for i in range(min(5, len(dados_preparados))):
        print(f"   {dados_preparados[i]}")
    
    # 🔥 ALTERAÇÃO PRINCIPAL: Limpar até linha fixa
    linha_inicio = 6
    linha_fim_dados = linha_inicio + len(dados_preparados) - 1
    
    # Define dois ranges diferentes:
    # 1. Range para LIMPAR (até linha 38)
    range_limpar = f"{nome_aba}!A{linha_inicio}:C{limpar_ate_linha}"
    
    # 2. Range para INSERIR (só onde tem dados)
    range_inserir = f"{nome_aba}!A{linha_inicio}:C{linha_fim_dados}"
    
    print(f"\n📍 Range para limpar: {range_limpar}")
    print(f"📍 Range para inserir: {range_inserir}")
    
    # Inserir dados no Google Sheets
    try:
        body = {'values': dados_preparados}
        
        # 🔥 PRIMEIRO: Limpar até a linha 38 (ou a linha que você definir)
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
        
        # 🔥 OPCIONAL: Limpar o que sobrar entre os dados e linha 38
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