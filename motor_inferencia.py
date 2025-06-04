# motor_inferencia.py
import pandas as pd
from reglas import obtener_efectividad_defensiva
from base_conocimiento import get_pokemon_df, guardar_datos_pokemon, get_movimientos_df

# Mapa para traducir tipos de inglés a español
mapa_tipos_ingles_a_espanol = {
    "Steel": "Acero", "Water": "Agua", "Bug": "Bicho", "Dragon": "Dragón",
    "Electric": "Eléctrico", "Ghost": "Fantasma", "Fire": "Fuego",
    "Fairy": "Hada", "Ice": "Hielo", "Fighting": "Lucha", "Normal": "Normal",
    "Grass": "Planta", "Psychic": "Psíquico", "Rock": "Roca",
    "Dark": "Siniestro", "Ground": "Tierra", "Poison": "Veneno", "Flying": "Volador"
}

# Invertir el mapa para traducción de español a inglés al guardar y para buscar movimientos
mapa_tipos_espanol_a_ingles = {v: k for k, v in mapa_tipos_ingles_a_espanol.items()}


def analizar_pokemon_por_nombre(nombre):
    df_pokemon = get_pokemon_df()
    pokemon_row = df_pokemon[df_pokemon['Name'].str.lower() == nombre.lower()]

    if pokemon_row.empty:
        return None

    pokemon_data = pokemon_row.iloc[0].to_dict()

    # Traducir tipos a español para la interfaz
    tipo1_ingles = pokemon_data.get('Type 1')
    tipo2_ingles = pokemon_data.get('Type 2')

    tipo1_espanol = mapa_tipos_ingles_a_espanol.get(tipo1_ingles, tipo1_ingles)
    tipo2_espanol = mapa_tipos_ingles_a_espanol.get(tipo2_ingles, tipo2_ingles) if tipo2_ingles else None

    pokemon_data['Type 1 (es)'] = tipo1_espanol
    pokemon_data['Type 2 (es)'] = tipo2_espanol

    # Calcular la mejor estadística base
    stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    mejor_stat = None
    valor_mejor_stat = -1

    for stat in stats:
        valor = pokemon_data.get(stat)
        if pd.notna(valor) and valor > valor_mejor_stat:
            valor_mejor_stat = valor
            mejor_stat = stat

    pokemon_data['Mejor Stat'] = mejor_stat

    # Calcular efectividad defensiva
    tipos_defensores = [tipo1_espanol]
    if tipo2_espanol:
        tipos_defensores.append(tipo2_espanol)
    
    efectividad_defensiva = obtener_efectividad_defensiva(tipos_defensores)
    pokemon_data['Efectividad Defensiva'] = efectividad_defensiva

    return pokemon_data

def agregar_nuevo_pokemon_a_bd(datos_pokemon_dict):
    df = get_pokemon_df()
    
    # Verificar si el Pokémon ya existe
    if not df[df['Name'].str.lower() == datos_pokemon_dict['Name'].lower()].empty:
        return False, "Error: Ya existe un Pokémon con ese nombre."

    # Traducir tipos de español a inglés para guardar
    tipo1_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 1'], datos_pokemon_dict['Type 1'])
    tipo2_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 2'], datos_pokemon_dict['Type 2']) if datos_pokemon_dict['Type 2'] else None

    # Asignar un nuevo ID. Asume que '#' es un ID numérico y simplemente incrementa el máximo.
    # Si '#' es el primer registro, asigna 1, de lo contrario, el máximo + 1.
    if df.empty:
        new_id = 1
    else:
        # Asegúrate de que la columna '#' sea numérica para el max()
        df['#'] = pd.to_numeric(df['#'], errors='coerce')
        new_id = df['#'].max() + 1 if not df['#'].isnull().all() else 1

    new_pokemon = {
        '#': int(new_id), # Asegúrate de que el ID sea un entero
        'Name': datos_pokemon_dict['Name'],
        'Type 1': tipo1_ingles,
        'Type 2': tipo2_ingles,
        'HP': datos_pokemon_dict['HP'],
        'Attack': datos_pokemon_dict['Attack'],
        'Defense': datos_pokemon_dict['Defense'],
        'Sp. Atk': datos_pokemon_dict['Sp. Atk'],
        'Sp. Def': datos_pokemon_dict['Sp. Def'],
        'Speed': datos_pokemon_dict['Speed'],
        'Generation': datos_pokemon_dict.get('Generation', 1), # Default a 1 si no se proporciona
        'Legendary': datos_pokemon_dict.get('Legendary', False) # Default a False si no se proporciona
    }
    
    # Usar pd.concat para agregar la nueva fila
    df_new_row = pd.DataFrame([new_pokemon])
    df = pd.concat([df, df_new_row], ignore_index=True)
    
    guardar_datos_pokemon(df) # Guardar los cambios
    return True, "Pokémon agregado exitosamente."


