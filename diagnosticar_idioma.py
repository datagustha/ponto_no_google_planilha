# diagnosticar_com_login.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()

def diagnosticar_com_login():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO COMPLETO - LOGIN + CÁLCULOS")
    print("=" * 60)
    
    # Criar pasta para screenshots
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # FORÇAR IDIOMA PORTUGUÊS (vamos testar se funciona)
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--accept-lang=pt-BR')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. VERIFICAR IDIOMA INICIAL
        print("\n🌐 Verificando idioma configurado...")
        lang = driver.execute_script("return navigator.language;")
        print(f"navigator.language: {lang}")
        
        # 2. FAZER LOGIN
        print("\n🔑 Fazendo login...")
        driver.get("https://www.pontomais.com.br")  # AJUSTE PARA SUA URL
        
        # Tirar print da tela de login
        time.sleep(3)
        driver.save_screenshot(f"screenshots/1_tela_login_{timestamp}.png")
        print("✅ Print: 1_tela_login")
        
        # Preencher login (AJUSTE SELETORES CONFORME SEU SITE)
        try:
            # Exemplo - ajustar para seu site
            usuario = driver.find_element(By.ID, "username")
            usuario.send_keys(os.getenv("PONTOMAIS_USER"))
            
            senha = driver.find_element(By.ID, "password")
            senha.send_keys(os.getenv("PONTOMAIS_PASS"))
            
            botao = driver.find_element(By.ID, "login-btn")
            botao.click()
            
            print("✅ Credenciais preenchidas")
        except Exception as e:
            print(f"⚠️ Erro ao preencher login: {e}")
            driver.save_screenshot(f"screenshots/1_erro_login_{timestamp}.png")
        
        # Aguardar login
        time.sleep(5)
        driver.save_screenshot(f"screenshots/2_apos_login_{timestamp}.png")
        print("✅ Print: 2_apos_login")
        
        # 3. ACESSAR CÁLCULOS
        print("\n📊 Acessando cálculos...")
        try:
            # Tentar encontrar link/botão de cálculos
            # AJUSTE O SELETOR PARA SEU SITE
            link_calculos = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Cálculos"))
            )
            link_calculos.click()
            print("✅ Link de cálculos clicado")
        except:
            try:
                link_calculos = driver.find_element(By.PARTIAL_LINK_TEXT, "Cálculo")
                link_calculos.click()
                print("✅ Link parcial 'Cálculo' clicado")
            except Exception as e:
                print(f"⚠️ Erro ao acessar cálculos: {e}")
        
        time.sleep(5)
        driver.save_screenshot(f"screenshots/3_tela_calculos_{timestamp}.png")
        print("✅ Print: 3_tela_calculos")
        
        # 4. PROCURAR CAMPOS DE DATA
        print("\n📅 Procurando campos de data...")
        
        # Salvar HTML da página para análise
        with open(f"screenshots/pagina_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ HTML salvo")
        
        # Listar todos os inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n📝 Inputs encontrados: {len(inputs)}")
        for i, input_elem in enumerate(inputs[:10]):  # Primeiros 10 inputs
            try:
                tipo = input_elem.get_attribute("type")
                nome = input_elem.get_attribute("name")
                id_elem = input_elem.get_attribute("id")
                placeholder = input_elem.get_attribute("placeholder")
                print(f"  Input {i}: type={tipo}, name={nome}, id={id_elem}, placeholder={placeholder}")
            except:
                pass
        
        # Procurar especificamente campos de data
        campos_data = driver.find_elements(By.XPATH, "//input[@type='date'] | //input[contains(@placeholder, 'data')] | //input[contains(@placeholder, 'date')]")
        print(f"\n📆 Campos de data encontrados: {len(campos_data)}")
        for campo in campos_data:
            try:
                print(f"  Placeholder: {campo.get_attribute('placeholder')}")
                print(f"  ID: {campo.get_attribute('id')}")
                print(f"  Name: {campo.get_attribute('name')}")
            except:
                pass
        
        # 5. TIRAR PRINT FINAL DA TELA INTEIRA
        driver.save_screenshot(f"screenshots/4_tela_completa_{timestamp}.png")
        print("✅ Print: 4_tela_completa")
        
        # 6. RESUMO
        print("\n" + "=" * 60)
        print("📊 RESUMO DO DIAGNÓSTICO")
        print("=" * 60)
        print(f"Idioma detectado: {lang}")
        print(f"Screenshots salvos: {len(os.listdir('screenshots'))}")
        print(f"Pasta: screenshots/")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        driver.save_screenshot(f"screenshots/erro_fatal_{timestamp}.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    diagnosticar_com_login()
