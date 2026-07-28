import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import unicodedata

# Todas as letras para minúsculas
def letras_minusculas(colunasStr):
    for coluna in colunasStr:
        df[coluna] = df[coluna].str.lower()

# Ano-do-evento FLOAT -> INT
def ano_Int ():
    df["ANO-DO-EVENTO"] = df["ANO-DO-EVENTO"].astype("Int64")
    df.to_csv("colunasNecessarias.csv", sep=";", index=False)

# Remove espaços
def remove_espacos (colunasStr):
    for coluna in colunasStr:
        df[coluna] = (
            df[coluna]
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

# Remove stop-words
nltk.download("stopwords")
stop_words = set(stopwords.words("portuguese"))

def remove_stopwords (texto):
    palavras = str(texto).split()
    palavras_validas = [
        palavra
        for palavra in palavras
        if palavra not in stop_words
    ]
    return " ".join(palavras_validas)
    
# Remove números e ordinais
def remove_numeros (texto):
    if pd.isna(texto):
        return texto
    texto = str(texto)
    texto = re.sub(r'\b\d+(?:[º°ªoa])?\b', ' ', texto)
    texto = re.sub(r'\b[IVXLCDM]+\b', ' ', texto, flags=re.IGNORECASE)
    return texto

# Remove pontuações
def remove_pontuacao(texto):
    texto = str(texto)
    return re.sub(r"[^\w\s]", " ", texto)

# Remove acentuação
def remove_acentos(texto):
    texto = str(texto)
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

# Trata CIDADE-DO-EVENTO
def local_evento(texto):
    texto = str(texto)
    return re.sub(r"[-/|(),.?\"'].*$", " ", texto)

### MAIN ###
df = pd.read_csv("teste_csv_MAGELA.csv", sep=";") # MUDAR o nome do arquivo para o do CSV que será tratado
df = df[
    [
        "NOME-DO-EVENTO",
        "TIPO-DE-EVENTO",
        "CLASSIFICACAO-DO-EVENTO",
        "ANO-DO-EVENTO",
        "PAIS-DO-EVENTO",
        "CIDADE-DO-EVENTO",
        "LOCAL-DO-EVENTO",
        "INSTITUICAO-PROMOTORA"
    ]
]
df.to_csv("colunasNecessarias.csv", sep=";",index=False)

df = pd.read_csv("colunasNecessarias.csv", sep=";")

colunasStr = [
    "NOME-DO-EVENTO",
    "TIPO-DE-EVENTO",
    "CLASSIFICACAO-DO-EVENTO",
    "PAIS-DO-EVENTO",
    "CIDADE-DO-EVENTO",
    "LOCAL-DO-EVENTO",
    "INSTITUICAO-PROMOTORA"
]

letras_minusculas(colunasStr)
ano_Int()
for coluna in ["CIDADE-DO-EVENTO", "LOCAL-DO-EVENTO", "INSTITUICAO-PROMOTORA"]:
    df[coluna] = df[coluna].apply(local_evento)
for coluna in colunasStr:
    df[coluna] = (
        df[coluna]
        .apply(remove_stopwords)
        .apply(remove_numeros)
        .apply(remove_acentos)
        .apply(remove_pontuacao)
    )
remove_espacos(colunasStr)

df.to_csv("eventosTratados.csv", sep=";",index=False)