def modificar_pokemon_en_bd(nombre_original, datos_pokemon_dict):
    df = get_pokemon_df()
    
    # Buscar el índice del Pokémon a modificar
    idx = df[df['Name'].str.lower() == nombre_original.lower()].index
    if idx.empty:
        return False, "Error: No se encontró el Pokémon original para modificar."

    # Verificar si el nuevo nombre ya existe en otro Pokémon (excepto el que se está modificando)
    new_name = datos_pokemon_dict['Name']
    if not df[(df['Name'].str.lower() == new_name.lower()) & (df['Name'].str.lower() != nombre_original.lower())].empty:
        return False, "Error: Ya existe otro Pokémon con el nuevo nombre especificado."

    # Traducir tipos de español a inglés para guardar
    tipo1_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 1'], datos_pokemon_dict['Type 1'])
    tipo2_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 2'], datos_pokemon_dict['Type 2']) if datos_pokemon_dict['Type 2'] else None

    # Actualizar la fila en el DataFrame
    df.loc[idx[0], 'Name'] = datos_pokemon_dict['Name']
    df.loc[idx[0], 'Type 1'] = tipo1_ingles
    df.loc[idx[0], 'Type 2'] = tipo2_ingles
    df.loc[idx[0], 'HP'] = datos_pokemon_dict['HP']
    df.loc[idx[0], 'Attack'] = datos_pokemon_dict['Attack']
    df.loc[idx[0], 'Defense'] = datos_pokemon_dict['Defense']
    df.loc[idx[0], 'Sp. Atk'] = datos_pokemon_dict['Sp. Atk']
    df.loc[idx[0], 'Sp. Def'] = datos_pokemon_dict['Sp. Def']
    df.loc[idx[0], 'Speed'] = datos_pokemon_dict['Speed']
    
    guardar_datos_pokemon(df) # Guardar los cambios
    return True, "Pokémon modificado exitosamente."

def buscar_movimiento_por_nombre(nombre_movimiento):
    df_movimientos = get_movimientos_df()
    movimiento_row = df_movimientos[df_movimientos['Name'].str.lower() == nombre_movimiento.lower()]
    
    if movimiento_row.empty:
        return None
    
    movimiento_data = movimiento_row.iloc[0].to_dict()
    return movimiento_data


def buscar_counters_para_pokemon(nombre_pokemon_objetivo):
    """
    Busca los mejores Pokémon y movimientos counter para un Pokémon objetivo.
    Retorna un diccionario con tipos efectivos, sugerencias de Pokémon y sugerencias de movimientos.
    """
    pokemon_objetivo_data = analizar_pokemon_por_nombre(nombre_pokemon_objetivo)

    if pokemon_objetivo_data is None:
        return None, "No se encontró el Pokémon objetivo."

    tipos_defensivos_objetivo = [pokemon_objetivo_data['Type 1 (es)']]
    if pokemon_objetivo_data['Type 2 (es)']:
        tipos_defensivos_objetivo.append(pokemon_objetivo_data['Type 2 (es)'])

    # Obtener qué tipos de ataque son fuertes contra el Pokémon objetivo
    efectividad_defensiva = obtener_efectividad_defensiva(tipos_defensivos_objetivo)
    tipos_fuertes_contra = efectividad_defensiva.get("fuertes_contra", [])

    if not tipos_fuertes_contra:
        return {}, "El Pokémon objetivo no tiene debilidades conocidas."

    sugerencias_pokemon = []
    df_pokemon = get_pokemon_df()
    for tipo_efectivo in tipos_fuertes_contra:
        # Buscar Pokémon que tengan el tipo efectivo como Type 1 o Type 2
        tipo_efectivo_ingles = mapa_tipos_espanol_a_ingles.get(tipo_efectivo, tipo_efectivo)
        
        pokemon_con_tipo_efectivo = df_pokemon[
            (df_pokemon['Type 1'] == tipo_efectivo_ingles) | 
            (df_pokemon['Type 2'] == tipo_efectivo_ingles)
        ]
        
        # Tomar los primeros 3 Pokémon como sugerencia por cada tipo efectivo
        for _, row in pokemon_con_tipo_efectivo.head(3).iterrows():
            # Asegurarse de que los tipos se muestren en español si son los que están en el DataFrame
            pkmn_tipo1_es = mapa_tipos_ingles_a_espanol.get(row['Type 1'], row['Type 1'])
            pkmn_tipo2_es = mapa_tipos_ingles_a_espanol.get(row['Type 2'], row['Type 2']) if pd.notna(row['Type 2']) else None
            
            tipos_pkmn_str = pkmn_tipo1_es
            if pkmn_tipo2_es:
                tipos_pkmn_str += f"/{pkmn_tipo2_es}"
            
            # Eliminado: " - Ideal contra tipo {tipo_efectivo}"
            sugerencias_pokemon.append(f"{row['Name']} (Tipos: {tipos_pkmn_str})")
            
    sugerencias_pokemon = list(set(sugerencias_pokemon)) # Eliminar duplicados y convertir a lista

    sugerencias_movimientos = {}
    df_movimientos = get_movimientos_df()
    for tipo_efectivo_espanol in tipos_fuertes_contra:
        # Buscar movimientos por tipo en ESPAÑOL, ya que el CSV está en español
        movimientos_de_tipo = df_movimientos[df_movimientos['Type'].str.lower() == tipo_efectivo_espanol.lower()]
        if not movimientos_de_tipo.empty:
            # Ordenar por poder de ataque (si está disponible y es numérico) y tomar los 3 mejores que tengan poder > 0
            movimientos_de_tipo['Power'] = pd.to_numeric(movimientos_de_tipo['Power'], errors='coerce')
            movimientos_de_tipo = movimientos_de_tipo[movimientos_de_tipo['Power'] > 0]
            movimientos_de_tipo = movimientos_de_tipo.sort_values(by='Power', ascending=False, na_position='last')
            sugerencias_movimientos[tipo_efectivo_espanol] = movimientos_de_tipo['Name'].head(3).tolist()
        else:
            sugerencias_movimientos[tipo_efectivo_espanol] = []

    return {
        "tipos_fuertes_contra": tipos_fuertes_contra,
        "sugerencias_pokemon": sugerencias_pokemon,
        "sugerencias_movimientos": sugerencias_movimientos
    }, "Counters encontrados exitosamente."