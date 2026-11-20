import numpy as np


def montar_rigidez(qntd_nos, conectividade, rigidezes):
    """
    Monta a matriz de rigidez global.
    Os índices dos nós e dos elementos começam em zero.
    As rigidezes seguem a mesma ordem da conectividade.
    """
    K = np.zeros((qntd_nos, qntd_nos))
    for elemento, nos in enumerate(conectividade):
        i, j = nos
        k = rigidezes[elemento]
        K[i, i] += k
        K[j, j] += k
        K[i, j] -= k
        K[j, i] -= k

    return K


def resolver_sistema(K, forcas_aplicadas, prescritos, valores_prescritos):
    """
    Recebe a matriz global, as forças aplicadas e as condições de deslocamento prescrito.
    Determina os índices livres, monta o sistema reduzido e o resolve.
    Reconstrói os deslocamentos globais e calcula as reações.
    """
    
    # qntd_nos, nesse caso, corresponde a quantidade total de graus de liberdade do sistema. 
    # Como cada nó possui apenas um grau de liberdade, a quantidade de nós é 
    # igual a quantidade de graus de liberdade.
    # Caso cada nó possuísse, por exemplo, 3 graus de liberdade, a quantidade total de graus 
    # de liberdade seria 3 vezes a quantidade de nós.

    qntd_nos = K.shape[0]
    livres = []
    for no in range(qntd_nos):
        if no not in prescritos:
            livres.append(no)
    K_ll = K[np.ix_(livres, livres)]
    K_lp = K[np.ix_(livres, prescritos)]
    forcas_livres = forcas_aplicadas[livres]
    forcas_corrigidas = forcas_livres - (K_lp @ valores_prescritos)
    deslocamentos_livres = np.linalg.solve(K_ll, forcas_corrigidas)
    deslocamentos = np.zeros(qntd_nos)
    deslocamentos[livres] = deslocamentos_livres
    deslocamentos[prescritos] = valores_prescritos
    forcas_nodais = K @ deslocamentos

    '''
    # Outra forma de calcular as forças nodais:
    K_pl = K[np.ix_(prescritos, livres)]
    K_pp = K[np.ix_(prescritos, prescritos)]

    forcas_prescritas = K_pl @ deslocamentos_livres + K_pp @ valores_prescritos
    forcas_nodais = np.zeros(qntd_nos)
    forcas_nodais[livres] = forcas_livres
    forcas_nodais[prescritos] = forcas_prescritas

    '''
    return deslocamentos, forcas_nodais


def calcular_forcas_elementos(conectividade, rigidezes, deslocamentos, alpha):
    """
    Calcula a força interna de cada mola/elemento a partir dos deslocamentos nodais.
    Para alpha=1 e conectividade orientada da esquerda para a direita,
    valores positivos indicam tração e negativos indicam compressão.
    """
    forcas_elementos = np.zeros(len(conectividade))
    for elemento, nos in enumerate(conectividade):
        i, j = nos
        delta = deslocamentos[j] - deslocamentos[i]
        forca_elemento = alpha*delta*rigidezes[elemento]
        forcas_elementos[elemento] = forca_elemento

    return forcas_elementos
