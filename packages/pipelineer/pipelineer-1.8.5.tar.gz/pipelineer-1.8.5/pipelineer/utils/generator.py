import os
import re
import json
import sys
import importlib.util
from .mappers import map_oracle_to_avro
import oracledb 



def generate_avro_and_mapping(sql_file_path, avro_output_path, json_output_path, sql_output_path, date_format):
    with open(sql_file_path, 'r') as sql_file:
        sql_content = sql_file.read()

    # Extraer nombre de la tabla
    table_name_match = re.search(r'CREATE TABLE\s+"[^"]+"\."([^"]+)"', sql_content, re.IGNORECASE)
    table_name = table_name_match.group(1).lower() if table_name_match else "unknown_table"

    # Extraer columnas
    columns = re.findall(r'"([^"]+)"\s+([A-Z0-9\(\),\s]+)', sql_content, re.IGNORECASE)

    # Crear esquema Avro
    avro_schema = {
        "type": "record",
        "name": table_name,
        "fields": []
    }

    # Mapeo JSON
    field_mappings = []
    column_names_types = []

    for column_name, column_type in columns:
        if column_name.lower() == table_name:
            continue  # Evitar campo si coincide con nombre de tabla

        # Mapeo Avro
        avro_type = map_oracle_to_avro(column_type)

        # Ajustar tipo para el JSON
        if isinstance(avro_type, dict) and avro_type.get("logicalType") == "decimal":
            json_type = "numeric"
        elif avro_type == "long":
            json_type = "int"
        else:
            json_type = avro_type

        # Añadir al esquema Avro
        avro_schema["fields"].append({
            "name": column_name,
            "type": ["null", avro_type] if isinstance(avro_type, str) else ["null", avro_type]
        })

        # Añadir al mapeo JSON
        field_mappings.append((column_name.upper(), json_type))

        # Mantener el nombre y tipo original para SQL
        column_names_types.append((column_name, column_type.strip().upper()))

    # Guardar esquema Avro
    if not os.path.isdir(avro_output_path):
        os.makedirs(avro_output_path)
    avro_file_path = os.path.join(avro_output_path, f"{table_name}.avsc")
    with open(avro_file_path, 'w') as avro_file:
        json.dump(avro_schema, avro_file, indent=4)

    # Guardar mapeo JSON (como dict)
    if not os.path.isdir(json_output_path):
        os.makedirs(json_output_path)
    json_file_path = os.path.join(json_output_path, f"{table_name}.json")
    with open(json_file_path, 'w') as json_file:
        # Convertir la lista a dict
        json.dump(dict(field_mappings), json_file, indent=4)

    # Generar consulta SQL
    select_columns = []
    for col_name, col_type in column_names_types:
        if col_name.lower() == table_name:
            continue
        if col_type.startswith("DATE"):
            format_string = 'YYYY-MM-DD HH24:MI:SS' if date_format == 'datetime' else 'YYYY-MM-DD'
            select_columns.append(f"TO_CHAR({col_name}, '{format_string}') AS {col_name}")
        else:
            select_columns.append(col_name)

    select_columns_str = ",\n    ".join(select_columns)
    sql_query = f"SELECT\n    {select_columns_str}\nFROM\n    {table_name.upper()}\nWHERE\n    ROWNUM <= 100"

    if not os.path.isdir(sql_output_path):
        os.makedirs(sql_output_path)
    sql_query_file_path = os.path.join(sql_output_path, f"{table_name}.sql")
    with open(sql_query_file_path, 'w') as query_file:
        query_file.write(sql_query)

    print(f"Generado Avro: {avro_file_path}")
    print(f"Generado JSON: {json_file_path}")
    print(f"Generado SQL: {sql_query_file_path}")

def process_multiple_sql_files(input_folder, avro_output_folder, json_output_folder, sql_output_folder, date_format='datetime'):
    if not os.path.isdir(input_folder):
        raise ValueError("La carpeta de entrada no existe.")

    sql_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.sql')]
    if not sql_files:
        raise ValueError("No se encontraron archivos SQL en la carpeta de entrada.")

    for sql_file in sql_files:
        sql_file_path = os.path.join(input_folder, sql_file)
        generate_avro_and_mapping(sql_file_path, avro_output_folder, json_output_folder, sql_output_folder, date_format)

    print("Proceso finalizado. Todos los archivos generados correctamente.")



