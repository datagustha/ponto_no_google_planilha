# src/dados_ponto.py - VERSÃO FINAL ESTÁVEL

import os
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# =========================================================
# CONFIG
# =========================================================

MODO_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'


# =========================================================
# ACESSAR RELATÓRIOS / CÁLCULOS
# =========================================================

def acessar_calculos(navegador):
    print("\n" + "=" * 50)
    print("🔍 ACESSANDO RELATÓRIOS / CÁLCULOS")
    print("=" * 50)

    time.sleep(5)

    wait = WebDriverWait(navegador, 30)

    # Tentativa 1 — Menu Relatórios
    try:
        relatorio = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Relatórios')]"))
        )
        relatorio.click()
        time.sleep(3)
    except:
        pass

    # Tentativa 2 — Botão Cálculos
    try:
        calculo = wait.until(EC.element_to_be_clickable((By.ID, "calculos")))
        calculo.click()
        time.sleep(4)
        print("✅ Entrou em Cálculos")
        return True
    except:
        pass

    # Tentativa 3 — Busca genérica
    try:
        elementos = navegador.find_elements(By.XPATH, "//*[contains(text(), 'Cálculos')]")
        for e in elementos:
            if e.is_displayed() and e.is_enabled():
                e.click()
                time.sleep(4)
                print("✅ Entrou em Cálculos (fallback)")
                return True
    except:
        pass

    print("❌ NÃO CONSEGUIU ACESSAR CÁLCULOS")
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
            campo.send_keys(valor)
            time.sleep(0.5)

        navegador.execute_script("""
            document.getElementById('dataInicio').dispatchEvent(new Event('change', {bubbles:true}));
            document.getElementById('dataFim').dispatchEvent(new Event('change', {bubbles:true}));
        """)

        return True
    except Exception as e:
        print(f"❌ Erro ao configurar datas: {e}")
        return False


# =========================================================
# ATUALIZAR RELATÓRIO
# =========================================================

def clicar_atualizar(navegador):
    print("🖱 Atualizando relatório...")

    try:
        botao = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.ID, "btnAtualizar"))
        )
        navegador.execute_script("arguments[0].click();", botao)

        WebDriverWait(navegador, 40).until(
            lambda d: d.execute_script(
                "return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length > 0"
            )
        )

        print("✅ Relatório carregado")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
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

    try:
        WebDriverWait(navegador, 40).until(
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

        return pd.DataFrame(dados, columns=["Data", "BSaldo", "BTotal"])

    except:
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
            if not avancar_funcionario(navegador):
                break
            continue

        if nome in historico:
            print("🔁 Loop detectado — encerrando")
            break

        historico.append(nome)

        df = extrair_dados(navegador)

        if not df.empty:
            if callback_processar(nome, df):
                contador += 1
        else:
            print("⚠️ Tabela vazia")

        if not avancar_funcionario(navegador):
            break

    print(f"\n🏁 Finalizado: {contador} funcionários processados")
    return contador
