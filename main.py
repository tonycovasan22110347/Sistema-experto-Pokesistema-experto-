import tkinter as tk
from tkinter import messagebox
from reglas import tipos_disponibles, calcular_efectividad # calcular_efectividad now handles combined types correctly

def calcular():
    seleccionados = [tipo for tipo, var in variables.items() if var.get()]
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Selecciona al menos un tipo.")
        return

    eficaz, no_eficaz, neutro, inmune = calcular_efectividad(seleccionados)

    resultado = f"""Tipos seleccionados: {', '.join(seleccionados)}

▶️ Efectivos contra: {', '.join(eficaz) if eficaz else 'Ninguno'}
⛔ Poco efectivos contra: {', '.join(no_eficaz) if no_eficaz else 'Ninguno'}
❌ Sin efecto contra: {', '.join(inmune) if inmune else 'Ninguno'}
🟰 Neutros contra: {', '.join(neutro) if neutro else 'Ninguno'}
"""
    texto_resultado.config(state="normal")
    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, resultado)
    texto_resultado.config(state="disabled")

# Crear ventana
ventana = tk.Tk()
ventana.title("Calculadora de Efectividad Pokémon")

# Variables
variables = {tipo: tk.BooleanVar() for tipo in tipos_disponibles}

# Crear checkboxes
frame_tipos = tk.Frame(ventana)
frame_tipos.pack(padx=10, pady=10)

# Organizar los checkboxes en columnas para una mejor visualización
num_columnas = 4
for i, tipo in enumerate(tipos_disponibles):
    row_num = i // num_columnas
    col_num = i % num_columnas
    chk = tk.Checkbutton(frame_tipos, text=tipo, variable=variables[tipo])
    chk.grid(row=row_num, column=col_num, sticky="w", padx=5, pady=2)

# Botón para calcular
boton_calcular = tk.Button(ventana, text="Calcular Efectividad", command=calcular)
boton_calcular.pack(pady=10)

# Área de texto para mostrar resultados
texto_resultado = tk.Text(ventana, wrap="word", width=60, height=15, state="disabled", bd=2, relief="groove")
texto_resultado.pack(padx=10, pady=10)

ventana.mainloop()