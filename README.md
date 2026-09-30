# Taller 2 – Ambientes virtuales de Python

**Machine Learning Engineering (CC3105)**, Universidad del Valle de Guatemala

Taller para aprender a usar ambientes virtuales con `venv` y con Conda, definir archivos de requisitos para proyectos de Machine Learning e incluir esos requisitos en el paquete del pipeline de scikit-learn.

## Estructura

```
taller2/
├── requirements.txt              # Requisitos del ambiente de ML (venv + pip)
├── requirements-pipeline.txt     # Requisitos mínimos del pipeline de scikit-learn
├── environment.yml               # Definición del ambiente de Conda
├── transactions-pipeline/        # Paquete del pipeline (reto 3a)
│   ├── pyproject.toml            # Lee sus dependencias de requirements.txt
│   ├── MANIFEST.in               # Incluye requirements.txt en el sdist
│   ├── requirements.txt
│   └── src/transactions_pipeline/
└── img/                          # Capturas de pantalla
```

---

## 1. Documentación de Python sobre ambientes virtuales

| Fuente | Sección |
|---|---|
| Python docs | [`venv` — Creation of virtual environments](https://docs.python.org/3/library/venv.html) |
| Python tutorial | [12. Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) |
| Python Packaging User Guide | [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) |
| VS Code | [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments) |

Un ambiente virtual es un directorio con su propio intérprete de Python y su propia carpeta `site-packages`. Así cada proyecto tiene dependencias aisladas del Python del sistema y de los demás proyectos.

Comandos principales en Windows / PowerShell:

```powershell
python -m venv .venv                 # crear
.\.venv\Scripts\Activate.ps1         # activar (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt      # instalar requisitos
pip freeze > requirements.txt        # congelar versiones instaladas
deactivate                           # salir del ambiente
```

En VS Code se puede hacer lo mismo con **Ctrl+Shift+P → Python: Create Environment → Venv**. VS Code detecta el `requirements.txt` y ofrece instalarlo.

## 2. Ambiente virtual con `venv` y archivo de requisitos

Por convención, el archivo de requisitos de pip se llama **`requirements.txt`**. Tiene un paquete por línea, normalmente con la versión fijada (`paquete==versión`), y se instala con `pip install -r requirements.txt`. También existen variantes como `requirements-dev.txt` o `requirements-pipeline.txt` para separar grupos de dependencias.

[`taller2/requirements.txt`](taller2/requirements.txt) contiene un ambiente típico de ML: `numpy`, `pandas`, `scipy`, `scikit-learn`, `matplotlib`, `joblib` y `jupyter`/`jupyterlab` con sus dependencias. Se generó con `pip freeze`.

![Ambiente venv creado y activado](taller2/img/01-venv.png)

La captura muestra la creación de un ambiente con `python -m venv` y la activación de `.venv`. El prompt cambia a `(.venv)` y `sys.prefix` apunta a la carpeta del ambiente. También se ven los paquetes de ML instalados desde `requirements.txt`.

## 3. Requisitos del pipeline de scikit-learn

[`taller2/requirements-pipeline.txt`](taller2/requirements-pipeline.txt) solo contiene lo que necesita el pipeline (`extract → clean → train`) para ejecutarse:

```
joblib==1.6.0
numpy==2.2.6
pandas==2.3.3
scikit-learn==1.7.2
scipy==1.15.3
```

### Reto 3a: incluir los requisitos en el paquete

El paquete `transactions-pipeline` de ejercicios anteriores se copió a [`taller2/transactions-pipeline/`](taller2/transactions-pipeline/). Se modificó para que **`requirements.txt` sea la única fuente de las dependencias**:

1. **`pyproject.toml`**: en lugar de listar `dependencies = [...]` a mano, se declaran como dinámicas y setuptools las lee del archivo:

   ```toml
   [project]
   dynamic = ["dependencies"]

   [tool.setuptools.dynamic]
   dependencies = { file = ["requirements.txt"] }
   ```

   Esto requiere `setuptools>=62.6` en `[build-system]`.

2. **`MANIFEST.in`**: `include requirements.txt`. Es la configuración adicional necesaria al empaquetar. Sin ella, el `requirements.txt` no entra en el *source distribution* (`.tar.gz`), y al instalar desde el sdist setuptools no encuentra el archivo y falla.

Resultado: `python -m build` genera un sdist que contiene `requirements.txt`, y `pip show` muestra que las dependencias del paquete son exactamente las del archivo.

![Paquete con requirements.txt incluido](taller2/img/02-paquete.png)

> Nota: fijar versiones exactas (`==`) en las dependencias de una librería puede causar conflictos con otros paquetes. Para un paquete publicado es más común usar rangos (`>=`) y dejar el `requirements.txt` con versiones exactas para reproducir el ambiente de entrenamiento.

## 4. Ambientes con Anaconda / Conda

| Fuente | Sección |
|---|---|
| Conda docs | [Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) |
| Conda docs | [Creating an environment from an environment.yml file](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) |
| Conda docs | [Sharing an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#sharing-an-environment) |

```powershell
conda create -n taller2-ml python=3.11 scikit-learn pandas   # crear desde la línea de comandos
conda env create -f environment.yml                          # crear desde archivo
conda activate taller2-ml
conda env list
conda env export --from-history > environment.yml            # exportar
conda env remove -n taller2-ml
```

![Creación del ambiente con conda env create](taller2/img/03-conda-create.png)

![Ambiente de Conda activado](taller2/img/04-conda-env.png)

### Reto 4a: archivo de requisitos para Conda

Sí se puede definir. El equivalente de `requirements.txt` en Conda es **`environment.yml`** ([`taller2/environment.yml`](taller2/environment.yml)):

```yaml
name: taller2-ml
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy=2.2.6
  - pandas=2.3.3
  - scipy=1.15.3
  - scikit-learn=1.7.2
  - joblib
  - matplotlib
  - jupyterlab
  - ipykernel
  - pip
  - pip:
      - -e ./transactions-pipeline
```

Diferencias con el `requirements.txt` de pip:

| | `requirements.txt` (pip) | `environment.yml` (conda) |
|---|---|---|
| Formato | Texto plano, un paquete por línea | YAML |
| Versión de Python | No la define; usa la del intérprete | Se declara (`python=3.11`) y Conda la instala |
| Sintaxis de versión | `paquete==1.2.3` | `paquete=1.2.3` (un solo `=`) |
| Origen de paquetes | PyPI | Canales (`conda-forge`, `defaults`) y PyPI en la sección `pip:` |
| Dependencias no Python | No (solo paquetes de Python) | Sí (CUDA, MKL, compiladores, librerías de C) |
| Nombre del ambiente | No aplica | `name:` |

Otras variantes que acepta Conda:
- `conda list --export > spec.txt` y luego `conda create -n env --file spec.txt`: un archivo de texto con formato `paquete=versión=build`.
- `conda list --explicit > spec-file.txt`: URLs exactas de cada paquete, para reproducir el ambiente en la misma plataforma.
- `conda env export --from-history`: exporta solo los paquetes que se pidieron explícitamente, lo que lo hace más portable entre sistemas operativos.

En este caso el `environment.yml` combina las dos cosas: Conda instala el stack científico con las mismas versiones del pipeline, y la sección `pip:` instala el paquete local en modo editable. Ese paquete trae sus dependencias desde su `requirements.txt`, que ya quedan satisfechas por lo que instaló Conda.

---

## Conclusiones

- **Reproducibilidad de experimentos.** Un modelo entrenado con `scikit-learn 1.7.2` puede no cargar, o dar resultados distintos, con otra versión (por ejemplo, un `model.joblib` serializado). Fijar versiones en `requirements.txt` o `environment.yml` permite que cualquier persona, o un servidor de CI, reconstruya exactamente el ambiente con que se entrenó el modelo.
- **Aislamiento entre proyectos.** Cada proyecto de ML puede necesitar versiones incompatibles (TensorFlow con cierta versión de NumPy, otro proyecto con PyTorch y CUDA). Con ambientes separados no se rompen entre sí ni se toca el Python del sistema.
- **Separar ambientes por etapa del ciclo de vida.** Conviene tener un ambiente "pesado" para exploración (Jupyter, matplotlib) y uno mínimo para producción o inferencia (`requirements-pipeline.txt`). Así las imágenes de Docker son más pequeñas y hay menos superficie de fallos y vulnerabilidades.
- **Una sola fuente de verdad para dependencias.** Al hacer que el paquete lea su `requirements.txt` (reto 3a), las dependencias del pipeline no se duplican entre el archivo y el `pyproject.toml`, y no pueden desincronizarse.
- **Conda vs venv.** `venv` + pip es liviano, viene con Python y basta para la mayoría de los proyectos. Conda conviene cuando hay dependencias fuera de Python (CUDA/cuDNN para GPU, MKL, GDAL) o cuando hace falta una versión específica de Python sin instalarla en el sistema. Se pueden combinar con la sección `pip:` del `environment.yml`.
- **Base para automatización.** Los mismos archivos de requisitos se usan en CI/CD, en Dockerfiles y en plataformas de entrenamiento en la nube. Definirlos bien desde el inicio facilita llevar el modelo a producción.

## Cómo reproducir

```powershell
cd taller2

# venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .\transactions-pipeline

# conda
conda env create -f environment.yml
conda activate taller2-ml
transactions-pipeline --help
```
