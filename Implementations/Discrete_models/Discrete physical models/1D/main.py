from read import *
from calc import *
from resul_mec import *
from resul_hid import *


def resolver_problema_mecanico():
    qntd_nos, conectividade, rigidezes, forcas_aplicadas, prescritos, valores_prescritos, alpha = ler_dados_entrada("entrada_mec.txt")
    K = montar_rigidez(qntd_nos, conectividade, rigidezes)
    deslocamentos, forcas_nodais = resolver_sistema(K, forcas_aplicadas, prescritos, valores_prescritos)
    forcas_elementos = calcular_forcas_elementos(conectividade, rigidezes, deslocamentos, alpha)
    escrever_resultados_mec("resultados_mec.txt", deslocamentos, forcas_nodais, forcas_elementos)

def resolver_problema_hidraulico():
    qntd_nos, conectividade, fatores_carga, vazoes_aplicadas, nos_pressao_prescrita, pressoes_prescritas, alpha = ler_dados_entrada("entrada_hid.txt")
    K = montar_rigidez(qntd_nos, conectividade, fatores_carga)
    pressoes, vazoes_nodais = resolver_sistema(K, vazoes_aplicadas, nos_pressao_prescrita, pressoes_prescritas)
    vazoes_elementos = calcular_forcas_elementos(conectividade, fatores_carga, pressoes, alpha)
    escrever_resultados_hid("resultados_hid.txt", pressoes, vazoes_nodais, vazoes_elementos)


def main():

    resolver_problema_mecanico()
    # resolver_problema_hidraulico()


if __name__ == "__main__":
    main()
