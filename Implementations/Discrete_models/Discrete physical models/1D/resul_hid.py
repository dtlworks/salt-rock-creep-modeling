def escrever_resultados_hid(nome_arquivo, pressoes, vazoes_nodais, vazoes_elementos):

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESULTADOS DO MODELO HIDRÁULICO\n")
        arquivo.write("\n\n")
        arquivo.write("ELEMENTOS\n")
        arquivo.write(f"{'Elemento':<12}{'Vazao (m³/s)':>18}\n")
        for elemento, vazao in enumerate(vazoes_elementos):
            arquivo.write(f"{elemento:<12}{vazao:>18.6f}\n")
        arquivo.write("\n\n")
        arquivo.write("NOS\n")
        arquivo.write(f"{'No':<12}{'Pressao (m)':>15}{'Vazao nodal (m³/s)':>22}\n")
        for no, (pressao, vazao_nodal) in enumerate(zip(pressoes, vazoes_nodais)):
            arquivo.write(f"{no:<12}{pressao:>15.6f}{vazao_nodal:>22.6f}\n")
