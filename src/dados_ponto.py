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

# 🔥 CORREÇÃO: ADICIONAR O DEF QUE ESTAVA FALTANDO
def configurar_datas_com_javascript_agressivo(navegador):
    """Configura datas e FORÇA o filtro a aplicar"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    # Formato BR (dia/mês/ano) - que o site USA
    data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
    data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS")
    print(f"Data início: {data_inicio}")
    print(f"Data fim: {data_fim}")
    print("=" * 50)
    
    try:
        # 1. Primeiro setar as datas
        script_setar = f"""
        // Setar data início
        var inicio = document.getElementById('dataInicio');
        inicio.value = '{data_inicio}';
        inicio.dispatchEvent(new Event('input', {{ bubbles: true }}));
        inicio.dispatchEvent(new Event('change', {{ bubbles: true }}));
        
        // Setar data fim
        var fim = document.getElementById('dataFim');
        fim.value = '{data_fim}';
        fim.dispatchEvent(new Event('input', {{ bubbles: true }}));
        fim.dispatchEvent(new Event('change', {{ bubbles: true }}));
        
        return {{ inicio: inicio.value, fim: fim.value }};
        """
        
        resultado = navegador.execute_script(script_setar)
        print(f"📋 Datas setadas: {resultado}")
        
        # 2. AGORA FORÇAR O FILTRO (clicar no botão atualizar)
        print("🔄 Forçando atualização do filtro...")
        
        script_clique = """
        var btn = document.getElementById('btnAtualizar');
        if (btn) {
            btn.click();
            return true;
        }
        return false;
        """
        
        navegador.execute_script(script_clique)
        time.sleep(5)  # Esperar atualizar
        
        # 3. Print para ver o resultado
        tirar_print(navegador, "02_apos_filtro.png", "(após aplicar filtro)")
        
        # 4. Verificar quantas linhas tem
        qtd_linhas = navegador.execute_script("""
            return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
        """)
        
        print(f"📊 Linhas após filtro: {qtd_linhas}")
        
        # Se tiver muitas linhas (>31), algo errado
        if qtd_linhas > 31:
            print("⚠️ Ainda parece ter muitos dias, tentando novamente...")
            navegador.execute_script("document.getElementById('btnAtualizar').click();")
            time.sleep(5)
            
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

# 🔥 FUNÇÃO NOVA: Forçar atualização com JavaScript
def forcar_atualizacao_com_javascript(navegador):
    """Força a atualização do relatório usando JavaScript direto no botão"""
    
    print("\n🔄 FORÇANDO ATUALIZAÇÃO COM JAVASCRIPT...")
    
    try:
        # Script para clicar no botão de múltiplas formas
        script_clique_forcado = """
        function forcarClique() {
            // Tentar por ID
            var btn = document.getElementById('btnAtualizar');
            if (btn) {
                console.log('Botão encontrado por ID');
                
                // Múltiplas formas de clicar
                btn.click();  // Clique normal
                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                
                // Disparar eventos de formulário
                var form = btn.closest('form');
                if (form) {
                    form.dispatchEvent(new Event('submit', { bubbles: true }));
                }
                
                return 'Cliques executados no botão por ID';
            }
            
            // Tentar por outros seletores
            var botoes = document.querySelectorAll('button');
            for (var i = 0; i < botoes.length; i++) {
                if (botoes[i].textContent.includes('Atualizar') || 
                    botoes[i].innerHTML.includes('fa-refresh') ||
                    botoes[i].className.includes('atualizar')) {
                    
                    console.log('Botão encontrado por texto:', botoes[i].textContent);
                    botoes[i].click();
                    botoes[i].dispatchEvent(new Event('click', { bubbles: true }));
                    return 'Clique executado em botão: ' + botoes[i].textContent;
                }
            }
            
            return 'Nenhum botão de atualizar encontrado';
        }
        
        return forcarClique();
        """
        
        # Executar o script
        resultado = navegador.execute_script(script_clique_forcado)
        print(f"✅ JavaScript retornou: {resultado}")
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Verificar quantas linhas tem agora
        qtd_linhas = navegador.execute_script("""
            return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
        """)
        
        print(f"📊 Linhas após atualização forçada: {qtd_linhas}")
        
        # Se ainda tiver muitas linhas, tentar novamente
        if qtd_linhas > 25:
            print("⚠️ Ainda com muitas linhas, tentando segunda vez...")
            time.sleep(2)
            navegador.execute_script("document.getElementById('btnAtualizar')?.click();")
            time.sleep(5)
            
            # Verificar novamente
            qtd_linhas_final = navegador.execute_script("""
                return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
            """)
            print(f"📊 Linhas após segunda tentativa: {qtd_linhas_final}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao forçar atualização: {e}")
        return False


# 📅 Modificar a função configurar_datas_relatorio para usar o novo método
def configurar_datas_relatorio(navegador):
    """Configura as datas do relatório usando JavaScript"""
    periodo_pop_up(navegador)
    
    # Primeiro configurar as datas
    if configurar_datas_com_javascript_agressivo(navegador):
        print("✅ Datas configuradas, agora forcando atualização...")
        
        # AGORA sim, forçar a atualização com JavaScript
        if forcar_atualizacao_com_javascript(navegador):
            print("✅ Atualização forçada com sucesso!")
            
            # Verificação final
            qtd_final = navegador.execute_script("""
                return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
            """)
            
            print(f"📊 VERIFICAÇÃO FINAL - Linhas no relatório: {qtd_final}")
            
            # Se ainda estiver errado, mostrar as primeiras datas para debug
            if qtd_final > 25:
                datas_debug = navegador.execute_script("""
                    var linhas = document.querySelectorAll('.tabela-calculos-wrapper tbody tr');
                    var primeirasDatas = [];
                    for(var i=0; i<Math.min(5, linhas.length); i++) {
                        var celulas = linhas[i].querySelectorAll('td');
                        if(celulas.length >= 3) {
                            primeirasDatas.push(celulas[2]?.innerText || '');
                        }
                    }
                    return primeirasDatas;
                """)
                print(f"⚠️ DEBUG - Primeiras 5 datas mostradas: {datas_debug}")
            
            return True
    
    print("❌ Falha ao configurar datas")
    return False


# 🔥 Opcional: Função de emergência para recarregar tudo
def resetar_e_aplicar_filtro(navegador):
    """Função de emergência: recarrega a página e reaplica tudo"""
    
    print("\n🚨 MODO EMERGÊNCIA: Recarregando página...")
    
    try:
        # Salvar URL atual
        url_atual = navegador.current_url
        
        # Recarregar a página
        navegador.get("https://pontoweb.secullum.com.br/#/calculos")
        time.sleep(5)
        
        # Reconfigurar datas
        hoje = datetime.now()
        ontem = hoje - timedelta(days=1)
        data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
        data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
        
        # Script completo
        script_completo = f"""
        // Configurar datas
        var inicio = document.getElementById('dataInicio');
        var fim = document.getElementById('dataFim');
        
        if(inicio && fim) {{
            inicio.value = '{data_inicio}';
            fim.value = '{data_fim}';
            
            // Disparar eventos
            inicio.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inicio.dispatchEvent(new Event('change', {{ bubbles: true }}));
            fim.dispatchEvent(new Event('input', {{ bubbles: true }}));
            fim.dispatchEvent(new Event('change', {{ bubbles: true }}));
            
            // Clicar no botão MÚLTIPLAS VEZES
            var btn = document.getElementById('btnAtualizar');
            if(btn) {{
                for(var i=0; i<3; i++) {{
                    btn.click();
                    btn.dispatchEvent(new MouseEvent('click', {{ bubbles: true }}));
                }}
            }}
            
            return true;
        }}
        return false;
        """
        
        navegador.execute_script(script_completo)
        time.sleep(7)
        
        # Verificar resultado
        qtd = navegador.execute_script("""
            return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
        """)
        
        print(f"📊 Linhas após emergência: {qtd}")
        return qtd <= 25
        
    except Exception as e:
        print(f"❌ Erro na emergência: {e}")
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
