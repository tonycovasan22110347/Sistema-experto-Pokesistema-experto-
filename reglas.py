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
    "Hielo": {
        "efectivo": ["Dragón", "Planta", "Tierra", "Volador"],
        "no_efectivo": ["Fuego", "Agua", "Hielo", "Acero"],
        "inmune": []
    },
    "Planta": {
        "efectivo": ["Agua", "Roca", "Tierra"],
        "no_efectivo": ["Acero", "Bicho", "Dragón", "Fuego", "Planta", "Volador", "Veneno"],
        "inmune": []
    },
    "Bicho": {
        "efectivo": ["Planta", "Psíquico", "Siniestro"],
        "no_efectivo": ["Acero", "Fantasma", "Fuego", "Hada", "Lucha", "Volador", "Veneno"],
        "inmune": []
    },
    "Eléctrico": {
        "efectivo": ["Agua", "Volador"],
        "no_efectivo": ["Dragón", "Eléctrico", "Planta"],
        "inmune": ["Tierra"]
    },
    "Lucha": {
        "efectivo": ["Acero", "Hielo", "Normal", "Roca", "Siniestro"],
        "no_efectivo": ["Bicho", "Hada", "Psíquico", "Volador", "Veneno"], # Corrected key name from no_eficaz
        "inmune": ["Fantasma"]
    },
    "Psíquico": {
        "efectivo": ["Lucha", "Veneno"],
        "no_efectivo": ["Acero", "Psíquico"], # Corrected key name from no_eficaz
        "inmune": ["Siniestro"]
    },
    "Fuego": {
        "efectivo": ["Acero", "Bicho", "Hielo", "Planta"],
        "no_efectivo": ["Agua", "Dragón", "Fuego", "Roca"],
        "inmune": []
    },
    "Tierra": {
        "efectivo": ["Acero", "Eléctrico", "Fuego", "Roca", "Veneno"],
        "no_efectivo": ["Bicho", "Planta"],
        "inmune": ["Volador"]
    },
    "Normal": {
        "efectivo": [],
        "no_efectivo": ["Acero", "Roca"],
        "inmune": ["Fantasma"]
    },
    "Veneno": {
        "efectivo": ["Hada", "Planta"],
        "no_efectivo": ["Fantasma", "Roca", "Tierra", "Veneno"],
        "inmune": ["Acero"]
    },
    "Roca": {
        "efectivo": ["Bicho", "Fuego", "Hielo", "Volador"],
        "no_efectivo": ["Acero", "Lucha", "Tierra"],
        "inmune": []
    },
    "Hada": {
        "efectivo": ["Dragón", "Lucha", "Siniestro"],
        "no_efectivo": ["Acero", "Fuego", "Veneno"],
        "inmune": []
    },
    "Dragón": {
        "efectivo": ["Dragón"],
        "no_efectivo": ["Acero"],
        "inmune": ["Hada"]
    },
    "Fantasma": {
        "efectivo": ["Fantasma", "Psíquico"],
        "no_efectivo": ["Siniestro"],
        "inmune": ["Normal"]
    },
    "Siniestro": {
        "efectivo": ["Fantasma", "Psíquico"],
        "no_efectivo": ["Lucha", "Siniestro", "Hada"],
        "inmune": []
    }
}

def calcular_efectividad(tipos_ataque):
    """
    Calcula la efectividad de un conjunto de tipos de ataque contra otros tipos (cuando ATACAN).
    Retorna sets de tipos que son eficaces, poco eficaces, neutros e inmunes.
    """
    eficaz = set()
    no_eficaz = set()
    inmune = set()
    neutro = set(tipos_disponibles)

    for tipo_ataque in tipos_ataque:
        datos = efectividad_ataque.get(tipo_ataque, {})
        eficaz.update(datos.get("efectivo", []))
        no_eficaz.update(datos.get("no_efectivo", []))
        inmune.update(datos.get("inmune", []))

    # Prioridad: Inmune > Poco Eficaz > Eficaz > Neutro
    # Un tipo inmune no puede ser efectivo o poco eficaz
    eficaz -= inmune
    no_eficaz -= inmune

    # Un tipo poco eficaz no puede ser eficaz
    eficaz -= no_eficaz

    # Los neutros son los que no cayeron en ninguna de las otras categorías
    neutro -= eficaz
    neutro -= no_eficaz
    neutro -= inmune

    return sorted(list(eficaz)), sorted(list(no_eficaz)), sorted(list(neutro)), sorted(list(inmune))


def obtener_efectividad_defensiva(tipos_defensor):
    """
    Calcula la efectividad de ataques de otros tipos contra un Pokémon con los tipos dados (DEFENSA).
    Retorna sets de tipos que son débiles contra el Pokémon, fuertes contra el Pokémon, inmunes al Pokémon, y neutros.
    """
    # Initialize multipliers for all possible attacking types
    multiplicadores = {tipo: 1.0 for tipo in tipos_disponibles}

    for tipo_defensor in tipos_defensor:
        for tipo_ataque, datos_ataque in efectividad_ataque.items():
            # If the current defending type is in the "efectivo" list of this attacking type,
            # it means the defending type is WEAK against this attacking type.
            if tipo_defensor in datos_ataque.get("efectivo", []):
                multiplicadores[tipo_ataque] *= 2.0  # Takes double damage

            # If the current defending type is in the "no_efectivo" list of this attacking type,
            # it means the defending type is RESISTANT (strong) against this attacking type.
            elif tipo_defensor in datos_ataque.get("no_efectivo", []):
                multiplicadores[tipo_ataque] *= 0.5  # Takes half damage

            # If the current defending type is in the "inmune" list of this attacking type,
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
    neutros_contra -= (fuertes_contra | debiles_contra | inmunes_contra)
    debiles_contra -= inmunes_contra
    fuertes_contra -= inmunes_contra

    return sorted(list(fuertes_contra)), sorted(list(debiles_contra)), sorted(list(inmunes_contra)), sorted(list(neutros_contra))