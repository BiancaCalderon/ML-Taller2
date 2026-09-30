# UV

**UV** es un gestor de paquetes de Python escrito en Rust. Este documento lo compara con pip + virtualenv, Conda y Poetry, con base en el tutorial de DataCamp.

## uv vs  pip, Conda y Poetry

| Aspecto | **uv** | **pip** | **Conda** | **Poetry** |
|---|---|---|---|---|
| Lenguaje | Rust | Python | Python | Python |
| Velocidad | Entre 10 y 100 veces más rápido que pip | Referencia base | Más lento que pip | Más rápido que pip, pero por debajo de uv |
| Uso de memoria | Muy bajo | Mayor | Alto | Moderado |
| Entornos virtuales | Integrados | Requieren dos herramientas separadas | Integrados | Integrados |
| Resolución de dependencias | Rápida y moderna | Básica | Completa | Moderna |
| Archivo de bloqueo (lock) | Sí (uv.lock) | No (solo requirements.txt) | Sí | Sí |
| Estructura de proyecto | Sí (uv init) | No | No | Sí |
| Publicación en PyPI | Sí | Sí (con twine) | Sí | Sí |
| Gestión de versiones de Python | Sí (uv python install) | No (necesita pyenv) | Sí | No |
| Compatibilidad con el ecosistema pip | Total (lee requirements.txt) | Nativa | Ecosistema propio | Más opinionado |
| Mensajes de error | Claros | Básicos | Buenos | Buenos |
| Consistencia entre plataformas | Sí | Limitada | Excelente | Buena |
| Huella de recursos | Mínima | Moderada | Pesada | Moderada |

## Equivalencia de comandos (pip y uv)

| Tarea | pip | uv |
|---|---|---|
| Crear entorno virtual | `python -m venv .venv` | `uv venv` |
| Instalar un paquete | `pip install paquete` | `uv add paquete` |
| Instalar desde requirements | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Desinstalar | `pip uninstall paquete` | `uv remove paquete` |
| Listar paquetes | `pip list` | `uv pip list` |
| Congelar versiones | `pip freeze` | `uv pip freeze` |

## Puntos clave

- **Reemplaza varias herramientas a la vez:** pip, virtualenv, pyenv y pip-tools.
- **Ejecución sin activar el entorno:** `uv run script.py` usa automáticamente el entorno del proyecto.
- **Herramientas de línea de comandos:** `uvx` (o `uv tool run`) ejecuta utilidades como black o ruff en un entorno temporal, sin ensuciar el proyecto.
- **Reproducibilidad:** `uv export -o requirements.txt` genera un archivo compatible cuando hace falta desplegar sin uv.
- **CI/CD y Docker:** compatible con GitHub Actions y capas de caché en Docker.

## Cuándo elegir cada una (según el tutorial)

**uv:** velocidad, bajo consumo y compatibilidad con pip en proyectos puramente Python.  
  
**Conda:** cuando se necesitan paquetes que no son de Python o entornos científicos complejos.  
  
**Poetry:** capacidades parecidas a uv, pero con un enfoque más rígido y menor rendimiento.  
  
  **pip + virtualenv:** siguen siendo válidos, aunque con más pasos manuales y sin lock file.

