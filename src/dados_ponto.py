# %%
# dados_ponto.py - VERSÃO SIMPLIFICADA
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime, timedelta

# Em dados_ponto.py, adicione no topo:
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# 📓 Acessar área de cálculos
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
        # Espera até 5 segundos pelo popup (não precisa de 10 pois é rápido)
        pop_up = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.ID, "btnNo"))
        )
        
        pop_up_name = pop_up.text.strip()
        
        if pop_up_name == "Não":
            print("✅ Pop up de período encontrado - Fechando...")
            pop_up.click()
            time.sleep(1)  # Pode reduzir para 1 segundo
            return True
        else:
            print("⚠️ Pop up encontrado mas não é o esperado")
            return False
            
    except (NoSuchElementException, TimeoutException):
        # Não encontrou o popup - isso é normal, não é erro
        print("ℹ️ Nenhum pop up de período encontrado")
        return False
    except Exception as e:
        print(f"⚠️ Erro ao verificar popup: {e}")
        return False
    

# 📅 Configurar calendário dos cálculos
def configurar_calendario_calculos(navegador):
    """Configura as datas no calendário da área de cálculos"""

    from datetime import datetime, timedelta

    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)

    print("=" * 50)
    print("📅 CONFIGURANDO DATAS DO RELATÓRIO")
    print(f"Hoje: {hoje.strftime('%d/%m/%Y')}")
    print(f"Ontem: {ontem.strftime('%d/%m/%Y')}")
    print("=" * 50)

    # 1️⃣ PRIMEIRO: DATA FIM (ONTEM) - SEGUNDO ÍCONE
    print("\n1️⃣ CONFIGURANDO DATA FIM (ontem)...")

    # Clica no SEGUNDO ícone de calendário (dataFim)
    calendarios = navegador.find_elements(
        By.CSS_SELECTOR, ".fa.fa-calendar-o, .fa-calendar"
    )

    if len(calendarios) >= 2:
        print(f"✅ Encontrados {len(calendarios)} calendários")
        calendarios[1].click()  # SEGUNDO ícone = dataFim
        time.sleep(2)

        # NAVEGAR E SELECIONAR ONTEM (fluxo completo)
        sucesso_fim = configurar_data_calendario(
            navegador, ontem.day, ontem.month, ontem.year
        )

        if sucesso_fim:
            print(f"✅ Data fim configurada: {ontem.day}/{ontem.month}/{ontem.year}")
        else:
            print("❌ Falha ao configurar data fim")
            return False
    else:
        print("❌ Não encontrou calendários suficientes")
        return False

    # Pequena pausa
    time.sleep(1)

    # 2️⃣ DEPOIS: DATA INÍCIO (DIA 1) - PRIMEIRO ÍCONE
    print("\n2️⃣ CONFIGURANDO DATA INÍCIO (dia 1)...")

    # Clica no PRIMEIRO ícone de calendário (dataInicio)
    calendarios = navegador.find_elements(
        By.CSS_SELECTOR, ".fa.fa-calendar-o, .fa-calendar"
    )

    if len(calendarios) >= 1:
        calendarios[0].click()  # PRIMEIRO ícone = dataInicio
        time.sleep(2)

        # NAVEGAR E SELECIONAR DIA 1 DO MÊS ATUAL
        sucesso_inicio = configurar_data_calendario(navegador, 1, hoje.month, hoje.year)

        if sucesso_inicio:
            print(f"✅ Data início configurada: 01/{hoje.month}/{hoje.year}")
        else:
            print("❌ Falha ao configurar data início")
            return False
    else:
        print("❌ Não encontrou calendário de início")
        return False

    # 3️⃣ FINALMENTE: ATUALIZAR
    print("\n3️⃣ ATUALIZANDO RELATÓRIO...")
    time.sleep(1)

    try:
        botao_atualizar = navegador.find_element(By.ID, "btnAtualizar")
        botao_atualizar.click()
        print("🔄 Atualizando...")
        time.sleep(3)

        print("✅ DATAS CONFIGURADAS COM SUCESSO!")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
        return False


