#%%
# main.py - SOLUÇÃO SIMPLES
import sys
import os
from dotenv import load_dotenv

# CORREÇÃO CRÍTICA: Configurar caminho do .env ANTES de importar outros módulos
def setup_env():
    """Configura o ambiente antes de tudo"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    env_path = os.path.join(base_path, '.env')
    
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_path)
        print(f"✅ .env carregado de: {env_path}")
        return True
    else:
        print(f"❌ .env não encontrado em: {env_path}")
        # Criar .env exemplo
        exemplo_path = os.path.join(base_path, '.env.exemplo')
        with open(exemplo_path, 'w') as f:
            f.write('EMAIL_SISTEMA=seu_email@empresa.com\nSENHA_SISTEMA=sua_senha\nGOOGLE_SHEETS_ID=seu_id')
        print(f"📝 Criado {exemplo_path} - Renomeie para .env e preencha")
        return False

# Executar configuração ANTES dos imports
if not setup_env():
    input("Pressione Enter para sair...")
    sys.exit(1)

# AGORA importar os outros módulos (eles já terão acesso às variáveis)
from src.fazer_login import login
from src.dados_ponto import processar_todos_funcionarios
from src.api_gs import autenticar_google_sheets, verificar_aba_existe
from src.inserir_dados import inserir_dados_ponto
import time

# Resto do seu código ORIGINAL (igual ao seu)
SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")

def callback_processar_funcionario(nome_funcionario, df_dados):
    print(f"\n{'='*50}")
    print(f"📋 Processando: {nome_funcionario}")
    print(f"{'='*50}")
    
    if not nome_funcionario or df_dados.empty:
        print("⚠️  Dados inválidos. Pulando...")
        return False
    
    try:
        service = autenticar_google_sheets()
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return False
    
    nome_aba = verificar_aba_existe(service, SPREADSHEET_ID, nome_funcionario)
    if not nome_aba:
        print(f"⚠️  Nenhuma aba encontrada para '{nome_funcionario}'. Pulando...")
        return False
    
    resultado = inserir_dados_ponto(
        service=service,
        spreadsheet_id=SPREADSHEET_ID,
        df_ponto=df_dados,
        nome_aba=nome_aba
    )
    
    if resultado:
        print(f"✅ {nome_funcionario}: Dados salvos com sucesso!")
        return True
    else:
        print(f"❌ {nome_funcionario}: Falha ao salvar dados")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🤖 BOT DE PONTO - INICIANDO...")
    print("="*60)
    
    print("\n🔐 Fazendo login no sistema...")
    navegador = login()
    time.sleep(3)
    
    print("\n🔄 Processando funcionários...")
    total = processar_todos_funcionarios(
        navegador=navegador,
        callback_processar=callback_processar_funcionario,
        max_tentativas=40
    )
    
    print("\n" + "="*60)
    print(f"🎉 PROCESSAMENTO CONCLUÍDO!")
    print(f"   ✅ Funcionários processados: {total}")
    print("="*60)
    
    navegador.quit()
    
    # Manter aberto para ver resultado
    if getattr(sys, 'frozen', False):
        input("\n✅ Concluído! Pressione Enter para fechar...")
