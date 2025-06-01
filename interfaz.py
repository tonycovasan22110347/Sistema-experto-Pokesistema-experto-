import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from motor_inferencia import analizar_pokemon_por_nombre, agregar_nuevo_pokemon_a_bd, modificar_pokemon_en_bd
from reglas import tipos_disponibles, calcular_efectividad
import os
from PIL import Image, ImageTk

# Variable global para almacenar el Pokémon actualmente cargado (para la modificación)
current_pokemon_data = None

# --- Funciones de la Interfaz Principal ---

def buscar():
    global current_pokemon_data
    nombre = entry_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Advertencia", "Por favor ingresa el nombre de un Pokémon.")
        return

    resultado = analizar_pokemon_por_nombre(nombre)
    if resultado is None:
        messagebox.showerror("Error", f"No se encontró el Pokémon '{nombre}'.")
        # Clear previous info if no Pokémon is found
        label_info_nombre_tipo.config(text="")
        label_info_mejor_stat.config(text="")
        for item in tree_stats.get_children():
            tree_stats.delete(item)
        for item in tree_effectiveness.get_children():
            tree_effectiveness.delete(item)
        boton_modificar_pokemon.config(state="disabled") # Deshabilitar si no se encuentra
        current_pokemon_data = None # Limpiar datos del Pokémon actual
        return

    current_pokemon_data = resultado # Guardar los datos del Pokémon para posible modificación

    # Habilitar/Deshabilitar el botón de modificar según si fue agregado por el usuario
    if current_pokemon_data.get('UserAdded', False): # Default a False si la columna no existe o es None
        boton_modificar_pokemon.config(state="normal")
    else:
        boton_modificar_pokemon.config(state="disabled")

    # Mostrar Nombre y Tipo(s)
    label_info_nombre_tipo.config(text=(
        f"Nombre: {resultado['Nombre']}\n"
        f"Tipo(s): {', '.join(resultado['Tipo(s)'])}"
    ))

    # Mostrar Mejor Stat
    label_info_mejor_stat.config(text=f"Mejor Stat: {resultado['Mejor Stat']}")


    # --- Actualizar Tabla de Stats (Formato Horizontal) ---
    for item in tree_stats.get_children():
        tree_stats.delete(item)

    stats_values = [
        resultado['Stats'].get('HP', 0),
        resultado['Stats'].get('Attack', 0),
        resultado['Stats'].get('Defense', 0),
        resultado['Stats'].get('Sp. Atk', 0),
        resultado['Stats'].get('Sp. Def', 0),
        resultado['Stats'].get('Speed', 0)
    ]
    tree_stats.insert("", "end", values=stats_values)


    # --- Actualizar Tabla de Efectividad de Tipos ---
    for item in tree_effectiveness.get_children():
        tree_effectiveness.delete(item)

    fuertes = resultado['Fuerte contra']
    debiles = resultado['Débil contra']
    inmunes = resultado['Inmune contra']
    neutros = resultado['Neutro contra']

    max_filas = max(len(fuertes), len(debiles), len(inmunes), len(neutros))

    for i in range(max_filas):
        fuerte_val = fuertes[i] if i < len(fuertes) else ""
        debil_val = debiles[i] if i < len(debiles) else ""
        inmune_val = inmunes[i] if i < len(inmunes) else ""
        neutro_val = neutros[i] if i < len(neutros) else ""
        tree_effectiveness.insert("", "end", values=(fuerte_val, debil_val, inmune_val, neutro_val))


# --- Nueva ventana para la Calculadora de Efectividad de Tipos ---

