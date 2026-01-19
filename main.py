
#%%
# main.py - CORRIGIDO
from src.fazer_login import login  # ← MUDOU: base → src
from src.dados_ponto import processar_todos_funcionarios, periodo_pop_up  # ← MUDOU: base → src
from src.api_gs import autenticar_google_sheets, verificar_aba_existe  # ← MUDOU
from src.inserir_dados import inserir_dados_ponto  # ← MUDOU
import time
from dotenv import load_dotenv
import os

load_dotenv()

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
    print("🤖 BOT DE PONTO - INICIANDO")
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