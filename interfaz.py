import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from motor_inferencia import analizar_pokemon_por_nombre, agregar_nuevo_pokemon_a_bd, modificar_pokemon_en_bd, buscar_movimiento_por_nombre, buscar_counters_para_pokemon
from reglas import tipos_disponibles
import os
from PIL import Image, ImageTk
import subprocess # Importar subprocess para ejecutar main.py

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
        # Limpiar información previa si no se encuentra Pokémon
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

    label_info_nombre_tipo.config(text=f"Nombre: {resultado['Name']} - Tipo: {resultado['Type 1 (es)']}" + (f"/{resultado['Type 2 (es)']}" if resultado['Type 2 (es)'] else ""))
    label_info_mejor_stat.config(text=f"Mejor Estadística Base: {resultado['Mejor Stat']} ({resultado.get(resultado['Mejor Stat'], 'N/A')})")

    # Limpiar Treeview de estadísticas
    for item in tree_stats.get_children():
        tree_stats.delete(item)
    # Insertar estadísticas
    tree_stats.insert("", "end", values=(
        resultado.get('HP', 'N/A'), resultado.get('Attack', 'N/A'), resultado.get('Defense', 'N/A'),
        resultado.get('Sp. Atk', 'N/A'), resultado.get('Sp. Def', 'N/A'), resultado.get('Speed', 'N/A')
    ))

    # Limpiar Treeview de efectividad
    for item in tree_effectiveness.get_children():
        tree_effectiveness.delete(item)
    
    efectividad = resultado.get('Efectividad Defensiva', {})
    # Insertar efectividad
    tree_effectiveness.insert("", "end", values=(
        ", ".join(efectividad.get('fuertes_contra', [])) or "Ninguno",
        ", ".join(efectividad.get('debiles_contra', [])) or "Ninguno",
        ", ".join(efectividad.get('inmunes_contra', [])) or "Ninguno",
        ", ".join(efectividad.get('neutros_contra', [])) or "Ninguno"
    ))
    boton_modificar_pokemon.config(state="normal") # Habilitar el botón de modificar

