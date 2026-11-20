# Usage guide — 1D discrete models and 2D trusses

This guide summarizes how to run the models, edit their input files, and find their outputs. The commands below start at the repository root. Each runnable project has its own `.venv` and `requirements.txt`; create and activate the environment in that project's directory before installing dependencies.

## Requirements

- Python 3.
- The 1D project requires `numpy`.
- The 2D project requires `numpy` and `pyvista` to generate animated GIFs.

Set up the 1D environment:

```bash
cd "Implementations/Discrete_models/Discrete physical models/1D"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set up the 2D environment instead:

```bash
cd "Implementations/Discrete_models/Discrete physical models/2D/truss_case"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 1D project

### Run

```bash
cd "Implementations/Discrete_models/Discrete physical models/1D"
python main.py
```

By default, `main.py` runs the mechanical problem in `entrada_mec.txt` and writes `resultados_mec.txt` in the `1D` directory.

The same program has a hydraulic flow that reuses the solver. To run it, edit `main.py`: comment out the `resolver_problema_mecanico()` call and uncomment `resolver_problema_hidraulico()`. The hydraulic flow reads `entrada_hid.txt` and writes `resultados_hid.txt`.

### Input format

Inputs are plain text; full-line comments and trailing comments after `#` are ignored. Node indices are zero-based.

- `NOS n`: total number of nodes (and degrees of freedom in this 1D model).
- `ELEMENTOS n`: introduces element rows. Each row contains `node_i node_j stiffness` for mechanics, or `node_i node_j load_factor` for hydraulics. The count in the header is informational; the parser reads rows until the next block.
- `FORCAS n`: introduces `node value` pairs. In the hydraulic model, values are nodal flow rates.
- `PRESCRITOS n`: introduces `node value` pairs for prescribed displacement or pressure.
- `ALPHA value`: integer parameter controlling the sign used to calculate element force/flow.

Nodes without a listed force/flow receive zero. Keep properties valid and inputs consistent: each element must connect valid node indices, and constraints must remove rigid body motions so the system can be solved.

### Calculations

The solver assembles the global stiffness matrix, applies prescribed values, and solves for free degrees of freedom. Mechanics reports displacements, nodal forces (including reactions at prescribed nodes), and axial force per element. Hydraulics uses the corresponding terms pressure, nodal flow, and element flow. In the mechanical calculation, with `ALPHA 1` and connectivity oriented left to right, positive element force means tension and negative means compression.

## 2D project (`2D/truss_case`)

### Run

Change to the solver directory before running. The included examples are:

```bash
cd "Implementations/Discrete_models/Discrete physical models/2D/truss_case"
python main.py exemplo1.txt 20000
python main.py exemplo2.txt 10000
python main.py exemplo3.txt 700
python main.py exemplo4.txt 40
```

The first argument is the input file path. The optional second argument is the visual displacement amplification; it defaults to `1000`. You may pass a relative or absolute input path. Each run writes `saidas/<input-name>.output` and `saidas/<input-name>.gif`; the `saidas` directory is created automatically. The `.output` file contains numerical results. The GIF animates the transition from the original structure (gray) to the deformed structure (red), with loads in black. Amplification changes the visualization only, not the numerical results.

Scales already used in the project notes: example 1 = `20000`, example 2 = `10000`, example 3 = `700`, example 4 = `40`.

### Input format

`.txt` files use zero-based node indices and `#` comments:

```text
NOS count
COORDENADAS
node x y
BARRAS
node_i node_j E area
CARGAS
node Fx Fy
RESTRICOES
node ux uy
```

- `COORDENADAS`: each node's `(x, y)` position.
- `BARRAS`: connectivity, Young's modulus `E`, and cross-sectional area. Row order defines the bar indices in the results.
- `CARGAS`: `Fx` and `Fy` components; unlisted components remain zero.
- `RESTRICOES`: prescribed `x` and `y` displacements; use `L` for a free degree of freedom or a number to prescribe displacement (usually `0.0` for a fixed support).
- Expected SI units: coordinates in m, `E` in Pa, area in m², loads in N, and displacements in m.

Each node has two degrees of freedom: `ux` and `uy`. Results list normal force, stress, and axial strain for each bar; for each node they list displacements and nodal forces/reactions. Positive axial force/strain means elongation (tension); negative means shortening (compression).

### Included examples

- `exemplo1.txt`: small introductory truss.
- `exemplo2.txt`: 12-node planar truss.
- `exemplo3.txt`: didactic model inspired by the Iron Bridge over the Antas River, with simplifying assumptions documented in the input file.
- `exemplo4.txt`: large Warren truss, also used as a processing and visualization stress test.

Example 3 does not represent the bridge's actual structural design and must not be used to assess its safety. Example 4 is also explicitly didactic, not a structural design. More generally, these scripts analyze idealized bars with a linear model; they do not check buckling, bending, dynamic effects, or code compliance.

## Main files

| Location | Purpose |
|---|---|
| `1D/main.py` | Selects and runs the mechanical or hydraulic case. |
| `1D/read.py`, `1D/calc.py` | Read inputs and assemble/solve the 1D system. |
| `1D/resul_mec.py`, `1D/resul_hid.py` | Write 1D results. |
| `2D/truss_case/main.py` | 2D command-line interface and case workflow. |
| `2D/truss_case/read.py`, `calc.py` | Read inputs, assemble stiffness, and calculate truss response. |
| `2D/truss_case/resul.py`, `visualizacao.py` | Write numerical output and GIF animation. |
| `2D/truss_case/saidas/` | Destination for 2D outputs; created automatically when needed. |
