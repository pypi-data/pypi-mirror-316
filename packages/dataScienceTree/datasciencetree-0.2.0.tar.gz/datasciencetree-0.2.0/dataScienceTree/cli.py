import importlib
import subprocess
from pathlib import Path

import click
import questionary
from cookiecutter.main import cookiecutter
from rich.console import Console
from rich.panel import Panel

console = Console()

PROJECT_CONFIGS = {
    "Análisis de Datos": {
        "estructura": [
            "data/raw",
            "data/processed",
            "notebooks",
            "src/utils",
            "src/visualization",
            "reports",
            "tests",
        ],
        "features": [
            "Pre-commit hooks",
            "Documentación (MKDocs)",
        ],
        "requirements": [
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "jupyter",
            "pytest",
            "black",
            "ruff",
            "ipykernel",
        ],
        "docker": False
    },
    "Machine Learning": {
        "estructura": [
            "data/raw",
            "data/processed",
            "notebooks",
            "src/utils",
            "src/visualization",
            "src/models",
            "src/features",
            "src/evaluation",
            "models/trained",
            "reports",
            "tests",
        ],
        "features": [
            "Pre-commit hooks",
            "Documentación (MKDocs)",
            "MLflow",
            "DVC",
        ],
        "requirements": [
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "jupyter",
            "mlflow",
            "dvc",
            "pytest",
            "black",
            "ruff",
            "ipykernel",
        ],
        "docker": True
    },
    "Data Engineering": {
        "estructura": [
            "data/raw",
            "data/processed",
            "data/external",
            "notebooks",
            "src/utils",
            "src/visualization",
            "src/models",
            "src/features",
            "src/pipelines",
            "src/etl",
            "src/api",
            "models/trained",
            "airflow/dags",
            "docker",
            "reports",
            "tests",
        ],
        "features": [
            "Pre-commit hooks",
            "Documentación (MKDocs)",
            "FastAPI",
            "Airflow",
            "MLflow",
            "DVC",
        ],
        "requirements": [
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "fastapi",
            "uvicorn",
            "apache-airflow",
            "mlflow",
            "dvc",
            "docker-compose",
            "pytest",
            "black",
            "ruff",
            "ipykernel",
        ],
        "docker": True
    }
}

def get_template_path():
    with importlib.resources.path("dataScienceTree", "template") as template_path:
        return str(template_path)

def validate_project_name(name: str) -> bool:
    return all(c.isalnum() or c in ("-", "_") for c in name)

def create_project_structure(project_path: Path, estructura: list):
    for path in estructura:
        (project_path / path).mkdir(parents=True, exist_ok=True)
        (project_path / path / '__init__.py').touch()

def create_requirements(project_path: Path, requirements: list):
    with open(project_path / 'requirements.txt', 'w') as f:
        f.write('\n'.join(requirements))

def create_dockerfile(project_path: Path, project_type: str):
    dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
"""

    if project_type == "Data Engineering":
        dockerfile_content += '\nCMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]'
    elif project_type == "Machine Learning":
        dockerfile_content += '\nCMD ["python", "src/models/train_model.py"]'

    with open(project_path / 'Dockerfile', 'w') as f:
        f.write(dockerfile_content)

def create_pyproject_toml(project_path: Path, project_name: str, project_type: str):
    content = f"""
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "Proyecto de {project_type}"
requires-python = ">=3.11"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.black]
line-length = 88
target-version = ['py311']
"""
    with open(project_path / 'pyproject.toml', 'w') as f:
        f.write(content)

@click.command()
@click.argument("project_name", required=True)
def main(project_name: str):
    """Crear un nuevo proyecto Python con buenas prácticas y herramientas modernas."""
    console.print(Panel.fit("Crear Proyecto Python", style="bold blue"))

    if not project_name:
        project_name = questionary.text(
            "¿Cuál es el nombre de tu proyecto?",
            validate=lambda text: len(text) > 0 and validate_project_name(text),
        ).ask()

    project_type = questionary.select(
        "Selecciona el tipo de proyecto:",
        choices=list(PROJECT_CONFIGS.keys())
    ).ask()

    config = PROJECT_CONFIGS[project_type]

    with console.status("[bold green]Creando proyecto..."):
        project_path = Path.cwd() / project_name
        project_path.mkdir(exist_ok=True)

        # Crear estructura de carpetas
        create_project_structure(project_path, config["estructura"])

        # Crear requirements.txt
        create_requirements(project_path, config["requirements"])

        # Crear pyproject.toml
        create_pyproject_toml(project_path, project_name, project_type)

        # Crear Dockerfile si es necesario
        if config["docker"]:
            create_dockerfile(project_path, project_type)

        # Instalar dependencias usando uv
        subprocess.run(
            ["uv", "pip", "install", "-r", "requirements.txt"], 
            cwd=project_path, 
            capture_output=True
        )

        # Inicializar git
        subprocess.run(["git", "init"], cwd=project_path, capture_output=True)

    console.print(f"\n✨ ¡Proyecto [bold green]{project_name}[/] creado exitosamente!")
    console.print("\nEstructura creada para:", project_type)
    console.print("\nCaracterísticas incluidas:")
    for feature in config["features"]:
        console.print(f"  - {feature}")

    console.print("\nPróximos pasos:")
    console.print(f"  1. cd {project_name}")

    if config["docker"]:
        console.print("  2. docker build -t {project_name} .")
        console.print("  3. docker run -p 8000:8000 {project_name}")

if __name__ == "__main__":
    main()