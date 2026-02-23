# teste_local_github.py
import os
import sys
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Forçar modo GitHub Actions
os.environ['GITHUB_ACTIONS'] = 'true'

print("=" * 60)
print("🧪 TESTANDO MODO GITHUB ACTIONS LOCALMENTE")
print("=" * 60)

# Importar versão GitHub do login
from src.fazer_login_github import login_github_actions as login
from src.dados_ponto import extrair_dados, acessar_calculos, configurar_datas_relatorio
from src.dados_ponto import MODO_GITHUB

print(f"📌 MODO_GITHUB = {MODO_GITHUB}")

def testar_extração():
    """Testa apenas a extração de dados"""
    
    print("\n🔐 FAZENDO LOGIN (uma única vez)...")
    navegador = login()
    
    if not navegador:
        print("❌ Falha no login")
        return
    
    print("✅ Login realizado com sucesso!")
    time.sleep(5)
    
    try:
        # 1. Acessar cálculos
        print("\n📊 ACESSANDO ÁREA DE CÁLCULOS...")
        if not acessar_calculos(navegador):
            print("❌ Não acessou cálculos")
            return
        
        # 2. Configurar datas
        print("\n📅 CONFIGURANDO DATAS...")
        if not configurar_datas_relatorio(navegador):
            print("❌ Não configurou datas")
            return
        
        # 3. EXTRAIR DADOS - VERSÃO ATUAL
        print("\n🔍 EXTRAINDO DADOS COM VERSÃO ATUAL...")
        df = extrair_dados(navegador)
        
        print("\n" + "=" * 60)
        print("📊 RESULTADO DA EXTRAÇÃO")
        print("=" * 60)
        
        if df.empty:
            print("❌ DataFrame VAZIO!")
        else:
            print(f"✅ DataFrame com {len(df)} linhas")
            print("\nPrimeiras 10 linhas:")
            print(df.head(10).to_string(index=False))
            
            print("\n📋 Info do DataFrame:")
            print(f"Colunas: {list(df.columns)}")
            print(f"Tipos:\n{df.dtypes}")
            
            # Verificar valores nulos
            print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
            
            # Salvar CSV para análise
            df.to_csv("teste_extracao.csv", index=False, encoding='utf-8-sig')
            print("\n💾 Dados salvos em 'teste_extracao.csv'")
        
        # 4. DEBUG: Salvar HTML e screenshot
        print("\n📸 Salvando debug...")
        with open("debug_pagina_completa.html", "w", encoding="utf-8") as f:
            f.write(navegador.page_source)
        
        navegador.save_screenshot("debug_tela.png")
        print("✅ HTML e screenshot salvos")
        
        # 5. Procurar tabela no HTML
        print("\n🔎 Buscando tabela no HTML...")
        page_source = navegador.page_source.lower()
        if 'tabela-calculos' in page_source or 'table' in page_source:
            print("✅ Encontrou referência a tabela no HTML")
            
            # Pegar trecho ao redor da tabela
            pos = page_source.find('tabela-calculos')
            if pos > 0:
                inicio = max(0, pos - 200)
                fim = min(len(page_source), pos + 500)
                trecho = page_source[inicio:fim]
                print(f"\nTrecho do HTML:\n{trecho}")
        else:
            print("❌ Nenhuma tabela encontrada no HTML")
            
            # Listar classes presentes
            print("\n📋 Classes encontradas na página:")
            classes = set()
            import re
            class_matches = re.findall(r'class=["\']([^"\']*)["\']', page_source)
            for c in class_matches:
                for classe in c.split():
                    classes.add(classe)
            print(list(classes)[:20])  # Mostrar primeiras 20 classes
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        input("\nPressione Enter para fechar o navegador...")
        navegador.quit()

if __name__ == "__main__":
    # Verificar se as variáveis de ambiente existem
    if not os.getenv("EMAIL_SISTEMA") or not os.getenv("SENHA_SISTEMA"):
        print("❌ ERRO: Variáveis EMAIL_SISTEMA e SENHA_SISTEMA não encontradas!")
        print("   Certifique-se de que o arquivo .env existe com:")
        print("   EMAIL_SISTEMA=seu_email")
        print("   SENHA_SISTEMA=sua_senha")
        print("   GOOGLE_SHEETS_ID=id_da_planilha")
        sys.exit(1)
    
    testar_extração()