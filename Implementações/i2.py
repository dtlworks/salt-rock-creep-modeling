import math
import pyvista as pv
from pathlib import Path

DIRETORIO_BASE = Path(__file__).parent

FOLGA_PLANO_APOIO = 0.0001
CONVERSAO_N_P_MPA = 1_000_000
CONVERSAO_GPA_P_PA = 1_000_000_000
AMPLIFICADOR_VISUAL = 500


def ler_dados() -> tuple[list[float], list[float], list[float], list[float]]:
    """
    Lê o arquivo .txt referente ao script, guardando os dados nele presente de forma organizada.
    Ideia de automatizar mais o script, ao invés de inputs via console.
    """
    caminho_arquivo = DIRETORIO_BASE / 'i2.txt'
    try:
        with open(caminho_arquivo, 'r', encoding = 'utf-8') as arquivo:
            linhas_validas = [
                linha.strip() for linha in arquivo
                if linha.strip() and not linha.strip().startswith('#')
            ]
            diametros = linhas_validas[1:int(linhas_validas[0])+1:1].copy()
            cargas = linhas_validas[int(linhas_validas[0])+1:int(linhas_validas[0])*2+1:1].copy()
            comprimentos = linhas_validas[int(linhas_validas[0])*2+1:int(linhas_validas[0])*3+1:1].copy()
            elasticidades = linhas_validas[int(linhas_validas[0])*3+1::1].copy()
            diametros = [float(d) for d in diametros]
            cargas = [float(c) for c in cargas]
            comprimentos = [float(c) for c in comprimentos]
            elasticidades = [float(e)*CONVERSAO_GPA_P_PA for e in elasticidades]
            return diametros, cargas, comprimentos, elasticidades
    except FileNotFoundError:
        raise ValueError(f"Arquivo de dados não encontrado: {caminho_arquivo}")
    except (ValueError, IndexError) as erro:
        raise ValueError(
            "Arquivo de dados malformado ou com valores inválidos. "
            f"Detalhe: {erro}"
        ) from erro


def calcular_secao_transversal(d: float) -> float:
    """
    Recebe o diâmetro (d em metros) do elemento estrutural.
    Calcula e retorna a área da seção transversal do mesmo.
    """
    return math.pi*(d/2)**2


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
    return calcular_forca_normal(cargas)/calcular_secao_transversal(d)


def calcular_deformacao_absoluta(tensao: float, modulo_elasticidade: float, comprimento: float) -> float:
    """
    Recebe os valores de tensão (Pa) e módulo de elasticidade (Pa). Calcula e retorna a deformação absoluta delta (L-L_0)
    do elemento estrutural respectivo. 
    """
    return (tensao/modulo_elasticidade)*comprimento


def caracterizar_tensao_media(tensao: float) -> str:
    """
    Recebe o valor da tensão no elemento.
    Retorna o tipo de tensão no mesmo.
    """
    if tensao > 0:
        return "Tração"
    elif tensao < 0:
        return "Compressão"
    return "Sem tensão"


def gerar_resultados_txt(cilindros: list, deformacoes: list, elasticidades: list) -> str:
    """
    Monta o texto formatado com o resumo dos resultados (tensão, deformação,
    módulo de elasticidade e estado) de cada elemento da estrutura, para exibição
    na cena 3D.
    """
    resultados = "Resultados:\n"
    for i, cilindro in enumerate(cilindros, start = 1):
        resultados += f"""
Elemento {i}                                              
Tensão: {cilindro['tensao']/CONVERSAO_N_P_MPA:.2f} MPa      
Deformação Ab.: {deformacoes[i-1]*1000:.3f} mm            
Módulo de elasticidade: {elasticidades[i-1]/CONVERSAO_GPA_P_PA} GPa              
Estado: {caracterizar_tensao_media(cilindro['tensao'])}
Amplificador visual: {AMPLIFICADOR_VISUAL}x\n
"""
    return resultados


