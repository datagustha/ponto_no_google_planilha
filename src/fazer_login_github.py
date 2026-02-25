# src/fazer_login_github.py - VERSÃO COM CORREÇÃO DE DNS

import os
import time
import pathlib
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_github_actions():
    """Versão com correção de DNS para GitHub Actions"""
    
    print("=" * 58)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 58)
    
    # TESTAR RESOLUÇÃO DE DNS PRIMEIRO
    print("\n🔍 Testando resolução de DNS...")
    dominios_teste = [
        "pontoweb.secullum.com.br",
        "app.secullum.com.br", 
        "www.secullum.com.br",
        "secullum.com.br"
    ]
    
    for dominio in dominios_teste:
        try:
            ip = socket.gethostbyname(dominio)
            print(f"   ✅ {dominio} -> {ip}")
        except Exception as e:
            print(f"   ❌ {dominio}: {e}")
    
    # Configuração do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # IMPORTANTE: Adicionar flags de DNS
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("\n🚀 Iniciando Chrome headless...")
    navegador = webdriver.Chrome(options=chrome_options)
    
    # Executar script para evitar detecção
    navegador.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # TENTAR PRIMEIRO O DOMÍNIO PRINCIPAL (que já funcionou antes)
        print("\n🌐 Tentando acesso direto ao PontoWeb...")
        navegador.get("https://pontoweb.secullum.com.br/")
        time.sleep(8)
        
        print(f"📍 URL atual: {navegador.current_url}")
        
        # Verificar se precisa clicar no botão "Acessar ponto Web"
        if "Account/Login" not in navegador.current_url:
            try:
                print("🔍 Procurando botão 'Acessar ponto Web'...")
                botao = WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Acessar ponto Web')]"))
                )
                botao.click()
                print("✅ Clicou no botão")
                time.sleep(5)
            except:
                print("ℹ️ Botão não encontrado, talvez já esteja na página de login")
        
        # AGORA FAZER LOGIN
        print("\n🔐 FAZENDO LOGIN...")
        
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
        
        # VERIFICAR SE LOGOU
        pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
        os.makedirs(pasta_prints, exist_ok=True)
        
        # Print após login
        navegador.save_screenshot(os.path.join(pasta_prints, "apos_login.png"))
        print("📸 Print após login salvo")
        
        # IR PARA RELATÓRIOS
        print("\n📊 Indo para relatórios...")
        navegador.get("https://pontoweb.secullum.com.br/#/homerelatorios")
        time.sleep(8)
        
        # Print da página de relatórios
        navegador.save_screenshot(os.path.join(pasta_prints, "relatorios.png"))
        print("📸 Print da página de relatórios salvo")
        
        print(f"\n📍 URL final: {navegador.current_url}")
        
        if "relatorios" in navegador.current_url.lower():
            print("\n✅✅✅ LOGIN E ACESSO A RELATÓRIOS CONCLUÍDOS!")
            return navegador
        else:
            print("\n⚠️ Pode não ter entrado em relatórios, mas vamos continuar...")
            return navegador
        
    except Exception as e:
        print(f"\n❌ ERRO NO LOGIN: {e}")
        print(f"📍 URL no erro: {navegador.current_url}")
        
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
