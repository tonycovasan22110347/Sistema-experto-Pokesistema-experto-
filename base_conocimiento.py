import pandas as pd
import os

_df_pokemon = None # Variable privada para mantener la referencia al DataFrame de Pokémon
_df_movimientos = None # Nueva variable para el DataFrame de movimientos

_DATA_DIR = "dataset" # Directorio donde se espera el CSV
_POKEMON_FILENAME = "Pokemon.csv" # Nombre del archivo CSV de Pokémon
_MOVIMIENTOS_FILENAME = "movimientos_pokemon.csv" # Nombre del archivo CSV de movimientos

def _get_full_path(filename):
    """Helper function to get the full path for a given filename."""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, _DATA_DIR, filename)

def cargar_datos_pokemon():
    """Carga los datos del CSV de Pokémon en un DataFrame global y lo retorna."""
    global _df_pokemon
    full_path = _get_full_path(_POKEMON_FILENAME)

    if not os.path.exists(os.path.join(os.path.dirname(__file__), _DATA_DIR)):
        os.makedirs(os.path.join(os.path.dirname(__file__), _DATA_DIR))
    
    if not os.path.exists(full_path):
        print(f"Advertencia: Archivo CSV de Pokémon no encontrado en {full_path}. Creando un archivo vacío con encabezados.")
        df_empty = pd.DataFrame(columns=[
            '#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary'
        ])
        df_empty.to_csv(full_path, index=False)
        _df_pokemon = df_empty
        return _df_pokemon

    _df_pokemon = pd.read_csv(full_path)
    return _df_pokemon

def cargar_datos_movimientos():
    """Carga los datos del CSV de movimientos en un DataFrame global y lo retorna."""
    global _df_movimientos
    full_path = _get_full_path(_MOVIMIENTOS_FILENAME)

    if not os.path.exists(os.path.join(os.path.dirname(__file__), _DATA_DIR)):
        os.makedirs(os.path.join(os.path.dirname(__file__), _DATA_DIR))

    if not os.path.exists(full_path):
        print(f"Advertencia: Archivo CSV de movimientos no encontrado en {full_path}. Creando un archivo vacío con encabezados.")
        df_empty = pd.DataFrame(columns=[
            'Name', 'Type', 'Category', 'Power', 'Accuracy', 'PP', 'Effect'
        ])
        df_empty.to_csv(full_path, index=False)
        _df_movimientos = df_empty
        return _df_movimientos

    _df_movimientos = pd.read_csv(full_path)
    return _df_movimientos

def obtener_pokemon(nombre, df):
    """Busca un Pokémon por nombre en el DataFrame."""
    if df is None:
        return pd.Series()
    return df[df['Name'].str.lower() == nombre.lower()].squeeze()

def obtener_movimiento(nombre, df):
    """Busca un movimiento por nombre en el DataFrame."""
    if df is None:
        return pd.Series()
    return df[df['Name'].str.lower() == nombre.lower()].squeeze()

def get_pokemon_df():
    """Retorna el DataFrame actual de Pokémon, cargándolo si aún no lo está."""
    global _df_pokemon
    if _df_pokemon is None:
        cargar_datos_pokemon()
    return _df_pokemon

def get_movimientos_df():
    """Retorna el DataFrame actual de movimientos, cargándolo si aún no lo está."""
    global _df_movimientos
    if _df_movimientos is None:
        cargar_datos_movimientos()
    return _df_movimientos

def guardar_datos_pokemon(df):
    """Guarda el DataFrame actualizado de Pokémon en el archivo CSV y actualiza la referencia interna."""
    global _df_pokemon
    df.to_csv(_get_full_path(_POKEMON_FILENAME), index=False)
    _df_pokemon = df # Actualizar la referencia interna después de guardar