# Salt Rock Creep Modeling

Portfólio de implementações computacionais desenvolvidas durante o PIBIC — *Modelagem mecânica discreta da fluência de rochas salinas aplicada a poços de petróleo: uma abordagem introdutória*.

**Orientador:** Prof. Dr. William Wagner Matos Lira

## Sobre

Este repositório documenta a evolução dos estudos em modelagem mecânica discreta aplicada à fluência de rochas salinas. Cada script `iN.py` em `Implementações/` representa um marco no aprendizado, partindo de versões primárias (soluções exploratórias, ainda com imperfeições) que amadurecem ao longo dos commits para versões mais robustas e completas.

Os tópicos percorridos incluem tensão axial, deformação, elasticidade 1D, viscoelasticidade (Maxwell, Kelvin-Voigt) e a aplicação desses conceitos à fluência de formações salinas em poços de petróleo.

## Implementações

- `i1.py` — Cálculo de tensão normal em cilindros coaxiais com visualização 3D (PyVista). Primeiro contato com a representação de estruturas e distribuição de tensões.
- `i2.py` — Cálculo de tensão normal e deformação elástica (lei de Hooke) em elementos estruturais, com slider interativo para alternar entre cenas pré e pós-deformação.

## Como usar

```bash
pip install -r requirements.txt
python Implementações/i1.py
```

## Licença

MIT &mdash; veja o arquivo [LICENSE](LICENSE).
