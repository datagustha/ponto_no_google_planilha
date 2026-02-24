# diagnosticar_idioma.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime

def diagnosticar_idioma():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE IDIOMA")
    print("=" * 60)
    
    # Criar pasta para screenshots
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Verificar idioma do navegador
        lang = driver.execute_script("return navigator.language;")
        languages = driver.execute_script("return navigator.languages;")
        
        print(f"\n🌐 Configurações do navegador:")
        print(f"navigator.language: {lang}")
        print(f"navigator.languages: {languages}")
        
        # Acessar Google
        print(f"\n📡 Acessando Google...")
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Tirar print do Google
        driver.save_screenshot(f"screenshots/google_{timestamp}.png")
        print(f"✅ Print salvo: google_{timestamp}.png")
        
        # Verificar idioma do Google
        html_lang = driver.find_element("tag name", "html").get_attribute("lang")
        print(f"HTML lang Google: {html_lang}")
        
        # Acessar site do seu sistema (substitua pela URL que você usa)
        # Vamos usar um site exemplo que muda conforme idioma
        print(f"\n📡 Acessando site de exemplo com data...")
        driver.get("https://www.timeanddate.com/")  # Site que mostra data
        time.sleep(3)
        
        # Tirar print
        driver.save_screenshot(f"screenshots/site_data_{timestamp}.png")
        print(f"✅ Print salvo: site_data_{timestamp}.png")
        
        # Procurar elementos com data
        try:
            # Tenta encontrar algum elemento que mostre data
            elementos = driver.find_elements("xpath", "//*[contains(text(), '202')]")
            if elementos:
                print(f"✅ Encontrado elemento com data: {elementos[0].text[:50]}")
        except:
            pass
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()
        print(f"\n📸 Screenshots salvos na pasta 'screenshots/'")

if __name__ == "__main__":
    diagnosticar_idioma()
