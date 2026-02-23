# %%
# %%
# dados_ponto.py - VERSÃO REVISADA COM DIGITAÇÃO DIRETA
# %%
# %%
# dados_ponto.py - VERSÃO OTIMIZADA PARA GITHUB ACTIONS
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

# Detectar se está rodando no GitHub Actions
MODO_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

# 📓 Acessar área de cálculos - VERSÃO OTIMIZADA
def acessar_calculos(navegador):
    """Acessa a área de cálculos do ponto - OTIMIZADO PARA GITHUB ACTIONS"""
    
    print("\n" + "=" * 50)
    print("🔍 TENTANDO ACESSAR RELATÓRIOS E CÁLCULOS")
    print("=" * 50)
    
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
            return True
    except:
        pass
    
    print("\n❌❌❌ NÃO CONSEGUIU ACESSAR CÁLCULOS")
    
    # DEBUG: Salvar HTML para análise
    if MODO_GITHUB:
        try:
            html = navegador.page_source
            with open("debug_acessar_calculos.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("📄 HTML salvo para debug: debug_acessar_calculos.html")
            
            # Listar textos visíveis
            textos = navegador.find_elements(By.XPATH, "//*[text()]")
            print("\n📋 Textos encontrados na página:")
            for t in textos[:20]:  # Primeiros 20
                if t.text.strip():
                    print(f"   - '{t.text.strip()}'")
        except:
            pass
    
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


# 📅 CONFIGURAR DATAS DIGITANDO DIRETAMENTE (igual ao seu original)
def configurar_datas_digitando(navegador):
    """Configura as datas DIGITANDO diretamente nos campos"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS (DIGITANDO DIRETO)")
    print(f"Data início: 01/{hoje.month:02d}/{hoje.year}")
    print(f"Data fim: {ontem.day:02d}/{ontem.month:02d}/{ontem.year}")
    print("=" * 50)
    
    try:
        print("\n1️⃣ Configurando DATA INÍCIO (digitando)...")
        campo_inicio = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "dataInicio"))
        )
        campo_inicio.click()
        time.sleep(0.5)
        campo_inicio.send_keys(Keys.CONTROL + "a")
        campo_inicio.send_keys(Keys.DELETE)
        time.sleep(0.5)
        data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
        campo_inicio.send_keys(data_inicio)
        print(f"✅ Data início digitada: {data_inicio}")
        campo_inicio.send_keys(Keys.TAB)
        time.sleep(1)
        
        print("\n2️⃣ Configurando DATA FIM (digitando)...")
        campo_fim = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "dataFim"))
        )
        campo_fim.click()
        time.sleep(0.5)
        campo_fim.send_keys(Keys.CONTROL + "a")
        campo_fim.send_keys(Keys.DELETE)
        time.sleep(0.5)
        data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
        campo_fim.send_keys(data_fim)
        print(f"✅ Data fim digitada: {data_fim}")
        campo_fim.send_keys(Keys.TAB)
        time.sleep(2)
        
        print("\n🔍 Verificando se as datas foram aplicadas...")
        valor_inicio = campo_inicio.get_attribute("value")
        valor_fim = campo_fim.get_attribute("value")
        
        print(f"📋 Data início atual: {valor_inicio}")
        print(f"📋 Data fim atual: {valor_fim}")
        
        if valor_inicio == data_inicio and valor_fim == data_fim:
            print("✅✅✅ DATAS CONFIGURADAS COM SUCESSO!")
            return True
        else:
            print("⚠️ As datas não foram aplicadas corretamente")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao configurar datas digitando: {e}")
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
        print("✅ RELATÓRIO ATUALIZADO COM SUCESSO!")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar relatório: {e}")
        return False


def configurar_datas_javascript(navegador):
    """Configura datas usando JavaScript"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
    data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
    
    try:
        script_inicio = f"""
        document.getElementById('dataInicio').value = '{data_inicio}';
        document.getElementById('dataInicio').dispatchEvent(new Event('change', {{ bubbles: true }}));
        """
        script_fim = f"""
        document.getElementById('dataFim').value = '{data_fim}';
        document.getElementById('dataFim').dispatchEvent(new Event('change', {{ bubbles: true }}));
        """
        
        navegador.execute_script(script_inicio)
        time.sleep(1)
        navegador.execute_script(script_fim)
        time.sleep(1)
        
        valor_inicio = navegador.execute_script("return document.getElementById('dataInicio').value;")
        valor_fim = navegador.execute_script("return document.getElementById('dataFim').value;")
        
        if valor_inicio == data_inicio and valor_fim == data_fim:
            print("✅✅✅ DATAS CONFIGURADAS COM JAVASCRIPT!")
            return True
        return False
    except Exception as e:
        print(f"❌ Erro com JavaScript: {e}")
        return False


def configurar_datas_relatorio(navegador):
    """Configura as datas do relatório"""
    periodo_pop_up(navegador)
    
    if configurar_datas_digitando(navegador):
        return atualizar_relatorio(navegador)
    
    if configurar_datas_javascript(navegador):
        return atualizar_relatorio(navegador)
    
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
    """Extrai os dados da tabela do funcionário atual - VERSÃO CORRIGIDA"""
    try:
        print("\n🔍 Extraindo dados da tabela...")
        
        # Aguardar tabela carregar
        tabela = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabela-calculos-wrapper"))
        )
        print("✅ Tabela encontrada!")

        # Pegar HTML da tabela
        html_tabela = tabela.get_attribute("innerHTML")
        
        # Ler TODAS as tabelas do HTML
        todas_tabelas = pd.read_html(html_tabela)
        print(f"📊 Encontradas {len(todas_tabelas)} tabelas no HTML")
        
        if not todas_tabelas:
            print("❌ Nenhuma tabela encontrada")
            return pd.DataFrame()
        
        # A tabela que queremos é a ÚLTIMA (ou a que tem 'Data' nas colunas)
        tabela_correta = None
        
        # Estratégia 1: Pegar a última tabela (geralmente é a de dados)
        tabela_correta = todas_tabelas[-1]
        print("✅ Usando a última tabela encontrada")
        
        # Estratégia 2: (fallback) Procurar tabela com colunas 'Data'
        if 'Data' not in tabela_correta.columns and len(todas_tabelas) > 1:
            for i, df in enumerate(todas_tabelas):
                if 'Data' in df.columns or 'BSaldo' in df.columns:
                    print(f"✅ Tabela {i} tem colunas de dados")
                    tabela_correta = df
                    break
        
        df = tabela_correta
        print(f"📊 Colunas da tabela selecionada: {list(df.columns)}")
        
        # Limpar dados
        # Remover linhas onde Data é NaN ou vazia
        if 'Data' in df.columns:
            df = df[df['Data'].notna()]
            df = df[df['Data'].astype(str).str.strip() != '']
            df = df[~df['Data'].astype(str).str.contains('Total|Média', case=False, na=False)]
        
        # Renomear colunas se necessário
        mapeamento = {}
        for col in df.columns:
            col_str = str(col).strip()
            if 'Data' in col_str or 'DIA' in col_str.upper():
                mapeamento[col] = 'Data'
            elif 'BSaldo' in col_str or 'SALDO' in col_str.upper() or 'BANCO' in col_str.upper():
                mapeamento[col] = 'BSaldo'
            elif 'BTotal' in col_str or 'TOTAL' in col_str.upper() or 'JORNADA' in col_str.upper():
                mapeamento[col] = 'BTotal'
        
        if mapeamento:
            df = df.rename(columns=mapeamento)
        
        # Garantir colunas necessárias
        for col in ['Data', 'BSaldo', 'BTotal']:
            if col not in df.columns:
                df[col] = ''
        
        # Manter só as colunas que importam
        df_final = df[['Data', 'BSaldo', 'BTotal']].copy()
        
        # Remover linhas totalmente vazias
        df_final = df_final.dropna(how='all')
        
        print(f"\n📊 Dados extraídos: {len(df_final)} linhas válidas")
        if not df_final.empty:
            print("\n📋 Primeiras 3 linhas:")
            print(df_final.head(3).to_string(index=False))
            
            # Debug: salvar CSV no GitHub Actions
            if os.getenv('GITHUB_ACTIONS') == 'true':
                df_final.to_csv('dados_extraidos_debug.csv', index=False)
                print("💾 Dados salvos para debug")
        
        return df_final

    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        import traceback
        traceback.print_exc()
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

    return contador


