import os
import argparse

def clean_migrations(project_path):
    """
    Limpia los archivos de migraciones en un proyecto Django.
    """
    apps_path = os.path.abspath(project_path)

    for app_name in os.listdir(apps_path):
        app_path = os.path.join(apps_path, app_name)
        migrations_path = os.path.join(app_path, 'migrations')

        if os.path.isdir(migrations_path):
            print(f"Procesando migraciones para la app: {app_name}")
            for file_name in os.listdir(migrations_path):
                if file_name != '__init__.py' and file_name.endswith('.py'):
                    os.remove(os.path.join(migrations_path, file_name))
                    print(f"   Archivo eliminado: {file_name}")
        else:
            print(f"No se encontró carpeta de migraciones para la app: {app_name}")

def main():
    """
    Punto de entrada para el comando clean-migrations.
    """
    parser = argparse.ArgumentParser(
        description="Limpia los archivos de migraciones en un proyecto Django."
    )
    parser.add_argument(
        "project_path",
        type=str,
        nargs="?",
        default=os.getcwd(),
        help="Ruta al proyecto Django (por defecto, el directorio actual)."
    )
    args = parser.parse_args()
    clean_migrations(args.project_path)
