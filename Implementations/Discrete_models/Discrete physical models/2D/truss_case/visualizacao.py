import numpy as np
import pyvista as pv



def calcular_coordenadas_deformadas(coordenadas, deslocamentos, mag):
    coordenadas_pos_deformacao = []
    for no in range(len(coordenadas)):
        i, j = coordenadas[no]
        x_d = i + mag*deslocamentos[2*no]
        y_d = j + mag*deslocamentos[2*no+1]
        coordenada_pos_deformacao = [x_d, y_d]
        coordenadas_pos_deformacao.append(coordenada_pos_deformacao)

    return np.array(coordenadas_pos_deformacao)


def criar_conectividade_linhas(conectividade):
    linhas = []
    for no_i, no_j in conectividade:
        trio = [2, no_i, no_j] 
        linhas += trio
    
    return np.array(linhas)


def identificar_apoios(qntd_nos, gdl_prescritos):
    apoios = {}
    prescritos = set(gdl_prescritos)
    for no in range(qntd_nos):
        gdl_x = no*2
        gdl_y = no*2+1
        x_restrito = gdl_x in prescritos
        y_restrito = gdl_y in prescritos
        if (x_restrito and y_restrito):
            apoios[no] = 'xy'
        elif (x_restrito):
            apoios[no] = 'x'
        elif (y_restrito):
            apoios[no] = 'y'

    return apoios


def criar_malha_apoio_xy(coordenada_no, escala):
    x, y = coordenada_no
    largura = 0.06*escala
    altura = 0.04*escala
    if y > 0:
        y_base = y + altura
    else:
        y_base = y-altura
    pontos_2d = np.array([
        [x, y],
        [x - largura / 2, y_base],
        [x + largura / 2, y_base]
    ])
    pontos_3d = np.column_stack([
        pontos_2d,
        np.zeros(len(pontos_2d))
    ])
    faces = np.array([3, 0, 1, 2])
    return pv.PolyData(pontos_3d, faces = faces)


def criar_malha_apoio_primeiro_genero(no_apoio, tipo, coordenadas, conectividade, escala):
    x, y = coordenadas[no_apoio]
    largura = 0.06*escala
    altura = 0.04*escala
    if tipo == "y":
        sentido = 1 if y > 0 else - 1
        pontos_2d = np.array([
            [x, y],
            [x - largura / 2, y + sentido*altura],
            [x + largura / 2, y + sentido*altura]
        ])
        centros_roletes = [
            [x - largura / 4, y + sentido*(altura+altura*0.12)],
            [x + largura / 4, y + sentido*(altura+altura*0.12)]
        ]
    else:
        vizinhos = []
        for no_i, no_j in conectividade:
            if no_i == no_apoio:
                vizinhos.append(no_j)
            elif no_j == no_apoio:
                vizinhos.append(no_i)
        x_medio_vizinhos = np.mean([coordenadas[n][0] for n in vizinhos])
        sentido = -1 if x_medio_vizinhos > x else 1
        pontos_2d = np.array([
            [x, y],
            [x + sentido * altura, y - largura / 2],
            [x + sentido * altura, y + largura / 2],
        ])
        centros_roletes = [
            [x + sentido * (altura + altura * 0.12), y - largura / 4],
            [x + sentido * (altura + altura * 0.12), y + largura / 4],
        ]
    pontos_3d = np.column_stack((pontos_2d, np.zeros(3)))
    triangulo = pv.PolyData(pontos_3d, faces=np.array([3, 0, 1, 2]))
    roletes = []
    raio = 0.008 * escala
    for cx, cy in centros_roletes:
        rolete = pv.Disc(
            center = (cx, cy, 0), inner = 0, outer = raio, normal = (0, 0, 1), r_res = 1, c_res = 20)
        roletes.append(rolete)

    return triangulo, roletes

def criar_setas_cargas(coordenadas, conectividade, forcas_aplicadas):
    setas = []
    comprimentos_barras = [
        np.linalg.norm(coordenadas[j] - coordenadas[i])
        for i, j in conectividade
    ]
    comprimento_seta = 0.35 * np.median(comprimentos_barras)
    raio_eixo = 0.025 * comprimento_seta
    raio_ponta = 0.09 * comprimento_seta
    for no, (x, y) in enumerate(coordenadas):
        fx = forcas_aplicadas[2 * no]
        fy = forcas_aplicadas[2 * no + 1]
        if fx != 0:
            sentido_x = np.sign(fx)
            inicio = (x, y, 0)
            direcao = (sentido_x, 0, 0)
            malha_seta = pv.Arrow(
                start=inicio, direction=direcao, scale=comprimento_seta,
                shaft_radius=raio_eixo, tip_radius=raio_ponta, tip_length=0.22,
            )
            setas.append((no, malha_seta, malha_seta.points.copy()))
        if fy != 0:
            sentido_y = np.sign(fy)
            inicio = (x, y, 0)
            direcao = (0, sentido_y, 0)
            malha_seta = pv.Arrow(
                start=inicio, direction=direcao, scale=comprimento_seta,
                shaft_radius=raio_eixo, tip_radius=raio_ponta, tip_length=0.22,
            )
            setas.append((no, malha_seta, malha_seta.points.copy()))

    return setas

