# base_conocimiento.py
import pandas as pd
import os

_df_pokemon = None # Variable privada para mantener la referencia al DataFrame
_DATA_DIR = "dataset" # Directorio donde se espera el CSV
_DATA_FILENAME = "Pokemon.csv" # Nombre del archivo CSV

def cargar_datos():
    """Carga los datos del CSV en un DataFrame global y lo retorna."""
    global _df_pokemon
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, _DATA_DIR, _DATA_FILENAME)

    if not os.path.exists(os.path.join(script_dir, _DATA_DIR)):
        os.makedirs(os.path.join(script_dir, _DATA_DIR))
    
    # Check if the CSV exists, if not, create an empty one with headers
    if not os.path.exists(full_path):
        print(f"Advertencia: Archivo CSV no encontrado en {full_path}. Creando un archivo vacío con encabezados.")
        df_empty = pd.DataFrame(columns=[
            '#', 'Name', 'Type 1', 'Type 2', 'HP', 'Attack', 'Defense',
            'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary', 'UserAdded' # Added UserAdded
        ])
        df_empty.to_csv(full_path, index=False)
        _df_pokemon = df_empty
        return _df_pokemon

    _df_pokemon = pd.read_csv(full_path)

    # Añadir la columna 'UserAdded' si no existe y establecer a False por defecto
    if 'UserAdded' not in _df_pokemon.columns:
        _df_pokemon['UserAdded'] = False
        # Opcional: guardar el DataFrame actualizado para persistir la nueva columna
        guardar_datos(_df_pokemon) # Guardar inmediatamente para que la columna exista

    return _df_pokemon

def obtener_pokemon(nombre, df):
    """Busca un Pokémon por nombre en el DataFrame."""
    if df is None:
        return pd.Series() # Retorna una Serie vacía si no hay datos
    return df[df['Name'].str.lower() == nombre.lower()].squeeze()

def get_pokemon_df():
    """Retorna el DataFrame actual de Pokémon, cargándolo si aún no lo está."""
    global _df_pokemon
    if _df_pokemon is None:
        cargar_datos() # Carga los datos si no han sido cargados
    return _df_pokemon

def guardar_datos(df):
    """Guarda el DataFrame actualizado en el archivo CSV y actualiza la referencia interna."""
    global _df_pokemon
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, _DATA_DIR, _DATA_FILENAME)
    df.to_csv(full_path, index=False)
    _df_pokemon = df # Asegura que la referencia global apunte al DataFrame guardado

# Cargar los datos una vez al iniciar el módulo para asegurar que 'UserAdded' se cree
get_pokemon_df()