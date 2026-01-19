import os
import sys
from pathlib import Path
from datetime import date
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.parent

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")

def autenticar_google_sheets():
    creds = None
    
    token_path = BASE_DIR / "config" / "token.json"
    credentials_path = BASE_DIR / "config" / "credentials.json"
    
    if not os.path.exists(credentials_path):
        print(f"❌ Arquivo de credenciais não encontrado: {credentials_path}")
        print("   Certifique-se de renomear o arquivo antigo para credentials.json")
        return None
    
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            print("✅ Token carregado do arquivo")
        except Exception as e:
            print(f"⚠️  Token inválido: {e}")
            creds = None
    
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Token expirado, renovando...")
                creds.refresh(Request())
                print("✅ Token renovado com sucesso")
            else:
                print("🔑 Criando novo token de acesso...")
                print("   Uma janela do navegador abrirá para autenticação.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES
                )
                creds = flow.run_local_server(
                    port=0,
                    authorization_prompt_message="Por favor, autorize o acesso ao Google Sheets",
                    success_message="✅ Autenticação concluída! Você pode fechar esta janela.",
                    open_browser=True
                )
                print("✅ Novo token criado")
            
            with open(token_path, "w") as token:
                token.write(creds.to_json())
            print(f"💾 Token salvo em {token_path}")
                
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            print("\n📝 Possíveis soluções:")
            print("   1. Verifique se credentials.json está no formato correto")
            print("   2. Certifique-se de que a API Google Sheets está ativada")
            print("   3. Tente excluir o token.json e executar novamente")
            return None
    
    return build("sheets", "v4", credentials=creds)

def funcionarios_ativos(service):
    RANGE_NAME = "funcionarios 👥!C5:C100"

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )

    values = result.get("values", [])
    return values

def pegar_dados(service):
    funcionarios = funcionarios_ativos(service)
    fun = funcionarios
    RANGE_NAME = f"ANDREY NASCIMENTO DA SILVA!A5:E5"

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )

    values = result.get("values", [])
    return values

def verificar_aba_existe(service, spreadsheet_id, nome_funcionario):
    """Verifica se existe uma aba com nome do funcionário e retorna o nome correto"""
    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        abas = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        
        nome_busca = nome_funcionario.upper().strip().replace("  ", " ")
        
        for aba_real in abas:
            aba_normalizada = aba_real.upper().strip().replace("  ", " ")
            
            if (nome_busca == aba_normalizada or 
                nome_busca in aba_normalizada or 
                aba_normalizada in nome_busca):
                print(f"✅ Aba encontrada: '{aba_real}' para funcionário '{nome_funcionario}'")
                return aba_real
        
        print(f"❌ Nenhuma aba encontrada para: {nome_funcionario}")
        print(f"   Abas disponíveis: {abas}")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao verificar abas: {e}")
        return None