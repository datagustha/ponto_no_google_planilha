# diagnosticar_idioma.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def diagnosticar_idioma():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE IDIOMA")
    print("=" * 60)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Verificar idioma do navegador
        lang = driver.execute_script("return navigator.language;")
        languages = driver.execute_script("return navigator.languages;")
        
        print(f"\n🌐 Configurações do navegador:")
        print(f"navigator.language: {lang}")
        print(f"navigator.languages: {languages}")
        
        # Acessar um site para ver como interpreta
        print(f"\n📡 Acessando site de teste...")
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Verificar idioma que o site detectou
        html_lang = driver.find_element("tag name", "html").get_attribute("lang")
        print(f"HTML lang detectado: {html_lang}")
        
        # Verificar texto de um elemento comum
        try:
            elemento = driver.find_element("link", {"hreflang": "pt-BR"})
            print("✅ Site tem versão em português")
        except:
            print("⚠️ Site pode estar em inglês")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()
        
if __name__ == "__main__":
    diagnosticar_idioma()
