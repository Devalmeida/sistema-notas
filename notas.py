import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Notas por Encontro", layout="centered")
st.title("📚 Lançamento de Notas Convertidas por Encontro")

# Entrada de nomes dos alunos
st.subheader("👨‍🎓 Alunos")
alunos = st.text_area("Digite os nomes dos alunos (um por linha)").splitlines()

# Número de encontros
st.subheader("📅 Configuração de Encontros")
num_encontros = st.number_input("Número total de encontros", min_value=1, step=1)

# Entrada dos pesos como inteiros
pesos = []
st.subheader("⚖️ Pesos de cada encontro (inteiros)")
for i in range(num_encontros):
    peso = st.number_input(f"Peso do Encontro E{i+1}", key=f"peso_{i}", step=1, format="%d")
    pesos.append(peso)

# Verificação da soma dos pesos
soma_pesos = sum(pesos)
if soma_pesos > 51:
    st.error(f"❌ Erro: A soma dos pesos é {soma_pesos}, que ultrapassa o limite de 51. Ajuste os valores antes de continuar.")
    st.stop()

# Inserção de notas individuais por encontro
st.subheader("📝 Notas individuais por encontro")
notas_convertidas = {}
for i in range(num_encontros):
    encontro = f"E{i+1}"
    peso = pesos[i]
    st.markdown(f"**Notas para {encontro} (Peso: {peso})**")
    notas = []
    for aluno in alunos:
        nota_str = st.text_input(f"Nota de {aluno} no {encontro}", key=f"nota_{aluno}_{encontro}")
        nota_str = nota_str.replace(",", ".")  # Aceita vírgula ou ponto
        try:
            nota = float(nota_str)
        except:
            nota = 0.0
        nota_convertida = round((nota * peso / 100) * 10, 1)
        notas.append(nota_convertida)
    notas_convertidas[encontro] = notas

# Construção da tabela final com notas convertidas
st.subheader("📊 Tabela Final de Notas Lançadas")
data = {"Aluno": alunos}
for i in range(num_encontros):
    encontro = f"E{i+1}"
    data[encontro] = notas_convertidas[encontro]

# Cálculo da nota final somando os valores convertidos
notas_finais = []
for idx, aluno in enumerate(alunos):
    soma = 0
    for i in range(num_encontros):
        encontro = f"E{i+1}"
        soma += notas_convertidas[encontro][idx]
    notas_finais.append(round(soma, 1))

data["Nota Final"] = notas_finais

df = pd.DataFrame(data)
st.dataframe(df)

# Salvamento automático no HD (D:\NotasSalvas)
caminho_hd = "D:/NotasSalvas"
os.makedirs(caminho_hd, exist_ok=True)
arquivo_csv = os.path.join(caminho_hd, "notas_alunos.csv")
df.to_csv(arquivo_csv, index=False)

st.success(f"✅ Arquivo salvo com sucesso em: `{arquivo_csv}`")