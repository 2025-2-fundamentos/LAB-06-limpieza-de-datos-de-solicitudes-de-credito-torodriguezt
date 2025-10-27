"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    input_file = "files/input/solicitudes_de_credito.csv"
    output_file = "files/output"
    
    # Leer el archivo
    df = pd.read_csv(input_file, sep=";", index_col=0)
    
    # Normalizar columnas de texto
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "monto_del_credito",
        "línea_credito",
    ]
    
    for columna in columnas_texto:
        df[columna] = (
            df[columna]
            .str.lower()
            .str.strip()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(".00", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
        )
    
    # Normalizar barrio (sin eliminar puntos ni comas)
    df["barrio"] = (
        df["barrio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )
    
    # Convertir comuna_ciudadano a entero
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
    
    # Convertir monto_del_credito a float
    df["monto_del_credito"] = df["monto_del_credito"].astype(float)
    
    # Normalizar fecha_de_beneficio (manejar ambos formatos: dd/mm/yyyy y yyyy/mm/dd)
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).combine_first(
        pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    )
    
    # Eliminar duplicados
    df = df.drop_duplicates()
    
    # Eliminar filas con valores faltantes
    df = df.dropna()
    
    # Guardar resultado
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    
    df.to_csv(
        f"{output_file}/solicitudes_de_credito.csv",
        sep=";",
        index=False,
    )

