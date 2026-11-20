# Salt Rock Creep Modeling

Portfólio de implementações computacionais desenvolvidas durante o PIBIC — *Modelagem mecânica discreta da fluência de rochas salinas aplicada a poços de petróleo: uma abordagem introdutória*.

**Orientador:** Prof. Dr. William Wagner Matos Lira

## Projetos

- [`Implementations/Fundamentals of the mechanics of materials/`](Implementations/Fundamentals%20of%20the%20mechanics%20of%20materials/) — scripts `i1.py` e `i2.py`, com visualização 3D usando PyVista.
- [`Implementations/Discrete_models/Discrete physical models/1D/`](Implementations/Discrete_models/Discrete%20physical%20models/1D/) — modelos discretos mecânico e hidráulico.
- [`Implementations/Discrete_models/Discrete physical models/2D/truss_case/`](Implementations/Discrete_models/Discrete%20physical%20models/2D/truss_case/) — análise e animação de treliças planas.

Cada projeto tem seu próprio `requirements.txt` e ambiente virtual `.venv`. Os ambientes são locais e não são versionados.

## Executar os scripts de materiais

```bash
cd "Implementations/Fundamentals of the mechanics of materials"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python i1.py  # ou python i2.py
```

## Executar o modelo discreto 1D

```bash
cd "Implementations/Discrete_models/Discrete physical models/1D"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

O caso mecânico usa `entrada_mec.txt` por padrão. As instruções para selecionar o caso hidráulico estão no [guia de uso](Implementations/Discrete_models/Discrete%20physical%20models/GUIA_DE_USO_PT.md).

## Executar o modelo de treliças 2D

```bash
cd "Implementations/Discrete_models/Discrete physical models/2D/truss_case"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py exemplo1.txt 20000
```

Os resultados numéricos e a animação GIF são gravados em `saidas/`. Exemplos adicionais e o formato dos arquivos estão descritos nos guias em português e [inglês](Implementations/Discrete_models/Discrete%20physical%20models/USAGE_GUIDE_EN.md).

## Licença

MIT — veja o arquivo [LICENSE](LICENSE).
