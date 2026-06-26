##f

import csv
import os
import io
import time
import zipfile
import xml.etree.ElementTree as ET

pastaCurriculos = r'F:\Exemplo Curriculos'     #pastas no meu computador (lucas josé)
saidaCSV = r'F:\ProjetoMagela\CSVMagela\Final'

#arquivos de saida:
csvEventos = os.path.join(saidaCSV, 'csvEventos.csv')
csvErros = os.path.join(saidaCSV, 'curriculosErro.csv')
csvVazios = os.path.join(saidaCSV, 'curriculosSemEventos.csv')

#variavel para melhorar fluxo lá embaixo
intervalo1 = 50
intervaloFlush = 200

#colunas csv final
COLUNAS = [
    'IDENTIFICADOR',
    'TIPO-REGISTRO',
    'NOME-DO-EVENTO',
    'TIPO-DE-EVENTO',
    'CLASSIFICACAO-DO-EVENTO',
    'ANO-DO-EVENTO',
    'PAIS-DO-EVENTO',
    'CIDADE-DO-EVENTO',
    'LOCAL-DO-EVENTO',
    'CODIGO-INSTITUICAO-PROMOTORA',
    'INSTITUICAO-PROMOTORA',
    'DURACAO-EM-SEMANAS',
]

#funcao para inicializar as colunas do final
def linha_vazia() -> dict:
    return {coluna: '' for coluna in COLUNAS}

#raizes dos eventos no xml
PARTICIPACOES = [
    ('PARTICIPACAO-EM-CONGRESSO',
     'DADOS-BASICOS-DA-PARTICIPACAO-EM-CONGRESSO',
     'DETALHAMENTO-DA-PARTICIPACAO-EM-CONGRESSO', 'CONGRESSO'),
    ('PARTICIPACAO-EM-SEMINARIO',
     'DADOS-BASICOS-DA-PARTICIPACAO-EM-SEMINARIO',
     'DETALHAMENTO-DA-PARTICIPACAO-EM-SEMINARIO', 'SEMINARIO'),
    ('PARTICIPACAO-EM-SIMPOSIO',
     'DADOS-BASICOS-DA-PARTICIPACAO-EM-SIMPOSIO',
     'DETALHAMENTO-DA-PARTICIPACAO-EM-SIMPOSIO', 'SIMPOSIO'),
    ('PARTICIPACAO-EM-OFICINA',
     'DADOS-BASICOS-DA-PARTICIPACAO-EM-OFICINA',
     'DETALHAMENTO-DA-PARTICIPACAO-EM-OFICINA', 'OFICINA'),
    ('PARTICIPACAO-EM-ENCONTRO',
     'DADOS-BASICOS-DA-PARTICIPACAO-EM-ENCONTRO',
     'DETALHAMENTO-DA-PARTICIPACAO-EM-ENCONTRO', 'ENCONTRO'),
    ('PARTICIPACAO-EM-EXPOSICAO',
     'DADOS-BASICOS-DA-PARTICIPACAO-EM-EXPOSICAO',
     'DETALHAMENTO-DA-PARTICIPACAO-EM-EXPOSICAO', 'EXPOSICAO'),
    ('OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS',
     'DADOS-BASICOS-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS',
     'DETALHAMENTO-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS', 'OUTRA'),
]

#funcoes
#funcao pra abrir pasta MODELO /C:/Curriculos/00/012393291843.xml <- se não me engano tá assim lá no pc
#caso não for assim, só arrumar lá na hora tirando ou colocando mais um with
def abridorDosZIP(pasta_raiz: str):
    with os.scandir(pasta_raiz) as subpastas:
        for sub in subpastas:
            if not sub.is_dir():
                continue
            with os.scandir(sub.path) as arquivos:
                for arq in arquivos:
                    if arq.is_file() and arq.name.lower().endswith('.zip'):
                        yield arq.path