def abrir_calculadora_tipos():
    ventana_calculadora = tk.Toplevel(ventana)
    ventana_calculadora.title("Calculadora de Efectividad de Tipos")
    ventana_calculadora.geometry("650x550")

    variables_calculadora = {tipo: tk.BooleanVar() for tipo in tipos_disponibles}

    frame_tipos_calculadora = tk.LabelFrame(ventana_calculadora, text="Selecciona Tipo(s) de Ataque")
    frame_tipos_calculadora.pack(padx=10, pady=10, fill="x")

    num_columnas_chk = 4
    for i, tipo in enumerate(tipos_disponibles):
        row_num = i // num_columnas_chk
        col_num = i % num_columnas_chk
        chk = tk.Checkbutton(frame_tipos_calculadora, text=tipo, variable=variables_calculadora[tipo])
        chk.grid(row=row_num, column=col_num, sticky="w", padx=5, pady=2)

    boton_calcular_calculadora = tk.Button(ventana_calculadora, text="Calcular Efectividad",
                                            command=lambda: calcular_efectividad_tipos(
                                                variables_calculadora, tree_resultados_calculadora
                                            ))
    boton_calcular_calculadora.pack(pady=10)

    frame_resultados_calculadora = tk.LabelFrame(ventana_calculadora, text="Resultados de Efectividad")
    frame_resultados_calculadora.pack(padx=10, pady=10, fill="both", expand=True)

    columnas_calculadora = ("eficaz", "no_eficaz", "inmune", "neutro")
    tree_resultados_calculadora = ttk.Treeview(frame_resultados_calculadora,
                                               columns=columnas_calculadora,
                                               show="headings")

    tree_resultados_calculadora.heading("eficaz", text="▶️ Efectivos contra")
    tree_resultados_calculadora.heading("no_eficaz", text="⛔ Poco efectivos contra")
    tree_resultados_calculadora.heading("inmune", text="❌ Sin efecto contra")
    tree_resultados_calculadora.heading("neutro", text="🟰 Neutros contra")

    tree_resultados_calculadora.column("eficaz", width=130, anchor="center")
    tree_resultados_calculadora.column("no_eficaz", width=130, anchor="center")
    tree_resultados_calculadora.column("inmune", width=130, anchor="center")
    tree_resultados_calculadora.column("neutro", width=130, anchor="center")

    scrollbar_calculadora = ttk.Scrollbar(frame_resultados_calculadora, orient="vertical", command=tree_resultados_calculadora.yview)
    tree_resultados_calculadora.configure(yscrollcommand=scrollbar_calculadora.set)
    scrollbar_calculadora.pack(side="right", fill="y")

    tree_resultados_calculadora.pack(fill="both", expand=True)

def calcular_efectividad_tipos(variables_calculadora, tree_destino):
    seleccionados = [tipo for tipo, var in variables_calculadora.items() if var.get()]
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Selecciona al menos un tipo para calcular.")
        return

    eficaz, no_eficaz, neutro, inmune = calcular_efectividad(seleccionados)

    for item in tree_destino.get_children():
        tree_destino.delete(item)

    max_filas_calc = max(len(eficaz), len(no_eficaz), len(neutro), len(inmune))
    for i in range(max_filas_calc):
        eficaz_val = eficaz[i] if i < len(eficaz) else ""
        no_eficaz_val = no_eficaz[i] if i < len(no_eficaz) else ""
        inmune_val = inmune[i] if i < len(inmune) else ""
        neutro_val = neutro[i] if i < len(neutro) else ""
        tree_destino.insert("", "end", values=(eficaz_val, no_eficaz_val, inmune_val, neutro_val))


# --- Nueva Ventana para Agregar/Modificar Pokémon (Unificada) ---

