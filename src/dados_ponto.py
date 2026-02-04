# %%
# %%
# dados_ponto.py - VERSÃO REVISADA COM DIGITAÇÃO DIRETA
# %%
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# 📓 Acessar área de cálculos
def acessar_calculos(navegador):
    """Acessa a área de cálculos do ponto"""
    try:
        # Relatório
        relatorio = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Relatórios')]"))
        )
        if relatorio.text == "Relatórios":
            relatorio.click()
            print("🖱 Clicando no botão Relatórios...")
            time.sleep(1)
    except:
        print("⚠️ Relatórios não encontrado")

    try:
        # Cálculos
        calculo = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "calculos"))
        )
        if calculo.text == "Cálculos":
            calculo.click()
            print("🖱 Clicando no botão Cálculos...")
            time.sleep(2)
            print("✅ Acesso aos cálculos realizado!")
            return True

    except:
        print("⚠️ Cálculos não encontrado")
        return False

    return False


# 📅 periodo informado
def periodo_pop_up(navegador):
    """Fecha o popup de período (quando tem mais de 60 dias) se aparecer"""
    try:
        # Espera até 5 segundos pelo popup
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
        # Não encontrou o popup - isso é normal
        print("ℹ️ Nenhum pop up de período encontrado")
        return False
    except Exception as e:
        print(f"⚠️ Erro ao verificar popup: {e}")
        return False


# 📅 Função para configurar data no calendário (MANTIDA COMO FALLBACK)
def configurar_data_calendario(navegador, dia, mes, ano, nome_campo=""):
    """Configura uma data específica no calendário - USADA APENAS SE PRECISAR"""
    
    meses_abrev = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }
    
    mes_abreviado = meses_abrev[mes]
    
    print(f"  🎯 Configurando {nome_campo} via calendário: {dia:02d}/{mes:02d}/{ano}")
    
    try:
        # Encontrar título do calendário
        try:
            titulo = navegador.find_element(By.CLASS_NAME, "navigation-title")
            titulo_texto = titulo.text.strip()
            print(f"  📋 Título do calendário: '{titulo_texto}'")
            
            # Lógica básica para navegar no calendário
            # Se não está no ano correto, clica no título para mudar
            if not str(ano) in titulo_texto:
                print(f"  🔄 Ano incorreto, clicando no título...")
                titulo.click()
                time.sleep(2)
                
                # Tenta encontrar e clicar no ano
                try:
                    ano_elemento = navegador.find_element(By.XPATH, f"//*[text()='{ano}']")
                    ano_elemento.click()
                    time.sleep(2)
                except:
                    pass
            
            # Tenta encontrar e clicar no dia
            try:
                dia_elemento = navegador.find_element(By.XPATH, f"//td[text()='{dia}' and not(contains(@class, 'disabled'))]")
                dia_elemento.click()
                time.sleep(1)
                print(f"  ✅ Data configurada via calendário")
                return True
            except:
                pass
                
        except Exception as e:
            print(f"  ⚠️ Erro no calendário: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro ao configurar data no calendário: {e}")
        return False
    
    return False


