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
    """Configura as datas usando JavaScript direto (mais confiável)"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS")
    print(f"Data início: 01/{hoje.month:02d}/{hoje.year}")
    print(f"Data fim: {ontem.day:02d}/{ontem.month:02d}/{ontem.year}")
    print("=" * 50)
    
    try:
        # 🔥 SOLUÇÃO: USAR JAVASCRIPT PARA SETAR O VALOR DIRETO
        data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
        data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
        
        # Script JavaScript para setar valores e forçar atualização
        script = f"""
        // Setar data início
        var campoInicio = document.getElementById('dataInicio');
        campoInicio.value = '{data_inicio}';
        campoInicio.dispatchEvent(new Event('change', {{ bubbles: true }}));
        campoInicio.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        
        // Setar data fim
        var campoFim = document.getElementById('dataFim');
        campoFim.value = '{data_fim}';
        campoFim.dispatchEvent(new Event('change', {{ bubbles: true }}));
        campoFim.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        
        // Forçar atualização do componente (se for React/Angular)
        var event = new Event('input', {{ bubbles: true }});
        campoInicio.dispatchEvent(event);
        campoFim.dispatchEvent(event);
        
        return true;
        """
        
        navegador.execute_script(script)
        print(f"✅ Datas configuradas via JavaScript")
        time.sleep(2)
        
        # Verificar se funcionou
        valor_inicio = navegador.execute_script("return document.getElementById('dataInicio').value;")
        valor_fim = navegador.execute_script("return document.getElementById('dataFim').value;")
        
        print(f"📋 Data início atual: '{valor_inicio}'")
        print(f"📋 Data fim atual: '{valor_fim}'")
        
        # Se ainda estiver errado, tenta uma abordagem mais agressiva
        if valor_fim != data_fim:
            print("⚠️ JavaScript simples falhou, tentando abordagem mais agressiva...")
            
            # Abordagem mais agressiva: limpar e setar com foco
            script_agressivo = f"""
            var campoFim = document.getElementById('dataFim');
            
            // Focar no campo
            campoFim.focus();
            
            // Limpar de todas as formas
            campoFim.value = '';
            campoFim.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            // Setar o valor
            campoFim.value = '{data_fim}';
            
            // Disparar todos os eventos possíveis
            campoFim.dispatchEvent(new Event('input', {{ bubbles: true }}));
            campoFim.dispatchEvent(new Event('change', {{ bubbles: true }}));
            campoFim.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            campoFim.dispatchEvent(new Event('keyup', {{ bubbles: true }}));
            
            // Se for um componente React, isso ajuda
            if (campoFim._valueTracker) {{
                campoFim._valueTracker.setValue('{data_fim}');
            }}
            
            return document.getElementById('dataFim').value;
            """
            
            valor_agressivo = navegador.execute_script(script_agressivo)
            print(f"📋 Após abordagem agressiva: '{valor_agressivo}'")
            
            if valor_agressivo == data_fim:
                print("✅ Abordagem agressiva funcionou!")
                valor_fim = valor_agressivo
        
        # Verificação final
        if valor_fim == data_fim or valor_fim == data_fim.replace('/', '-'):
            print("✅✅✅ DATAS CONFIGURADAS COM SUCESSO!")
            return True
        else:
            print(f"❌ Ainda errado: esperado '{data_fim}', obtido '{valor_fim}'")
            
            # Última tentativa: usar o método antigo mas com JavaScript puro
            return configurar_datas_javascript(navegador)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return configurar_datas_javascript(navegador)

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
