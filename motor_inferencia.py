# motor_inferencia.py
import pandas as pd
from reglas import calcular_efectividad, obtener_efectividad_defensiva, tipos_disponibles
from base_conocimiento import get_pokemon_df, guardar_datos

# Mapa para traducir tipos de inglés a español
mapa_tipos_ingles_a_espanol = {
    "Steel": "Acero", "Water": "Agua", "Bug": "Bicho", "Dragon": "Dragón",
    "Electric": "Eléctrico", "Ghost": "Fantasma", "Fire": "Fuego",
    "Fairy": "Hada", "Ice": "Hielo", "Fighting": "Lucha", "Normal": "Normal",
    "Grass": "Planta", "Psychic": "Psíquico", "Rock": "Roca",
    "Dark": "Siniestro", "Ground": "Tierra", "Poison": "Veneno", "Flying": "Volador"
}

# Invertir el mapa para traducción de español a inglés al guardar
mapa_tipos_espanol_a_ingles = {v: k for k, v in mapa_tipos_ingles_a_espanol.items()}


def analizar_pokemon_por_nombre(nombre):
    df_pokemon = get_pokemon_df()
    pokemon_row = df_pokemon[df_pokemon['Name'].str.lower() == nombre.lower()]

    if pokemon_row.empty:
        return None

    # Usar .iloc[0] para obtener la primera fila como una Serie si hay múltiples
    pokemon = pokemon_row.iloc[0]

    tipo1_ingles = pokemon['Type 1']
    tipo2_ingles = pokemon['Type 2'] if pd.notna(pokemon['Type 2']) else None

    tipo1_esp = mapa_tipos_ingles_a_espanol.get(tipo1_ingles, tipo1_ingles)
    tipo2_esp = mapa_tipos_ingles_a_espanol.get(tipo2_ingles, tipo2_ingles) if tipo2_ingles else None

    tipos_pokemon = [tipo1_esp]
    if tipo2_esp:
        tipos_pokemon.append(tipo2_esp)

    stats = {
        'HP': int(pokemon.get('HP', 0)),
        'Attack': int(pokemon.get('Attack', 0)),
        'Defense': int(pokemon.get('Defense', 0)),
        'Sp. Atk': int(pokemon.get('Sp. Atk', 0)),
        'Sp. Def': int(pokemon.get('Sp. Def', 0)),
        'Speed': int(pokemon.get('Speed', 0))
    }

    mejor_stat_nombre = None
    mejor_stat_valor = -1
    for stat_name, stat_value in stats.items():
        if pd.notna(stat_value) and stat_value > mejor_stat_valor:
            mejor_stat_valor = stat_value
            mejor_stat_nombre = stat_name

    fuertes_contra, debiles_contra, inmunes_contra, neutros_contra = obtener_efectividad_defensiva(tipos_pokemon)

    return {
        'ID': pokemon['#'], # Incluir el ID para facilitar la modificación
        'Nombre': pokemon['Name'],
        'Tipo(s)': tipos_pokemon,
        'Stats': stats,
        'Mejor Stat': f"{mejor_stat_nombre}: {mejor_stat_valor}",
        'Fuerte contra': debiles_contra,
        'Débil contra': fuertes_contra,
        'Inmune contra': inmunes_contra,
        'Neutro contra': neutros_contra,
        'UserAdded': pokemon.get('UserAdded', False) # Obtener el valor de UserAdded
    }

def agregar_nuevo_pokemon_a_bd(datos_pokemon_dict):
    df = get_pokemon_df()

    tipo1_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 1'], datos_pokemon_dict['Type 1'])
    tipo2_ingles = None
    if datos_pokemon_dict.get('Type 2'):
        tipo2_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 2'], datos_pokemon_dict['Type 2'])

    # Verificar si el nombre ya existe (case-insensitive)
    if df['Name'].str.lower().isin([datos_pokemon_dict['Name'].lower()]).any():
        return False, "Un Pokémon con ese nombre ya existe en la base de datos."

    new_id = df['#'].max() + 1 if not df.empty else 1

    new_row = {
        '#': new_id,
        'Name': datos_pokemon_dict['Name'],
        'Type 1': tipo1_ingles,
        'Type 2': tipo2_ingles,
        'HP': datos_pokemon_dict['HP'],
        'Attack': datos_pokemon_dict['Attack'],
        'Defense': datos_pokemon_dict['Defense'],
        'Sp. Atk': datos_pokemon_dict['Sp. Atk'],
        'Sp. Def': datos_pokemon_dict['Sp. Def'],
        'Speed': datos_pokemon_dict['Speed'],
        'Generation': datos_pokemon_dict.get('Generation', 1),
        'Legendary': datos_pokemon_dict.get('Legendary', False),
        'UserAdded': True # Marcar como agregado por el usuario
    }

    new_df_row = pd.DataFrame([new_row])
    df_updated = pd.concat([df, new_df_row], ignore_index=True)

    guardar_datos(df_updated)
    return True, "Pokémon agregado exitosamente."

def modificar_pokemon_en_bd(pokemon_id, datos_pokemon_dict):
    df = get_pokemon_df()

    # Convertir tipos de español a inglés
    tipo1_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 1'], datos_pokemon_dict['Type 1'])
    tipo2_ingles = None
    if datos_pokemon_dict.get('Type 2'):
        tipo2_ingles = mapa_tipos_espanol_a_ingles.get(datos_pokemon_dict['Type 2'], datos_pokemon_dict['Type 2'])

    # Encontrar el índice del Pokémon a modificar por su ID
    idx = df.index[df['#'] == pokemon_id].tolist()
    if not idx:
        return False, "No se encontró el Pokémon a modificar."

    # Verificar si el nuevo nombre ya existe en otro Pokémon
    new_name_lower = datos_pokemon_dict['Name'].lower()
    existing_pokemon_with_new_name = df[(df['Name'].str.lower() == new_name_lower) & (df['#'] != pokemon_id)]
    if not existing_pokemon_with_new_name.empty:
        return False, "Un Pokémon con ese nombre ya existe."

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
    # Mantener Generation y Legendary como están, o actualizar si los agregas al formulario
    df.loc[idx[0], 'Generation'] = datos_pokemon_dict.get('Generation', df.loc[idx[0], 'Generation'])
    df.loc[idx[0], 'Legendary'] = datos_pokemon_dict.get('Legendary', df.loc[idx[0], 'Legendary'])
    df.loc[idx[0], 'UserAdded'] = True # Asegurarse de que siga siendo True si ya lo era

    guardar_datos(df) # Guarda el DataFrame actualizado
    return True, "Pokémon modificado exitosamente."