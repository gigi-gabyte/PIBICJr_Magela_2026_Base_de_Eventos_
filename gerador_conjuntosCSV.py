import pandas as pd

df = pd.read_csv("eventosTratados.csv", sep=";") # Mudar nome do arquivo
df["ANO-DO-EVENTO"] = df["ANO-DO-EVENTO"].astype("Int64")

# PRIMEIRO CONJUNTO: NOME-DO-EVENTO
df["NOME-DO-EVENTO"].to_csv("conjunto1.csv", sep="|",index=False)

# SEGUNDO CONJUNTO: NOME-DO-EVENTO | ANO-DO-EVENTO
df[
    [
        "NOME-DO-EVENTO",
        "ANO-DO-EVENTO"
    ]
].to_csv("conjunto2.csv", sep="|",index=False)

# TERCEIRO CONJUNTO: NOME-DO-EVENTO | ANO-DO-EVENTO | PAIS-DO-EVENTO
df[
    [
        "NOME-DO-EVENTO",
        "ANO-DO-EVENTO",
        "PAIS-DO-EVENTO"
    ]
].to_csv("conjunto3.csv", sep="|",index=False)

# QUARTO CONJUNTO: NOME-DO-EVENTO | ANO-DO-EVENTO | PAIS-DO-EVENTO | CIDADE-DO-EVENTO
df[
    [
        "NOME-DO-EVENTO",
        "ANO-DO-EVENTO",
        "PAIS-DO-EVENTO",
        "CIDADE-DO-EVENTO"
    ]
].to_csv("conjunto4.csv", sep="|",index=False)


'''
CÓDIGO ALTERNATIVO: Todos os atributos em uma só coluna

# SEGUNDO CONJUNTO: NOME-DO-EVENTO | ANO-DO-EVENTO
df["NOME-DO-EVENTO|ANO-DO-EVENTO"] = (
    df["NOME-DO-EVENTO"] + "|" + 
    df["ANO-DO-EVENTO"].astype("Int64").astype(str)
)
df["NOME-DO-EVENTO|ANO-DO-EVENTO"].to_csv("conjunto2.csv", sep="|",index=False)

# TERCEIRO CONJUNTO: NOME-DO-EVENTO | ANO-DO-EVENTO | PAIS-DO-EVENTO
df["NOME-DO-EVENTO|ANO-DO-EVENTO|PAIS-DO-EVENTO"] = (
    df["NOME-DO-EVENTO|ANO-DO-EVENTO"] + "|" +
    df["PAIS-DO-EVENTO"]
)
df["NOME-DO-EVENTO|ANO-DO-EVENTO|PAIS-DO-EVENTO"].to_csv("conjunto3.csv", sep="|",index=False)

# QUARTO CONJUNTO: NOME-DO-EVENTO | ANO-DO-EVENTO | PAIS-DO-EVENTO | CIDADE-DO-EVENTO
df["NOME-DO-EVENTO|ANO-DO-EVENTO|PAIS-DO-EVENTO|CIDADE-DO-EVENTO"] = (
    df["NOME-DO-EVENTO|ANO-DO-EVENTO|PAIS-DO-EVENTO"] + "|" +
    df["CIDADE-DO-EVENTO"]
)
df["NOME-DO-EVENTO|ANO-DO-EVENTO|PAIS-DO-EVENTO|CIDADE-DO-EVENTO"].to_csv("conjunto4.csv", sep="|",index=False)
'''