# 📅 CONFIGURAR DATAS DIGITANDO DIRETAMENTE (MÉTODO PREFERIDO)
def configurar_datas_digitando(navegador):
    """Configura as datas DIGITANDO diretamente nos campos - MÉTODO MAIS CONFIÁVEL"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS (DIGITANDO DIRETO)")
    print(f"Data início: 01/{hoje.month:02d}/{hoje.year}")
    print(f"Data fim: {ontem.day:02d}/{ontem.month:02d}/{ontem.year}")
    print("=" * 50)
    
    try:
        # 1. PRIMEIRO: DATA INÍCIO
        print("\n1️⃣ Configurando DATA INÍCIO (digitando)...")
        
        # Encontra o campo de data início pelo ID
        campo_inicio = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "dataInicio"))
        )
        
        # Clica no campo para focar
        campo_inicio.click()
        time.sleep(0.5)
        
        # Seleciona todo o texto atual (Ctrl+A) e apaga
        campo_inicio.send_keys(Keys.CONTROL + "a")
        campo_inicio.send_keys(Keys.DELETE)
        time.sleep(0.5)
        
        # Digita a nova data (formato DD/MM/YYYY)
        data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
        campo_inicio.send_keys(data_inicio)
        
        print(f"✅ Data início digitada: {data_inicio}")
        
        # Pressiona Tab para sair do campo
        campo_inicio.send_keys(Keys.TAB)
        time.sleep(1)
        
        # 2. DEPOIS: DATA FIM
        print("\n2️⃣ Configurando DATA FIM (digitando)...")
        
        # Encontra o campo de data fim pelo ID
        campo_fim = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "dataFim"))
        )
        
        # Clica no campo para focar
        campo_fim.click()
        time.sleep(0.5)
        
        # Seleciona todo o texto atual (Ctrl+A) e apaga
        campo_fim.send_keys(Keys.CONTROL + "a")
        campo_fim.send_keys(Keys.DELETE)
        time.sleep(0.5)
        
        # Digita a nova data
        data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
        campo_fim.send_keys(data_fim)
        
        print(f"✅ Data fim digitada: {data_fim}")
        
        # Pressiona Tab
        campo_fim.send_keys(Keys.TAB)
        time.sleep(2)
        
        # 3. VERIFICA SE AS DATAS FORAM APLICADAS
        print("\n🔍 Verificando se as datas foram aplicadas...")
        time.sleep(1)
        
        # Lê os valores atuais para confirmar
        valor_inicio = campo_inicio.get_attribute("value")
        valor_fim = campo_fim.get_attribute("value")
        
        print(f"📋 Data início atual: {valor_inicio}")
        print(f"📋 Data fim atual: {valor_fim}")
        
        if valor_inicio == data_inicio and valor_fim == data_fim:
            print("✅✅✅ DATAS CONFIGURADAS COM SUCESSO!")
            return True
        else:
            print("⚠️ As datas não foram aplicadas corretamente")
            print(f"   Esperado início: {data_inicio}, Obtido: {valor_inicio}")
            print(f"   Esperado fim: {data_fim}, Obtido: {valor_fim}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao configurar datas digitando: {e}")
        import traceback
        traceback.print_exc()
        return False


# 📅 CONFIGURAR DATAS COM JAVASCRIPT (MÉTODO ALTERNATIVO)
def configurar_datas_javascript(navegador):
    """Configura datas usando JavaScript - MÉTODO ALTERNATIVO"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    data_inicio = f"01/{hoje.month:02d}/{hoje.year}"
    data_fim = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
    
    print("=" * 50)
    print("📅 CONFIGURANDO DATAS (VIA JAVASCRIPT)")
    print(f"Data início: {data_inicio}")
    print(f"Data fim: {data_fim}")
    print("=" * 50)
    
    try:
        # Usa JavaScript para definir os valores diretamente
        script_inicio = f"""
        document.getElementById('dataInicio').value = '{data_inicio}';
        document.getElementById('dataInicio').dispatchEvent(new Event('change', {{ bubbles: true }}));
        """
        
        script_fim = f"""
        document.getElementById('dataFim').value = '{data_fim}';
        document.getElementById('dataFim').dispatchEvent(new Event('change', {{ bubbles: true }}));
        """
        
        # Aplica as datas
        navegador.execute_script(script_inicio)
        time.sleep(1)
        navegador.execute_script(script_fim)
        time.sleep(1)
        
        # Verifica se funcionou
        valor_inicio = navegador.execute_script("return document.getElementById('dataInicio').value;")
        valor_fim = navegador.execute_script("return document.getElementById('dataFim').value;")
        
        print(f"📋 Data início via JS: {valor_inicio}")
        print(f"📋 Data fim via JS: {valor_fim}")
        
        if valor_inicio == data_inicio and valor_fim == data_fim:
            print("✅✅✅ DATAS CONFIGURADAS COM JAVASCRIPT!")
            return True
        else:
            print("⚠️ JavaScript não aplicou corretamente")
            return False
            
    except Exception as e:
        print(f"❌ Erro com JavaScript: {e}")
        return False


# 📅 FUNÇÃO PRINCIPAL PARA CONFIGURAR DATAS
def configurar_datas_relatorio(navegador):
    """Configura as datas do relatório usando o melhor método disponível"""
    
    print("=" * 50)
    print("🔄 CONFIGURANDO DATAS DO RELATÓRIO")
    print("=" * 50)
    
    # 1. Primeiro fecha qualquer popup
    periodo_pop_up(navegador)
    
    # 2. Tenta digitar diretamente (método mais confiável)
    print("\n🔄 Tentando método de digitação direta...")
    if configurar_datas_digitando(navegador):
        # Se funcionou, tenta atualizar
        return atualizar_relatorio(navegador)
    
    # 3. Se não funcionou, tenta JavaScript
    print("\n🔄 Digitação direta falhou, tentando JavaScript...")
    if configurar_datas_javascript(navegador):
        # Se funcionou, tenta atualizar
        return atualizar_relatorio(navegador)
    
    # 4. Se nada funcionou, tenta o método antigo do calendário (fallback)
    print("\n🔄 Métodos diretos falharam, tentando calendário...")
    return configurar_calendario_antigo(navegador)


def configurar_calendario_antigo(navegador):
    """Método antigo usando calendário (fallback apenas)"""
    
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)
    
    try:
        # Tenta encontrar e usar o calendário (método simplificado)
        print("🔍 Buscando calendários...")
        
        # Encontra os ícones de calendário
        calendarios = navegador.find_elements(
            By.CSS_SELECTOR, ".fa.fa-calendar-o, .fa-calendar, i.fa-calendar"
        )
        
        if len(calendarios) >= 2:
            print(f"✅ Encontrados {len(calendarios)} calendários")
            
            # Primeiro calendário (data início)
            print("📌 Configurando data início via calendário...")
            try:
                calendarios[0].click()
                time.sleep(2)
                configurar_data_calendario(navegador, 1, hoje.month, hoje.year, "início")
                navegador.find_element(By.TAG_NAME, "body").click()
                time.sleep(2)
            except:
                pass
            
            # Segundo calendário (data fim)
            print("📌 Configurando data fim via calendário...")
            try:
                calendarios[1].click()
                time.sleep(2)
                configurar_data_calendario(navegador, ontem.day, ontem.month, ontem.year, "fim")
                navegador.find_element(By.TAG_NAME, "body").click()
                time.sleep(2)
            except:
                pass
            
            return atualizar_relatorio(navegador)
        
        return False
        
    except Exception as e:
        print(f"❌ Erro no método do calendário: {e}")
        return False


