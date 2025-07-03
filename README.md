# 📄 ProjetoSistemasEspecialistas

## 🎯 Descrição

Este sistema especialista foi desenvolvido para ajudar os alunos da **UFAPE** a verificar se já cumprem os requisitos obrigatórios das **Atividades Curriculares Complementares (ACC)** e **Atividades Curriculares de Extensão (ACEX)**, com base na **Resolução CONSEPE Nº 008/2024**.

O sistema recebe as horas informadas pelo aluno, compara com as regras da resolução e fornece uma resposta explicativa, indicando se o aluno já está apto ou o que falta para integralizar as atividades.

---

## 🧑‍💻 Tecnologias utilizadas

- **Python** — linguagem principal
- **[Streamlit](https://streamlit.io/)** — interface web interativa
- **[Experta](https://github.com/nilp0inter/experta)** — motor de inferência para o sistema especialista

---

## 🗺️ Funcionalidades

✅ Entrada de dados:
- Ano e período de ingresso na UFAPE
- Horas realizadas em cada natureza de ACC
- Horas realizadas em ACEX

✅ Validação automática:
- Verifica se o aluno cumpre o mínimo de 15h em pelo menos duas naturezas de ACC (Art. 10 e 12, Seção V — Das Disposições Gerais)
- Aplica o limite máximo de 120h por natureza (Art. 11)
- Checa a obrigatoriedade de ACEX (obrigatória para ingressantes a partir de 2022.2)

✅ Saída explicativa:
- Indica quais naturezas foram consideradas válidas
- Mostra se os requisitos foram ou não atendidos
- Apresenta justificativas fundamentadas com artigos e seções da resolução

---

## ⚖️ Regras principais (baseadas na Resolução CONSEPE Nº 008/2024)

- **ACC**:
  - Máximo de 120h por natureza (Art. 11)
  - Mínimo de 15h para ser considerada (Art. 12)
  - Deve ter no mínimo duas naturezas válidas (Art. 10)
- **ACEX**:
  - Obrigatória para ingressantes a partir de 2022.2 (Art. 38, Capítulo V)

---

## 🚀 Como executar

1️⃣ Clone o repositório ou baixe o projeto:

```bash
git clone https://github.com/seu-usuario/ProjetoSistemasEspecialistas.git
cd ProjetoSistemasEspecialistas
pip install streamlit experta
streamlit run verificador_acc_acex.py

