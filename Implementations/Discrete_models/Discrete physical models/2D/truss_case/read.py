import numpy as np


def ler_dados_entrada(nome_arquivo):
    with open(nome_arquivo, "r", encoding = "utf-8") as arquivo: 
        linhas_limpas = []
        for linha in arquivo:
            linha_limpa = linha.split("#", 1)[0].strip()
            if linha_limpa:
                linhas_limpas.append(linha_limpa)

    conectividade = []
    deslocamentos_prescritos = []
    modulos_elasticidade = []
    areas = []
    gdl_prescritos = []
    coordenadas_por_no = {}
    bloco_atual = None

    for linha in linhas_limpas:
        campos = linha.split()
        if campos[0] == "NOS":
            qntd_nos = int(campos[1])
            forcas_aplicadas = np.zeros(2*qntd_nos)
        elif campos[0] == "COORDENADAS":
            bloco_atual = "COORDENADAS"
        elif campos[0] == "BARRAS":
            bloco_atual = "BARRAS"
        elif campos[0] == "CARGAS":
            bloco_atual = "CARGAS"        
        elif campos[0] == "RESTRICOES":
            bloco_atual = "RESTRICOES" 
        elif bloco_atual == "COORDENADAS":
            indice_do_no = int(campos[0])
            x = float(campos[1])
            y = float(campos[2])
            coordenadas_por_no[indice_do_no] = [x, y]
        elif bloco_atual == "BARRAS":
            conectividade.append([int(campos[0]), int(campos[1])])
            modulos_elasticidade.append(float(campos[2]))
            areas.append(float(campos[3]))        
        elif bloco_atual == "CARGAS":
            no = int(campos[0])
            i, j = 2*no, 2*no+1
            forcas_aplicadas[i] = float(campos[1])
            forcas_aplicadas[j] = float(campos[2])
        elif bloco_atual == "RESTRICOES":
            no = int(campos[0])
            for componente, valor in enumerate(campos[1:3]):
                if valor.upper() != "L":
                    gdl = 2*no + componente
                    gdl_prescritos.append(gdl)
                    deslocamentos_prescritos.append(float(valor))

    deslocamentos_prescritos = np.array(deslocamentos_prescritos)
    coordenadas = np.array([coordenadas_por_no[no] for no in range(qntd_nos)], dtype = float)
    
    return qntd_nos, coordenadas, conectividade, modulos_elasticidade, areas, forcas_aplicadas, gdl_prescritos, deslocamentos_prescritos
