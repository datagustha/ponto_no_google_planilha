# teste_simples.py
import os
import time
import pandas as pd
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

print("=" * 60)
print("🧪 TESTE SIMPLES - EXTRAIR DADOS")
print("=" * 60)

from src.fazer_login_github import login_github_actions
from src.dados_ponto import acessar_calculos, configurar_datas_relatorio, extrair_dados

# 1. LOGIN
navegador = login_github_actions()
if not navegador:
    print("❌ Login falhou")
    exit()

input("\n⏸️  Verifique se o login funcionou e pressione Enter...")

# 2. ACESSAR CÁLCULOS
print("\n📊 ACESSANDO CÁLCULOS...")
if not acessar_calculos(navegador):
    print("❌ Falha ao acessar cálculos")
    navegador.quit()
    exit()

input("⏸️  Verifique se entrou em Cálculos e pressione Enter...")

# 3. CONFIGURAR DATAS
print("\n📅 CONFIGURANDO DATAS...")
if not configurar_datas_relatorio(navegador):
    print("❌ Falha ao configurar datas")
    navegador.quit()
    exit()

input("⏸️  Datas configuradas? Pressione Enter...")

# 4. EXTRAIR DADOS
print("\n🔍 EXTRAINDO DADOS...")
df = extrair_dados(navegador)

print("\n" + "=" * 60)
print("📊 RESULTADO:")
print("=" * 60)

if df.empty:
    print("❌ DataFrame VAZIO!")
else:
    print(f"✅ {len(df)} linhas extraídas")
    print(f"\nPrimeiras 10 linhas:")
    print(df.head(10).to_string(index=False))
    
    # Salvar CSV
    df.to_csv("teste_resultado.csv", index=False, encoding='utf-8-sig')
    print("\n💾 Salvo em 'teste_resultado.csv'")

input("\n⏸️  Pressione Enter para fechar...")
navegador.quit()