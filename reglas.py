# reglas.py

tipos_disponibles = [
    "Acero", "Agua", "Bicho", "Dragón", "Eléctrico", "Fantasma", "Fuego",
    "Hada", "Hielo", "Lucha", "Normal", "Planta", "Psíquico", "Roca",
    "Siniestro", "Tierra", "Veneno", "Volador"
]

# Definición de la efectividad de un tipo de ataque contra un tipo defensor
# Clave: Tipo de ataque
# Valor: Diccionario con listas de tipos defensores para "efectivo", "no_efectivo", "inmune"
efectividad_ataque = {
    "Acero": {
        "efectivo": ["Hada", "Hielo", "Roca"],
        "no_efectivo": ["Fuego", "Agua", "Eléctrico", "Acero"],
        "inmune": []
    },
    "Volador": {
        "efectivo": ["Bicho", "Planta", "Lucha"],
        "no_efectivo": ["Roca", "Acero", "Eléctrico"],
        "inmune": ["Tierra"] # Corrected: Flying is immune to Ground attacks
    },
    "Agua": {
        "efectivo": ["Fuego", "Roca", "Tierra"],
        "no_efectivo": ["Agua", "Planta", "Dragón"],
        "inmune": []
    },
    "Bicho": {
        "efectivo": ["Planta", "Psíquico", "Siniestro"],
        "no_efectivo": ["Lucha", "Volador", "Veneno", "Fantasma", "Acero", "Fuego", "Hada"],
        "inmune": []
    },
    "Dragón": {
        "efectivo": ["Dragón"],
        "no_efectivo": ["Acero"],
        "inmune": ["Hada"]
    },
    "Eléctrico": {
        "efectivo": ["Agua", "Volador"],
        "no_efectivo": ["Eléctrico", "Planta", "Dragón"],
        "inmune": ["Tierra"]
    },
    "Fantasma": {
        "efectivo": ["Psíquico", "Fantasma"],
        "no_efectivo": ["Siniestro"],
        "inmune": ["Normal"]
    },
    "Fuego": {
        "efectivo": ["Bicho", "Acero", "Hielo", "Planta"],
        "no_efectivo": ["Fuego", "Agua", "Roca", "Dragón"],
        "inmune": []
    },
    "Hada": {
        "efectivo": ["Lucha", "Dragón", "Siniestro"],
        "no_efectivo": ["Fuego", "Veneno", "Acero"],
        "inmune": []
    },
    "Hielo": {
        "efectivo": ["Volador", "Tierra", "Planta", "Dragón"],
        "no_efectivo": ["Fuego", "Agua", "Hielo", "Acero"],
        "inmune": []
    },
    "Lucha": {
        "efectivo": ["Normal", "Hielo", "Roca", "Siniestro", "Acero"],
        "no_efectivo": ["Volador", "Veneno", "Bicho", "Psíquico", "Hada"],
        "inmune": ["Fantasma"]
    },
    "Normal": {
        "efectivo": [],
        "no_efectivo": ["Roca", "Acero"],
        "inmune": ["Fantasma"]
    },
    "Planta": {
        "efectivo": ["Agua", "Tierra", "Roca"],
        "no_efectivo": ["Volador", "Veneno", "Bicho", "Acero", "Fuego", "Planta", "Dragón"],
        "inmune": []
    },
    "Psíquico": {
        "efectivo": ["Lucha", "Veneno"],
        "no_efectivo": ["Psíquico", "Acero"],
        "inmune": ["Siniestro"]
    },
    "Roca": {
        "efectivo": ["Volador", "Bicho", "Fuego", "Hielo"],
        "no_efectivo": ["Lucha", "Tierra", "Acero"],
        "inmune": []
    },
    "Siniestro": {
        "efectivo": ["Psíquico", "Fantasma"],
        "no_efectivo": ["Lucha", "Hada", "Siniestro"],
        "inmune": []
    },
    "Tierra": {
        "efectivo": ["Eléctrico", "Fuego", "Veneno", "Roca", "Acero"],
        "no_efectivo": ["Bicho", "Planta"],
        "inmune": ["Volador"]
    },
    "Veneno": {
        "efectivo": ["Planta", "Hada"],
        "no_efectivo": ["Veneno", "Tierra", "Roca", "Fantasma"],
        "inmune": ["Acero"]
    }
}

