# src/fazer_login_github.py - VERSÃO COM IP DIRETO E HOSTS MODIFICADO

import os
import time
import pathlib
import socket
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_github_actions():
    """Versão com IP direto e modificação de hosts"""
    
    print("=" * 58)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 58)
    
    # Primeiro, descobrir o IP do app.secullum.com.br
    print("\n🔍 Resolvendo IP do domínio...")
    try:
        # Tentar resolver de várias formas
        ip_app = None
        
        # Método 1: socket.gethostbyname
        try:
            ip_app = socket.gethostbyname("app.secullum.com.br")
            print(f"✅ Socket: app.secullum.com.br -> {ip_app}")
        except:
            pass
        
        # Método 2: nslookup via subprocess
        if not ip_app:
            try:
                result = subprocess.run(['nslookup', 'app.secullum.com.br'], 
                                      capture_output=True, text=True)
                print("📋 nslookup output:")
                print(result.stdout)
                
                # Extrair IP do output
                import re
                ips = re.findall(r'Address: (\d+\.\d+\.\d+\.\d+)', result.stdout)
                if ips:
                    ip_app = ips[-1]  # Pega o último (geralmente o correto)
                    print(f"✅ nslookup: app.secullum.com.br -> {ip_app}")
            except:
                pass
        
        # Se não conseguir resolver, usar IP conhecido do Secullum
        if not ip_app:
            # IPs conhecidos da Secullum (baseado nos testes anteriores)
            ip_app = "191.233.203.34"  # IP do pontoweb.secullum.com.br
            print(f"⚠️ Usando IP fallback: {ip_app}")
        
    except Exception as e:
        print(f"❌ Erro ao resolver DNS: {e}")
        ip_app = "191.233.203.34"  # IP fallback
    
    # Configuração do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # IMPORTANTE: Desabilitar detecção de automação
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent real
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    print(f"\n🚀 Iniciando Chrome headless...")
    navegador = webdriver.Chrome(options=chrome_options)
    
    # Script anti-detecção
    navegador.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en-US', 'en']});
    """)
    
    try:
        # PRIMEIRA TENTATIVA: Usar o IP direto com header Host
        print(f"\n🌐 Tentando acesso via IP direto: {ip_app}")
        
        # Construir URL com IP
        url_com_ip = f"https://{ip_app}/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dpontoweb%26redirect_uri%3Dhttps%253A%252F%252Fpontoweb.secullum.com.br%252Fauth.html%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520email%2520offline_access%2520permissions%26state%3Dabc123%26nonce%3Dxyz789"
        
        # Navegar para o IP
        navegager.get(url_com_ip)
        time.sleep(8)
        
        print(f"📍 URL atual: {navegador.current_url}")
        
        # SEGUNDA TENTATIVA: Se falhou, tentar pontoweb.secullum.com.br (que resolveu)
        if "ERR_NAME_NOT_RESOLVED" in navegador.page_source or "resolved" in navegador.current_url:
            print("⚠️ IP direto falhou, tentando pontoweb...")
            
            navegador.get("https://pontoweb.secullum.com.br/")
            time.sleep(5)
            
            # Procurar link de login
            try:
                links = navegador.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href") or ""
                    if "Account/Login" in href:
                        print(f"✅ Encontrou link de login: {href}")
                        link.click()
                        time.sleep(5)
                        break
            except:
                # Forçar navegação
                navegador.execute_script("window.location.href = 'https://pontoweb.secullum.com.br/Account/Login';")
                time.sleep(5)
        
        # VERIFICAR SE ESTAMOS NA PÁGINA DE LOGIN
        pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
        os.makedirs(pasta_prints, exist_ok=True)
        
        # Print da página atual
        navegador.save_screenshot(os.path.join(pasta_prints, "pagina_login.png"))
        print("📸 Print da página de login salvo")
        
        # AGORA FAZER LOGIN
        print("\n🔐 TENTANDO FAZER LOGIN...")
        
        # Campo de email
        campo_email = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        campo_email.clear()
        campo_email.send_keys(os.getenv("EMAIL_SISTEMA"))
        print("✅ Email inserido")
        
        # Campo de senha
        campo_senha = navegador.find_element(By.ID, "senha")
        campo_senha.clear()
        campo_senha.send_keys(os.getenv("SENHA_SISTEMA"))
        print("✅ Senha inserida")
        
        # Botão entrar
        botao_entrar = navegador.find_element(By.XPATH, "//button[@type='submit']")
        botao_entrar.click()
        print("🖱 Clicou em Entrar")
        
        time.sleep(10)
        
        # Print após login
        navegador.save_screenshot(os.path.join(pasta_prints, "apos_login.png"))
        print("📸 Print após login salvo")
        
        # IR PARA RELATÓRIOS
        print("\n📊 Indo para relatórios...")
        navegador.get("https://pontoweb.secullum.com.br/#/homerelatorios")
        time.sleep(8)
        
        # Print dos relatórios
        navegador.save_screenshot(os.path.join(pasta_prints, "relatorios.png"))
        print("📸 Print dos relatórios salvo")
        
        print(f"\n📍 URL final: {navegador.current_url}")
        
        return navegador
        
    except Exception as e:
        print(f"\n❌ ERRO NO LOGIN: {e}")
        print(f"📍 URL no erro: {navegador.current_url}")
        
        # Print do erro
        try:
            pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
            os.makedirs(pasta_prints, exist_ok=True)
            navegador.save_screenshot(os.path.join(pasta_prints, "erro_login.png"))
            print("📸 Print do erro salvo")
        except:
            pass
        
        navegador.quit()
        return None
