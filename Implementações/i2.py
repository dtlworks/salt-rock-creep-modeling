import math
import pyvista as pv

folga_plano_apoio = 0.0001
conversao_n_p_mpa = 1_000_000
conversao_gpa_p_pa = 1_000_000_000
amplificador_visual = 500

def calcular_secao_transversal(d: float) -> float:
    """
    Recebe o diâmetro (d em metros) do elemento estrutural.
    Calcula e retorna a área da seção transversal do mesmo.
    """
    return math.pi*(d/2)**2


def calcular_forca_normal(cargas: list) -> float:
    """
    Recebe um array fatiado com todas as cargas que influem no elemento. 
    A partir do correto fatiamento do array, cálcula e retorna a força/carga normal axial 
    "resultante" (f) no elemento em questão. Note que no problema em questão, a força
    normal no elemento i é dada pelo somatório de cargas até Pi, isto é, 
    f1 = p1; f2 = p1 + p2; ...; fn = p1 + p2 + ... + pn.
    """
    return sum(cargas)


def calcular_tensao_media_elemento(d: float, cargas: list) -> float:
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


def ler_float(mensagem: str) -> float:
    """
    Função destinada a tratamento de erro na leitura exclusiva de pontos flutuantes.
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("ERRO: Forneça um valor válido.")


def ler_int(mensagem: str) -> int:
    """
    Função destinada a tratamento de erro na leitura exclusiva de números inteiros.
    """
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("ERRO: Forneça um valor válido.")


def ler_dadof_mq_0(mensagem: str) -> float:
    """
    Função destinada a filtragem de dado de input, isto é, leitura exclusiva de pontos flutuantes maiores que zero.
    """
    while True:
        n = ler_float(mensagem)
        if n <= 0:
            print('ERRO: Informe um valor válido.')
            continue
        return n


def ler_dadoi_mq_0(mensagem: str) -> int:
    """
    Função destinada a filtragem de dado de input, isto é, leitura exclusiva de números inteiros maiores que zero.
    """
    while True:
        n = ler_int(mensagem)
        if n <= 0:
            print('ERRO: Informe um valor válido.')
            continue
        return n


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
Tensão: {cilindro['tensao']/conversao_n_p_mpa:.2f} MPa      
Deformação Ab.: {deformacoes[i-1]*1000:.4f} mm            
Módulo de elasticidade: {elasticidades[i-1]/conversao_gpa_p_pa} GPa              
Estado: {caracterizar_tensao_media(cilindro['tensao'])}
Amplificador visual: {amplificador_visual}x\n
"""
    return resultados


def visualizar_estrutura(cilindros: list, tensoes: list, diametros: list, deformacoes: list, elasticidades: list) -> None:
    """
    Função destinada a geração, integração estabelecimento de malhas, de forma espacial, coerentes com a 
    lógica do problema mecânico estabelecido. Os parâmetros são utilizados para integralização de dados, 
    acertificando sua posterior visualização e análise.
    """
    plotter = pv.Plotter()
    tensao_min = min(tensoes)/conversao_n_p_mpa
    tensao_max = max(tensoes)/conversao_n_p_mpa
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
            comprimento = cilindro['comprimento'] + (cilindro['deformacao'] * ativo * amplificador_visual)
            elemento_estrutural = pv.Cylinder(
                radius = cilindro['diametro']/2,
                height = comprimento,
                center = (0, y_acumulado + comprimento/2, 0),
                direction = (0, 1, 0)
            )
            y_acumulado += comprimento
            elemento_estrutural.cell_data['tensao'] = [cilindro['tensao']/conversao_n_p_mpa] * elemento_estrutural.n_cells
            plotter.add_mesh(
                elemento_estrutural, show_edges = True, scalars = 'tensao', cmap = 'coolwarm',
                clim = [tensao_min, tensao_max], scalar_bar_args = {'fmt': '%.2f MPa', 'title': 'Tensão Média\n'},
                name = f'cilindro_{indice}'
            )

        cord_y_max = y_acumulado + folga_plano_apoio
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
        fmt = '%.0f',
        title_height = 0.035
    )
    plotter.add_text(gerar_resultados_txt(cilindros, deformacoes, elasticidades), font_size = 12, 
                     position = 'upper_left', color = 'black', shadow = True)
    plotter.show()


def main() -> None:
    n = ler_dadoi_mq_0('Informe o número de elementos que compõem a estrutura: ')
       
    elementos = list()
    cargas = list()
    comprimentos = list()
    diametros = list()
    tensoes = list()
    elasticidades = list()
    deformacoes = list()

    for i in range(n):
        while True:
            diametro = ler_dadof_mq_0(f'Forneça o diâmetro (em Metros) do elemento {i+1}: ')
            if i > 0 and diametro <= diametros[i-1]:
                print('ERRO: Para o problema em questão, queremos diâmetros que crescem conforme o número de elementos.')
                continue
            break
        carga = ler_float(f'Forneça a carga (em Newtons) aplicada na extremidade do elemento {i+1}: ')
        comprimento = ler_dadof_mq_0(f'Forneça o comprimento (em Metros) do elemento {i+1}: ')
        elasticidade = ler_dadof_mq_0(f'Forneça o módulo de elasticidade (em GPa) do elemento {i+1}: ')*conversao_gpa_p_pa
        diametros.append(diametro)
        cargas.append(carga)
        comprimentos.append(comprimento)
        elasticidades.append(elasticidade)

    for j in range(n):
        tensao = calcular_tensao_media_elemento(diametros[j], cargas[:j+1])
        deformacao_absoluta = calcular_deformacao_absoluta(tensao, elasticidades[j], comprimentos[j])
        tensoes.append(tensao)
        deformacoes.append(deformacao_absoluta)

    for k in range(n):
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