def abrir_ventana_agregar_modificar(modo, pokemon_data=None):
    ventana_am = tk.Toplevel(ventana)
    ventana_am.title("Agregar/Modificar Pokémon" if modo == "agregar" else f"Modificar {pokemon_data['Name']}")
    ventana_am.transient(ventana) # Hace que la ventana de agregar/modificar dependa de la principal
    ventana_am.grab_set() # Bloquea la ventana principal hasta que esta sea cerrada

    campos = ['Name', 'Type 1', 'Type 2', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(ventana_am, text=campo + ":").grid(row=i, column=0, padx=5, pady=2, sticky="w")
        if campo.startswith("Type"):
            # Usar Combobox para los tipos
            cb = ttk.Combobox(ventana_am, values=tipos_disponibles + [""]) # Añadir "" para 'Type 2' opcional
            cb.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            # Guardar referencia al Combobox en el diccionario de entradas
            entradas[campo] = cb
            if modo == "modificar" and pokemon_data:
                # Obtener el tipo en español para preseleccionar en el Combobox
                tipo_espanol = pokemon_data.get(f'{campo} (es)', '')
                cb.set(tipo_espanol)
        else:
            entry = tk.Entry(ventana_am)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            entradas[campo] = entry
            if modo == "modificar" and pokemon_data and campo in pokemon_data:
                entry.insert(0, pokemon_data[campo])

    # Botón Guardar
    if modo == "agregar":
        boton_guardar = tk.Button(ventana_am, text="Guardar", command=lambda: guardar_pokemon_desde_ventana_agregar_modificar("agregar", None, entradas, ventana_am))
    else: # modo == "modificar"
        boton_guardar = tk.Button(ventana_am, text="Guardar Cambios", command=lambda: guardar_pokemon_desde_ventana_agregar_modificar("modificar", pokemon_data['Name'], entradas, ventana_am))
    boton_guardar.grid(row=len(campos), column=0, columnspan=2, pady=10)

def guardar_pokemon_desde_ventana_agregar_modificar(modo, original_name, entradas, ventana_am):
    datos = {campo: entradas[campo].get().strip() for campo in entradas}
    
    # Validar campos numéricos
    stats_numericas = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    for stat in stats_numericas:
        try:
            datos[stat] = int(datos[stat])
            if datos[stat] < 0:
                messagebox.showerror("Error de Validación", f"El valor de {stat} no puede ser negativo.")
                return
        except ValueError:
            messagebox.showerror("Error de Validación", f"Por favor ingresa un valor numérico para {stat}.")
            return
    
    # Validar que los tipos sean válidos (o vacíos si es Type 2)
    for tipo_campo_key in ['Type 1', 'Type 2']:
        tipo_valor = datos[tipo_campo_key]
        if tipo_valor and tipo_valor not in tipos_disponibles:
            if tipo_campo_key == 'Type 2' and tipo_valor == "": # Permitir Type 2 vacío
                continue
            messagebox.showerror("Error de Validación", f"El tipo '{tipo_valor}' no es válido para {tipo_campo_key}. Por favor, selecciona de la lista.")
            return

    # Asegurarse de que Type 1 no esté vacío
    if not datos['Type 1']:
        messagebox.showerror("Error de Validación", "El Tipo 1 no puede estar vacío.")
        return

    # Si Type 2 es un string vacío, asegúralo como None para el procesamiento del motor de inferencia
    if datos['Type 2'] == "":
        datos['Type 2'] = None

    success, mensaje = (agregar_nuevo_pokemon_a_bd(datos) if modo == "agregar" 
                        else modificar_pokemon_en_bd(original_name, datos))
    
    if success:
        messagebox.showinfo("Éxito", mensaje)
        ventana_am.destroy() # Cerrar la ventana de agregar/modificar
        buscar() # Actualizar la interfaz principal (si se modificó el Pokémon actualmente mostrado)
    else:
        messagebox.showerror("Error", mensaje)

def buscar_movimiento_gui():
    nombre_movimiento = entry_nombre_movimiento.get().strip()
    if not nombre_movimiento:
        messagebox.showwarning("Advertencia", "Por favor ingresa el nombre de un movimiento.")
        return

    movimiento_data = buscar_movimiento_por_nombre(nombre_movimiento)
    if movimiento_data:
        info_movimiento = f"Nombre: {movimiento_data.get('Name', 'N/A')}\n" \
                         f"Tipo: {movimiento_data.get('Type', 'N/A')}\n" \
                         f"Categoría: {movimiento_data.get('Category', 'N/A')}\n" \
                         f"Poder: {movimiento_data.get('Power', 'N/A')}\n" \
                         f"Precisión: {movimiento_data.get('Accuracy', 'N/A')}\n" \
                         f"PP: {movimiento_data.get('PP', 'N/A')}\n" \
                         f"Efecto: {movimiento_data.get('Effect', 'N/A')}"
        messagebox.showinfo("Información del Movimiento", info_movimiento)
    else:
        messagebox.showerror("Error", f"No se encontró el movimiento '{nombre_movimiento}'.")

def buscar_counter():
    nombre = entry_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Advertencia", "Por favor ingresa el nombre de un Pokémon para buscar sus counters.")
        return

    counters_data, mensaje = buscar_counters_para_pokemon(nombre)

    if counters_data is None or not counters_data: 
        messagebox.showerror("Error", mensaje)
        return
    
    # Crear una nueva ventana para mostrar los counters
    ventana_counters = tk.Toplevel(ventana)
    ventana_counters.title(f"Counters para {nombre}")
    ventana_counters.transient(ventana)
    ventana_counters.grab_set()

    tk.Label(ventana_counters, text=f"Counters para {nombre}:", font=("Arial", 12, "bold")).pack(pady=10)

    # Tipos que le hacen daño
    frame_tipos_dano = tk.LabelFrame(ventana_counters, text="Tipos que le hacen daño (Debilidades del objetivo)")
    frame_tipos_dano.pack(padx=10, pady=5, fill="x", ipadx=5, ipady=5) 
    tk.Label(frame_tipos_dano, text=", ".join(counters_data['tipos_fuertes_contra']) if counters_data['tipos_fuertes_contra'] else "Ninguno").pack(padx=5, pady=2)

    # Sugerencias de Pokémon
    frame_sugerencias_pokemon = tk.LabelFrame(ventana_counters, text="Sugerencias de Pokémon Counter")
    frame_sugerencias_pokemon.pack(padx=10, pady=5, fill="x", ipadx=5, ipady=5) 
    if counters_data['sugerencias_pokemon']:
        for pkmn_sug in counters_data['sugerencias_pokemon']:
            tk.Label(frame_sugerencias_pokemon, text=pkmn_sug, justify=tk.LEFT).pack(padx=5, pady=1, anchor="w")
    else:
        tk.Label(frame_sugerencias_pokemon, text="No se encontraron sugerencias de Pokémon que exploten sus debilidades principales.").pack(padx=5, pady=2)

    # Sugerencias de Movimientos
    # Mostrar los ataques de los tipos que le hacen más daño al Pokémon buscado
    frame_sugerencias_movimientos = tk.LabelFrame(ventana_counters, text="Ataques Sugeridos (Tipos de Debilidad)")
    frame_sugerencias_movimientos.pack(padx=10, pady=5, fill="x", ipadx=5, ipady=5)
    
    if counters_data['sugerencias_movimientos']:
        for tipo_efectivo, movimientos in counters_data['sugerencias_movimientos'].items():
            if movimientos:
                movs_str = ", ".join(movimientos)
                tk.Label(frame_sugerencias_movimientos, text=f"Tipo {tipo_efectivo}: {movs_str}", justify=tk.LEFT).pack(padx=5, pady=1, anchor="w")
            else:
                tk.Label(frame_sugerencias_movimientos, text=f"Tipo {tipo_efectivo}: No se encontraron ataques sugeridos.", justify=tk.LEFT).pack(padx=5, pady=1, anchor="w")
    else:
        tk.Label(frame_sugerencias_movimientos, text="No se encontraron sugerencias de ataques para los tipos efectivos.", justify=tk.LEFT).pack(padx=5, pady=2)


def abrir_calculadora_efectividad():
    """Abre la aplicación de la calculadora de efectividad en una ventana separada."""
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'main.py')
        subprocess.Popen(['python', script_path])
    except FileNotFoundError:
        messagebox.showerror("Error", "No se pudo encontrar el intérprete de Python o el archivo 'main.py'. Asegúrate de que Python esté en tu PATH y 'main.py' en el mismo directorio.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al abrir la calculadora de efectividad: {e}")


