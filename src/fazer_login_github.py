# src/fazer_login_github.py - VERSÃO COM HEADERS E COOKIES

import os
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_github_actions():
    """Versão com headers realísticos para GitHub Actions"""
    
    print("=" * 58)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 58)
    
    # Configuração do Chrome com opções anti-detecção
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # Opções para parecer um navegador real
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-features=BlinkGenPropertyTrees")
    
    # User agent de Windows/Chrome real
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Remover evidências de automação
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("🚀 Iniciando Chrome headless...")
    navegador = webdriver.Chrome(options=chrome_options)
    
    # Script para remover vestígios de automação
    navegador.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en-US', 'en']});
    """)
    
    try:
        # PASSO 1: Primeiro acessar a página de login DIRETAMENTE (URL correta)
        print("\n🌐 Acessando página de login diretamente...")
        
        # URL direta do login (importante!)
        url_login = "https://app.secullum.com.br/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dpontoweb%26redirect_uri%3Dhttps%253A%252F%252Fpontoweb.secullum.com.br%252Fauth.html%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520email%2520offline_access%2520permissions%26state%3Dabc123%26nonce%3Dxyz789"
        
        # Tentar primeiro com a URL completa
        navegador.get(url_login)
        time.sleep(8)
        
        print(f"📍 URL atual: {navegador.current_url}")
        
        # Se ainda estiver na página institucional, tentar abordagem diferente
        if "secullum.com.br/pt" in navegador.current_url:
            print("⚠️ Redirecionado para página institucional. Tentando abordagem alternativa...")
            
            # Limpar cookies e tentar novamente
            navegador.delete_all_cookies()
            
            # Tentar acessar via pontoweb primeiro
            navegador.get("https://pontoweb.secullum.com.br/")
            time.sleep(5)
            
            # Procurar botão de login
            try:
                botao_login = navegador.find_element(By.XPATH, "//a[contains(@href, 'Account/Login')]")
                botao_login.click()
                print("✅ Clicou no link de login")
                time.sleep(5)
            except:
                # Tentar JavaScript para navegação
                navegador.execute_script("window.location.href = 'https://app.secullum.com.br/Account/Login';")
                time.sleep(5)
        
        # PASSO 2: VERIFICAR SE ESTAMOS NA PÁGINA DE LOGIN
        print("\n🔍 Verificando se está na página de login...")
        
        # Tirar print para diagnóstico
        pasta_prints = os.path.join(pathlib.Path(__file__).parent.parent, "prints")
        os.makedirs(pasta_prints, exist_ok=True)
        navegador.save_screenshot(os.path.join(pasta_prints, "pagina_atual.png"))
        print("📸 Print da página atual salvo")
        
        # PASSO 3: Tentar encontrar campos de login
        print("\n🔐 TENTANDO FAZER LOGIN...")
        
        # Tentar múltiplos seletores para o campo de email
        campo_email = None
        seletores_email = [
            (By.ID, "login"),
            (By.ID, "Email"),
            (By.ID, "username"),
            (By.NAME, "login"),
            (By.NAME, "email"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.CSS_SELECTOR, "input[placeholder*='mail']"),
        ]
        
        for by, selector in seletores_email:
            try:
                campo_email = WebDriverWait(navegador, 3).until(
                    EC.presence_of_element_located((by, selector))
                )
                print(f"✅ Campo email encontrado com: {selector}")
                break
            except:
                continue
        
        if not campo_email:
            # Se não encontrar, listar todos os inputs
            print("\n📋 Inputs encontrados na página:")
            inputs = navegador.find_elements(By.TAG_NAME, "input")
            for i, inp in enumerate(inputs):
                tipo = inp.get_attribute("type")
                id_ = inp.get_attribute("id")
                name = inp.get_attribute("name")
                print(f"   {i+1}. type={tipo}, id={id_}, name={name}")
            
            raise Exception("Não encontrou campo de email")
        
        campo_email.clear()
        campo_email.send_keys(os.getenv("EMAIL_SISTEMA"))
        print("✅ Email inserido")
        
        # Campo de senha
        campo_senha = None
        seletores_senha = [
            (By.ID, "senha"),
            (By.ID, "password"),
            (By.ID, "Password"),
            (By.NAME, "senha"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
        ]
        
        for by, selector in seletores_senha:
            try:
                campo_senha = navegador.find_element(by, selector)
                print(f"✅ Campo senha encontrado com: {selector}")
                break
            except:
                continue
        
        if not campo_senha:
            raise Exception("Não encontrou campo de senha")
        
        campo_senha.clear()
        campo_senha.send_keys(os.getenv("SENHA_SISTEMA"))
        print("✅ Senha inserida")
        
        # Botão de login
        botao_entrar = None
        seletores_botao = [
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Entrar')]"),
            (By.XPATH, "//button[contains(text(), 'Login')]"),
            (By.XPATH, "//input[@type='submit']"),
        ]
        
        for by, selector in seletores_botao:
            try:
                botao_entrar = navegador.find_element(by, selector)
                print(f"✅ Botão encontrado com: {selector}")
                break
            except:
                continue
        
        if not botao_entrar:
            raise Exception("Não encontrou botão de login")
        
        botao_entrar.click()
        print("🖱 Clicou em Entrar")
        
        # Aguardar login
        time.sleep(10)
        
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
        
        if "relatorios" in navegador.current_url.lower() or "homerelatorios" in navegador.current_url.lower():
            print("\n✅✅✅ LOGIN E ACESSO A RELATÓRIOS CONCLUÍDOS!")
        else:
            print("\n⚠️ URL final não é de relatórios, mas vamos continuar...")
        
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
