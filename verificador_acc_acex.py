# Importando as bibliotecas necessárias
import streamlit as st
from experta import *

# --------------------------------------------------------------------------
# 1. DEFINIÇÃO DOS FATOS (A ESTRUTURA DE DADOS DO SISTEMA)
# --------------------------------------------------------------------------

class Atividades(Fact):
    """
    Fato de entrada: Armazena os dados inseridos pelo usuário na interface.
    """
    ano_ingresso = Field(int, mandatory=True)
    periodo_ingresso = Field(int, mandatory=True)
    acc_ensino = Field(int, default=0)
    acc_pesquisa = Field(int, default=0)
    acc_extensao = Field(int, default=0)
    acc_arte = Field(int, default=0)
    acc_adm = Field(int, default=0)
    acc_inter = Field(int, default=0)
    acex = Field(int, default=0)

class Resultado(Fact):
    """
    Fato de saída: Armazena as conclusões e mensagens geradas pelo motor de inferência.
    """
    mensagens = Field(list, default=[])

# MUDANÇA 1: Criamos um fato específico para controlar a execução da regra
class TarefaAnalise(Fact):
    """
    Fato de controle: Usado para iniciar e parar a execução da regra e evitar loops.
    """
    status = Field(str, mandatory=True)


# --------------------------------------------------------------------------
# 2. MOTOR DE INFERÊNCIA (O CÉREBRO DO SISTEMA ESPECIALISTA)
# --------------------------------------------------------------------------

class VerificaRequisitos(KnowledgeEngine):

    # MUDANÇA 2: A regra agora busca por uma tarefa com status 'pendente'
    @Rule(AS.tarefa << TarefaAnalise(status='pendente'),
          AS.atv << Atividades(),
          AS.res << Resultado())
    def processar_regras_acc(self, tarefa, atv, res):
        """
        Esta é a regra principal que aplica a lógica da resolução sobre os dados do aluno.
        """
        mensagens_geradas = []

        # --- (Toda a lógica de análise de ACC e ACEX permanece a mesma) ---
        mensagens_geradas.append(("header", "Análise de ACC (Atividades Complementares)"))
        accs_computadas = {
            "Ensino": min(atv["acc_ensino"], 120), "Pesquisa": min(atv["acc_pesquisa"], 120),
            "Extensão": min(atv["acc_extensao"], 120), "Arte e Cultura": min(atv["acc_arte"], 120),
            "Administração Univ.": min(atv["acc_adm"], 120), "Interdisciplinar": min(atv["acc_inter"], 120)
        }
        for natureza, horas in accs_computadas.items():
            if horas > 0:
                mensagens_geradas.append(("info", f"Para a natureza '{natureza}', foram computadas {horas}h. (Limite de 120h por natureza aplicado conforme Art. 11)."))
        naturezas_validas = [n for n, h in accs_computadas.items() if h >= 15]
        if len(naturezas_validas) >= 2:
            mensagens_geradas.append(("success", f"✅ Requisito cumprido: Horas em {len(naturezas_validas)} naturezas distintas com no mínimo 15h cada (conforme Art. 10 e Art. 12)."))
        else:
            mensagens_geradas.append(("warning", f"⚠️ Requisito pendente: Você precisa de no mínimo 15h em pelo menos DUAS naturezas distintas. Atualmente, você possui apenas {len(naturezas_validas)} (conforme Art. 10 e Art. 12)."))
        mensagens_geradas.append(("header", "Análise de ACEX (Atividades de Extensão)"))
        ingresso_requer_acex = atv["ano_ingresso"] > 2022 or (atv["ano_ingresso"] == 2022 and atv["periodo_ingresso"] == 2)
        if ingresso_requer_acex:
            if atv["acex"] > 0:
                mensagens_geradas.append(("success", f"✅ ACEX declarada com {atv['acex']}h. Este requisito é obrigatório para seu ingresso em {atv['ano_ingresso']}.{atv['periodo_ingresso']} (conforme Art. 38)."))
            else:
                mensagens_geradas.append(("warning", f"⚠️ Requisito pendente: A declaração de horas de ACEX é obrigatória para ingressantes a partir do semestre 2022.2 (conforme Art. 38)."))
        else:
            mensagens_geradas.append(("info", f"ℹ️ ACEX não é obrigatória para seu ingresso em {atv['ano_ingresso']}.{atv['periodo_ingresso']} (anterior a 2022.2)."))

        # Atualiza o fato Resultado
        self.modify(res, mensagens=mensagens_geradas)
        
        # MUDANÇA 3: A regra modifica a tarefa para 'concluido', quebrando o loop.
        self.modify(tarefa, status='concluido')


