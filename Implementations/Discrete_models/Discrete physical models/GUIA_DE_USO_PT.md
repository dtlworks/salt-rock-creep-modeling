# Guia de uso — modelos discretos 1D e treliças 2D

Este guia resume como executar os modelos, editar as entradas e localizar os resultados. Os comandos abaixo partem da raiz do repositório. Cada projeto executável tem seu próprio `.venv` e `requirements.txt`; crie e ative o ambiente na pasta do projeto antes de instalar as dependências.

## Requisitos

- Python 3.
- O projeto 1D requer `numpy`.
- O projeto 2D requer `numpy` e `pyvista` para gerar animações GIF.

Preparação do ambiente 1D:

```bash
cd "Implementations/Discrete_models/Discrete physical models/1D"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Para preparar o ambiente 2D:

```bash
cd "Implementations/Discrete_models/Discrete physical models/2D/truss_case"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Projeto 1D

### Execução

```bash
cd "Implementations/Discrete_models/Discrete physical models/1D"
python main.py
```

Por padrão, `main.py` executa o problema mecânico definido em `entrada_mec.txt` e escreve `resultados_mec.txt` na pasta `1D`.

O mesmo programa contém um fluxo hidráulico baseado no mesmo solver. Para executá-lo, edite `main.py`: comente a chamada `resolver_problema_mecanico()` e descomente `resolver_problema_hidraulico()`. O fluxo hidráulico lê `entrada_hid.txt` e grava `resultados_hid.txt`.

### Formato da entrada

Os arquivos de entrada são texto simples; linhas iniciadas por `#` e comentários após `#` são ignorados. Os índices dos nós começam em zero.

- `NOS n`: número total de nós (e graus de liberdade no modelo 1D).
- `ELEMENTOS n`: introduz as linhas dos elementos. Cada linha tem `no_i no_j rigidez` — no caso mecânico — ou `no_i no_j fator_de_carga` — no caso hidráulico. A contagem escrita no cabeçalho é informativa; a leitura prossegue pelas linhas até o próximo bloco.
- `FORCAS n`: introduz pares `no valor`. No modelo hidráulico, os valores representam vazões nodais.
- `PRESCRITOS n`: introduz pares `no valor` de deslocamento ou pressão prescritos.
- `ALPHA valor`: parâmetro inteiro que define o sinal usado no cálculo das forças/vazões de elemento.

Nós sem força/vazão listada recebem zero. Use propriedades positivas e entradas coerentes: cada elemento deve conectar dois nós válidos e as restrições devem remover os movimentos rígidos para que o sistema possa ser resolvido.

### O que é calculado

O solver monta a matriz de rigidez global, aplica os valores prescritos e resolve os graus de liberdade livres. Para mecânica, informa deslocamentos, forças nodais (incluindo reações nos nós prescritos) e força axial por elemento. Para hidráulica, os termos correspondem a pressão, vazão nodal e vazão de elemento. No cálculo mecânico, com `ALPHA 1` e conectividade orientada da esquerda para a direita, força de elemento positiva indica tração e negativa indica compressão.

## Projeto 2D (`2D/truss_case`)

### Execução

Entre na pasta do solver antes de executar. Os exemplos incluídos são:

```bash
cd "Implementations/Discrete_models/Discrete physical models/2D/truss_case"
python main.py exemplo1.txt 20000
python main.py exemplo2.txt 10000
python main.py exemplo3.txt 700
python main.py exemplo4.txt 40
```

O primeiro argumento é o caminho do arquivo de entrada. O segundo, opcional, é a amplificação visual dos deslocamentos; se omitido, vale `1000`. É possível informar um caminho relativo ou absoluto para a entrada. Cada execução grava `saidas/<nome-da-entrada>.output` e `saidas/<nome-da-entrada>.gif`; a pasta `saidas` é criada automaticamente. O arquivo `.output` contém os resultados numéricos e o GIF anima a transição entre a estrutura original (cinza) e deformada (vermelha), com cargas em preto. A amplificação afeta apenas a visualização, não os resultados numéricos.

Escalas já usadas nas notas do projeto: exemplo 1 = `20000`, exemplo 2 = `10000`, exemplo 3 = `700`, exemplo 4 = `40`.

### Formato da entrada

Arquivos `.txt` com índices de nó começando em zero e comentários com `#`:

```text
NOS quantidade
COORDENADAS
no x y
BARRAS
no_i no_j E area
CARGAS
no Fx Fy
RESTRICOES
no ux uy
```

- `COORDENADAS`: posição `(x, y)` de cada nó.
- `BARRAS`: conectividade, módulo de elasticidade `E` e área da seção. A ordem das linhas define os índices das barras nos resultados.
- `CARGAS`: componentes `Fx` e `Fy`; componentes não listadas permanecem zero.
- `RESTRICOES`: deslocamentos prescritos em `x` e `y`; use `L` para deixar o grau de liberdade livre ou um número para prescrever o deslocamento (em geral `0.0` para apoio fixo).
- Unidades esperadas no padrão SI: coordenadas em m, `E` em Pa, área em m², cargas em N e deslocamentos em m.

Cada nó tem dois graus de liberdade: `ux` e `uy`. O resultado lista força normal, tensão e deformação axial por barra; por nó, lista deslocamentos e forças nodais/reação. Valores positivos de força/deformação axial indicam alongamento (tração); negativos indicam encurtamento (compressão).

### Exemplos incluídos

- `exemplo1.txt`: treliça pequena para embasamento.
- `exemplo2.txt`: treliça plana de 12 nós.
- `exemplo3.txt`: modelo didático inspirado na Ponte de Ferro sobre o Rio das Antas, com hipóteses simplificadoras registradas no próprio arquivo.
- `exemplo4.txt`: modelo Warren grande, usado também como teste de processamento e visualização.

O exemplo 3 não representa o projeto estrutural real da ponte e não deve ser usado para avaliar sua segurança. O exemplo 4 também é explicitamente didático, não sendo um projeto estrutural. Em geral, os scripts são ferramentas de análise linear de barras idealizadas: não verificam flambagem, flexão, efeitos dinâmicos ou atendimento a normas.

## Arquivos principais

| Local | Função |
|---|---|
| `1D/main.py` | Seleciona e executa o caso mecânico ou hidráulico. |
| `1D/read.py`, `1D/calc.py` | Leitura das entradas e montagem/solução do sistema 1D. |
| `1D/resul_mec.py`, `1D/resul_hid.py` | Escrita dos resultados 1D. |
| `2D/truss_case/main.py` | Interface de linha de comando e fluxo do caso 2D. |
| `2D/truss_case/read.py`, `calc.py` | Leitura, montagem da rigidez e cálculo da resposta da treliça. |
| `2D/truss_case/resul.py`, `visualizacao.py` | Saída numérica e animação GIF. |
| `2D/truss_case/saidas/` | Destino das saídas 2D; criada automaticamente quando necessário. |