def dados(navegador):
    """Função principal que extrai dados do funcionário atual"""
    acessar_calculos(navegador)
    nome = obter_funcionario_atual(navegador)
    if not nome:
        return None, None
    df = extrair_dados(navegador)
    return nome, df


# #%%
# from fazer_login import *

# # 🧪 TESTE SIMPLES
# if __name__ == "__main__":
#     print("🧪 TESTANDO VERSÃO SIMPLES (40 tentativas)")
#     print("=" * 50)

#     navegador = login()
#     time.sleep(3)

#     #%%

#     # 1. Acessar cálculos (só entra na área)
#     sucesso_acesso = acessar_calculos(navegador)

# #%%
#     if sucesso_acesso:
        
        

#         # 2. Configurar datas no calendário
#         sucesso_config = configurar_datas_relatorio(navegador)
#         # if sucesso_config:
#         #     # 3. Extrair dados
#         #     dados = extrair_dados(navegador)
#         #     if not dados.empty:
#         #         print(f"\n✅ Dados extraídos: {len(dados)} registros")
#         #         print(dados.to_string(index=False))
#         #     else:
#         #         print("❌ Nenhum dado extraído")
#         # else:
#         #     print("❌ Falha ao configurar datas")
#     else:
#         print("❌ Falha ao acessar cálculos")

#     time.sleep(3)
 


    # # Função de teste
    # def callback_teste(nome, dados):
    #     print(f"   📝 Callback: Processando {nome} ({len(dados)} dias)")
    #     return True

    # # Executa
    # total = processar_todos_funcionarios(
    #     navegador=navegador,
    #     callback_processar=callback_teste,
    #     max_tentativas=40  # ← Você pode mudar este número!
    # )

    # print(f"\n🎯 RESULTADO: {total} funcionários processados")
    # navegador.quit()
