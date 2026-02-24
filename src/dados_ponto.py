# %%
# dados_ponto.py - VERSÃO DEFINITIVA COM JAVASCRIPT E PRINTS
# %%
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import pathlib

# Detectar se está rodando no GitHub Actions
MODO_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

# Configurar pasta para prints
pasta_arquivo = pathlib.Path(__file__).parent.parent
pasta_prints = os.path.join(pasta_arquivo, "prints")
os.makedirs(pasta_prints, exist_ok=True)

def tirar_print(navegador, nome_arquivo, descricao=""):
    """Tira print para debug"""
    try:
        caminho = os.path.join(pasta_prints, nome_arquivo)
        navegador.save_screenshot(caminho)
        print(f"📸 Print salvo: {nome_arquivo} {descricao}")
        return True
    except Exception as e:
        print(f"❌ Erro ao tirar print: {e}")
        return False

# 📓 Acessar área de cálculos - VERSÃO OTIMIZADA
def acessar_calculos(navegador):
    """Acessa a área de cálculos do ponto - OTIMIZADO PARA GITHUB ACTIONS"""
    
    print("\n" + "=" * 50)
    print("🔍 TENTANDO ACESSAR RELATÓRIOS E CÁLCULOS")
    print("=" * 50)
    
    # Print antes de acessar
    tirar_print(navegador, "00_antes_acessar.png", "(antes de acessar cálculos)")
    
    # Tempos de espera diferentes para GitHub Actions
    if MODO_GITHUB:
        print("⏳ GitHub Actions detectado - usando timeouts maiores...")
        espera_inicial = 10
        espera_elemento = 30
    else:
        espera_inicial = 3
        espera_elemento = 10
    
    time.sleep(espera_inicial)
    
    # TENTATIVA 1: Procurar por "Relatórios" no menu
    try:
        print("\n📋 Tentativa 1: Procurando 'Relatórios' no menu...")
        relatorio = WebDriverWait(navegador, espera_elemento).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Relatórios')]"))
        )
        print(f"✅ Encontrou: '{relatorio.text}'")
        relatorio.click()
        print("🖱 Clicou em Relatórios")
        time.sleep(3)
    except Exception as e:
        print(f"⚠️ Não encontrou 'Relatórios': {e}")
    
    # TENTATIVA 2: Procurar por "Cálculos" por ID
    try:
        print("\n📋 Tentativa 2: Procurando 'Cálculos' por ID...")
        calculo = WebDriverWait(navegador, espera_elemento).until(
            EC.element_to_be_clickable((By.ID, "calculos"))
        )
        print(f"✅ Encontrou: '{calculo.text}'")
        calculo.click()
        print("🖱 Clicou em Cálculos")
        time.sleep(3)
        print("✅✅✅ ACESSO AOS CÁLCULOS REALIZADO!")
        tirar_print(navegador, "01_acessou_calculos.png", "(após acessar cálculos)")
        return True
    except Exception as e:
        print(f"⚠️ Não encontrou 'Cálculos' por ID: {e}")
    
    # TENTATIVA 3: Busca genérica por texto
    try:
        print("\n📋 Tentativa 3: Busca genérica por 'Cálculos'...")
        elementos = navegador.find_elements(By.XPATH, "//*[contains(text(), 'Cálculos') or contains(text(), 'CALCULOS')]")
        if elementos:
            print(f"✅ Encontrou {len(elementos)} elementos")
            for elem in elementos:
                if elem.is_displayed() and elem.is_enabled():
                    elem.click()
                    print(f"🖱 Clicou em: {elem.text[:50]}")
                    time.sleep(3)
                    print("✅✅✅ ACESSO AOS CÁLCULOS REALIZADO!")
                    tirar_print(navegador, "01_acessou_calculos.png", "(após acessar cálculos)")
                    return True
    except Exception as e:
        print(f"⚠️ Busca genérica falhou: {e}")
    
    # TENTATIVA 4: JavaScript
    try:
        print("\n📋 Tentativa 4: Usando JavaScript...")
        resultado = navegador.execute_script("""
            var elementos = document.querySelectorAll('span, a, button, div');
            for(var i=0; i<elementos.length; i++) {
                var texto = elementos[i].textContent || '';
                if(texto.includes('Cálculos') || texto.includes('CALCULOS')) {
                    elementos[i].click();
                    return true;
                }
            }
            return false;
        """)
        if resultado:
            print("✅ JavaScript conseguiu clicar!")
            time.sleep(3)
            tirar_print(navegador, "01_acessou_calculos.png", "(após acessar cálculos)")
            return True
    except Exception as e:
        print(f"⚠️ JavaScript falhou: {e}")
    
    # TENTATIVA 5: Tentar URL direta (se souber)
    try:
        print("\n📋 Tentativa 5: Tentando URL direta...")
        navegador.get("https://pontoweb.secullum.com.br/#/calculos")
        time.sleep(5)
        if "calculos" in navegador.current_url.lower():
            print("✅ URL direta funcionou!")
            tirar_print(navegador, "01_acessou_calculos.png", "(após URL direta)")
            return True
    except:
        pass
    
    print("\n❌❌❌ NÃO CONSEGUIU ACESSAR CÁLCULOS")
    return False


