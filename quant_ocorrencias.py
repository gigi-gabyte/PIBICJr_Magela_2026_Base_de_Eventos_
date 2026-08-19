import csv
from collections import Counter
import os
import time

csvEntrada = r''
csvSaida = r''

csvConjunto1_ordenado = os.path.join(csvSaida, 'conjunto1_ordenado.csv')
csvConjunto2_ordenado = os.path.join(csvSaida, 'conjunto2_ordenado.csv')
csvConjunto3_ordenado = os.path.join(csvSaida, 'conjunto3_ordenado.csv')

intervaloFlush = 300000

def main():
    os.makedirs(csvSaida, exist_ok=True)
    inicio = time.time()
    totalLinhas = 0
    totalLinhas1 = 0
    totalLinhas2 = 0
    totalLinhas3 = 0

    frequencia_evento = Counter()
    frequencia_evento_pais = Counter()
    frequencia_evento_cidade = Counter()

    with open(csvEntrada, newline='', encoding='utf-8', mode='r') as f_entrada, \
        open(csvConjunto1_ordenado, newline='', encoding='utf-8', mode='w') as f1, \
        open(csvConjunto2_ordenado, newline='', encoding='utf-8', mode='w') as f2, \
        open(csvConjunto3_ordenado, newline='', encoding='utf-8', mode='w') as f3:

        # Leitura e contagem das linhas como tuplas
        leitor = csv.DictReader(f_entrada, delimiter='|')

        for linha in leitor:

            totalLinhas += 1  

            nome = linha["NOME-DO-EVENTO"]
            pais = linha["PAIS-DO-EVENTO"]
            cidade = linha["CIDADE-DO-EVENTO"]
    
            frequencia_evento[nome] += 1
            frequencia_evento_pais[(nome, pais)] += 1
            frequencia_evento_cidade[(nome, cidade)] += 1

        eventos_ordenados = sorted(
            frequencia_evento,
            key=frequencia_evento.get,
            reverse=True
        )
        eventos_paises_ordenados = sorted(
            frequencia_evento_pais,
            key=frequencia_evento_pais.get,
            reverse=True
        )
        eventos_cidades_ordenados = sorted(
            frequencia_evento_cidade,
            key=frequencia_evento_cidade.get,
            reverse=True
        )

        # Ordenação EVENTO
        escritor = csv.DictWriter(f1, delimiter='|', fieldnames= ['NOME-DO-EVENTO', 'OCORRENCIAS-EVENTO'])
        escritor.writeheader()

        for evento in eventos_ordenados:
            escritor.writerow({
                'NOME-DO-EVENTO': evento,
                'OCORRENCIAS-EVENTO':
                    frequencia_evento[evento]
            })
            totalLinhas1 += 1
            
            if totalLinhas1 % intervaloFlush == 0:
                f1.flush()

        # Ordenação EVENTO-PAÍS
        escritor = csv.DictWriter(f2, delimiter='|', fieldnames= ['NOME-DO-EVENTO', 'PAIS-DO-EVENTO', 'OCORRENCIAS-EVENTO-PAIS'])
        escritor.writeheader()

        for evento, pais in eventos_paises_ordenados:
            escritor.writerow({
                'NOME-DO-EVENTO': evento,
                'PAIS-DO-EVENTO': pais,
                'OCORRENCIAS-EVENTO-PAIS':
                    frequencia_evento_pais[(evento, pais)]
            })
            totalLinhas2 += 1
            
            if totalLinhas2 % intervaloFlush == 0:
                f2.flush()

        # Ordenação EVENTO-CIDADE
        escritor = csv.DictWriter(f3, delimiter='|', fieldnames= ['NOME-DO-EVENTO', 'CIDADE-DO-EVENTO', 'OCORRENCIAS-EVENTO-CIDADE'])
        escritor.writeheader()

        for evento, cidade in eventos_cidades_ordenados:
            escritor.writerow({
                'NOME-DO-EVENTO': evento,
                'CIDADE-DO-EVENTO': cidade,
                'OCORRENCIAS-EVENTO-CIDADE':
                    frequencia_evento_cidade[(evento, cidade)]
            })
            totalLinhas3 += 1
            
            if totalLinhas3 % intervaloFlush == 0:
                f3.flush()
        

    tempo_total = time.time() - inicio
    print(f' Tempo de execução: {tempo_total:.2f} s')
    print(f' Total de linhas lidas: {totalLinhas}')
    print(f' Qntd de linhas conjunto 1: {totalLinhas1}')
    print(f' Qntd de linhas conjunto 2: {totalLinhas2}')
    print(f' Qntd de linhas conjunto 3: {totalLinhas3}')

if __name__ == '__main__':
    main()
