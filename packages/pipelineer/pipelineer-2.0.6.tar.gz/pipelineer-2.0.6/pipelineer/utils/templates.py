import re
import os
def generate_gcs_object_name(resources_config_path):
    """
    Genera el valor de GCS_OBJECT_NAME basado en los datos de resources_config.py.
    """
    resources_config = {}
    with open(resources_config_path, "r") as file:
        exec(file.read(), resources_config)

    resources = resources_config.get("RESOURCES_CONFIG", {})
    dominio = resources.get("dominio", "unknown")
    subdominio = resources.get("subdominio", "unknown")
    origen = resources.get("origen", "unknown")
    producto = resources.get("producto", "unknown")

    return f"{dominio}/{subdominio}/{producto}/{origen}/tables_to_process.py"

def get_dag_file_name():
    """
    Busca el archivo que comienza con 'dag_' en el directorio actual.
    """
    for file in os.listdir("."):
        if file.startswith("dag_") and file.endswith(".py"):
            return file
    raise FileNotFoundError("No se encontró un archivo que comience con 'dag_' en el directorio actual.")



def replace_template(template_file, resources_config_path):
    """
    Reemplaza el contenido del archivo DAG con el template y actualiza las variables dinámicamente.
    """
    # Obtener el nombre del archivo DAG
    try:
        dag_file = get_dag_file_name()
    except FileNotFoundError as e:
        print(e)
        return

    # Confirmar con el usuario si desea proceder
    confirmation = input(f"¿Está seguro de reemplazar el contenido de '{dag_file}' con el del template? (si/no): ").lower()
    if confirmation not in ["si", "s", "yes", "y"]:
        print("Operación cancelada.")
        return

    try:
        # Generar el valor de GCS_OBJECT_NAME
        gcs_object_name = generate_gcs_object_name(resources_config_path)

        # Leer el contenido del template
        with open(template_file, "r") as template:
            content = template.read()

        # Reemplazar la variable GCS_OBJECT_NAME en el contenido del template
        content = re.sub(
            r'GCS_OBJECT_NAME\s*=\s*".*?"', 
            f'GCS_OBJECT_NAME = "{gcs_object_name}"', 
            content
        )

        # Reemplazar la variable DAG_NAME en el contenido del template
        dag_name = os.path.splitext(dag_file)[0]  # Nombre del archivo sin la extensión .py
        content = re.sub(
            r'DAG_NAME\s*=\s*".*?"', 
            f'DAG_NAME = "{dag_name}"', 
            content
        )

        # Escribir el contenido actualizado en el archivo DAG
        with open(dag_file, "w") as dag:
            dag.write(content)

        print(f"Contenido de '{dag_file}' reemplazado con éxito.")
        print(f"GCS_OBJECT_NAME: {gcs_object_name}")
        print(f"DAG_NAME: {dag_name}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{template_file}' o '{dag_file}'.")
    except Exception as e:
        print(f"Error al reemplazar contenido: {e}")