# dados_ponto.py - VERSÃO FINAL GITHUB ACTIONS 100% ESTÁVEL

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import pathlib


# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================

MODO_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

pasta_arquivo = pathlib.Path(__file__).parent.parent
pasta_prints = os.path.join(pasta_arquivo, "prints")
os.makedirs(pasta_prints, exist_ok=True)


# =========================================================
# CRIAR NAVEGADOR STEALTH
# =========================================================

def criar_navegador():
    chrome_options = Options()

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Headless moderno
    chrome_options.add_argument("--headless=new")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)

    # Remove navigator.webdriver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
            """
        },
    )

    return driver


# =========================================================
# PRINT DEBUG
# =========================================================

def tirar_print(navegador, nome_arquivo, descricao=""):
    try:
        caminho = os.path.join(pasta_prints, nome_arquivo)
        navegador.save_screenshot(caminho)
        print(f"📸 Print salvo: {nome_arquivo} {descricao}")
        return True
    except Exception as e:
        print(f"❌ Erro ao tirar print: {e}")
        return False


# =========================================================
# ACESSAR RELATÓRIOS
# =========================================================

def acessar_calculos(navegador):
    print("\n" + "=" * 60)
    print("🔍 ACESSANDO RELATÓRIOS / CÁLCULOS")
    print("=" * 60)

    tirar_print(navegador, "00_antes_acessar.png")

    time.sleep(10 if MODO_GITHUB else 5)

    try:
        navegador.get("https://pontoweb.secullum.com.br/#/homerelatorios")
        WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.ID, "dataInicio"))
        )
        print("✅ Página de relatórios carregada")
        tirar_print(navegador, "01_relatorios.png")
        return True

    except Exception as e:
        print(f"❌ Falha ao acessar relatórios: {e}")
        tirar_print(navegador, "erro_relatorios.png")
        return False


# =========================================================
# POPUP PERÍODO
# =========================================================

def periodo_pop_up(navegador):
    try:
        botao = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.ID, "btnNo"))
        )
        botao.click()
        print("✅ Popup fechado")
        time.sleep(1)
    except:
        print("ℹ️ Nenhum popup")


# =========================================================
# CONFIGURAR DATAS
# =========================================================

def configurar_datas(navegador):
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)

    data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
    data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"

    print(f"📅 Período: {data_inicio} → {data_fim}")

    try:
        inicio = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.ID, "dataInicio"))
        )
        fim = navegador.find_element(By.ID, "dataFim")

        for campo, valor in [(inicio, data_inicio), (fim, data_fim)]:
            campo.click()
            campo.send_keys(Keys.CONTROL + "a")
            campo.send_keys(Keys.DELETE)
            time.sleep(0.5)
            campo.send_keys(valor)
            time.sleep(0.5)

        navegador.execute_script("""
            document.getElementById('dataInicio').dispatchEvent(new Event('change', {bubbles:true}));
            document.getElementById('dataFim').dispatchEvent(new Event('change', {bubbles:true}));
        """)

        print("✅ Datas configuradas")
        return True

    except Exception as e:
        print(f"❌ Erro ao configurar datas: {e}")
        return False


# =========================================================
# ATUALIZAR RELATÓRIO
# =========================================================

def clicar_atualizar(navegador):
    print("🖱️ Atualizando relatório...")

    try:
        botao = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.ID, "btnAtualizar"))
        )
        navegador.execute_script("arguments[0].click();", botao)

        WebDriverWait(navegador, 30).until(
            lambda d: d.execute_script(
                "return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length > 0"
            )
        )

        print("✅ Relatório carregado")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
        tirar_print(navegador, "erro_atualizar.png")
        return False


# =========================================================
# OBTER FUNCIONÁRIO ATUAL
# =========================================================

def obter_funcionario_atual(navegador):
    try:
        nome = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[id*='react-select']"))
        ).text.strip()

        print(f"👤 Funcionário: {nome}")
        return nome

    except:
        print("❌ Nome não encontrado")
        return None


# =========================================================
# AVANÇAR FUNCIONÁRIO
# =========================================================

def avancar_funcionario(navegador):
    seletores = [
        "i.fa-arrow-right",
        "button i.fa-arrow-right",
        "[class*='arrow-right']",
        "button[title*='Próximo']",
    ]

    for seletor in seletores:
        try:
            seta = navegador.find_element(By.CSS_SELECTOR, seletor)
            navegador.execute_script("arguments[0].click();", seta)
            time.sleep(3)
            return True
        except:
            continue

    print("❌ Não achou botão próximo")
    return False


# =========================================================
# EXTRAIR DADOS DA TABELA
# =========================================================

def extrair_dados(navegador):
    print("📊 Extraindo dados...")

    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    navegador.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    try:
        WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabela-calculos-wrapper"))
        )

        dados = navegador.execute_script("""
            let linhas = document.querySelectorAll('.tabela-calculos-wrapper tbody tr');
            let dados = [];

            linhas.forEach(l => {
                let td = l.querySelectorAll('td');
                if (td.length >= 19) {
                    let data = td[2].innerText.trim();
                    let bSaldo = td[17].innerText.trim().replace('+','');
                    let bTotal = td[18].innerText.trim().replace('+','');
                    if (data) dados.push([data, bSaldo, bTotal]);
                }
            });

            return dados;
        """)

        print(f"✅ {len(dados)} linhas coletadas")

        return pd.DataFrame(dados, columns=["Data", "BSaldo", "BTotal"])

    except Exception as e:
        print(f"❌ Erro extração: {e}")
        return pd.DataFrame()


# =========================================================
# PROCESSAR TODOS FUNCIONÁRIOS
# =========================================================

def processar_todos_funcionarios(navegador, callback_processar, max_tentativas=40):
    print("\n🚀 INICIANDO PROCESSAMENTO")

    if not acessar_calculos(navegador):
        return 0

    periodo_pop_up(navegador)

    if not configurar_datas(navegador):
        return 0

    if not clicar_atualizar(navegador):
        return 0

    contador = 0
    historico = []

    for i in range(max_tentativas):
        print(f"\n🔄 Funcionário {i+1}/{max_tentativas}")

        nome = obter_funcionario_atual(navegador)

        if not nome:
            avancar_funcionario(navegador)
            continue

        if nome in historico:
            print("🔁 Loop detectado, encerrando")
            break

        historico.append(nome)

        df = extrair_dados(navegador)

        if not df.empty:
            if callback_processar(nome, df):
                contador += 1
                print(f"✅ Processado: {nome}")
        else:
            print("⚠️ Tabela vazia")

        if not avancar_funcionario(navegador):
            break

    tirar_print(navegador, "99_final.png")
    print(f"\n🏁 Finalizado: {contador} funcionários processados")

    return contador


# =========================================================
# FUNÇÃO SIMPLES PARA TESTE
# =========================================================

def dados(navegador):
    acessar_calculos(navegador)
    nome = obter_funcionario_atual(navegador)
    df = extrair_dados(navegador)
    return nome, df