def parse_oracle_schema(schema_file):
    """
    Analiza un archivo SQL con la definición de una tabla Oracle y extrae:
    - Campos (nombre, tipo, nullabilidad)
    - Claves primarias
    """

    with open(schema_file, 'r') as file:
        content = file.read()

    # Extraer el contenido entre CREATE TABLE ... ( ... ) para columnas y constraints
    table_def_match = re.search(
        r'CREATE TABLE\s+"[^"]+"\."[^"]+"\s*\((.*?)\)\s*',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not table_def_match:
        raise ValueError("No se encontró la definición CREATE TABLE en el esquema.")

    table_def_content = table_def_match.group(1)

    # Dividir el contenido por líneas y limpiar espacios
    lines = [l.strip() for l in table_def_content.split('\n') if l.strip()]

    fields = []
    primary_keys = []

    # Expresión regular para columnas:
    # - Nombre de columna: "col" o col
    # - Tipo: una secuencia de caracteres alfanuméricos, paréntesis, coma o espacio
    # - Opcional: NOT NULL o NOT NULL ENABLE
    col_pattern = re.compile(
        r'^(?:"(?P<colq>[^"]+)"|(?P<col>[A-Za-z0-9_]+))\s+(?P<type>[A-Za-z0-9\(\)\s,]+)(?P<notnull>NOT NULL(?: ENABLE)?)?\s*(,)?$',
        re.IGNORECASE
    )

    # Expresión regular para constraint de PRIMARY KEY
    # Maneja caso con o sin comillas en las columnas
    pk_pattern = re.compile(r'PRIMARY KEY\s*\(([^)]+)\)', re.IGNORECASE)

    # Bandera para saber si seguimos analizando columnas
    parsing_columns = True

    for line in lines:
        # Si la línea empieza con CONSTRAINT, puede ser PK u otra constraint
        if line.upper().startswith("CONSTRAINT"):
            # Intentar encontrar PRIMARY KEY
            pk_match = pk_pattern.search(line)
            if pk_match:
                pk_cols = pk_match.group(1)
                # Extraer columnas de la PK, removiendo comillas y espacios
                primary_keys = [c.strip().strip('"').lower() for c in pk_cols.split(',')]
            # Esta línea no es columna, así que si aún estábamos parseando columnas, continuamos,
            # pero no la consideramos como columna.
            continue

        # Si la línea tiene palabras clave típicas de almacenamiento u otras cosas
        # que no son columnas ni constraints, dejamos de parsear columnas.
        if re.match(r'^(PCTFREE|PCTUSED|INITRANS|MAXTRANS|NOCOMPRESS|LOGGING|STORAGE|TABLESPACE|ENABLE ROW MOVEMENT|SEGMENT CREATION)', line, re.IGNORECASE):
            parsing_columns = False
            continue

        if not parsing_columns:
            # Ya no estamos en sección de columnas, no hacemos nada con esta línea.
            continue

        # Intentar parsear la columna
        col_match = col_pattern.match(line)
        if col_match:
            column_name = col_match.group('colq') or col_match.group('col')
            column_type = col_match.group('type').strip().upper()
            not_null_part = col_match.group('notnull')
            is_not_null = "NOT NULL" if not_null_part else "NULL"

            # Mapeo de tipos
            if column_type.startswith("NUMBER"):
                if "," in column_type:
                    # NUMBER(p, s)
                    m = re.match(r"NUMBER\((\d+),\s*(\d+)\)", column_type)
                    if m:
                        precision, scale = map(int, m.groups())
                        column_type = "NUMERIC" if precision <= 38 else "BIGNUMERIC"
                    else:
                        column_type = "NUMERIC"
                else:
                    column_type = "INT64"
            elif column_type.startswith("VARCHAR2") or column_type.startswith("CHAR"):
                column_type = "STRING"
            elif column_type.startswith("DATE"):
                column_type = "DATETIME"
            elif column_type.startswith("RAW"):
                column_type = "BYTES"
            elif column_type in ["CLOB", "NCLOB"]:
                column_type = "STRING"
            elif column_type == "BLOB":
                column_type = "BYTES"
            else:
                # Caso genérico
                column_type = "STRING"

            fields.append((column_name.lower(), column_type, is_not_null))
        else:
            # Línea no reconocida como columna, puede ser constraint u otra cosa
            # Dejamos de parsear columnas en este punto.
            parsing_columns = False

    # Si no se encontró PK en el bloque principal, intentar en todo el contenido (por si está afuera)
    if not primary_keys:
        pk_match = pk_pattern.search(content)
        if pk_match:
            pk_cols = pk_match.group(1)
            primary_keys = [c.strip().strip('"').lower() for c in pk_cols.split(',')]

    return fields, primary_keys


def extract_column_comments(schema_file):
    """
    Extrae comentarios de columnas de un archivo de esquema Oracle.
    Soporta líneas como:
    COMMENT ON COLUMN "OPS$ANDES"."COB_COMPRO"."CPA_CODIGO" IS 'secuencia';
    """
    comments = {}
    pattern = re.compile(
        r'COMMENT ON COLUMN\s+"[^"]+"\."[^"]+"\."([^"]+)"\s+IS\s+\'(.+?)\'',
        re.IGNORECASE
    )
    with open(schema_file, 'r') as file:
        content = file.read()
        for match in pattern.finditer(content):
            column = match.group(1).lower()
            comment = match.group(2)
            comments[column] = comment
    return comments


def generate_bigquery_table_scripts(config_folder, schema_folder, config_file=None, output_folder="sql/bigquery/scripts/"):
    if not os.path.isdir(config_folder):
        raise ValueError(f"La carpeta de configuración no existe: {config_folder}")
    if not os.path.isdir(schema_folder):
        raise ValueError(f"La carpeta de esquemas no existe: {schema_folder}")

    config_files = [os.path.join(config_folder, f) for f in os.listdir(config_folder) if f.endswith(".json")]
    if config_file:
        config_files = [os.path.join(config_folder, config_file)]

    if not config_files:
        raise ValueError("No se encontraron archivos de configuración en la carpeta especificada.")

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    for file in config_files:
        with open(file, 'r') as f:
            config = json.load(f)

        table_name = config.get("table_name")
        zones = config.get("zone", ["stg"])
        partition_field = config.get("partition_field")
        clustering_fields = config.get("clustering_fields", [])
        dataset = config.get("dataset")
        labels = config.get("labels", [])

        if not table_name or not dataset:
            raise ValueError(f"El archivo de configuración {file} debe contener 'table_name' y 'dataset'.")

        schema_file = os.path.join(schema_folder, f"{table_name.lower()}.sql")
        if not os.path.isfile(schema_file):
            print(f"Esquema no encontrado: {schema_file}. Saltando {table_name}.")
            continue

        fields, primary_keys = parse_oracle_schema(schema_file)
        column_comments = extract_column_comments(schema_file)

        for zone in zones:
            zone_dataset = "staging_dataset" if zone == "stg" else dataset
            bq_table_name = f"{zone}_{table_name.lower()}"

            script_lines = [f"CREATE TABLE `${{PROJECT_NAME}}.{zone_dataset}.{bq_table_name}` ("]
            for column_name, column_type, is_not_null in fields:
                comment = column_comments.get(column_name, "")
                comment_line = f" OPTIONS(description='{comment}')" if comment else ""
                script_lines.append(f"  {column_name} {column_type} {is_not_null}{comment_line},")

            # Agregar campos por defecto
            script_lines.append("  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),")
            script_lines.append("  fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP()")

            # Quitar la última coma si existe
            if script_lines[-1].endswith(","):
                script_lines[-1] = script_lines[-1][:-1]

            script_lines.append(")")

            if partition_field:
                script_lines.append(f"PARTITION BY DATETIME_TRUNC({partition_field}, DAY)")

            if clustering_fields:
                script_lines.append(f"CLUSTER BY {', '.join(clustering_fields)}")

            if primary_keys:
                script_lines.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

            if labels:
                label_list = ", ".join([f"('{label['key']}', '{label['value']}')" for label in labels])
                script_lines.append(f"OPTIONS(labels=[{label_list}])")

            script = "\n".join(script_lines)

            output_file = os.path.join(output_folder, f"{zone}_{table_name.lower()}.sql")
            with open(output_file, 'w') as output:
                output.write(script)

            print(f"Script generado: {output_file}")

def extract_primary_keys(schema_file):
    """
    Extrae las claves primarias (PKs) de un archivo de esquema Oracle.
    """
    with open(schema_file, 'r') as file:
        content = file.read()

    pk_match = re.search(r'CONSTRAINT .* PRIMARY KEY \((.*?)\)', content, re.IGNORECASE)
    if pk_match:
        pk_fields = pk_match.group(1).replace('"', '').split(",")
        return [pk_field.strip().lower() for pk_field in pk_fields]

    return []  # Si no hay PKs definidas




def map_oracle_to_bigquery(column_type):
    """
    Mapea los tipos de datos Oracle a BigQuery.
    """
    if column_type.startswith("NUMBER"):
        if "," in column_type:  # NUMBER(p, s)
            return "NUMERIC"
        return "INT64"
    elif column_type.startswith("VARCHAR2") or column_type.startswith("CHAR"):
        return "STRING"
    elif column_type.startswith("DATE"):
        return "DATETIME"
    elif column_type.startswith("RAW"):
        return "BYTES"
    elif column_type in ["CLOB", "NCLOB"]:
        return "STRING"
    elif column_type == "BLOB":
        return "BYTES"
    return "STRING"  # Tipo por defecto

def generate_bigquery_store_procedures(config_folder, schema_folder, output_folder):
    """
    Genera procedimientos almacenados para MERGE en BigQuery a partir de configuraciones y esquemas Oracle.
    """
    # Verificar existencia de carpetas
    if not os.path.isdir(config_folder):
        raise ValueError(f"La carpeta de configuración no existe: {config_folder}")
    if not os.path.isdir(schema_folder):
        raise ValueError(f"La carpeta de esquemas no existe: {schema_folder}")
    
    # Crear carpeta de salida si no existe
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    # Procesar cada archivo JSON de configuración
    config_files = [
        os.path.join(config_folder, f) for f in os.listdir(config_folder)
        if f.endswith(".json")
    ]

    if not config_files:
        raise ValueError("No se encontraron archivos de configuración en la carpeta especificada.")

    for config_file in config_files:
        with open(config_file, 'r') as f:
            config = json.load(f)

        table_name = config.get("table_name")
        merge_fields = config.get("merge_fields")
        dataset = config.get("dataset", "dep")  # Por defecto, 'dep'

        if not table_name or not merge_fields:
            print(f"Saltando {config_file}. 'table_name' o 'merge_fields' faltantes.")
            continue

        # Leer el esquema desde el archivo .sql
        schema_file = os.path.join(schema_folder, f"{table_name.lower()}.sql")
        if not os.path.isfile(schema_file):
            print(f"Esquema no encontrado: {schema_file}. Saltando {table_name}.")
            continue

        # Extraer solo los nombres de los campos
        all_fields = [field[0] for field in parse_oracle_schema(schema_file)]

        if not all_fields:
            print(f"No se encontraron campos en el esquema de {table_name}. Saltando.")
            continue

        # Añadir campos especiales
        all_fields.append("fecha_creacion")
        all_fields.append("fecha_actualizacion")

        # Preparar nombres de tabla y procedimiento
        target_table = f"{dataset}.dep_{table_name.lower()}"
        source_table = f"staging_dataset.stg_{table_name.lower()}"
        procedure_name = f"{dataset}.sp_merge_dep_{table_name.lower()}"

        # Crear las cláusulas ON, UPDATE y INSERT
        on_clause = " AND ".join([f"T.{field} = S.{field}" for field in merge_fields])

        # Update clause: incluir fecha_actualizacion con CURRENT_TIMESTAMP()
        update_fields = [field for field in all_fields if field not in ["fecha_creacion", "fecha_actualizacion"]]
        update_clause = ",\n      ".join([f"T.{field} = S.{field}" for field in update_fields])
        update_clause += ",\n      T.fecha_actualizacion = CURRENT_TIMESTAMP()"

        # Insert clause: todos los campos
        insert_fields = ",\n      ".join(all_fields)
        insert_values = ",\n      ".join(
            [f"S.{field}" if field not in ["fecha_creacion", "fecha_actualizacion"]
             else "CURRENT_TIMESTAMP()" for field in all_fields]
        )

        # Generar el procedimiento almacenado
        procedure_script = f"""
CREATE OR REPLACE PROCEDURE `${{PROJECT_NAME}}.{procedure_name}`()
BEGIN
  MERGE `{target_table}` T
  USING `{source_table}` S
  ON {on_clause}
  WHEN MATCHED THEN
    UPDATE SET
      {update_clause}
  WHEN NOT MATCHED THEN
    INSERT (
      {insert_fields}
    )
    VALUES (
      {insert_values}
    );
END;
"""

        # Guardar el archivo
        output_file = os.path.join(output_folder, f"sp_merge_dep_{table_name.lower()}.sql")
        with open(output_file, 'w') as output:
            output.write(procedure_script)

        print(f"Procedimiento almacenado generado: {output_file}")


def extract_oracle_schemas(output_folder, tables_config="schemas/config/oracle_tables.py", config_path="connections/oracle_config.py"):
    """
    Extrae el esquema de tablas Oracle y genera archivos SQL.
    """
    # Cargar listado de tablas
    table_list = load_table_list(tables_config)
    print(f"Tablas a procesar: {table_list}")

    # Cargar configuración Oracle
    config = load_oracle_config(config_path)
    # Fuerza el uso del Thin Client
    oracledb.init_oracle_client(lib_dir=None, driver_mode=oracledb.DRIVER_MODE_THIN)
    # Conectar a Oracle
    try:
        connection = oracledb.connect(user=config['user'], password=config['password'], host=config['host'], service_name=config['service_name'], port=1521)
        print("Conexión a Oracle exitosa.")
    except Exception as e:
        raise Exception(f"Error conectándose a Oracle: {e}")

    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Procesar cada tabla
    for table in table_list:
        try:
            cursor = connection.cursor()

            # Obtener el esquema de la tabla
            cursor.execute(f"""
                SELECT DBMS_METADATA.GET_DDL('TABLE', '{table}') FROM DUAL
            """)
            ddl = cursor.fetchone()[0]

            # Limpiar el esquema (opcional)
            ddl_cleaned = re.sub(r'SEGMENT\s+CREATION.*?;', ';', ddl, flags=re.DOTALL)

            # Guardar el esquema en un archivo .sql
            file_path = os.path.join(output_folder, f"{table.lower()}.sql")
            with open(file_path, 'w') as f:
                f.write(ddl_cleaned)
            print(f"Esquema generado para la tabla: {table}")

        except Exception as e:
            print(f"Error extrayendo esquema para {table}: {e}")
        finally:
            cursor.close()

    connection.close()
    print("Extracción completada.")

def load_table_list(config_path="schemas/config/oracle_tables.py"):
    """
    Carga el listado de tablas desde un archivo .py.
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"El archivo de configuración no existe: {config_path}")
    
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    if not hasattr(config, "ORACLE_TABLES"):
        raise AttributeError("El archivo de configuración no contiene 'ORACLE_TABLES'.")

    return config.ORACLE_TABLES

def load_oracle_config(config_path):
    """
    Carga la configuración de conexión Oracle desde un archivo .py usando exec.
    """
    oracle_config = {}
    try:
        with open(config_path, "r") as file:
            exec(file.read(), oracle_config)
        connection_config = oracle_config.get("CONNECTION_CONFIG", {})
        if not connection_config:
            raise ValueError("CONNECTION_CONFIG no definido en el archivo de configuración.")
        return connection_config
    except Exception as e:
        raise Exception(f"Error al cargar la configuración Oracle: {e}")