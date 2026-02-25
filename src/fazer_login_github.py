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
    """
    Login + navegação completa para GitHub Actions (headless)
    Usando Selenium Manager (mais estável que webdriver-manager)
    """
    print("=" * 60)
    print("🔧 CONFIGURANDO CHROME PARA GITHUB ACTIONS")
    print("=" * 60)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 👉 Selenium Manager resolve driver automaticamente
    navegador = webdriver.Chrome(options=chrome_options)

    # Remove flag webdriver
    navegador.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
            """
        },
    )

    print("🚀 Chrome iniciado com Selenium Manager")

    # =========================================================
    # ACESSAR SITE
    # =========================================================

    print("🌐 Acessando site...")
    navegador.get("https://pontoweb.secullum.com.br/")

    wait = WebDriverWait(navegador, 30)
    time.sleep(5)

    # =========================================================
    # BOTÃO "ACESSAR PONTO WEB"
    # =========================================================

    try:
        print("🔍 Procurando botão 'Acessar ponto Web'...")
        botao_acessar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Acessar ponto Web')]"))
        )
        navegador.execute_script("arguments[0].click();", botao_acessar)
        print("✅ Clicou em 'Acessar ponto Web'")
        time.sleep(3)
    except (TimeoutException, NoSuchElementException):
        print("ℹ️ Botão não encontrado — seguindo fluxo normal")

    # =========================================================
    # LOGIN
    # =========================================================

    print("\n🔐 REALIZANDO LOGIN...")

    try:
        campo_email = wait.until(EC.presence_of_element_located((By.ID, "Email")))
        campo_email.send_keys(os.getenv("EMAIL_SISTEMA"))
        print("✅ Email inserido")

        campo_senha = navegador.find_element(By.ID, "Senha")
        campo_senha.send_keys(os.getenv("SENHA_SISTEMA"))
        print("✅ Senha inserida")

        botao = navegador.find_element(By.ID, "login")
        navegador.execute_script("arguments[0].click();", botao)
        print("🖱 Clicou em Entrar")

        time.sleep(6)

        # =========================================================
        # FECHAR POPUP
        # =========================================================

        try:
            popup = WebDriverWait(navegador, 5).until(
                EC.element_to_be_clickable((By.ID, "modal-portaria-671-ok"))
            )
            navegador.execute_script("arguments[0].click();", popup)
            print("✅ Popup fechado")
            time.sleep(2)
        except:
            print("ℹ️ Nenhum popup exibido")

        print("✅ LOGIN REALIZADO COM SUCESSO")
        return navegador

    except Exception as e:
        print(f"❌ ERRO NO LOGIN: {e}")
        return None