def atualizar_relatorio(navegador):
    """Clica no botão Atualizar para aplicar as datas"""
    
    print("\n3️⃣ ATUALIZANDO RELATÓRIO...")
    
    try:
        # Tenta encontrar o botão Atualizar
        botao_atualizar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "btnAtualizar"))
        )
        
        botao_atualizar.click()
        print("🔄 Atualizando relatório...")
        time.sleep(5)  # Aguarda o processamento
        
        print("✅ RELATÓRIO ATUALIZADO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar relatório: {e}")
        return False


# 👤 Obter funcionário atual
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


# ➡️ Navegação entre funcionários
def avancar_funcionario(navegador):
    """Clica na setinha para próximo funcionário"""
    try:
        # Tenta encontrar a seta de várias formas
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


# 📊 Extrair dados da tabela
def extrair_dados(navegador):
    """Extrai os dados da tabela do funcionário atual"""
    try:
        tabela = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabela-calculos-wrapper"))
        )
        print("✅ Tabela encontrada!")

        html_tabela = tabela.get_attribute("innerHTML")
        dfs = pd.read_html(html_tabela)

        if not dfs:
            print("❌ Nenhuma tabela no HTML")
            return pd.DataFrame()

        df = dfs[0]
        colunas_necessarias = ["Data", "BSaldo", "BTotal"]

        df_final = pd.DataFrame()
        for col in colunas_necessarias:
            if col in df.columns:
                df_final[col] = df[col]
            else:
                df_final[col] = ""

        print(f"📊 Dados extraídos: {len(df_final)} linhas")
        return df_final

    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        return pd.DataFrame()


# 🎯 FUNÇÃO PRINCIPAL ATUALIZADA
def processar_todos_funcionarios(navegador, callback_processar, max_tentativas=40):
    """Processa funcionários com limite de tentativas"""

    print(f"🚀 INICIANDO PROCESSAMENTO (máximo: {max_tentativas} tentativas)")
    print("=" * 50)

    # 1. Acessa sistema
    if not acessar_calculos(navegador):
        print("❌ Não conseguiu acessar cálculos")
        return 0

    # 2. CONFIGURA DATAS DO RELATÓRIO (USANDO MÉTODO DE DIGITAÇÃO)
    print("\n📅 CONFIGURANDO PERÍODO DO RELATÓRIO...")
    if not configurar_datas_relatorio(navegador):
        print("❌ Não conseguiu configurar datas do relatório")
        return 0

    contador = 0
    historico_nomes = []  # Guarda nomes já vistos

    # 3. Loop principal com limite
    for tentativa in range(max_tentativas):
        print(f"\n🔄 TENTATIVA {tentativa + 1}/{max_tentativas}")

        # Pega nome atual
        nome_atual = obter_funcionario_atual(navegador)
        if not nome_atual:
            print("⚠️ Não pegou nome, continuando...")
            # Tenta avançar mesmo sem nome
            avancar_funcionario(navegador)
            continue

        print(f"📝 Nome: {nome_atual}")
        print(f"📊 Histórico até agora: {len(historico_nomes)} nomes")

        # VERIFICAÇÃO: Já viu este nome? (proteção contra loop)
        if nome_atual in historico_nomes:
            print(f"🚫 REPETIÇÃO! '{nome_atual}' já foi visto")
            print("   Parando para evitar loop infinito")
            break

        # Se é nome novo, adiciona ao histórico
        historico_nomes.append(nome_atual)

        # Extrai dados
        df_dados = extrair_dados(navegador)

        # Processa dados
        if not df_dados.empty:
            sucesso = callback_processar(nome_atual, df_dados)
            if sucesso:
                contador += 1
                print(f"✅ #{contador}: {nome_atual} processado")
        else:
            print(f"⚠️ Tabela vazia para {nome_atual}")

        # Tenta avançar para o próximo (exceto na última tentativa)
        if tentativa < max_tentativas - 1:
            print("➡️  Tentando avançar...")
            if not avancar_funcionario(navegador):
                print("❌ Não conseguiu avançar, parando...")
                break
        else:
            print("🎯 Última tentativa concluída")

    # 4. Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    print(f"✅ Processados com sucesso: {contador}")
    print(f"🔁 Tentativas realizadas: {min(tentativa + 1, max_tentativas)}")
    print(f"📜 Nomes únicos encontrados: {len(historico_nomes)}")

    if historico_nomes:
        print("\n📋 Lista completa:")
        for i, nome in enumerate(historico_nomes, 1):
            print(f"   {i:2d}. {nome}")

    return contador


# 🎯 Função de compatibilidade
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