# --- Configuración de la Ventana Principal ---
ventana = tk.Tk()
ventana.title("Pokedex Avanzada")
ventana.geometry("750x850") # Ajustado el tamaño para acomodar la imagen y más espacio

# Frame para la entrada de búsqueda de Pokémon
frame_busqueda = tk.Frame(ventana)
frame_busqueda.pack(padx=10, pady=10)

tk.Label(frame_busqueda, text="Nombre del Pokémon:").pack(side=tk.LEFT, padx=5)
entry_nombre = tk.Entry(frame_busqueda, width=30)
entry_nombre.pack(side=tk.LEFT, padx=5)

boton_buscar = tk.Button(frame_busqueda, text="Buscar Pokémon", command=buscar)
boton_buscar.pack(side=tk.LEFT, padx=5)

# Nuevo botón "Buscar Counter"
boton_buscar_counter = tk.Button(frame_busqueda, text="Buscar Counter", command=buscar_counter)
boton_buscar_counter.pack(side=tk.LEFT, padx=5)

# Sección de la imagen y el texto "sistema pokexperto"
# Asegúrate de que 'pokemon.PNG' esté en el mismo directorio que este script
try:
    img_path = os.path.join(os.path.dirname(__file__), "pokemon.PNG")
    original_img = Image.open(img_path)
    # Redimensionar la imagen si es demasiado grande para la interfaz
    width, height = original_img.size
    new_width = 250 # Ajusta esto según el tamaño deseado
    new_height = int(new_width * (height / width))
    resized_img = original_img.resize((new_width, new_height), Image.LANCZOS)
    pokemon_img = ImageTk.PhotoImage(resized_img)
    
    label_img = tk.Label(ventana, image=pokemon_img)
    label_img.image = pokemon_img # Mantener una referencia para evitar que sea recolectada por el garbage collector
    label_img.pack(pady=10)
    
    label_pokexperto = tk.Label(ventana, text="Sistema Pokexperto", font=("Arial", 14, "bold"))
    label_pokexperto.pack(pady=(0, 10)) # Pequeño padding inferior
except FileNotFoundError:
    messagebox.showwarning("Advertencia", "La imagen 'pokemon.PNG' no se encontró. Asegúrate de que esté en el mismo directorio que 'interfaz.py'.")
    label_img = tk.Label(ventana, text="[IMAGEN NO ENCONTRADA]", fg="red") # Placeholder
    label_img.pack(pady=10)
