# -*- coding: utf-8 -*-
import csv
import glob
import xml.etree.ElementTree as et
import io
import zipfile
import os
import time

start_time = time.time()

# Define os diretórios usados

# Cloque aqui o diretório onde os currículos estão armazenados
base_dir = r'E:\curriculos_8818077_2024-11-27'

# Coloque o diretório em que o extrator pegará os dados
curriculos = glob.glob(r'E:\curriculos_8818077_2024-11-27\data\repo_2024\*\*.*')

# Coloque onde ficará os resultados
result_dir = r'E:\Dennyo\codigos\extrator_preprint\data'


colunas_artigo = ['TITULO-DO-ARTIGO','ANO','NATUREZA','LOCAL-NATUREZA','MEIO-DE-DIVULGACAO',
                  'GRANDE-AREA-DO-CONHECIMENTO-1',"AREA-DO-CONHECIMENTO-1",'SUB-AREA-DO-CONHECIMENTO-1',
                  'GRANDE-AREA-DO-CONHECIMENTO-2',"AREA-DO-CONHECIMENTO-2",'SUB-AREA-DO-CONHECIMENTO-2',
                  'GRANDE-AREA-DO-CONHECIMENTO-3',"AREA-DO-CONHECIMENTO-3",'SUB-AREA-DO-CONHECIMENTO-3',
                  'DOI', 'PAIS-DE-PUBLICACAO', 'IDIOMA', 'HOME-PAGE-DO-TRABALHO', 'ISSN', 'VOLUME', 'PAGINA-INICIAL', 'PAGINA-FINAL', 'NUMERO-DE-PAGINAS', 'IDENTIFICADOR']

colunas_autor= ['IDENTIFICADOR','NOME-AUTOR', 'ORCID', 'CEP', 'INSTITUICAO', 'COD-INSTITUICAO' ,
                'NOME-GRANDE-AREA-DO-CONHECIMENTO', 'NOME-DA-AREA-DO-CONHECIMENTO', "MAIOR-FORMACAO", "ANO-DE-CONCLUSAO", "TEM_PREPRINT"]


artigos = os.path.join(result_dir, 'dados_artigos_atualizados.csv')

autores = os.path.join(result_dir, 'dados_autores_atualizados.csv')

with open(artigos, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter= ",")

    escritor.writerow(colunas_artigo)

with open(autores, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter= ",")

    escritor.writerow(colunas_autor)

contagem_artigos = 0
contagem_preprints = 0
contagem_autor = 0
contagem_erro = 0
autores_com_erro = {}

def Maior_Formacao(formacoes: et.Element) -> tuple[str, str]:
    """
    Determina a maior formação acadêmica concluída de um pesquisador.

    Parâmetros:
        formacoes (Element): nó <FORMACAO-ACADEMICA-TITULACAO> do XML.

    Retorna:
        tuple[str, str]: (categoria da formação, ano de conclusão)
                         ou ("NAO_INFORMADO", "") se nenhuma formação estiver concluída.
    """

    # Ordem de prioridade das formações (da mais alta para a mais baixa)
    categorias_prioritarias = ["DOUTORADO", "MESTRADO", "ESPECIALIZACAO", "GRADUACAO", "ENSINO-TECNICO"]

    if formacoes is None:
        return ("NAO_INFORMADO", "")

    for categoria_formacao in categorias_prioritarias:
        # Busca todos os cursos dessa categoria usando ElementTree
        cursos_da_categoria = formacoes.findall(categoria_formacao)

        # Filtra apenas os cursos concluídos
        cursos_concluidos = [curso for curso in cursos_da_categoria if curso.get("STATUS-DO-CURSO") == "CONCLUIDO"]

        if cursos_concluidos:
            # Pega o curso mais recente pelo ano de conclusão
            curso_mais_recente = max(
                cursos_concluidos,
                key=lambda c: int(c.get("ANO-DE-CONCLUSAO", "0") or "0")
            )
            return (categoria_formacao, curso_mais_recente.get("ANO-DE-CONCLUSAO"))

    return ("NAO_INFORMADO", "")

