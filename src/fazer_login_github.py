# src/fazer_login_github.py - VERSÃO CORRIGIDA (sem webdriver-manager)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def login_github_actions():
    """
    Versão do login otimizada para GitHub Actions
    SEM webdriver-manager - usa ChromeDriver do sistema
    """
    print("=" * 50)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 50)
    
    # Configurações específicas para GitHub Actions
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
    
    # No GitHub Actions, o ChromeDriver já está no PATH
    print("🚀 Iniciando Chrome (usando ChromeDriver do sistema)...")
    
    # NÃO usar Service, apenas options
    navegador = webdriver.Chrome(options=chrome_options)
    
    # Esconder que é automação
    navegador.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Acessar o site
    print("🌐 Acessando Secullum Ponto Web...")
    navegador.get("https://pontoweb.secullum.com.br/#/cartao-ponto")
    time.sleep(3)
    
    # Aguardar carregamento
    try:
        print("⏳ Aguardando site carregar...")
        aguardar_site = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Acessar Ponto Web')]"))
        )
        print("✅ Site carregado com sucesso")
        
        print("🖱 Clicando em Acessar Ponto Web...")
        aguardar_site.click()
        time.sleep(2)
        
    except TimeoutException:
        print("❌ Timeout ao carregar site")
        try:
            elemento_acessar = navegador.find_element(By.XPATH, "//a[contains(., 'Acessar Ponto Web')]")
            elemento_acessar.click()
            print("✅ Conseguiu clicar no botão")
        except Exception as e:
            print(f"❌ Não conseguiu clicar: {e}")
            return None
    
    # Login
    print("\n🔐 FAZENDO LOGIN...")
    
    try:
        # Campo de email
        campo_login = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        login_usuario = os.getenv("EMAIL_SISTEMA")
        campo_login.send_keys(login_usuario)
        print(f"✅ Login inserido: {login_usuario[:3]}...")
        
        # Campo de senha
        campo_senha = navegador.find_element(By.ID, "Senha")
        senha_usuario = os.getenv("SENHA_SISTEMA")
        campo_senha.send_keys(senha_usuario)
        print("✅ Senha inserida")
        
        # Botão entrar
        navegador.find_element(By.ID, "login").click()
        print("🖱 Clicou no botão Entrar")
        time.sleep(3)
        
        # Fechar popup se aparecer
        try:
            popup = WebDriverWait(navegador, 5).until(
                EC.element_to_be_clickable((By.ID, "modal-portaria-671-ok"))
            )
            popup.click()
            print("✅ Popup fechado")
        except:
            print("ℹ️ Nenhum popup encontrado")
        
        print("✅ LOGIN REALIZADO COM SUCESSO!")
        return navegador
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None