def abrir_ventana_agregar_modificar_pokemon(pokemon_a_modificar=None):
    is_modifying = pokemon_a_modificar is not None
    ventana_accion_pokemon = tk.Toplevel(ventana)
    ventana_accion_pokemon.title("Modificar Pokémon" if is_modifying else "Agregar Nuevo Pokémon")
    ventana_accion_pokemon.geometry("400x550")

    entradas = {} # Diccionario para almacenar las referencias a los widgets de entrada

    def crear_campo(parent, row, text, entry_type="entry", options=None, default_value=""):
        tk.Label(parent, text=text + ":").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        if entry_type == "entry":
            entry = tk.Entry(parent, width=30)
            entry.insert(0, default_value)
        elif entry_type == "combobox":
            entry = ttk.Combobox(parent, values=options, state="readonly", width=27)
            entry.set(default_value if default_value in options else (options[0] if options else "")) # Set default value
        entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
        entradas[text] = entry
        return entry

    frame_form = tk.LabelFrame(ventana_accion_pokemon, text="Detalles del Pokémon")
    frame_form.pack(padx=10, pady=10, fill="both", expand=True)

    # Campos de entrada con valores precargados si es modificación
    nombre_default = pokemon_a_modificar['Nombre'] if is_modifying else ""
    tipo1_default = pokemon_a_modificar['Tipo(s)'][0] if is_modifying and pokemon_a_modificar['Tipo(s)'] else ""
    tipo2_default = pokemon_a_modificar['Tipo(s)'][1] if is_modifying and len(pokemon_a_modificar['Tipo(s)']) > 1 else ""

    crear_campo(frame_form, 0, "Nombre", default_value=nombre_default)
    
    tipos_ordenados = sorted(tipos_disponibles) # Para que el combobox tenga un orden consistente
    crear_campo(frame_form, 1, "Tipo 1", "combobox", tipos_ordenados, default_value=tipo1_default)
    
    tipos_con_vacio = [""] + tipos_ordenados # Añadir opción vacía
    crear_campo(frame_form, 2, "Tipo 2", "combobox", tipos_con_vacio, default_value=tipo2_default)

    stats_to_load = pokemon_a_modificar['Stats'] if is_modifying else {}
    crear_campo(frame_form, 3, "HP", default_value=str(stats_to_load.get('HP', "")))
    crear_campo(frame_form, 4, "Attack", default_value=str(stats_to_load.get('Attack', "")))
    crear_campo(frame_form, 5, "Defense", default_value=str(stats_to_load.get('Defense', "")))
    crear_campo(frame_form, 6, "Sp. Atk", default_value=str(stats_to_load.get('Sp. Atk', "")))
    crear_campo(frame_form, 7, "Sp. Def", default_value=str(stats_to_load.get('Sp. Def', "")))
    crear_campo(frame_form, 8, "Speed", default_value=str(stats_to_load.get('Speed', "")))

    def procesar_pokemon():
        datos_pokemon = {}
        try:
            nombre_pokemon = entradas["Nombre"].get().strip()
            if not nombre_pokemon:
                messagebox.showerror("Error de Validación", "El nombre del Pokémon no puede estar vacío.")
                return

            datos_pokemon['Name'] = nombre_pokemon
            
            tipo1 = entradas["Tipo 1"].get().strip()
            if not tipo1 or tipo1 not in tipos_disponibles:
                 messagebox.showerror("Error de Validación", "Selecciona un Tipo 1 válido.")
                 return
            datos_pokemon['Type 1'] = tipo1

            tipo2 = entradas["Tipo 2"].get().strip()
            datos_pokemon['Type 2'] = tipo2 if tipo2 else None

            stats_nombres = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
            for stat_name in stats_nombres:
                stat_val = entradas[stat_name].get().strip()
                if not stat_val.isdigit():
                    messagebox.showerror("Error de Validación", f"El valor de '{stat_name}' debe ser un número entero positivo.")
                    return
                # Asegurarse de que los stats sean positivos
                int_stat_val = int(stat_val)
                if int_stat_val < 0:
                    messagebox.showerror("Error de Validación", f"El valor de '{stat_name}' no puede ser negativo.")
                    return
                datos_pokemon[stat_name] = int_stat_val
            
            if is_modifying:
                pokemon_id = pokemon_a_modificar['ID']
                success, msg = modificar_pokemon_en_bd(pokemon_id, datos_pokemon)
            else:
                success, msg = agregar_nuevo_pokemon_a_bd(datos_pokemon)
            
            if success:
                messagebox.showinfo("Éxito", msg)
                ventana_accion_pokemon.destroy()
                # Opcional: auto-buscar el Pokémon recién agregado/modificado en la interfaz principal
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, nombre_pokemon)
                buscar() # Re-busca para actualizar la interfaz principal
            else:
                messagebox.showerror("Error", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")


    # Botones de acción
    frame_botones = tk.Frame(ventana_accion_pokemon)
    frame_botones.pack(pady=10)

    btn_text = "Guardar Cambios" if is_modifying else "Guardar Pokémon"
    tk.Button(frame_botones, text=btn_text, command=procesar_pokemon).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Cancelar", command=ventana_accion_pokemon.destroy).pack(side="left", padx=5)

# --- Interfaz Principal (Ventana principal) ---

ventana = tk.Tk()
ventana.title("Buscador y Efectividad de Pokémon")

# --- Cargar y mostrar la imagen ---
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "Pokemon.PNG") # Asumiendo que Pokemon.PNG está en el directorio del script

try:
    image = Image.open(image_path)
    ancho_max = 300
    if image.width > ancho_max:
        proporcion = ancho_max / image.width
        alto_nuevo = int(image.height * proporcion)
        image = image.resize((ancho_max, alto_nuevo), Image.Resampling.LANCZOS)

    pokemon_logo = ImageTk.PhotoImage(image)

    label_logo = tk.Label(ventana, image=pokemon_logo)
    label_logo.image = pokemon_logo
    label_logo.pack(pady=(10, 0))
