import math
from random import randint

import pyvista as pv

FOLGA_PLANO_APOIO = 0.001
PA_PRA_MPA = 1_000_000
ALTURA_MIN = 100
ALTURA_MAX = 500
ALTURA_DIVISOR = 1000


def calcular_secao_transversal(d: float) -> float:
    """
    Recebe o diâmetro (d em metros) do elemento estrutural.
    Calcula e retorna a área da seção transversal do mesmo.
    """
    return math.pi*(d**2)/4


def calcular_forca_normal(cargas: list[float]) -> float:
    """
    Recebe um array fatiado com todas as cargas que influem no elemento. 
    A partir do correto fatiamento do array, cálcula e retorna a força/carga normal axial 
    "resultante" (f) no elemento em questão. Note que no problema em questão, a força
    normal no elemento i é dada pelo somatório de cargas até Pi, isto é, 
    f1 = p1; f2 = p1 + p2; ...; fn = p1 + p2 + ... + pn.
    """
    return sum(cargas)


def calcular_tensao_media_elemento(d: float, cargas: list[float]) -> float:
    """
    Recebe o diâmetro do elemento e as cargas atuantes no mesmo.
    Cálcula e retorna a tensão média.
    """
    return calcular_forca_normal(cargas) / calcular_secao_transversal(d)


def caracterizar_tensao_media(tensao: float) -> str:
    """
    Recebe o valor da tensão no elemento.
    Retorna o tipo de tensão no mesmo.
    """
    if tensao > 0:
        return "Tração"
    if tensao < 0:
        return "Compressão"
    return "Sem tensão"


def ler_float(mensagem: str) -> float:
    """
    Função destinada a tratamento de erro na leitura exclusiva de pontos flutuantes.
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print('ERRO: Forneça um valor válido.')


def ler_int(mensagem: str) -> int:
    """
    Função destinada a tratamento de erro na leitura exclusiva de números inteiros.
    """
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print('ERRO: Forneça um valor válido.')


def gerar_resultados_txt(cilindros: list) -> str:
    """
    Monta o texto formatado com o resumo dos resultados (tensão e estado)
    de cada elemento da estrutura, para exibição na cena 3D.
    """
    resultados = "Resultados:\n"
    for i, cilindro in enumerate(cilindros, start = 1):
        resultados += f"""
Elemento {i}                                              
Tensão: {cilindro['tensao']:.2f} MPa                
Estado: {caracterizar_tensao_media(cilindro['tensao'])}
"""
    return resultados


def visualizar_estrutura(cilindros: list[dict], tensoes: list[float], diametros: list[float]) -> None:
    """
    Função destinada a geração, integração estabelecimento de malhas, de forma espacial, coerentes com a 
    lógica do problema mecânico estabelecido. Os parâmetros são utilizados para integralização de dados, 
    acertificando sua posterior visualização e análise.
    """
    limite = max(abs(min(tensoes)), abs(max(tensoes)))
    if limite == 0:
        limite = 1e-3
    l_min, l_max = -limite, limite
    d_max = max(diametros)
    o_x = d_max * 3
    o_y = d_max * 3
    z_max = cilindros[-1]['posicao_z'] + cilindros[-1]['altura'] + FOLGA_PLANO_APOIO

    plotter = pv.Plotter()
    for c in cilindros:
        cilindro = pv.Cylinder(
            radius = c['diametro']/2,
            height = c['altura'],
            center = (0, 0, c['posicao_z'] + c['altura']/2),
            direction = (0, 0, 1),
        )
        cilindro.cell_data['tensao'] = [c['tensao']] * cilindro.n_cells
        plotter.add_mesh(
            cilindro,
            show_edges = True,
            scalars = 'tensao',
            cmap = 'coolwarm',
            clim = [l_min, l_max],
            scalar_bar_args = {'fmt': '%.3f MPa', 'title': 'Tensão Média\n'},
        )

    superficie_de_apoio = pv.Plane(
        center = (0, 0, z_max),
        direction = (0, 0, 1),
        i_size = o_x,
        j_size = o_y,
    )
    plotter.add_mesh(superficie_de_apoio, color = 'gray', opacity = 1)
    plotter.add_text(gerar_resultados_txt(cilindros), font_size = 12,
                     position = 'upper_left', color = 'black', shadow = True)
    plotter.show()


def main() -> None:
    while True:
        n = ler_int('Informe o número de cilindros que compõem a estrutura: ')
        if n <= 0:
            print('ERRO: Forneça um valor positivo.')
            continue
        break

    cargas: list[float] = []
    diametros: list[float] = []
    tensoes: list[float] = []
    cilindros: list[dict] = []

    for i in range(n):
        while True:
            diametro = ler_float(f'Forneça o diâmetro (em Metros) do cilindro {i+1}: ')
            if diametro <= 0:
                print('ERRO: Informe um valor válido para o diâmetro.')
                continue
            if i > 0 and diametro < diametros[i-1]:
                print('ERRO: Para o problema em questão, queremos diâmetros que crescem conforme o número de elementos.')
                continue
            break
        diametros.append(diametro)
        carga = ler_float(f'Forneça a carga (em Newtons) aplicada na extremidade do cilindro {i+1}: ')
        cargas.append(carga)

    for j in range(n):
        cargas_no_elemento = cargas[:j+1]
        tensao = (calcular_tensao_media_elemento(diametros[j], cargas_no_elemento)/PA_PRA_MPA)
        tensoes.append(tensao)

    z = 0
    for k in range(n):
        altura = randint(ALTURA_MIN, ALTURA_MAX)/ALTURA_DIVISOR
        cilindro = {
            'cilindro': k+1,
            'carga': cargas[k],
            'diametro': diametros[k],
            'tensao': tensoes[k],
            'altura': altura,
            'posicao_z': z,
        }
        z += altura
        cilindros.append(cilindro)

    visualizar_estrutura(cilindros, tensoes, diametros)


if __name__ == '__main__':
    main()
