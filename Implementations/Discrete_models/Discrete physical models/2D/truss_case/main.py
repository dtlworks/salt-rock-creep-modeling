import sys
from pathlib import Path

from calc import *
from read import *
from resul import *
from visualizacao import *


def main(arquivo_entrada, arquivo_saida, mag):
    qntd_nos, coordenadas, conectividade, modulos_elasticidade, areas, forcas_aplicadas, gdl_prescritos, deslocamentos_prescritos = ler_dados_entrada(arquivo_entrada)
    K_global = montar_matriz_rigidez_global(qntd_nos, coordenadas, conectividade, modulos_elasticidade, areas)
    deslocamentos, forcas_globais = resolver_trelica(K_global, forcas_aplicadas, gdl_prescritos, deslocamentos_prescritos)
    forcas, tensoes, deformacoes = calcular_esforcos_barras(coordenadas, conectividade, modulos_elasticidade, areas, deslocamentos)
    escrever_resultados(arquivo_saida, forcas, tensoes, deformacoes, deslocamentos, forcas_globais)
    nome_gif = arquivo_saida.with_suffix(".gif")
    visualizar_trelica(coordenadas, conectividade, deslocamentos, gdl_prescritos, forcas_aplicadas, mag, nome_gif)

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Uso: python main.py caminho/arquivo.txt [magnitude]")
        print("Exemplo: python main.py exemplo3.txt 1000")
        print("Se magnitude for omitida, sera usado o valor 1000.")
    else:
        arquivo_entrada = Path(sys.argv[1])
        mag = float(sys.argv[2]) if len(sys.argv) == 3 else 1000.0
        diretorio_saidas = Path(__file__).resolve().parent / "saidas"
        diretorio_saidas.mkdir(exist_ok = True)
        arquivo_saida = diretorio_saidas / f"{arquivo_entrada.stem}.output"
        main(arquivo_entrada, arquivo_saida, mag)
