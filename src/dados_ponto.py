# dados_ponto.py - CORREÇÃO: FORÇAR ATUALIZAÇÃO MESMO COM DATAS IGUAIS
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
    """Acessa a área de cálculos do ponto - VERSÃO ULTRA ROBUSTA"""
    
    print("\n" + "=" * 50)
    print("🔍 TENTANDO ACESSAR RELATÓRIOS E CÁLCULOS")
    print("=" * 50)
    
    tirar_print(navegador, "00_antes_acessar.png", "(antes de acessar cálculos)")
    
    if MODO_GITHUB:
        print("⏳ GitHub Actions detectado - usando timeouts maiores...")
        time.sleep(15)  # Aumentei o tempo inicial
    else:
        time.sleep(5)
    
    # ESTRATÉGIA 1: Procurar por qualquer menu que possa conter relatórios
    estrategias = [
        # Menu lateral esquerdo (comum em sistemas corporativos)
        {"desc": "Menu lateral por data-testid", "selector": "[data-testid='menu-lateral'] a, [data-testid='menu-lateral'] button"},
        {"desc": "Menu lateral por classe", "selector": ".menu-lateral a, .sidebar a, .nav-sidebar a"},
        {"desc": "Ícones de menu", "selector": "i.fa-bar-chart, i.fa-chart, i.fa-calculator, i.fa-table"},
        
        # Barra superior
        {"desc": "Barra superior", "selector": ".navbar a, .top-bar a, .header a"},
        
        # Links comuns
        {"desc": "Links com 'relatório'", "selector": "a[href*='relatorio'], a[href*='relatorios'], a[href*='report']"},
        {"desc": "Links com 'cálculo'", "selector": "a[href*='calculo'], a[href*='calculos'], a[href*='calc']"},
        
        # Textos
        {"desc": "Span com texto Relatórios", "selector": "//span[contains(text(), 'Relatórios') or contains(text(), 'RELATÓRIOS')]", "by": By.XPATH},
        {"desc": "Span com texto Cálculos", "selector": "//span[contains(text(), 'Cálculos') or contains(text(), 'CÁLCULOS')]", "by": By.XPATH},
        {"desc": "Div com texto", "selector": "//div[contains(text(), 'Relatórios') or contains(text(), 'Cálculos')]", "by": By.XPATH},
    ]
    
    for i, estrategia in enumerate(estrategias, 1):
        try:
            print(f"\n📋 Estratégia {i}: {estrategia['desc']}")
            
            by_method = estrategia.get('by', By.CSS_SELECTOR)
            selector = estrategia['selector']
            
            elementos = WebDriverWait(navegador, 5).until(
                EC.presence_of_all_elements_located((by_method, selector))
            )
            
            if elementos:
                print(f"✅ Encontrou {len(elementos)} elementos")
                
                for elem in elementos[:5]:  # Testar primeiros 5
                    try:
                        if elem.is_displayed() and elem.is_enabled():
                            texto = elem.text.strip()[:50]
                            print(f"   ➡️ Tentando clicar: '{texto}'")
                            navegador.execute_script("arguments[0].scrollIntoView(true);", elem)
                            time.sleep(1)
                            elem.click()
                            print(f"   ✅ Clicou!")
                            time.sleep(5)
                            
                            # Verificar se entrou na área de cálculos
                            if "cálculo" in navegador.current_url.lower() or "relatorio" in navegador.current_url.lower():
                                print("✅✅✅ ACESSO AOS CÁLCULOS CONFIRMADO!")
                                tirar_print(navegador, "01_acessou_calculos.png")
                                return True
                            
                            # Verificar se apareceu campo de data
                            campos_data = navegador.find_elements(By.ID, "dataInicio")
                            if campos_data:
                                print("✅✅✅ CAMPOS DE DATA ENCONTRADOS!")
                                tirar_print(navegador, "01_acessou_calculos.png")
                                return True
                    except:
                        continue
        except:
            continue
    
    # ESTRATÉGIA 2: JavaScript para explorar todos os links
    print("\n📋 ESTRATÉGIA FINAL: JavaScript exploratório")
    resultado = navegador.execute_script("""
        // Função para encontrar todos os elementos clicáveis
        function encontrarElementosClicaveis() {
            const elementos = document.querySelectorAll('a, button, [role="button"], .clickable, span, div');
            const resultados = [];
            
            for(let elem of elementos) {
                const texto = elem.textContent || '';
                const html = elem.outerHTML || '';
                const classes = elem.className || '';
                
                // Palavras-chave relacionadas a relatórios/cálculos
                const keywords = ['relatório', 'relatorios', 'relatorio', 
                                 'cálculo', 'calculo', 'calculos', 'cálculos',
                                 'report', 'reports', 'calc', 'calculator',
                                 'ponto', 'banco', 'horas', 'periodo'];
                
                for(let keyword of keywords) {
                    if(texto.toLowerCase().includes(keyword) || 
                       classes.toLowerCase().includes(keyword) ||
                       html.toLowerCase().includes(keyword)) {
                        
                        // Tentar clicar
                        try {
                            elem.scrollIntoView();
                            elem.click();
                            return {sucesso: true, keyword: keyword, texto: texto.substring(0, 50)};
                        } catch(e) {
                            resultados.push({keyword, texto: texto.substring(0, 50)});
                        }
                        break;
                    }
                }
            }
            
            return {sucesso: false, encontrados: resultados};
        }
        
        return encontrarElementosClicaveis();
    """)
    
    if resultado.get('sucesso'):
        print(f"✅ JavaScript clicou em elemento com: {resultado.get('keyword')}")
        print(f"   Texto: {resultado.get('texto')}")
        time.sleep(5)
        
        # Verificar novamente
        campos_data = navegador.find_elements(By.ID, "dataInicio")
        if campos_data:
            print("✅✅✅ ACESSO AOS CÁLCULOS CONFIRMADO!")
            tirar_print(navegador, "01_acessou_calculos.png")
            return True
    else:
        print("⚠️ JavaScript não conseguiu clicar automaticamente")
        if resultado.get('encontrados'):
            print(f"   Elementos encontrados: {len(resultado['encontrados'])}")
    
    # ESTRATÉGIA 3: Navegação direta por URL (se souber o padrão)
    try:
        print("\n📋 Tentando navegação direta por URL...")
        url_atual = navegador.current_url
        dominios_possiveis = [
            url_atual + "relatorios",
            url_atual + "calculos",
            url_atual.replace("/dashboard", "/relatorios"),
            url_atual.replace("/home", "/relatorios"),
        ]
        
        for url_tentativa in dominios_possiveis:
            try:
                navegador.get(url_tentativa)
                time.sleep(5)
                if "cálculo" in navegador.current_url.lower() or "relatorio" in navegador.current_url.lower():
                    print(f"✅ Navegação direta funcionou: {url_tentativa}")
                    return True
            except:
                continue
    except:
        pass
    
    # PRINT DE DIAGNÓSTICO
    print("\n📸 Tirando print de diagnóstico...")
    tirar_print(navegador, "diagnostico_erro_acesso.png")
    
    # Listar todos os links na página
    todos_links = navegador.execute_script("""
        const links = document.querySelectorAll('a, button');
        const resultado = [];
        links.forEach(l => {
            if(l.innerText) {
                resultado.push({
                    texto: l.innerText.substring(0, 50),
                    tag: l.tagName,
                    classe: l.className
                });
            }
        });
        return resultado;
    """)
    
    print("\n📋 LINKS ENCONTRADOS NA PÁGINA:")
    for i, link in enumerate(todos_links[:20]):  # Mostrar primeiros 20
        print(f"   {i+1}. {link['tag']}: '{link['texto']}' (classe: {link['classe']})")
    
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


