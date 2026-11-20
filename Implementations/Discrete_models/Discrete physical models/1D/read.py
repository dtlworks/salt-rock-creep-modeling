import numpy as np


def ler_dados_entrada(nome_arquivo):
    """
    Lê os dados de um modelo mecânico em um arquivo de texto.
    Retorna:
        qntd_nos
        conectividade
        rigidezes
        forcas_aplicadas
        prescritos
        valores_prescritos
        alpha
    """
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        linhas_limpas = []
        for linha in arquivo:
            linha_limpa = linha.split("#", 1)[0].strip()
            if linha_limpa != '':
                linhas_limpas.append(linha_limpa)

    conectividade = []
    rigidezes = []
    prescritos = []
    valores_prescritos = []
    bloco_atual = None

    for linha in linhas_limpas:
        campos = linha.split()
        if campos[0] == "NOS":
            qntd_nos = int(campos[1])
            forcas_aplicadas = np.zeros(qntd_nos)
        elif campos[0] == "ELEMENTOS":
            bloco_atual = "ELEMENTOS"
        elif campos[0] == "FORCAS":
            bloco_atual = "FORCAS"
        elif campos[0] == "PRESCRITOS":
            qntd_prescritos = int(campos[1])
            bloco_atual = "PRESCRITOS"
        elif campos[0] == "ALPHA":
            alpha = int(campos[1])
            bloco_atual = None
        elif bloco_atual == "ELEMENTOS":
            no_i = int(campos[0])    
            no_j = int(campos[1])
            rigidez = float(campos[2])
            conectividade.append([no_i, no_j])
            rigidezes.append(rigidez) 
        elif bloco_atual == 'FORCAS':
            forcas_aplicadas[int(campos[0])] = float(campos[1])
        elif bloco_atual == 'PRESCRITOS':
            prescritos.append(int(campos[0]))
            valores_prescritos.append(float(campos[1]))
    valores_prescritos = np.array(valores_prescritos)

    return qntd_nos, conectividade, rigidezes, forcas_aplicadas, prescritos, valores_prescritos, alpha