# --------------------------------------------------------------------------
# 3. INTERFACE COM O USUÁRIO (CONSTRUÍDA COM STREAMLIT)
# --------------------------------------------------------------------------

st.set_page_config(page_title="Analisador de ACC e ACEX - UFAPE", layout="centered")
st.title("🤖 Analisador de ACC e ACEX")
st.write("Sistema especialista para verificar o cumprimento dos requisitos da Resolução CONSEPE Nº 008/2024.")
st.markdown("---")
st.header("1. Insira suas informações")
st.subheader("Semestre de Ingresso na UFAPE")
col_ano, col_periodo = st.columns([0.7, 0.3])
with col_ano:
    ano_ingresso = st.number_input("Ano", min_value=2015, max_value=2025, value=2024, label_visibility="collapsed")
with col_periodo:
    periodo_ingresso = st.radio("Período", [1, 2], horizontal=True, label_visibility="collapsed")
st.caption(f"Você selecionou o semestre de ingresso: {ano_ingresso}.{periodo_ingresso}")
st.subheader("Carga horária de ACC por Natureza")
st.write("Informe o total de horas que você possui em cada natureza de ACC. O sistema aplicará o limite de 120h.")
col1, col2 = st.columns(2)
with col1:
    acc_ensino = st.number_input("Ensino", 0, 500, 0)
    acc_pesquisa = st.number_input("Pesquisa", 0, 500, 0)
    acc_extensao = st.number_input("Extensão", 0, 500, 0)
with col2:
    acc_arte = st.number_input("Arte e Cultura", 0, 500, 0)
    acc_adm = st.number_input("Administração Universitária", 0, 500, 0)
    acc_inter = st.number_input("Interdisciplinar", 0, 500, 0)
st.subheader("Carga horária de ACEX")
acex = st.number_input("Total de horas em Atividades de Extensão (ACEX)", 0, 500, 0)
st.markdown("---")

# --------------------------------------------------------------------------
# 4. EXECUÇÃO E EXIBIÇÃO DOS RESULTADOS
# --------------------------------------------------------------------------

if st.button("Analisar Requisitos", type="primary"):
    engine = VerificaRequisitos()
    engine.reset()
    
    # Declara o fato de controle com status 'pendente'
    engine.declare(TarefaAnalise(status='pendente'))
    engine.declare(Resultado())
    engine.declare(Atividades(
        ano_ingresso=ano_ingresso,
        periodo_ingresso=periodo_ingresso,
        acc_ensino=acc_ensino,
        acc_pesquisa=acc_pesquisa,
        acc_extensao=acc_extensao,
        acc_arte=acc_arte,
        acc_adm=acc_adm,
        acc_inter=acc_inter,
        acex=acex
    ))
    
    engine.run()

    st.header("2. Resultado da Análise")
    for fact in engine.facts.values():
        if isinstance(fact, Resultado) and fact["mensagens"]:
            for tipo, texto in fact["mensagens"]:
                if tipo == "success":
                    st.success(texto, icon="✅")
                elif tipo == "warning":
                    st.warning(texto, icon="⚠️")
                elif tipo == "info":
                    st.info(texto, icon="ℹ️")
                elif tipo == "header":
                    st.subheader(texto)
        
    st.markdown("---")
    st.write("Análise concluída. Role para cima para ver todos os detalhes.")