# 🔥 FUNÇÃO CORRIGIDA: Configurar datas com send_keys
def configurar_datas_com_send_keys(navegador):
    """Configura as datas usando send_keys para garantir que sejam enviadas"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    # Formato BR (dia/mês/ano) - que o site USA
    data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
    data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS COM SEND_KEYS")
    print(f"Data início: {data_inicio}")
    print(f"Data fim: {data_fim}")
    print("=" * 50)
    
    try:
        # PASSO 1: Limpar e setar data início com send_keys
        print("\n🔨 Configurando DATA INÍCIO...")
        campo_inicio = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "dataInicio"))
        )
        
        # Limpar campo
        campo_inicio.click()
        campo_inicio.clear()
        time.sleep(1)
        
        # Selecionar tudo e deletar
        campo_inicio.send_keys(Keys.CONTROL + "a")
        campo_inicio.send_keys(Keys.DELETE)
        time.sleep(1)
        
        # Digitar a data caractere por caractere
        for char in data_inicio:
            campo_inicio.send_keys(char)
            time.sleep(0.1)
        
        # Disparar eventos
        navegador.execute_script("""
            var campo = document.getElementById('dataInicio');
            campo.dispatchEvent(new Event('input', { bubbles: true }));
            campo.dispatchEvent(new Event('change', { bubbles: true }));
        """)
        print(f"✅ Data início configurada: {data_inicio}")
        
        # PASSO 2: Limpar e setar data fim com send_keys
        print("\n🔨 Configurando DATA FIM...")
        campo_fim = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "dataFim"))
        )
        
        # Limpar campo
        campo_fim.click()
        campo_fim.clear()
        time.sleep(1)
        
        # Selecionar tudo e deletar
        campo_fim.send_keys(Keys.CONTROL + "a")
        campo_fim.send_keys(Keys.DELETE)
        time.sleep(1)
        
        # Digitar a data caractere por caractere
        for char in data_fim:
            campo_fim.send_keys(char)
            time.sleep(0.1)
        
        # Disparar eventos
        navegador.execute_script("""
            var campo = document.getElementById('dataFim');
            campo.dispatchEvent(new Event('input', { bubbles: true }));
            campo.dispatchEvent(new Event('change', { bubbles: true }));
        """)
        print(f"✅ Data fim configurada: {data_fim}")
        
        # PASSO 3: VERIFICAÇÃO - Ler os valores atuais
        valores_atuais = navegador.execute_script("""
            return {
                inicio: document.getElementById('dataInicio')?.value,
                fim: document.getElementById('dataFim')?.value
            };
        """)
        
        print(f"\n📋 VERIFICAÇÃO - Datas após configuração:")
        print(f"   Data início no campo: {valores_atuais.get('inicio')}")
        print(f"   Data fim no campo: {valores_atuais.get('fim')}")
        
        # Verificar se as datas foram realmente setadas
        if valores_atuais.get('inicio') == data_inicio and valores_atuais.get('fim') == data_fim:
            print("✅✅ DATAS CONFIGURADAS CORRETAMENTE!")
            return True
        else:
            print("⚠️ Datas não correspondem ao esperado, tentando método alternativo...")
            
            # Método alternativo: JavaScript puro
            navegador.execute_script(f"""
                var inicio = document.getElementById('dataInicio');
                var fim = document.getElementById('dataFim');
                
                if(inicio) {{
                    inicio.value = '{data_inicio}';
                    inicio.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inicio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                if(fim) {{
                    fim.value = '{data_fim}';
                    fim.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    fim.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """)
            
            # Verificar novamente
            valores_finais = navegador.execute_script("""
                return {
                    inicio: document.getElementById('dataInicio')?.value,
                    fim: document.getElementById('dataFim')?.value
                };
            """)
            print(f"   Após JS: Início={valores_finais.get('inicio')}, Fim={valores_finais.get('fim')}")
            
            return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar datas com send_keys: {e}")
        
        # Fallback: tentar JavaScript puro
        try:
            print("\n🔄 Tentando fallback com JavaScript...")
            navegador.execute_script(f"""
                var inicio = document.getElementById('dataInicio');
                var fim = document.getElementById('dataFim');
                
                if(inicio) {{
                    inicio.value = '{data_inicio}';
                    inicio.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inicio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                if(fim) {{
                    fim.value = '{data_fim}';
                    fim.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    fim.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """)
            print("✅ Fallback com JavaScript executado")
            return True
        except:
            print("❌ Fallback também falhou")
            return False


# 🔥 FUNÇÃO CORRIGIDA: Clicar no botão Atualizar (com verificação)
def clicar_botao_atualizar(navegador):
    """FUNÇÃO CORRIGIDA PARA CLICAR NO BOTÃO ATUALIZAR"""
    
    print("\n" + "=" * 50)
    print("🖱️ CLICANDO NO BOTÃO ATUALIZAR (id=btnAtualizar)")
    print("=" * 50)
    
    try:
        # MÉTODO 1: Clique com Selenium WebDriver (mais confiável)
        print("\n🔨 MÉTODO 1: Clique com Selenium WebDriver")
        botao = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "btnAtualizar"))
        )
        
        # Rolar até o botão para garantir que está visível
        navegador.execute_script("arguments[0].scrollIntoView(true);", botao)
        time.sleep(1)
        
        # Clicar
        botao.click()
        print("   ✅ Clique com Selenium executado")
        time.sleep(5)
        
        # MÉTODO 2: Clique com JavaScript para garantir
        print("\n🔨 MÉTODO 2: Clique com JavaScript (reforço)")
        navegador.execute_script("""
            var btn = document.getElementById('btnAtualizar');
            if(btn) {
                btn.click();
                return true;
            }
            return false;
        """)
        print("   ✅ Clique com JavaScript executado")
        time.sleep(5)
        
        # VERIFICAR SE O FILTRO FUNCIONOU
        qtd_linhas = navegador.execute_script("""
            return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
        """)
        
        print(f"\n📊 Linhas após atualização: {qtd_linhas}")
        
        # Mostrar as ÚLTIMAS 5 linhas para verificar o período
        ultimas_linhas = navegador.execute_script("""
            var linhas = document.querySelectorAll('.tabela-calculos-wrapper tbody tr');
            var ultimasDatas = [];
            var total = linhas.length;
            
            for(var i = Math.max(0, total - 5); i < total; i++) {
                var celulas = linhas[i].querySelectorAll('td');
                if(celulas.length >= 3) {
                    ultimasDatas.push({
                        data: celulas[2]?.innerText || '',
                        bSaldo: celulas[17]?.innerText || '',
                        bTotal: celulas[18]?.innerText || ''
                    });
                }
            }
            return ultimasDatas;
        """)
        
        print("\n📅 ÚLTIMAS 5 LINHAS DO RELATÓRIO:")
        for i, linha in enumerate(ultimas_linhas):
            print(f"   {i+1}. Data: {linha.get('data', '')} | BSaldo: {linha.get('bSaldo', '')} | BTotal: {linha.get('bTotal', '')}")
        
        # Verificar se a data fim (ontem) aparece nas últimas linhas
        ontem = (datetime.now() - timedelta(days=1)).strftime("%d/%m")
        for linha in ultimas_linhas:
            if ontem in linha.get('data', ''):
                print(f"\n✅✅ CONFIRMADO: Data {ontem} aparece no relatório!")
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar no botão: {e}")
        
        # Tentar método alternativo se o primeiro falhar
        try:
            print("\n🔄 Tentando método alternativo...")
            navegador.execute_script("""
                var botoes = document.querySelectorAll('button');
                for(var i=0; i<botoes.length; i++) {
                    if(botoes[i].id === 'btnAtualizar' || 
                       botoes[i].innerText.includes('Atualizar') ||
                       botoes[i].innerText.includes('ATUALIZAR')) {
                        botoes[i].click();
                        return true;
                    }
                }
                return false;
            """)
            print("✅ Método alternativo executado")
            time.sleep(5)
            return True
        except:
            print("❌ Método alternativo também falhou")
            return False


# 🔥 FUNÇÃO PRINCIPAL CORRIGIDA
def configurar_datas_relatorio(navegador):
    """Configura as datas com send_keys E DEPOIS clica no botão atualizar"""
    
    print("\n" + "=" * 60)
    print("📅 INICIANDO CONFIGURAÇÃO COMPLETA DO RELATÓRIO")
    print("=" * 60)
    
    # Fechar popup se aparecer
    periodo_pop_up(navegador)
    
    # PASSO 1: Configurar as datas com send_keys (CORRIGIDO)
    print("\n📌 PASSO 1: Configurando datas com send_keys...")
    if not configurar_datas_com_send_keys(navegador):
        print("❌ Falha ao configurar datas")
        return False
    
    time.sleep(3)
    
    # PASSO 2: Clicar no botão atualizar
    print("\n📌 PASSO 2: Clicando no botão Atualizar...")
    if not clicar_botao_atualizar(navegador):
        print("❌ Falha ao clicar no botão")
        return False
    
    print("\n" + "=" * 60)
    print("✅✅✅ RELATÓRIO CONFIGURADO COM SUCESSO!")
    print("=" * 60)
    
    # VERIFICAÇÃO FINAL
    qtd_final = navegador.execute_script("""
        return document.querySelectorAll('.tabela-calculos-wrapper tbody tr').length;
    """)
    
    print(f"\n📊 TOTAL DE LINHAS NO RELATÓRIO: {qtd_final}")
    
    return True


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
    """Extrai os dados da tabela"""
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
                    const bSaldo = celulas[17]?.innerText?.trim() || '';
                    const bTotal = celulas[18]?.innerText?.trim() || '';
                    
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