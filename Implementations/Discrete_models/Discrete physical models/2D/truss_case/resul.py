def escrever_resultados(nome_arquivo, forcas, tensoes, deformacoes, deslocamentos, forcas_globais):
    with open(nome_arquivo, "w", encoding = 'utf-8') as arquivo:
        arquivo.write("RESULTADOS DA TRELICA 2D\n")
        arquivo.write("\n\n")
        arquivo.write("BARRAS\n")
        arquivo.write(f"{'Barra':<8}{'Forca Normal (N)':>20}{'Tensao (Pa)':>16}{'Deformacao':>16}\n")
        for elemento, (forca, tensao, deformacao) in enumerate(zip(forcas, tensoes, deformacoes)):
            arquivo.write(f"{elemento:<8}{forca:>20.4e}{tensao:>16.4e}{deformacao:>16.4e}\n")
        arquivo.write("\n\n")
        arquivo.write("NOS\n")
        arquivo.write(f"{'No':<8}{'ux (m)':>20}{'uy (m)':>16}{'Fx nodal (N)':>16}{'Fy nodal (N)':>16}\n")
        for no in range(len(deslocamentos)//2):
            i, j = 2*no, 2*no+1
            arquivo.write(f"{no:<8}{deslocamentos[i]:>20.4e}{deslocamentos[j]:>16.4e}{forcas_globais[i]:>16.4e}{forcas_globais[j]:>16.4e}\n")
