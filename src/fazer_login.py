# 📚 bibliotecas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()

def login():
    # 🔧 configurações
    navegador = webdriver.Chrome()

    # 🌐 acessa o site
    navegador.get("https://pontoweb.secullum.com.br/#/cartao-ponto")

    # 📝 Esperar site abrir e expandir
    try:
        #aguardando repsosta do site
        aguardar_site = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Acessar Ponto Web')]"))).text
        print(f'resposta do site: {aguardar_site}')

        # enquanto não carregar o site, aguarda
        while aguardar_site != "Acessar Ponto Web":

            #aguardando repsosta do site
            aguardar_site = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Acessar Ponto Web')]"))).text
            print(f'Nova resposta do site: {aguardar_site}')
            # se carregar, maximiza a tela
            if aguardar_site == "Acessar Ponto Web":
                print("✅ Site carregado com sucesso")
                break
            
            else:
                print("⏳Aguardando o site carregar...")
                time.sleep(2)

        # Maximizar a tela
        print("🖥Maximizando a tela...")
        navegador.maximize_window()

        # clicar em acessar ponto web
        print("🖱Clicando em Acessar Ponto Web...")
        elemento_acessar = navegador.find_element(By.XPATH, "//a[contains(., 'Acessar Ponto Web')]")
        elemento_acessar.click()

    except:
        print("Erro ao carregar o site")
        elemento_acessar = navegador.find_element(By.XPATH, "//a[contains(., 'Acessar Ponto Web')]").text
        print(aguardar_site)

    # 📃 login e senha
    # inserir o login
    # encontrar o campo de login
    campo_login = navegador.find_element(By.ID, "Email")

    login_usuario = os.getenv("EMAIL_SISTEMA")
    campo_login.send_keys(login_usuario)
    print("✅ Login inserido com sucesso")

    # encontrar o campo de senha
    campo_senha = navegador.find_element(By.ID, "Senha")
    # inserir a senha
    senha_usuario = os.getenv("SENHA_SISTEMA")
    campo_senha.send_keys(senha_usuario)
    print("✅ Senha inserida com sucesso")


    # encontrar o botão de login
    botao_entrar = navegador.find_element(By.ID, "login").click()
    print("🖱 Clicando no botão Entrar...")

    # 📜 fechar pop up
    try:
        # Primeiro verifica se o elemento existe (sem tentar pegar .text logo)
        popup_element = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "modal-portaria-671-ok"))
        )
        
        # Agora pega o texto
        popup_text = popup_element.text
        print(f"Popup encontrado. Texto: {popup_text}")

        # Clica no popup
        popup_element.click()
        print("🖱 Clicando no botão OK do popup...")

    except TimeoutException:
        # Isso é NORMAL - nem sempre o popup aparece
        print("ℹ️ Nenhum popup encontrado (isso é normal). Continuando...")
        
    except Exception as e:
        # Outros erros inesperados
        print(f"⚠️ Erro inesperado ao lidar com popup: {e}")
        # Continue mesmo assim
        pass

    return navegador