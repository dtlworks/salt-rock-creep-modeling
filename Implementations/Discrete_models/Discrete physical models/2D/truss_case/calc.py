import numpy as np


def calcular_rigidez_elemento(coordenadas_i, coordenadas_j, E, area):
    """
    Calcula o fator EA/L e os cossenos diretores de uma barra de treliça.
    Retorna:
        fator_rigidez, c, s
    """
    dx = coordenadas_j[0] - coordenadas_i[0]
    dy = coordenadas_j[1] - coordenadas_i[1]
    comprimento = ((dx)**2 + (dy)**2)**0.5
    c = dx/comprimento
    s = dy/comprimento
    fator_rigidez = (E*area)/comprimento

    return fator_rigidez, c, s, comprimento


def montar_matriz_rigidez_elemento(fator_rigidez, c, s):
    """
    Calcula e monta a matriz de rigidez do elemento.
    Retorna:
        matriz_rigidez_elemento
    """
    matriz_base = np.array([
        [c**2, c*s, -c**2, -c*s],
        [c*s, s**2, -c*s, -s**2],
        [-c**2, -c*s, c**2, c*s],
        [-c*s, -s**2, c*s, s**2]
    ])
    matriz_rigidez_elemento = fator_rigidez * matriz_base

    return matriz_rigidez_elemento


def montar_matriz_rigidez_global(qntd_nos, coordenadas, conectividade, modulos_elasticidade, areas):
    """
    Calcula e monta a matriz de rigidez global, que será utilizada para cálculos posteriores.
    É necessário que coordenadas, conectividade, modulos_elasticidade e areas mantenham a mesma ordem de elementos.
    Retorna:
        K_global
    """
    K_global = np.zeros((2 * qntd_nos, 2 * qntd_nos))
    for elemento, nos in enumerate(conectividade):
        i, j = nos
        coordenadas_i = coordenadas[i]
        coordenadas_j = coordenadas[j]
        fator_rigidez, c, s, comprimento = calcular_rigidez_elemento(coordenadas_i, coordenadas_j, modulos_elasticidade[elemento], areas[elemento])
        matriz_rigidez_elemento = montar_matriz_rigidez_elemento(fator_rigidez, c, s)
        gdl_elemento = [2*i, 2*i + 1, 2*j, 2*j + 1]
        for linha_local, gdl_linha in enumerate(gdl_elemento):
            for coluna_local, gdl_coluna in enumerate(gdl_elemento):
                K_global[gdl_linha, gdl_coluna] += matriz_rigidez_elemento[linha_local, coluna_local]

    return K_global


def resolver_trelica(K_global, forcas_aplicadas, gdl_prescritos, deslocamentos_prescritos):
    """
    Recebe a matriz global, as forças aplicadas e as condições de deslocamento prescrito.
    Determina os índices livres, monta o sistema reduzido e o resolve.
    Reconstrói os deslocamentos globais e calcula as reações.
    Retorna:
        deslocamentos, forcas_globais
    """
    qntd_gdl = K_global.shape[0]
    livres = []
    gdl_prescritos_set = set(gdl_prescritos) # para acelerar a consulta
    for gdl in range(qntd_gdl):
        if gdl not in gdl_prescritos_set:
            livres.append(gdl)
    K_ll = K_global[np.ix_(livres, livres)]
    K_lp = K_global[np.ix_(livres, gdl_prescritos)]
    forcas_livres = forcas_aplicadas[livres]
    forcas_corrigidas = forcas_livres - (K_lp @ deslocamentos_prescritos)
    deslocamentos_livres = np.linalg.solve(K_ll, forcas_corrigidas)
    deslocamentos = np.zeros(qntd_gdl)
    deslocamentos[livres] = deslocamentos_livres
    deslocamentos[gdl_prescritos] = deslocamentos_prescritos
    # forcas_globais = K_global @ deslocamentos -> método mais custoso computacionalmente para problemas mais complexos de treliça
    K_pl = K_global[np.ix_(gdl_prescritos, livres)]
    K_pp = K_global[np.ix_(gdl_prescritos, gdl_prescritos)]
    forcas_prescritas = (K_pl @ deslocamentos_livres) + (K_pp @ deslocamentos_prescritos)
    forcas_globais = np.zeros(qntd_gdl)
    forcas_globais[livres] = forcas_livres
    forcas_globais[gdl_prescritos] = forcas_prescritas
    
    return deslocamentos, forcas_globais


def calcular_esforcos_barras(coordenadas, conectividade, modulos_elasticidade, areas, deslocamentos):
    """
    Recebe coordenadas, conectividade, modulos_elasticidade, areas, deslocamentos.
    Com os parâmetros recebidos calcula força, tensão e deformação axiais no elemento.
    Retorna:
        forcas, tensoes, deformacoes
    """
    qntd_elementos = len(conectividade)
    forcas = np.zeros(qntd_elementos)
    tensoes = np.zeros(qntd_elementos)
    deformacoes = np.zeros(qntd_elementos)
    for elemento, nos in enumerate(conectividade):
        i, j = nos
        coordenadas_i = coordenadas[i]
        coordenadas_j = coordenadas[j]
        gdl_elemento = [2*i, 2*i+1, 2*j, 2*j+1]
        fator_rigidez, c, s, comprimento = calcular_rigidez_elemento(coordenadas_i, coordenadas_j, modulos_elasticidade[elemento], areas[elemento])
        variacao_comprimento = (c*(deslocamentos[gdl_elemento[2]]- deslocamentos[gdl_elemento[0]]) + 
                                s*(deslocamentos[gdl_elemento[3]]- deslocamentos[gdl_elemento[1]]))    
        deformacoes[elemento] = variacao_comprimento/comprimento
        tensoes[elemento] = deformacoes[elemento]*modulos_elasticidade[elemento]
        forcas[elemento] = tensoes[elemento]*areas[elemento]

    return forcas, tensoes, deformacoes