#funcao pra ler xml
def lerOsXML(caminho_zip: str) -> ET.Element:
    with open(caminho_zip, 'rb') as f:
        zip_bytes = io.BytesIO(f.read())
    with zipfile.ZipFile(zip_bytes) as zip_data:
        nomesXML = [n for n in zip_data.namelist() if n.lower().endswith('.xml')]
        if not nomesXML:
            raise ValueError('currículo vazio')
        with zip_data.open(nomesXML[0]) as xml_data:
            return ET.fromstring(xml_data.read())

#funcao pra extrair string das raizes
def extrairEventos(root: ET.Element, identificador: str, escrever) -> int:
    total = 0

    #TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS
    for trabalho in root.findall('.//TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS'):
        db = trabalho.find('DADOS-BASICOS-DO-TRABALHO')
        dd = trabalho.find('DETALHAMENTO-DO-TRABALHO')
        if db is None or dd is None:
            continue
        linha = linha_vazia()
        linha.update({
            'IDENTIFICADOR': identificador,
            'TIPO-REGISTRO': 'TRABALHO-EM-EVENTOS',
            'NOME-DO-EVENTO': dd.get('NOME-DO-EVENTO', ''),
            'CLASSIFICACAO-DO-EVENTO': dd.get('CLASSIFICACAO-DO-EVENTO', ''),
            'ANO-DO-EVENTO': dd.get('ANO-DE-REALIZACAO', ''),
            'PAIS-DO-EVENTO': db.get('PAIS-DO-EVENTO', ''),
            'CIDADE-DO-EVENTO': dd.get('CIDADE-DO-EVENTO', ''),
        })
        escrever(linha)
        total += 1

    #APRESENTACAO-DE-TRABALHO
    for apresentacao in root.findall('.//APRESENTACAO-DE-TRABALHO'):
        db = apresentacao.find('DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO')
        dd = apresentacao.find('DETALHAMENTO-DA-APRESENTACAO-DE-TRABALHO')
        if db is None or dd is None:
            continue
        linha = linha_vazia()
        linha.update({
            'IDENTIFICADOR': identificador,
            'TIPO-REGISTRO': 'APRESENTACAO-DE-TRABALHO',
            'NOME-DO-EVENTO': dd.get('NOME-DO-EVENTO', ''),
            'TIPO-DE-EVENTO': db.get('NATUREZA', ''),   # aqui SIM é tipo de evento
            'ANO-DO-EVENTO': db.get('ANO', ''),
            'PAIS-DO-EVENTO': db.get('PAIS', ''),
            'INSTITUICAO-PROMOTORA': dd.get('INSTITUICAO-PROMOTORA', ''),
            'LOCAL-DO-EVENTO': dd.get('LOCAL-DA-APRESENTACAO', ''),
            'CIDADE-DO-EVENTO': dd.get('CIDADE-DA-APRESENTACAO', ''),
        })
        escrever(linha)
        total += 1

    #ORGANIZACAO-DE-EVENTO
    for organizacao in root.findall('.//ORGANIZACAO-DE-EVENTO'):
        db = organizacao.find('DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO')
        dd = organizacao.find('DETALHAMENTO-DA-ORGANIZACAO-DE-EVENTO')
        if db is None or dd is None:
            continue
        linha = linha_vazia()
        linha.update({
            'IDENTIFICADOR': identificador,
            'TIPO-REGISTRO': 'ORGANIZACAO-DE-EVENTO',
            'TIPO-DE-EVENTO': db.get('TIPO', ''),
            'ANO-DO-EVENTO': db.get('ANO', ''),
            'PAIS-DO-EVENTO': db.get('PAIS', ''),
            'INSTITUICAO-PROMOTORA': dd.get('INSTITUICAO-PROMOTORA', ''),
            'LOCAL-DO-EVENTO': dd.get('LOCAL', ''),
            'CIDADE-DO-EVENTO': dd.get('CIDADE', ''),
            'DURACAO-EM-SEMANAS': dd.get('DURACAO-EM-SEMANAS', ''),
        })
        escrever(linha)
        total += 1

    #PARTICIPACAO-EM-{TIPO} + OUTRAS-PARTICIPACOES
    for rotulo, tag_dados, tag_detalh, tipo_evento in PARTICIPACOES:
        for participacao in root.findall(f'.//{rotulo}'):
            db = participacao.find(tag_dados)
            dd = participacao.find(tag_detalh)
            if db is None or dd is None:
                continue
            linha = linha_vazia()
            linha.update({
                'IDENTIFICADOR': identificador,
                'TIPO-REGISTRO': rotulo,
                'NOME-DO-EVENTO': dd.get('NOME-DO-EVENTO', ''),
                'TIPO-DE-EVENTO': tipo_evento,
                'ANO-DO-EVENTO': db.get('ANO', ''),
                'PAIS-DO-EVENTO': db.get('PAIS', ''),
                'CODIGO-INSTITUICAO-PROMOTORA': dd.get('CODIGO-INSTITUICAO', ''),
                'INSTITUICAO-PROMOTORA': dd.get('NOME-INSTITUICAO', ''),
                'LOCAL-DO-EVENTO': dd.get('LOCAL-DO-EVENTO', ''),
                'CIDADE-DO-EVENTO': dd.get('CIDADE-DO-EVENTO', ''),
            })
            escrever(linha)
            total += 1
    return total

