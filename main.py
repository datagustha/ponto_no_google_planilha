# main.py
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Importar seus módulos
from src.api_gs import autenticar_google_sheets, verificar_aba_existe
from src.inserir_dados import inserir_dados_ponto
from src.dados_ponto import processar_todos_funcionarios

# Carregar variáveis de ambiente
load_dotenv()

# Detectar ambiente
if os.getenv('GITHUB_ACTIONS') == 'true':
    print("\n🏃 Rodando no GitHub Actions")
    # Importar versão especial para GitHub
    from src.fazer_login_github import login_github_actions as login
    MODO_GITHUB = True
else:
    print("\n💻 Rodando localmente")
    from src.fazer_login import login
    MODO_GITHUB = False

print("\n" + "=" * 60)
print("🤖 BOT DE PONTO - INICIANDO...")
print("=" * 60)

def processar_funcionario_callback(nome_funcionario, df_dados):
    """Callback para processar cada funcionário"""
    
    print(f"\n📊 Processando {nome_funcionario}...")
    
    # 1. Autenticar no Google Sheets
    service = autenticar_google_sheets()
    if not service:
        print("❌ Falha na autenticação do Google Sheets")
        return False
    
    # 2. Verificar se a aba existe
    nome_aba_correto = verificar_aba_existe(service, os.getenv("GOOGLE_SHEETS_ID"), nome_funcionario)
    if not nome_aba_correto:
        print(f"❌ Aba não encontrada para {nome_funcionario}")
        return False
    
    # 3. Inserir dados
    resultado = inserir_dados_ponto(
        service=service,
        spreadsheet_id=os.getenv("GOOGLE_SHEETS_ID"),
        df_ponto=df_dados,
        nome_aba=nome_aba_correto,
        limpar_ate_linha=38
    )
    
    if resultado:
        print(f"✅ {nome_funcionario} processado com sucesso!")
        return True
    else:
        print(f"❌ Falha ao processar {nome_funcionario}")
        return False

def main():
    """Função principal"""
    
    try:
        # Verificar variáveis de ambiente
        variaveis_necessarias = ["EMAIL_SISTEMA", "SENHA_SISTEMA", "GOOGLE_SHEETS_ID"]
        for var in variaveis_necessarias:
            if not os.getenv(var):
                print(f"❌ Variável {var} não encontrada")
                return 1
        
        # 1. Fazer login no sistema
        navegador = login()
        if not navegador:
            print("❌ Falha no login. Abortando.")
            return 1
        
        time.sleep(3)
        
        # 2. Processar todos os funcionários
        print("\n🚀 INICIANDO PROCESSAMENTO DOS FUNCIONÁRIOS...")
        
        total_processados = processar_todos_funcionarios(
            navegador=navegador,
            callback_processar=processar_funcionario_callback,
            max_tentativas=40
        )
        
        # 3. Fechar navegador
        navegador.quit()
        
        print("\n" + "=" * 60)
        print(f"✅ PROCESSAMENTO CONCLUÍDO!")
        print(f"📊 Total de funcionários processados: {total_processados}")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERRO NA EXECUÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    # No GitHub Actions, não usar input()
    if os.getenv('GITHUB_ACTIONS') == 'true':
        sys.exit(main())
    else:
        # Localmente, pode perguntar antes de sair
        resultado = main()
        input("\nPressione Enter para sair...")
        sys.exit(resultado)