except Exception as e:
    messagebox.showwarning("Error", f"No se pudo cargar la imagen 'pokemon.PNG': {e}")
    label_img = tk.Label(ventana, text=f"[ERROR AL CARGAR IMAGEN: {e}]", fg="red") # Placeholder
    label_img.pack(pady=10)


# Frame para los botones de acción (Agregar, Modificar, Calculadora)
frame_acciones_pokemon = tk.Frame(ventana)
frame_acciones_pokemon.pack(pady=5)

boton_agregar_pokemon = tk.Button(frame_acciones_pokemon, text="Agregar Nuevo Pokémon", command=lambda: abrir_ventana_agregar_modificar("agregar"))
boton_agregar_pokemon.pack(side=tk.LEFT, padx=5)

boton_modificar_pokemon = tk.Button(frame_acciones_pokemon, text="Modificar Pokémon", command=lambda: abrir_ventana_agregar_modificar("modificar", current_pokemon_data), state="disabled")
boton_modificar_pokemon.pack(side=tk.LEFT, padx=5)

# Botón para abrir la Calculadora de Efectividad de Tipos
boton_calculadora_efectividad = tk.Button(frame_acciones_pokemon, text="Calculadora de Efectividad de Tipos", command=abrir_calculadora_efectividad)
boton_calculadora_efectividad.pack(side=tk.LEFT, padx=5)


# Frame para la información del Pokémon encontrado
frame_info = tk.LabelFrame(ventana, text="Información del Pokémon")
frame_info.pack(padx=10, pady=10, fill="x")

label_info_nombre_tipo = tk.Label(frame_info, text="")
label_info_nombre_tipo.pack(anchor="w", padx=5, pady=2)

label_info_mejor_stat = tk.Label(frame_info, text="")
label_info_mejor_stat.pack(anchor="w", padx=5, pady=2)

frame_stats = tk.LabelFrame(ventana, text="Estadísticas Base")
frame_stats.pack(padx=10, pady=10, fill="x")

columnas_stats = ("HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed")
tree_stats = ttk.Treeview(frame_stats, columns=columnas_stats, show="headings", height=1)

for col in columnas_stats:
    tree_stats.heading(col, text=col)
    tree_stats.column(col, width=60, anchor="center")
tree_stats.pack(fill="x", expand=False)

frame_effectiveness = tk.LabelFrame(ventana, text="Efectividad de Tipos")
frame_effectiveness.pack(padx=10, pady=10, fill="both", expand=True)

columnas_effectiveness = ("fuerte", "debil", "inmune", "neutro")
tree_effectiveness = ttk.Treeview(frame_effectiveness, columns=columnas_effectiveness, show="headings")

tree_effectiveness.heading("fuerte", text="⛔ Debil contra")
tree_effectiveness.heading("debil", text="▶️ Fuerte contra")
tree_effectiveness.heading("inmune", text="❌ Inmune contra")
tree_effectiveness.heading("neutro", text="🟰 Neutro contra")

tree_effectiveness.column("fuerte", width=150, anchor="w")
tree_effectiveness.column("debil", width=150, anchor="w")
tree_effectiveness.column("inmune", width=150, anchor="w")
tree_effectiveness.column("neutro", width=150, anchor="w")
tree_effectiveness.pack(fill="both", expand=True)


# Separador para la sección de Movimientos
ttk.Separator(ventana, orient='horizontal').pack(fill='x', padx=10, pady=10)

# Frame para la búsqueda de Movimientos
frame_busqueda_movimiento = tk.Frame(ventana)
frame_busqueda_movimiento.pack(padx=10, pady=10)

tk.Label(frame_busqueda_movimiento, text="Nombre del Movimiento:").pack(side=tk.LEFT, padx=5)
entry_nombre_movimiento = tk.Entry(frame_busqueda_movimiento, width=30)
entry_nombre_movimiento.pack(side=tk.LEFT, padx=5)

boton_buscar_movimiento = tk.Button(frame_busqueda_movimiento, text="Buscar Movimiento", command=buscar_movimiento_gui)
boton_buscar_movimiento.pack(side=tk.LEFT, padx=5)


# Ejecutar el bucle principal de la aplicación
ventana.mainloop()