def calcular_efectividad(tipos_atacantes):
    """
    Calcula la efectividad de un conjunto de tipos de ataque contra otros tipos.
    Retorna cuatro listas: eficaz, no_eficaz, neutro, inmune.
    """
    efectivos = set()
    no_efectivos = set()
    inmunes = set()

    for tipo_atacante in tipos_atacantes:
        if tipo_atacante in efectividad_ataque:
            efectivos.update(efectividad_ataque[tipo_atacante].get("efectivo", []))
            no_efectivos.update(efectividad_ataque[tipo_atacante].get("no_efectivo", []))
            inmunes.update(efectividad_ataque[tipo_atacante].get("inmune", []))
    
    # Asegurarse de que no haya solapamientos
    # Prioridad: Inmune > Efectivo > No Efectivo
    
    # Si un tipo es inmune, no puede ser efectivo ni no efectivo
    efectivos = efectivos - inmunes
    no_efectivos = no_efectivos - inmunes
    
    # Si un tipo es efectivo, no puede ser no efectivo
    no_efectivos = no_efectivos - efectivos

    # Todos los tipos disponibles
    todos_los_tipos = set(tipos_disponibles)
    
    # Los neutros son los que no están en ninguna de las otras categorías
    neutros = todos_los_tipos - efectivos - no_efectivos - inmunes

    return sorted(list(efectivos)), sorted(list(no_efectivos)), sorted(list(neutros)), sorted(list(inmunes))


def obtener_efectividad_defensiva(tipos_defensores):
    """
    Calcula la efectividad defensiva de un Pokémon basado en sus tipos.
    Retorna diccionarios de tipos que son 'fuertes_contra', 'debiles_contra', 'inmunes_contra', 'neutros_contra'.
    """
    multiplicadores = {tipo_ataque: 1.0 for tipo_ataque in tipos_disponibles}

    for tipo_defensor in tipos_defensores:
        if tipo_defensor is None:
            continue
        
        # Iterar a través de todos los tipos de ataque y ajustar multiplicadores
        for tipo_ataque, datos_ataque in efectividad_ataque.items():
            if tipo_defensor in datos_ataque.get("efectivo", []):
                multiplicadores[tipo_ataque] *= 2.0  # Takes double damage
            elif tipo_defensor in datos_ataque.get("no_efectivo", []):
                multiplicadores[tipo_ataque] *= 0.5 # Takes half damage
            # Only consider immune if it's explicitly in the attacking type's immune list against the defending type,
            # it means the defending type is IMMUNE to this attacking type.
            elif tipo_defensor in datos_ataque.get("inmune", []):
                multiplicadores[tipo_ataque] *= 0.0 # Takes zero damage

    # Categorize based on final multipliers
    fuertes_contra = set() # Types that are 2x or 4x effective against the Pokemon (Pokemon is weak to them)
    debiles_contra = set() # Types that are 0.5x or 0.25x effective against the Pokemon (Pokemon is strong against them)
    inmunes_contra = set() # Types that are 0x effective against the Pokemon (Pokemon is immune to them)
    neutros_contra = set() # Types that are 1x effective against the Pokemon

    for tipo_ataque, multi in multiplicadores.items():
        if multi == 0.0:
            inmunes_contra.add(tipo_ataque)
        elif multi >= 2.0: # Could be 2x, 4x, etc.
            fuertes_contra.add(tipo_ataque)
        elif multi <= 0.5 and multi > 0: # Could be 0.5x, 0.25x, etc.
            debiles_contra.add(tipo_ataque)
        else: # Multiplier is 1.0
            neutros_contra.add(tipo_ataque)

    # Ensure no overlaps by giving priority to higher multipliers (inmune > fuerte > débil > neutro)
    # This logic is mostly handled by how the multiplicadores are calculated, but good to ensure uniqueness.
    
    return {
        "fuertes_contra": sorted(list(fuertes_contra)),
        "debiles_contra": sorted(list(debiles_contra)),
        "inmunes_contra": sorted(list(inmunes_contra)),
        "neutros_contra": sorted(list(neutros_contra))
    }