#loop principal - chamar funcoes anteriores e escrever
def main():
    os.makedirs(saidaCSV, exist_ok=True)
    with open(csvEventos, mode='w', newline='', encoding='utf-8') as f_eventos: #\
        # open(csvErros, mode='w', newline='', encoding='utf-8') as f_erros, \
        # open(csvVazios, mode='w', newline='', encoding='utf-8') as f_vazios:

        escritor_eventos = csv.writer(f_eventos, delimiter=';')
        escritor_eventos.writerow(COLUNAS)

        #escritor_erros = csv.writer(f_erros)
        #escritor_erros.writerow(['IDENTIFICADOR', 'ERRO'])

        #escritor_vazios = csv.writer(f_vazios)
        #escritor_vazios.writerow(['IDENTIFICADOR'])

        def escrever(linha: dict) -> None:
            escritor_eventos.writerow([linha[c] for c in COLUNAS])

        contagemCurriculos = 0
        contagemEventos = 0
        contagemErros = 0
        contagemVazios = 0
        identificador = ''
        inicio = time.time()

        for caminho_zip in abridorDosZIP(pastaCurriculos):
            identificador = os.path.splitext(os.path.basename(caminho_zip))[0]
            contagemCurriculos += 1

            try:
                root = lerOsXML(caminho_zip)
                n_eventos = extrairEventos(root, identificador, escrever)
                contagemEventos += n_eventos
                if n_eventos == 0:
                    contagemVazios += 1
            #continua sem parar
            except Exception as erro:
                contagemErros += 1

            if contagemCurriculos % intervaloFlush == 0:
                f_eventos.flush()
                #f_erros.flush()
                #f_vazios.flush()

            if contagemCurriculos % intervalo1 == 0:
                decorrido = time.time() - inicio
                taxa = contagemCurriculos / decorrido if decorrido > 0 else 0
                print(f'{contagemCurriculos:>10} currículos'
                    f'{contagemEventos:>10} eventos'
                    #f'{contagemErros:>6} erros'
                    #f'{contagemVazios:>8} vazios'
                    f'{taxa:6.1f} de c por s')

    tempo_total = time.time() - inicio
    print(f'currículos a: {contagemCurriculos}')
    print(f'eventos totais: {contagemEventos}')
    print(f'currículos c e: {contagemErros} ')
    print(f'currículos s e: {contagemVazios} ')
    print(f'totaltime: {tempo_total} s')
    #print(f'CSV final em: {csvEventos}')

if __name__ == '__main__':
    main()