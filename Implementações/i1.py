from __future__ import annotations

import math
from random import randint

import pyvista as pv

PA_PRA_MPA = 1_000_000
ALTURA_MIN = 100
ALTURA_MAX = 500
ALTURA_DIVISOR = 1000


def calcular_secao_transversal(d: float) -> float:
    return math.pi * (d ** 2) / 4


def calcular_forca_normal(cargas: list[float]) -> float:
    return sum(cargas)


def calcular_tensao_media_elemento(d: float, cargas: list[float]) -> float:
    return calcular_forca_normal(cargas) / calcular_secao_transversal(d)


def caracterizar_tensao_media(tensao: float) -> str:
    if tensao > 0:
        return "Tração"
    if tensao < 0:
        return "Compressão"
    return "Sem tensão"


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print('ERRO: Forneça um valor válido.')


def ler_int(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print('ERRO: Forneça um valor válido.')


def visualizar_estrutura(
    cilindros: list[dict],
    tensoes: list[float],
    diametros: list[float],
) -> None:
    l_min = min(tensoes)
    l_max = max(tensoes)
    d_max = max(diametros)
    o_x = d_max * 3
    o_y = d_max * 3
    z_max = cilindros[-1]['posicao_z'] + cilindros[-1]['altura'] + 0.0001

    plotter = pv.Plotter()
    for c in cilindros:
        cilindro = pv.Cylinder(
            radius=c['diametro'] / 2,
            height=c['altura'],
            center=(0, 0, c['posicao_z'] + c['altura'] / 2),
            direction=(0, 0, 1),
        )
        cilindro.cell_data['tensao'] = [c['tensao']] * cilindro.n_cells
        plotter.add_mesh(
            cilindro,
            show_edges=True,
            scalars='tensao',
            cmap='coolwarm',
            clim=[l_min, l_max],
            scalar_bar_args={'fmt': '%.3f MPa', 'title': 'Tensão Média\n'},
        )

    superficie_de_apoio = pv.Plane(
        center=(0, 0, z_max),
        direction=(0, 0, 1),
        i_size=o_x,
        j_size=o_y,
    )
    plotter.add_mesh(superficie_de_apoio, color='gray', opacity=1)
    plotter.show()


def main() -> None:
    while True:
        while True:
            n = ler_int('Informe o número de cilindros que compõem a estrutura: ')
            if n <= 0:
                print('ERRO: Forneça um valor positivo.')
            else:
                break

        cargas: list[float] = []
        diametros: list[float] = []
        tensoes: list[float] = []
        cilindros: list[dict] = []

        for i in range(n):
            while True:
                d = ler_float(f'Forneça o diâmetro (em Metros) do cilindro {i + 1}: ')
                if d <= 0:
                    print('ERRO: Informe um valor válido para o diâmetro.')
                elif i > 0 and d < diametros[i - 1]:
                    print(
                        'ERRO: Para o problema em questão, queremos diâmetros '
                        'que crescem conforme o número de elementos.'
                    )
                else:
                    break
            diametros.append(d)
            p = ler_float(
                f'Forneça a carga (em Newtons) aplicada na extremidade '
                f'do cilindro {i + 1}): '
            )
            cargas.append(p)

        for j in range(n):
            cargas_no_elemento = cargas[:j + 1]
            tensao = (
                calcular_tensao_media_elemento(diametros[j], cargas_no_elemento)
                / PA_PRA_MPA
            )
            tensoes.append(tensao)
            print(
                f'A tensão média no cilindro {j + 1} é {tensao:.2f} MPa '
                f'{caracterizar_tensao_media(tensao)}'
            )

        z = 0.0
        for k in range(n):
            altura = randint(ALTURA_MIN, ALTURA_MAX) / ALTURA_DIVISOR
            cilindro = {
                'cilindro': k + 1,
                'carga': cargas[k],
                'diametro': diametros[k],
                'tensao': tensoes[k],
                'altura': altura,
                'posicao_z': z,
            }
            z += altura
            cilindros.append(cilindro)

        for c in cilindros:
            print(c)

        visualizar_estrutura(cilindros, tensoes, diametros)
        break


if __name__ == '__main__':
    main()
