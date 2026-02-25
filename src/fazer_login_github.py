# src/fazer_login_github.py - VERSÃO HIPER SIMPLIFICADA

import os
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_github_actions():
    """Versão simplificada para GitHub Actions"""
    
    print("=" * 58)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 58)
    
    # Configuração do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("🚀 Iniciando Chrome headless...")
    navegador = webdriver.Chrome(options=chrome_options)
    
    # Executar script para evitar detecção
    navegador.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # PASSO 1: Ir direto para a página de login (evitar o botão inicial)
        print("\n🌐 Acessando página de login diretamente...")
        navegador.get("https://app.secullum.com.br/Account/Login")
        time.sleep(5)
        
        # PASSO 2: Fazer login
        print("🔐 FAZENDO LOGIN...")
        
        # Email
        campo_email = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        campo_email.clear()
        campo_email.send_keys(os.getenv("EMAIL_SISTEMA"))
        print("✅ Email inserido")
        
        # Senha
        campo_senha = navegador.find_element(By.ID, "senha")
        campo_senha.clear()
        campo_senha.send_keys(os.getenv("SENHA_SISTEMA"))
        print("✅ Senha inserida")
        
        # Botão entrar
        botao_entrar = navegador.find_element(By.XPATH, "//button[@type='submit']")
        botao_entrar.click()
        print("🖱 Clicou em Entrar")
        
        # Aguardar login
        time.sleep(8)
        
        # PASSO 3: Verificar se logou (tirar print)
        print("\n📸 Tirando print após login...")
        pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
        os.makedirs(pasta_prints, exist_ok=True)
        navegador.save_screenshot(os.path.join(pasta_prints, "apos_login.png"))
        
        # PASSO 4: Ir para relatórios
        print("\n📊 Indo para relatórios...")
        navegador.get("https://pontoweb.secullum.com.br/#/homerelatorios")
        time.sleep(8)
        
        # Print da página de relatórios
        navegador.save_screenshot(os.path.join(pasta_prints, "relatorios.png"))
        print("✅ Print da página de relatórios salvo")
        
        print("\n✅✅✅ LOGIN E ACESSO A RELATÓRIOS CONCLUÍDOS!")
        return navegador
        
    except Exception as e:
        print(f"\n❌ ERRO NO LOGIN: {e}")
        
        # Tentar tirar print do erro
        try:
            pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
            os.makedirs(pasta_prints, exist_ok=True)
            navegador.save_screenshot(os.path.join(pasta_prints, "erro_login.png"))
            print("📸 Print do erro salvo")
        except:
            pass
        
        navegador.quit()
        return None