def configurar_data_calendario(navegador, dia, mes, ano):
    """Configura uma data específica no calendário (fluxo completo)"""

    meses_abrev = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez",
    }

    print(f"  🎯 Configurando: {dia}/{mes}/{ano}")

    try:
        # 1. CLICAR NO TÍTULO DO MÊS PARA VER ANO
        print("  📍 Clicando no mês para ver ano...")
        titulo_mes = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "navigation-title"))
        )
        titulo_mes.click()
        time.sleep(1.5)

        # 2. VERIFICAR ANO ATUAL
        titulo_ano = navegador.find_element(By.CLASS_NAME, "navigation-title")
        ano_atual = titulo_ano.text.strip()
        print(f"  📅 Ano atual: {ano_atual}")

        # 3. SE ANO ERRADO, SELECIONAR ANO CORRETO
        if ano_atual != str(ano):
            print(f"  🔄 Selecionando ano {ano}...")
            titulo_ano.click()
            time.sleep(1)

            # Procurar ano desejado
            anos = navegador.find_elements(By.CSS_SELECTOR, ".year.cell, .year")
            for ano_elem in anos:
                if ano_elem.text.strip() == str(ano):
                    ano_elem.click()
                    print(f"  ✅ Ano {ano} selecionado")
                    time.sleep(1.5)
                    break

        # 4. SELECIONAR MÊS
        mes_abreviado = meses_abrev[mes]
        print(f"  📅 Selecionando mês {mes_abreviado}...")

        meses = navegador.find_elements(By.CSS_SELECTOR, ".month.cell")
        for mes_elem in meses:
            if mes_elem.text.strip() == mes_abreviado:
                mes_elem.click()
                print(f"  ✅ Mês {mes_abreviado} selecionado")
                time.sleep(2)
                break

        # 5. SELECIONAR DIA
        print(f"  📍 Selecionando dia {dia}...")
        dias = navegador.find_elements(By.CSS_SELECTOR, ".day.cell:not(.disabled)")

        for dia_elem in dias:
            if dia_elem.text.strip() == str(dia):
                dia_elem.click()
                print(f"  ✅ Dia {dia} selecionado")
                time.sleep(1)
                return True

        print(f"  ❌ Dia {dia} não encontrado")
        return False

    except Exception as e:
        print(f"  ❌ Erro no calendário: {e}")
        return False

    # Pequena pausa
    time.sleep(1)

    # 2️⃣ DEPOIS: DATA INÍCIO (DIA 1) - PRIMEIRO ÍCONE
    print("\n2️⃣ CONFIGURANDO DATA INÍCIO (dia 1)...")

    # Clica no PRIMEIRO ícone de calendário (dataInicio)
    calendarios = navegador.find_elements(By.CSS_SELECTOR, ".fa.fa-calendar")

    if len(calendarios) >= 1:
        calendarios[0].click()  # PRIMEIRO ícone = dataInicio
        time.sleep(2)

        # NAVEGAR E SELECIONAR DIA 1 DO MÊS ATUAL
        navegar_para_mes_ano(navegador, hoje.month, hoje.year)
        selecionar_dia(navegador, 1)  # SEMPRE dia 1

        print(f"✅ Data início configurada: 01/{hoje.month}/{hoje.year}")
    else:
        print("❌ Não encontrou calendário de início")
        return False

    # 3️⃣ FINALMENTE: ATUALIZAR
    print("\n3️⃣ ATUALIZANDO RELATÓRIO...")
    time.sleep(1)

    try:
        botao_atualizar = navegador.find_element(By.ID, "btnAtualizar")
        botao_atualizar.click()
        print("🔄 Atualizando...")
        time.sleep(3)

        print("✅ DATAS CONFIGURADAS COM SUCESSO!")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")
        return False
    
