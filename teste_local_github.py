from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def login_github_actions():
    """Login SIMPLES para teste local"""
    print("=" * 50)
    print("🚀 INICIANDO CHROME")
    print("=" * 50)
    
    # Chrome NORMAL (com janela)
    navegador = webdriver.Chrome()
    navegador.maximize_window()
    
    # Acessar site
    print("🌐 Acessando site...")
    navegador.get("https://pontoweb.secullum.com.br/")
    time.sleep(3)
    
    # Login
    print("\n🔐 FAZENDO LOGIN...")
    
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
    
    # Botão
    botao = navegador.find_element(By.ID, "login")
    botao.click()
    print("🖱 Clicou em Entrar")
    
    time.sleep(5)
    
    # Fechar popup se aparecer
    try:
        popup = navegador.find_element(By.ID, "modal-portaria-671-ok")
        popup.click()
        print("✅ Popup fechado")
    except:
        pass
    
    print("✅ LOGIN OK!")
    return navegador