# 📅 periodo informado (igual ao seu original)
def periodo_pop_up(navegador):
    """Fecha o popup de período (quando tem mais de 60 dias) se aparecer"""
    try:
        pop_up = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.ID, "btnNo"))
        )
        pop_up_name = pop_up.text.strip()
        if pop_up_name == "Não":
            print("✅ Pop up de período encontrado - Fechando...")
            pop_up.click()
            time.sleep(1)
            return True
        else:
            print("⚠️ Pop up encontrado mas não é o esperado")
            return False
    except (NoSuchElementException, TimeoutException):
        print("ℹ️ Nenhum pop up de período encontrado")
        return False
    except Exception as e:
        print(f"⚠️ Erro ao verificar popup: {e}")
        return False


def configurar_datas_com_javascript_agressivo(navegador):
    """Configura datas usando JavaScript MUITO agressivo - 100% confiável"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    # FORMATO AMERICANO (MM/DD/YYYY) para enviar ao site
    data_inicio_us = f"{hoje.month:02d}/01/{hoje.year}"
    data_fim_us = f"{ontem.month:02d}/{ontem.day:02d}/{ontem.year}"
    
    # FORMATO BRASILEIRO (DD/MM/YYYY) só para exibição
    data_inicio_br = f"01/{hoje.month:02d}/{hoje.year}"
    data_fim_br = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS VIA JAVASCRIPT AGRESSIVO")
    print(f"Data início (BR): {data_inicio_br} → Enviando (US): {data_inicio_us}")
    print(f"Data fim (BR): {data_fim_br} → Enviando (US): {data_fim_us}")
    print("=" * 50)
    
    try:
        # Script JavaScript super agressivo
        script = f"""
        (function() {{
            console.log("🔄 Iniciando configuração agressiva de datas...");
            
            function dispararTodosEventos(elemento) {{
                if (!elemento) return;
                
                // Disparar TODOS os eventos possíveis
                var eventos = ['input', 'change', 'blur', 'keyup', 'keydown', 'keypress', 'focus'];
                eventos.forEach(function(tipo) {{
                    try {{
                        var evento = new Event(tipo, {{ bubbles: true, cancelable: true }});
                        elemento.dispatchEvent(evento);
                    }} catch(e) {{}}
                }});
                
                // Se for React, atualizar tracker
                if (elemento._valueTracker) {{
                    elemento._valueTracker.setValue(elemento.value);
                }}
            }}
            
            // 1️⃣ DATA INÍCIO
            var inicio = document.getElementById('dataInicio');
            if (inicio) {{
                inicio.focus();
                inicio.value = '';  // Limpar
                inicio.value = '{data_inicio_us}';
                dispararTodosEventos(inicio);
                inicio.blur();
                console.log("✅ Data início setada:", inicio.value);
            }}
            
            // 2️⃣ DATA FIM
            var fim = document.getElementById('dataFim');
            if (fim) {{
                fim.focus();
                fim.value = '';  // Limpar
                fim.value = '{data_fim_us}';
                dispararTodosEventos(fim);
                fim.blur();
                console.log("✅ Data fim setada:", fim.value);
            }}
            
            // 3️⃣ VERIFICAÇÃO
            return {{
                inicio: document.getElementById('dataInicio')?.value || 'não encontrado',
                fim: document.getElementById('dataFim')?.value || 'não encontrado'
            }};
        }})();
        """
        
        # Executar script
        resultado = navegador.execute_script(script)
        
        print(f"\n🔍 VERIFICAÇÃO APÓS JAVASCRIPT:")
        print(f"📋 Data início no campo: '{resultado['inicio']}'")
        print(f"📋 Data fim no campo: '{resultado['fim']}'")
        
        # Print para ver visualmente
        tirar_print(navegador, "02_datas_configuradas.png", "(após configurar datas)")
        
        # Verificar se está no formato americano (que o site aceita)
        if resultado['fim'] == data_fim_us:
            print("✅✅✅ DATAS CONFIGURADAS COM SUCESSO (formato US)!")
            
            # AGORA CONVERTEMOS OS DADOS PARA BR QUANDO SALVARMOS NA PLANILHA
            print(f"📌 LEMBRETE: Os dados serão convertidos para formato BR ao salvar na planilha")
            return True
        else:
            print(f"⚠️ Data fim esperada: '{data_fim_us}', obtida: '{resultado['fim']}'")
            
            # TENTATIVA 2: Abordagem ainda mais agressiva
            print("\n🔄 Tentativa 2: Abordagem com timeout e múltiplas tentativas...")
            
            for tentativa in range(3):
                script_retry = f"""
                var fim = document.getElementById('dataFim');
                fim.focus();
                fim.select();
                document.execCommand('selectAll');
                document.execCommand('delete');
                fim.value = '{data_fim_us}';
                fim.dispatchEvent(new Event('input', {{ bubbles: true }}));
                fim.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return document.getElementById('dataFim').value;
                """
                
                valor = navegador.execute_script(script_retry)
                print(f"  Tentativa {tentativa+1}: '{valor}'")
                time.sleep(1)
                
                if valor == data_fim_us:
                    print("✅ Sucesso na tentativa", tentativa+1)
                    tirar_print(navegador, "02_datas_configuradas_final.png", "(após múltiplas tentativas)")
                    return True
            
            return False
            
    except Exception as e:
        print(f"❌ Erro no JavaScript agressivo: {e}")
        tirar_print(navegador, "02_erro_datas.png", "(erro ao configurar datas)")
        return False


def atualizar_relatorio(navegador):
    """Clica no botão Atualizar para aplicar as datas"""
    print("\n3️⃣ ATUALIZANDO RELATÓRIO...")
    try:
        botao_atualizar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "btnAtualizar"))
        )
        botao_atualizar.click()
        print("🔄 Atualizando relatório...")
        time.sleep(5)
        
        # Print após atualizar
        tirar_print(navegador, "03_apos_atualizar.png", "(após atualizar relatório)")
        
        print("✅ RELATÓRIO ATUALIZADO COM SUCESSO!")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar relatório: {e}")
        return False


def configurar_datas_relatorio(navegador):
    """Configura as datas do relatório usando JavaScript"""
    periodo_pop_up(navegador)
    
    # Usar apenas JavaScript agressivo (abandonar digitação)
    if configurar_datas_com_javascript_agressivo(navegador):
        return atualizar_relatorio(navegador)
    
    print("❌ Falha ao configurar datas")
    return False


def obter_funcionario_atual(navegador):
    """Pega o nome do funcionário atualmente selecionado"""
    try:
        nome_elemento = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "react-select-3--value-item"))
        )
        nome = nome_elemento.text.strip()
        print(f"✅ Funcionário atual: {nome}")
        return nome
    except:
        print("❌ Não consegui pegar o nome do funcionário")
        return None


def avancar_funcionario(navegador):
    """Clica na setinha para próximo funcionário"""
    try:
        seletores = [
            "i.fa-arrow-right",
            "button i.fa-arrow-right",
            "[class*='arrow-right']",
            "button[title*='próximo']",
            "button[title*='next']",
        ]

        for seletor in seletores:
            try:
                seta = navegador.find_element(By.CSS_SELECTOR, seletor)
                seta.click()
                print("➡️  Avançando para próximo funcionário...")
                time.sleep(2)
                return True
            except:
                continue

        print("❌ Não encontrou setinha para avançar")
        return False
    except Exception as e:
        print(f"❌ Erro ao avançar: {e}")
        return False


def extrair_dados(navegador):
    """Extrai os dados da tabela - VERSÃO FUNCIONAL"""
    try:
        print("🔍 Extraindo dados...")
        
        WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabela-calculos-wrapper"))
        )
        time.sleep(2)
        
        script = """
        function extrairDados() {
            const linhas = document.querySelectorAll('.tabela-calculos-wrapper tbody tr');
            const dados = [];
            
            for (let linha of linhas) {
                const celulas = linha.querySelectorAll('td');
                if (celulas.length >= 20) {
                    const data = celulas[2]?.innerText?.trim() || '';
                    const bSaldo = celulas[18]?.innerText?.trim() || '';
                    const bTotal = celulas[19]?.innerText?.trim() || '';
                    
                    if (data && data !== '') {
                        dados.push([data, bSaldo, bTotal]);
                    }
                }
            }
            return dados;
        }
        return extrairDados();
        """
        
        dados = navegador.execute_script(script)
        print(f"✅ Encontrou {len(dados)} linhas")
        
        if dados:
            df = pd.DataFrame(dados, columns=["Data", "BSaldo", "BTotal"])
            df['BSaldo'] = df['BSaldo'].str.replace('+', '')
            df['BTotal'] = df['BTotal'].str.replace('+', '')
            return df
        
        return pd.DataFrame()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return pd.DataFrame()


def processar_todos_funcionarios(navegador, callback_processar, max_tentativas=40):
    """Processa funcionários com limite de tentativas"""

    print(f"🚀 INICIANDO PROCESSAMENTO (máximo: {max_tentativas} tentativas)")
    print("=" * 50)

    # Tempo extra para GitHub Actions
    if MODO_GITHUB:
        print("⏳ Aguardando interface carregar (GitHub Actions)...")
        time.sleep(10)

    if not acessar_calculos(navegador):
        print("❌ Não conseguiu acessar cálculos")
        return 0

    print("\n📅 CONFIGURANDO PERÍODO DO RELATÓRIO...")
    if not configurar_datas_relatorio(navegador):
        print("❌ Não conseguiu configurar datas do relatório")
        return 0

    contador = 0
    historico_nomes = []

    for tentativa in range(max_tentativas):
        print(f"\n🔄 TENTATIVA {tentativa + 1}/{max_tentativas}")

        nome_atual = obter_funcionario_atual(navegador)
        if not nome_atual:
            print("⚠️ Não pegou nome, continuando...")
            avancar_funcionario(navegador)
            continue

        print(f"📝 Nome: {nome_atual}")

        if nome_atual in historico_nomes:
            print(f"🚫 REPETIÇÃO! '{nome_atual}' já foi visto")
            break

        historico_nomes.append(nome_atual)
        df_dados = extrair_dados(navegador)

        if not df_dados.empty:
            sucesso = callback_processar(nome_atual, df_dados)
            if sucesso:
                contador += 1
                print(f"✅ #{contador}: {nome_atual} processado")
        else:
            print(f"⚠️ Tabela vazia para {nome_atual}")

        if tentativa < max_tentativas - 1:
            print("➡️  Tentando avançar...")
            if not avancar_funcionario(navegador):
                print("❌ Não conseguiu avançar, parando...")
                break

    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    print(f"✅ Processados com sucesso: {contador}")
    print(f"📜 Nomes únicos encontrados: {len(historico_nomes)}")
    
    # Print final
    tirar_print(navegador, "99_final.png", "(após processamento)")

    return contador


def dados(navegador):
    """Função principal que extrai dados do funcionário atual"""
    acessar_calculos(navegador)
    nome = obter_funcionario_atual(navegador)
    if not nome:
        return None, None
    df = extrair_dados(navegador)
    return nome, df