def visualizar_estrutura(cilindros: list, tensoes: list, diametros: list, deformacoes: list, elasticidades: list) -> None:
    """
    Função destinada a geração, integração estabelecimento de malhas, de forma espacial, coerentes com a 
    lógica do problema mecânico estabelecido. Os parâmetros são utilizados para integralização de dados, 
    acertificando sua posterior visualização e análise.
    """
    tensoes = [t/CONVERSAO_N_P_MPA for t in tensoes]
    plotter = pv.Plotter()
    tensao_min = min(tensoes)
    tensao_max = max(tensoes)
    if tensao_min == tensao_max:
        tensao_min -= 1e-3
        tensao_max += 1e-3
    diametro_max = max(diametros)
    cord_x_plano = diametro_max * 3.5
    cord_z_plano = diametro_max * 3.5

    def criar_estrutura(value: float) -> None:
        """
        Função utilizada como callback para o slider de deformação previsto.
        Recebe o parâmetro variável value, que vem a ser os valores dos intervalos 
        estabelecidos para o slider; 0 = pré-deformação e 1 = pós-deformação.
        Retorna as duas cenas construídas com embasamento em value. 
        """
        ativo = round(value)
        y_acumulado = 0
        for indice, cilindro in enumerate(cilindros):
            comprimento = cilindro['comprimento'] + (cilindro['deformacao'] * ativo * AMPLIFICADOR_VISUAL)
            elemento_estrutural = pv.Cylinder(
                radius = cilindro['diametro']/2,
                height = comprimento,
                center = (0, y_acumulado + comprimento/2, 0),
                direction = (0, 1, 0)
            )
            y_acumulado += comprimento
            elemento_estrutural.cell_data['tensao'] = [cilindro['tensao']/CONVERSAO_N_P_MPA] * elemento_estrutural.n_cells
            plotter.add_mesh(
                elemento_estrutural, show_edges = False, scalars = 'tensao', cmap = 'rainbow',
                clim = [tensao_min, tensao_max], scalar_bar_args = {'fmt': '%.2f MPa', 'title': 'Tensão Média\n'},
                name = f'cilindro_{indice}'
            )
        cord_y_max = y_acumulado + FOLGA_PLANO_APOIO
        superficie_apoio = pv.Plane(
            center = (0, cord_y_max, 0),
            direction = (0, 1, 0),
            i_size = cord_x_plano,
            j_size = cord_z_plano
        )
        plotter.add_mesh(superficie_apoio, color = 'gray', opacity = 1, name = 'superficie_apoio')
    plotter.add_slider_widget(
        criar_estrutura,
        [0, 1],
        value = 0,
        title = 'Pré (0) / Pós-deformação (1)',
        title_opacity = 1,
        title_color = 'black',
        fmt = '%.2f',
        title_height = 0.035
    )
    plotter.add_text(gerar_resultados_txt(cilindros, deformacoes, elasticidades), font_size = 12, 
                     position = 'upper_left', color = 'black', shadow = True)
    plotter.show()


def main() -> None:

    diametros, cargas, comprimentos, elasticidades = ler_dados()
    elementos = list()
    tensoes = list()
    deformacoes = list()
    
    for j in range(len(cargas)):
        tensao = calcular_tensao_media_elemento(diametros[j], cargas[:j+1])
        deformacao_absoluta = calcular_deformacao_absoluta(tensao, elasticidades[j], comprimentos[j])
        tensoes.append(tensao)
        deformacoes.append(deformacao_absoluta)

    for k in range(len(cargas)):
        elemento = {
            'elemento': k+1,
            'carga': cargas[k],
            'diametro': diametros[k],
            'comprimento': comprimentos[k],
            'tensao': tensoes[k],
            'deformacao': deformacoes[k],
        }
        elementos.append(elemento)
    visualizar_estrutura(elementos, tensoes, diametros, deformacoes, elasticidades)


if __name__ == '__main__':
    main()
