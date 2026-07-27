import math
from random import randint
import pyvista as pv

def calcular_secao_transversal(d: float) -> float:
    """
    Recebe o diâmetro (d) do elemento cilídnrico.
    Cálcula e retorna a área da seção transversal do mesmo.
    """
    return ((d/2)**2)*math.pi

def calcular_forca_normal(cargas: list, f_1: bool) -> float:
    """
    Recebe um array com todas as cargas que influem no elemento, determinado a carga total. 
    A partir da carga total, cálcula e retorna a força/carga normal axial "resultante" (f) no elemento em questão.
    """
    if not f_1:
        f = 0
        for c in cargas:
            f += c
        return f
    else:
        return cargas[0]

def calcular_tensao_media_elemento(d: float, cargas: list, f_1: bool) -> float:
    """
    Recebe o diâmetro do elemento e as cargas atuantes no mesmo.
    Cálcula e retorna a tensão média.
    """
    return calcular_forca_normal(cargas, f_1)/calcular_secao_transversal(d)

def caracterizar_tensao_media(tensao: float) -> str:
    """
    Recebe o valor da tensão no elemento.
    Retorna o tipo de tensão no mesmo.
    """
    if tensao > 0:
        return "Tração"
    elif tensao < 0:
        return "Compressão"
    else:
        return "Sem tensão"

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print('ERRO: Forneça um valor válido.')

def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print('ERRO: Forneça um valor válido')

def visualizar_estrutura(cilindros, tensoes, diametros):
    plotter = pv.Plotter()
    for c in cilindros:
        l_min = min(tensoes)
        l_max = max(tensoes)
        d_max = max(diametros)
        o_x = d_max * 3
        o_y = d_max * 3
        z_max = c['posicao_z'] + c['altura'] + 0.0001
        cilindro = pv.Cylinder(
            radius = c['diametro']/2,
            height = c['altura'],
            center = (0, 0, c['posicao_z'] + c['altura']/2),
            direction = (0,0,1)
        )
        cilindro.cell_data['tensao'] = c['tensao'] * cilindro.n_cells 
        plotter.add_mesh(cilindro, show_edges = True, scalars = 'tensao', cmap = 'coolwarm', 
                         clim = [l_min, l_max], scalar_bar_args = {'fmt': '%.3f MPa', 'title': 'Tensão Média\n'})
    superficie_de_apoio = pv.Plane(
        center = (0, 0, z_max),
        direction = (0, 0, 1),
        i_size = o_x,
        j_size = o_y
    )
    plotter.add_mesh(superficie_de_apoio, color = 'gray', opacity = 1)
    plotter.show()

def main():
    while True:
        while True:
            n = ler_int('Informe o número de cilindros que compõem a estrutura: ')
            if n <= 0:
                print('ERRO: Forneça um valor positivo.')
            else:
                break

        cargas = list()
        diametros = list()
        tensoes = list()
        cilindros = list()
        cilindro = dict()

        for i in range(n):
            if i == 0:
                while True: 
                    d = ler_float(f'Forneça o diâmetro (em Metros) do cilindro {i+1}: ')
                    if d <= 0:
                        print('ERRO: Informe um valor válido para o diâmetro.')
                        continue
                    break
                diametros.append(d)
                p = ler_float(f'Forneça a carga (em Newtons) aplicada na extremidade do cilindro {i+1}): ')
                cargas.append(p)
            else:
                while True:
                    d = ler_float(f'Forneça o diâmetro (em Metros) do cilindro {i+1}: ')
                    if d < diametros[i-1]:
                        print(f'ERRO: Para o problema em questão, queremos diâmetros que crescem conforme o número de elementos.')
                    else:
                        break
                diametros.append(d)
                p = ler_float(f'Forneça a carga (em Newtons) aplicada na extremidade do cilindro {i+1}): ')
                cargas.append(p)

        for j in range (n):
            if j == 0:
                tensao = calcular_tensao_media_elemento(diametros[j], cargas, f_1 = True)/1_000_000
                tensoes.append(tensao)
                print(f'A tensão média no cilindro {j+1} é {tensao:.2f} MPa {caracterizar_tensao_media(tensao)}')
            else:
                tensao = calcular_tensao_media_elemento(diametros[j], cargas[:j+1], f_1 = False)/1_000_000
                tensoes.append(tensao)
                print(f'A tensão média no cilindro {j+1} é {tensao:.2f} MPa {caracterizar_tensao_media(tensao)}')

        z = 0
        for k in range(n):
            altura = randint(100,500)/1000
            cilindro = {
                'cilindro': k+1,
                'carga': cargas[k],
                'diametro': diametros[k],
                'tensao': tensoes[k],
                'altura': altura,
                'posicao_z': z
            }
            z += altura
            cilindros.append(cilindro)
        for c in cilindros:
            print(c)
        visualizar_estrutura(cilindros, tensoes, diametros)
        break

if __name__ == '__main__':
    main()