except FileNotFoundError:
    print(f"Error: No se encontró el archivo de imagen en: {image_path}")
    messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen del logo. Asegúrate de que 'Pokemon.PNG' esté en la misma carpeta que 'interfaz.py'.")
except Exception as e:
    print(f"Error al cargar la imagen: {e}")
    messagebox.showerror("Error de Imagen", f"Hubo un error al cargar la imagen del logo: {e}. Asegúrate de tener Pillow instalado (pip install Pillow).")

# --- Título "Sistema Pokexperto" debajo de la imagen ---
label_title = tk.Label(ventana, text="Sistema Pokexperto", font=("Arial", 14, "bold"), fg="blue")
label_title.pack(pady=(0, 10))

# --- Frame para entrada y botón de búsqueda ---
frame_busqueda = tk.Frame(ventana)
frame_busqueda.pack(padx=10, pady=10)

tk.Label(frame_busqueda, text="Nombre del Pokémon:").grid(row=0, column=0, sticky="w")
entry_nombre = tk.Entry(frame_busqueda, width=30)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

boton_buscar = tk.Button(frame_busqueda, text="Buscar Pokémon", command=buscar)
boton_buscar.grid(row=0, column=2, padx=5, pady=5)

# --- Botones de acción general ---
frame_acciones = tk.Frame(ventana)
frame_acciones.pack(pady=5)

boton_abrir_calculadora = tk.Button(frame_acciones, text="Abrir Calculadora de Tipos", command=abrir_calculadora_tipos)
boton_abrir_calculadora.pack(side="left", padx=5)

boton_agregar_pokemon = tk.Button(frame_acciones, text="Agregar Nuevo Pokémon", command=lambda: abrir_ventana_agregar_modificar_pokemon(None))
boton_agregar_pokemon.pack(side="left", padx=5)

boton_modificar_pokemon = tk.Button(frame_acciones, text="Modificar Pokémon", state="disabled", command=lambda: abrir_ventana_agregar_modificar_pokemon(current_pokemon_data))
boton_modificar_pokemon.pack(side="left", padx=5)


# --- Frame para mostrar información básica (Nombre y Tipo) ---
frame_info_basica = tk.LabelFrame(ventana, text="Información del Pokémon")
frame_info_basica.pack(padx=10, pady=5, fill="x")

label_info_nombre_tipo = tk.Label(frame_info_basica, justify=tk.LEFT)
label_info_nombre_tipo.pack(padx=10, pady=2, anchor="w")

label_info_mejor_stat = tk.Label(frame_info_basica, justify=tk.LEFT, font=("Arial", 10, "italic"))
label_info_mejor_stat.pack(padx=10, pady=2, anchor="w")


# --- Frame para Stats en tabla ---
frame_stats = tk.LabelFrame(ventana, text="Estadísticas Base")
frame_stats.pack(padx=10, pady=5, fill="x")

columnas_stats = ("HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed")
tree_stats = ttk.Treeview(frame_stats, columns=columnas_stats, show="headings", height=1)

for col in columnas_stats:
    tree_stats.heading(col, text=col)
    tree_stats.column(col, width=60, anchor="center")

tree_stats.pack(fill="x", expand=False)

# --- Frame para mostrar resultados de efectividad (con Treeview) ---
frame_effectiveness = tk.LabelFrame(ventana, text="Efectividad de Tipos")
frame_effectiveness.pack(padx=10, pady=10, fill="both", expand=True)

columnas_effectiveness = ("fuerte", "debil", "inmune", "neutro")
tree_effectiveness = ttk.Treeview(frame_effectiveness, columns=columnas_effectiveness, show="headings")

tree_effectiveness.heading("fuerte", text="▶️ Fuerte contra")
tree_effectiveness.heading("debil", text="⛔ Débil contra")
tree_effectiveness.heading("inmune", text="❌ Inmune contra")
tree_effectiveness.heading("neutro", text="🟰 Neutro contra")

tree_effectiveness.column("fuerte", width=120, anchor="center")
tree_effectiveness.column("debil", width=120, anchor="center")
tree_effectiveness.column("inmune", width=120, anchor="center")
tree_effectiveness.column("neutro", width=120, anchor="center")

scrollbar_effectiveness = ttk.Scrollbar(frame_effectiveness, orient="vertical", command=tree_effectiveness.yview)
tree_effectiveness.configure(yscrollcommand=scrollbar_effectiveness.set)
scrollbar_effectiveness.pack(side="right", fill="y")

tree_effectiveness.pack(fill="both", expand=True)

ventana.mainloop()