def visualizar_trelica(coordenadas, conectividade, deslocamentos, gdl_prescritos, forcas_aplicadas, mag, nome_gif):
    coordenadas_pos_deformacao = calcular_coordenadas_deformadas(coordenadas, deslocamentos, mag)
    apoios = identificar_apoios(len(coordenadas), gdl_prescritos)
    escala = np.ptp(coordenadas, axis = 0).max()
    setas_animadas = criar_setas_cargas(coordenadas, conectividade, forcas_aplicadas)
    pontos_originais_3d = np.column_stack((coordenadas, np.zeros(len(coordenadas))))
    pontos_deformados_3d = np.column_stack((coordenadas_pos_deformacao, np.zeros(len(coordenadas))))
    linhas = criar_conectividade_linhas(conectividade)
    malha_original = pv.PolyData(pontos_originais_3d, lines = linhas)
    malha_deformada = pv.PolyData(pontos_deformados_3d, lines = linhas)
    malha_deformada.points = pontos_originais_3d.copy()
    plotter = pv.Plotter(off_screen = True)
    plotter.add_mesh(malha_original, color = "lightgray", line_width = 3)
    plotter.add_mesh(malha_deformada, color = "red", line_width = 3)
    roletes_animados = []
    triangulos_animados = []
    apoios_visuais = {}
    tolerancia = max(escala, 1.0) * 1e-9
    for no, tipo in apoios.items():
        chave = tuple(np.round(coordenadas[no] / tolerancia).astype(int))
        if chave not in apoios_visuais or tipo == "xy":
            apoios_visuais[chave] = (no, tipo)
    for no, tipo in apoios_visuais.values():
        if tipo == 'xy':
            malha_apoio = criar_malha_apoio_xy(coordenadas[no], escala)
            plotter.add_mesh(malha_apoio, color = "dimgray", show_edges = True, edge_color = "black", line_width = 2)
        elif tipo in ('x', 'y'):
            triangulo, roletes = criar_malha_apoio_primeiro_genero(no, tipo, coordenadas, conectividade, escala)
            plotter.add_mesh(triangulo, color = "dimgray", show_edges = True, edge_color = "black", line_width = 2)
            triangulos_animados.append((no, triangulo, triangulo.points.copy()))
            for rolete in roletes:
                plotter.add_mesh(rolete, color = "black")
                roletes_animados.append((no, rolete, rolete.points.copy()))
    for no, seta, pontos_iniciais in setas_animadas:
        plotter.add_mesh(seta, color = "black")
    deslocamentos_por_no = deslocamentos.reshape(-1, 2)
    magnitudes = np.linalg.norm(deslocamentos_por_no, axis = 1)
    deslocamento_maximo = magnitudes.max()
    texto_legenda = (
        "TRELIÇA 2D\n\n"
        f"Deformação amplificada: {mag}x\n"
        "Cinza: estrutura original\n"
        "Vermelho: estrutura deformada\n"
        "Preto: cargas aplicadas")
    texto_info = (
        f"Nós: {len(coordenadas)}   Barras: {len(conectividade)}\n"
        f"Deslocamento máximo: {deslocamento_maximo:.3e} m")
    plotter.add_text(texto_legenda, position = "upper_left", font_size = 12, color = "black", shadow = True)
    plotter.add_text(texto_info, position = "lower_left", font_size = 12, color = "black", shadow = True)
    plotter.view_xy()
    plotter.enable_parallel_projection()
    plotter.open_gif(nome_gif, fps = 20)
    n_quadros = 60
    fatores = np.linspace(0.0, 1.0, n_quadros)
    for t in fatores:
        pontos_quadro = (1-t)*pontos_originais_3d + t*pontos_deformados_3d
        malha_deformada.points = pontos_quadro
        for no, rolete, pontos_iniciais in roletes_animados:
            deslocamento_no = pontos_quadro[no] - pontos_originais_3d[no]
            rolete.points = pontos_iniciais + deslocamento_no
        for no, triangulo, pontos_iniciais in triangulos_animados:
            deslocamento_no = pontos_quadro[no] - pontos_originais_3d[no]
            triangulo.points = pontos_iniciais + deslocamento_no
        for no, seta, pontos_iniciais in setas_animadas:
            deslocamento_no = pontos_quadro[no] - pontos_originais_3d[no]
            seta.points = pontos_iniciais + deslocamento_no
        plotter.write_frame()
    
    plotter.close()
