# Poetry

**Poetry** es una herramienta unificada para gestionar dependencias, entornos virtuales y publicación de paquetes en Python. Este documento resume su comparación con pip, con base en el tutorial de DataCamp (que solo contrasta Poetry con pip).

## Poetry vs pip

| Aspecto | **Poetry** | **pip** |
|---|---|---|
| Rol | Herramienta completa de dependencias y proyectos | Instalador de paquetes |
| Resolución de dependencias | Avanzada: detecta conflictos antes de instalar | Lineal y simple; puede generar conflictos |
| Entornos virtuales | Los crea y gestiona automáticamente por proyecto | Requiere virtualenv o venv y activación manual |
| Configuración del proyecto | Un solo archivo pyproject.toml | requirements.txt para dependencias y setup.py para metadatos |
| Archivo de bloqueo (lock) | Sí (poetry.lock) | No incluido |
| Publicación de paquetes | Integrada (poetry build y poetry publish) | Requiere herramientas extra (twine, setuptools) |

## Equivalencia de comandos (pip y Poetry)

| Tarea | pip | Poetry |
|---|---|---|
| Crear proyecto | (manual) | `poetry new nombre` o `poetry init` |
| Instalar un paquete | `pip install paquete` | `poetry add paquete` |
| Instalar todo lo del proyecto | `pip install -r requirements.txt` | `poetry install` |
| Desinstalar | `pip uninstall paquete` | `poetry remove paquete` |
| Ejecutar un script | `python script.py` (con entorno activo) | `poetry run python script.py` |
| Abrir el entorno | `source .venv/bin/activate` | `poetry shell` |
| Listar entornos | (manual) | `poetry env list` |
| Cambiar versión de Python | (recrear el entorno) | `poetry env use python3.11` |
| Exportar dependencias | `pip freeze > requirements.txt` | `poetry export -f requirements.txt --output requirements.txt` |
| Actualizar dependencias | `pip install -U paquete` | `poetry update` |

## Sintaxis de versiones de dependencias

| Símbolo | Significado | Ejemplo |
|---|---|---|
| `^` | Permite actualizaciones menores y de parche, no mayores | ^1.2.3 → de 1.2.3 a 1.9.9, no 2.0.0 |
| `~` | Solo actualizaciones de parche | ~1.2.3 → de 1.2.3 a 1.2.9, no 1.3.0 |
| Versión exacta | Solo esa versión | 1.2.3 |
| `>`, `<`, `>=`, `<=` | Límites de comparación | >=1.2.3 |
| Rango | Combina restricciones con coma | >=1.2.3,<2.0.0 |
| `*` | Cualquier versión que coincida | 1.2.* |

## Grupos de dependencias

| Necesidad | Comando |
|---|---|
| Añadir a un grupo | `poetry add --group dev black mypy` |
| Instalar sin ciertos grupos | `poetry install --without ui,dev` |
| Incluir un grupo opcional | `poetry install --with docs` |
| Instalar solo un grupo | `poetry install --only ui` |
| Solo dependencias de ejecución | `poetry install --only main` |
| Quitar de un grupo | `poetry remove streamlit --group ui` |


## Configuración útil

| Objetivo | Comando |
|---|---|
| Ver toda la configuración | `poetry config --list` |
| Crear `.venv` dentro del proyecto | `poetry config virtualenvs.in-project true` |
| Cambiar la ruta de los entornos | `poetry config virtualenvs.path ruta/nueva` |
| Ajustar núcleos de instalación | `poetry config installer.max-workers 10` |

Por defecto, Poetry guarda los entornos en su directorio de caché, no en el proyecto.

## Cuándo usar cada una (según el tutorial)

| **Poetry** |  **pip** |
|---|---|
| Necesidad de trabajar en equipo y necesitas entornos reproducibles | Escribir scripts simples con pocas dependencias |
|  Publicar en PyPI | Aprendiendo Python |
| El árbol de dependencias es complejo y puede haber conflictos | Solo se necesita instalar un paquete rápido |
| Gestión automática de entornos virtuales | No se puede instalar Poetry en el entorno |
| Centralizar en una sola herramienta para todo el flujo | Se mantiene en proyectos antiguos ya configurados con pip |


## poetry add frente a poetry install

- `poetry add`: se usa para agregar dependencias nuevas (actualiza `pyproject.toml` y `poetry.lock`).
- `poetry install`: úsalo para preparar un proyecto existente a partir del lock file.
- Haz commit de `pyproject.toml` y `poetry.lock` al control de versiones.

## Buenas prácticas destacadas

- Incluir `poetry.lock` en el repositorio para aplicaciones; para librerías, el tutorial recomienda excluirlo.
- Usar `poetry run` para garantizar que los scripts corren en el entorno correcto.
- Mantener las dependencias de desarrollo separadas con `--group dev`.
- Validar con `poetry check` antes de cada commit.
- Probar la publicación en TestPyPI antes de subir a PyPI.
- Usar `poetry version patch/minor/major` para versionado semántico.
- Generar `requirements.txt` con `poetry export` cuando otras herramientas lo necesiten.

## Fuente

- [Python Poetry: Modern And Efficient Python Environment And Dependency Management – DataCamp](https://www.datacamp.com/tutorial/python-poetry)
