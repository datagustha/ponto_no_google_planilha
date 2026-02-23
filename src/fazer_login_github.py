# src/fazer_login_github.py - VERSÃO PARA GITHUB ACTIONS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def login_github_actions():
    """
    Versão do login para GitHub Actions (headless)
    """
    print("=" * 50)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 50)
    
    # Configurações headless para GitHub Actions
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("🚀 Iniciando Chrome headless...")
    navegador = webdriver.Chrome(options=chrome_options)
    
    # Esconder automação
    navegador.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Acessar site
    print("🌐 Acessando site...")
    navegador.get("https://pontoweb.secullum.com.br/")
    time.sleep(5)
    
    # Tentar clicar no botão "Acessar ponto Web" se existir
    try:
        print("🔍 Procurando botão 'Acessar ponto Web'...")
        botao_acessar = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Acessar ponto Web')]"))
        )
        botao_acessar.click()
        print("✅ Clicou no botão Acessar ponto Web")
        time.sleep(3)
    except (TimeoutException, NoSuchElementException):
        print("ℹ️ Botão não encontrado, continuando...")
    
    # LOGIN
    print("\n🔐 FAZENDO LOGIN...")
    
    try:
        # Email
        campo_email = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        campo_email.send_keys(os.getenv("EMAIL_SISTEMA"))
        print("✅ Email inserido")
        
        # Senha
        campo_senha = navegador.find_element(By.ID, "Senha")
        campo_senha.send_keys(os.getenv("SENHA_SISTEMA"))
        print("✅ Senha inserida")
        
        # Botão Entrar
        botao = navegador.find_element(By.ID, "login")
        botao.click()
        print("🖱 Clicou em Entrar")
        
        time.sleep(5)
        
        # Fechar popup se aparecer
        try:
            popup = WebDriverWait(navegador, 3).until(
                EC.element_to_be_clickable((By.ID, "modal-portaria-671-ok"))
            )
            popup.click()
            print("✅ Popup fechado")
        except:
            pass
        
        print("✅ LOGIN REALIZADO!")
        return navegador
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None