for curriculo in curriculos:

    try:

        if curriculo.split('.')[-1] == 'zip':
            with open(curriculo, 'rb') as curriculo_zip:
                content = curriculo_zip.read()

            zip_memory = io.BytesIO(content)
            zip_data = zipfile.ZipFile(zip_memory)

            relative_path = os.path.relpath(curriculo, base_dir)
            relative_path_no_ext = os.path.splitext(relative_path)[0]
            parts = relative_path_no_ext.split(os.sep)
            identificador = parts[-1]

            contagem_autor +=1

            with zip_data.open(f'{identificador}.xml') as xml_data:
                xml_content = xml_data.read()
                root = et.fromstring(xml_content)

        autor_preprint = ""

        for artigo in root.findall(".//ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO"):
            dados_basicos = artigo.find("DADOS-BASICOS-DO-ARTIGO")
            dados_detalhados = artigo.find("DETALHAMENTO-DO-ARTIGO")

            natureza = str(dados_basicos.get('NATUREZA')).upper()
            local_natureza = "ARTIGOS-PUBLICADOS"
            meio_divulgacao = str(dados_basicos.get('MEIO-DE-DIVULGACAO')).upper()
            titulo = str(dados_basicos.get('TITULO-DO-ARTIGO'))
            ano = str(dados_basicos.get('ANO-DO-ARTIGO'))
            doi = str(dados_basicos.get('DOI'))
            pais_publicacao = str(dados_basicos.get('PAIS-DE-PUBLICACAO'))
            idioma = str(dados_basicos.get('IDIOMA'))
            home_page = str(dados_basicos.get('HOME-PAGE-DO-TRABALHO'))

            issn = str(dados_detalhados.get('ISSN'))
            volume = str(dados_detalhados.get('VOLUME'))
            pagina_inicial = str(dados_detalhados.get('PAGINA-INICIAL'))
            pagina_final = str(dados_detalhados.get('PAGINA-FINAL'))
            n_paginas = str(dados_detalhados.get('NUMERO-DE-PAGINAS'))

            areas_conhecimento = []
            areas_conhecimento.append(artigo.find(".//AREA-DO-CONHECIMENTO-1"))
            areas_conhecimento.append(artigo.find(".//AREA-DO-CONHECIMENTO-2"))
            areas_conhecimento.append(artigo.find(".//AREA-DO-CONHECIMENTO-3"))

            nome_grande_area_conhecimento = []
            nome_area_conhecimento = []
            nome_sub_area_conhecimento = []

            cont = 0

            for i in areas_conhecimento:
                if(areas_conhecimento[cont] is None):
                    nome_grande_area_conhecimento.append("")
                    nome_area_conhecimento.append("")
                    nome_sub_area_conhecimento.append("")
                else:
                    nome_grande_area_conhecimento.append(str(i.get("NOME-GRANDE-AREA-DO-CONHECIMENTO")))
                    nome_area_conhecimento.append(str(i.get("NOME-DA-AREA-DO-CONHECIMENTO")))
                    nome_sub_area_conhecimento.append(str(i.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO")))
                cont+=1

            formas_preprint = {"PRE PRINT", "PRE-PRINT", "PREPRINT", "PRÉ PRINT", "PRÉ-PRINT", "PRÉPRINT"}
            if(natureza in formas_preprint or meio_divulgacao in formas_preprint):

                contagem_preprints += 1
                natureza = "PREPRINT"
                if (autor_preprint != identificador):
                    autor_preprint = identificador

            dados_artigo = [titulo, ano, natureza, local_natureza, meio_divulgacao,
                            nome_grande_area_conhecimento[0], nome_area_conhecimento[0], nome_sub_area_conhecimento[0],
                            nome_grande_area_conhecimento[1], nome_area_conhecimento[1], nome_sub_area_conhecimento[1],
                            nome_grande_area_conhecimento[2], nome_area_conhecimento[2], nome_sub_area_conhecimento[2],
                            doi, pais_publicacao, idioma, home_page, issn, volume, pagina_inicial, pagina_final, n_paginas, identificador]

            contagem_artigos += 1
            print(f'Artigo: {contagem_artigos}\nAutor {contagem_autor}: {identificador}\n')

            with open(artigos, mode='a', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv, delimiter = ",")

                escritor.writerow(dados_artigo)



        outra_producao = root.find(".//OUTRA-PRODUCAO-BIBLIOGRAFICA")
        if (outra_producao is not None):

            for artigo in root.findall(".//OUTRA-PRODUCAO-BIBLIOGRAFICA"):

                dados_basicos = artigo.find("DADOS-BASICOS-DE-OUTRA-PRODUCAO")
                dados_detalhados = artigo.find("DETALHAMENTO-DE-OUTRA-PRODUCAO")
                n_paginas = ""

                natureza = str(dados_basicos.get('NATUREZA')).upper()
                local_natureza = "DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA"
                meio_divulgacao = str(dados_basicos.get('MEIO-DE-DIVULGACAO')).upper()
                titulo = str(dados_basicos.get('TITULO'))
                ano = str(dados_basicos.get('ANO'))
                doi = str(dados_basicos.get('DOI'))
                pais_publicacao = str(dados_basicos.get('PAIS-DE-PUBLICACAO'))
                idioma = str(dados_basicos.get('IDIOMA'))
                home_page = str(dados_basicos.get('HOME-PAGE-DO-TRABALHO'))

                issn = str(dados_detalhados.get('ISSN-ISBN'))
                volume = str(dados_detalhados.get('VOLUME'))
                pagina_inicial = str(dados_detalhados.get('PAGINA-INICIAL'))
                pagina_final = str(dados_detalhados.get('PAGINA-FINAL'))
                n_paginas = str(dados_detalhados.get('NUMERO-DE-PAGINAS'))

                areas_conhecimento = []
                areas_conhecimento.append(artigo.find(".//AREA-DO-CONHECIMENTO-1"))
                areas_conhecimento.append(artigo.find(".//AREA-DO-CONHECIMENTO-2"))
                areas_conhecimento.append(artigo.find(".//AREA-DO-CONHECIMENTO-3"))

                nome_grande_area_conhecimento = []
                nome_area_conhecimento = []
                nome_sub_area_conhecimento = []

                cont = 0

                for i in areas_conhecimento:
                    if(areas_conhecimento[cont] is None):
                        nome_grande_area_conhecimento.append("")
                        nome_area_conhecimento.append("")
                        nome_sub_area_conhecimento.append("")
                    else:
                        nome_grande_area_conhecimento.append(str(i.get("NOME-GRANDE-AREA-DO-CONHECIMENTO")))
                        nome_area_conhecimento.append(str(i.get("NOME-DA-AREA-DO-CONHECIMENTO")))
                        nome_sub_area_conhecimento.append(str(i.get("NOME-DA-SUB-AREA-DO-CONHECIMENTO")))
                    cont+=1

                formas_preprint = {"PRE PRINT", "PRE-PRINT", "PREPRINT", "PRÉ PRINT", "PRÉ-PRINT", "PRÉPRINT"}
                if(natureza in formas_preprint or meio_divulgacao in formas_preprint):

                    contagem_preprints += 1
                    natureza = "PREPRINT"
                    if (autor_preprint != identificador):
                        autor_preprint = identificador

                dados_artigo = [titulo, ano, natureza, local_natureza, meio_divulgacao,
                                nome_grande_area_conhecimento[0], nome_area_conhecimento[0], nome_sub_area_conhecimento[0],
                                nome_grande_area_conhecimento[1], nome_area_conhecimento[1], nome_sub_area_conhecimento[1],
                                nome_grande_area_conhecimento[2], nome_area_conhecimento[2], nome_sub_area_conhecimento[2],
                                doi, pais_publicacao, idioma, home_page, issn, volume, pagina_inicial, pagina_final, n_paginas, identificador]

                contagem_artigos +=1
                print(f'Artigo: {contagem_artigos}\nAutor {contagem_autor}: {identificador}\n')

                with open(artigos, mode='a', newline='', encoding='utf-8') as arquivo_csv:
                    escritor = csv.writer(arquivo_csv, delimiter = ",")

                    escritor.writerow(dados_artigo)

        for element in root.findall('.//DADOS-GERAIS'):

            nome = str(element.get('NOME-COMPLETO'))
            orcid_id = str(element.get('ORCID-ID'))
            endereco_prof = element.find('.//ENDERECO-PROFISSIONAL')

            if endereco_prof is not None:
                nome_instituicao = str(endereco_prof.get('NOME-INSTITUICAO-EMPRESA'))
                cod_instituicao = str(endereco_prof.get('CODIGO-INSTITUICAO-EMPRESA'))
                CEP = str(endereco_prof.get('CEP'))
            else:
                nome_instituicao = "NAO INFORMADO"
                cod_instituicao = "NAO INFORMADO"
                CEP = "NAO INFORMADO"

            area_atuacao = element.find("AREAS-DE-ATUACAO/AREA-DE-ATUACAO[@SEQUENCIA-AREA-DE-ATUACAO='1']")

            if(area_atuacao is None):
                nome_grande_area_do_conhecimento = "NAO INFORMADO"
                nome_da_area_do_conhecimento = "NAO INFORMADO"
            else:
                nome_grande_area_do_conhecimento = str(area_atuacao.get("NOME-GRANDE-AREA-DO-CONHECIMENTO"))
                nome_da_area_do_conhecimento = str(area_atuacao.get("NOME-DA-AREA-DO-CONHECIMENTO"))

            formacoes = element.find("FORMACAO-ACADEMICA-TITULACAO")
            dados_formacao = Maior_Formacao(formacoes=formacoes)
            maior_formacao = dados_formacao[0]
            ano_conclusao = dados_formacao[1]

            tem_preprint = "SIM" if autor_preprint == identificador else "NAO"

            dados_autor = [identificador, nome, orcid_id, CEP, nome_instituicao, cod_instituicao,
                           nome_grande_area_do_conhecimento, nome_da_area_do_conhecimento, maior_formacao, ano_conclusao, tem_preprint]

            with open(autores, mode='a', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv, delimiter = ",")

                escritor.writerow(dados_autor)


    except Exception as Erro:
        print(f"Error: {Erro}")
        print(f'Erro com o identificador: {identificador}\n')
        contagem_erro +=1
        autores_com_erro[identificador] = Erro
        pass



if len(autores_com_erro) > 0:
    erros = os.path.join(result_dir,'autores_com_erro.csv')
    with open(erros, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv, delimiter = ",")

        escritor.writerow(['Identificador', 'Erro'])
        for autor, erro in autores_com_erro.items():
            escritor.writerow([autor, erro])

print(f'\nTotal de artigos analisados: {contagem_artigos}\nTotal de Preprints identificados: {contagem_preprints}\nTotal de autores: {contagem_autor}\nTotal de erros: {contagem_erro}')

if len(autores_com_erro) > 0:
    print("Os erros e os autores com quem ocorreram foram registrados em: autores_com_erro.csv")

end_time = time.time()

execution_time = end_time - start_time

print(f"\nTempo de execução: {execution_time:.6f} segundos")