def configurar_datas_com_popup(navegador):
    """Configura datas do calendário com tratamento de popup"""
    
    print("=" * 50)
    print("🔄 CONFIGURANDO DATAS COM TRATAMENTO DE POPUP")
    print("=" * 50)
    
    # 1. PRIMEIRO verifica e fecha popup se existir
    popup_encontrado = periodo_pop_up(navegador)
    
    if popup_encontrado:
        print("✅ Popup fechado com sucesso")
    
    # 2. DEPOIS configura as datas
    sucesso = configurar_calendario_calculos(navegador)
    
    # 3. Se configurou datas, verifica novamente se apareceu novo popup
    # (às vezes o popup pode reaparecer após configurar datas)
    if sucesso:
        print("🔍 Verificando se popup reapareceu após configuração...")
        periodo_pop_up(navegador)  # Só tenta fechar se aparecer
    
    return sucesso


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


# ➡️ Navegação entre funcionários (SIMPLES)
def avancar_funcionario(navegador):
    """Clica na setinha para próximo funcionário - SEM VERIFICAÇÃO COMPLEXA"""
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
                time.sleep(2)  # Aguardar carregamento
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

        # Limpar horários com *
        # colunas_horario = ['BSaldo', 'BTotal']
        # for col in colunas_horario:
        #     if col in df_final.columns:
        #         df_final[col] = df_final[col].apply(
        #             lambda x: str(x).split('*')[0].strip() if pd.notna(x) else ''
        #         )

        print(f"📊 Dados extraídos: {len(df_final)} linhas")
        print(f"{df_final}")
        return df_final

    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        return pd.DataFrame()


# 🎯 **FUNÇÃO PRINCIPAL NOVA (40 TENTATIVAS)**
def processar_todos_funcionarios(navegador, callback_processar, max_tentativas=40):
    """Processa funcionários com limite de tentativas - VERSÃO SIMPLES"""

    print(f"🚀 INICIANDO PROCESSAMENTO (máximo: {max_tentativas} tentativas)")
    print("=" * 50)

    # 1. Acessa sistema
    if not acessar_calculos(navegador):
        print("❌ Não conseguiu acessar cálculos")
        return 0

    # 2. CONFIGURA DATAS DO CALENDÁRIO (NOVO!)
    print("\n📅 CONFIGURANDO PERÍODO DO RELATÓRIO...")
    if not configurar_datas_com_popup(navegador):
        print("❌ Não conseguiu configurar datas do calendário")
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


# 🎯 Função de compatibilidade (mantém seu código antigo)
def dados(navegador):
    """Função principal que extrai dados do funcionário atual"""
    acessar_calculos(navegador)
    nome = obter_funcionario_atual(navegador)
    if not nome:
        return None, None
    df = extrair_dados(navegador)
    return nome, df


# from fazer_login import *

# # 🧪 TESTE SIMPLES
# if __name__ == "__main__":
#     print("🧪 TESTANDO VERSÃO SIMPLES (40 tentativas)")
#     print("=" * 50)

#     navegador = login()
#     time.sleep(3)

#     # 1. Acessar cálculos (só entra na área)
#     sucesso_acesso = acessar_calculos(navegador)

#     if sucesso_acesso:
        
        

#         # 2. Configurar datas no calendário
#         sucesso_config = configurar_calendario_calculos(navegador)
#         if sucesso_config:
#             # 3. Extrair dados
#             dados = extrair_dados(navegador)
#             if not dados.empty:
#                 print(f"\n✅ Dados extraídos: {len(dados)} registros")
#                 print(dados.to_string(index=False))
#             else:
#                 print("❌ Nenhum dado extraído")
#         else:
#             print("❌ Falha ao configurar datas")
#     else:
#         print("❌ Falha ao acessar cálculos")

#     time.sleep(3)
#     navegador.quit()

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
