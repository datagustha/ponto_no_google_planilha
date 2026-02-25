# src/fazer_login_github.py - VERSÃO FINAL DEFINITIVA PARA GITHUB ACTIONS

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def login_github_actions():
    """Versão para GitHub Actions com navegação direta"""
    
    print("=" * 58)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 58)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # User agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    print("🚀 Chrome iniciado com Selenium Manager")
    navegador = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. Acessar site
        print("🌐 Acessando site...")
        navegador.get("https://pontoweb.secullum.com.br/")
        time.sleep(5)
        
        # 2. Clicar no botão
        print("🔍 Procurando botão 'Acessar ponto Web'...")
        botao = WebDriverWait(navegador, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Acessar ponto Web')]"))
        )
        botao.click()
        print("✅ Clicou em 'Acessar ponto Web'")
        time.sleep(3)
        
        # 3. Fazer login
        print("🔐 REALIZANDO LOGIN...")
        
        email = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        email.send_keys(os.getenv("EMAIL_SISTEMA"))
        print("✅ Email inserido")
        
        senha = navegador.find_element(By.ID, "senha")
        senha.send_keys(os.getenv("SENHA_SISTEMA"))
        print("✅ Senha inserida")
        
        botao_entrar = navegador.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        botao_entrar.click()
        print("🖱 Clicou em Entrar")
        time.sleep(5)
        
        # Verificar popup
        try:
            popup = navegador.find_element(By.ID, "btnYes")
            popup.click()
            print("✅ Fechou popup")
            time.sleep(2)
        except:
            print("ℹ️ Nenhum popup exibido")
        
        print("✅ LOGIN REALIZADO COM SUCESSO")
        
        # AGORA VAMOS DIRETO PARA RELATÓRIOS AQUI MESMO
        print("\n🔍 TENTANDO ACESSAR RELATÓRIOS DIRETAMENTE...")
        
        # Tentar navegação direta
        navegador.get("https://pontoweb.secullum.com.br/#/homerelatorios")
        time.sleep(10)
        
        if "relatorios" in navegador.current_url.lower():
            print("✅✅✅ ACESSOU RELATÓRIOS!")
            
            # Tirar print para confirmar
            pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
            os.makedirs(pasta_prints, exist_ok=True)
            navegador.save_screenshot(os.path.join(pasta_prints, "apos_login.png"))
        
        return navegador
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        navegador.quit()
        return None
