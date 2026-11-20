def escrever_resultados_mec(nome_arquivo, deslocamentos, forcas_nodais, forcas_elementos):
    """
    Escreve em arquivo texto os resultados do modelo mecânico
    """
    with open(nome_arquivo, "w", encoding = 'utf-8') as arquivo:
        arquivo.write("RESULTADOS DO MODELO MECÂNICO\n")
        arquivo.write("\n\n")
        arquivo.write("ELEMENTOS\n")
        arquivo.write(f"{'Elemento':<12}{'Forca (kN)':>15}\n")
        for elemento, forca in enumerate(forcas_elementos):
            arquivo.write(f"{elemento:<12}{forca:>15.6f}\n")
        arquivo.write("\n\n")
        arquivo.write("NOS\n")
        arquivo.write(f"{'No':<12}{'Deslocamento (m)':>15}{'Forca nodal (kN)':>18}\n")
        for no, (deslocamento, forca_nodal) in enumerate(zip(deslocamentos, forcas_nodais)):
            arquivo.write(f"{no:<12}{deslocamento:>15.6f}{forca_nodal:>18.6f}\n")
