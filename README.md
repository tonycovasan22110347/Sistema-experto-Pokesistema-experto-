

# Sistema de Información y Efectividad de Pokémon

## ¡Bienvenido al Sistema Pokexperto\!

Este proyecto es una aplicación de escritorio interactiva desarrollada en Python que permite a los usuarios explorar la vasta base de datos de Pokémon y sus movimientos, analizar sus fortalezas y debilidades estratégicas, y gestionar sus propios registros personalizados de Pokémon.

-----

## 🚀 Características Principales

  * **Búsqueda Detallada de Pokémon:**
      * Visualiza tipos, estadísticas base, mejor estadística.
      * Análisis completo de efectividad defensiva (Fuerte contra, Débil contra, Inmune contra, Neutro contra).
      * **Sugerencias de Counters:** Obtén recomendaciones de Pokémon y movimientos para contrarrestar al Pokémon buscado, basándose en sus debilidades.
  * **Búsqueda y Visualización de Movimientos:**
      * Consulta detalles de cualquier movimiento Pokémon, incluyendo tipo, categoría, poder, precisión, PP y efecto.
  * **Calculadora de Efectividad de Tipos:**
      * Simula combates para entender las interacciones de tipos entre ataques y defensores, mostrando qué tipos son eficaces, poco efectivos, inmunes o neutros.
  * **Gestión de Pokémon Personalizados:**
      * **Agregar Nuevo Pokémon:** Introduce nuevos Pokémon a tu base de datos local.
      * **Modificar Pokémon:** Edita la información de los Pokémon que tú mismo has agregado previamente. Los Pokémon originales del sistema están protegidos contra modificaciones.

-----

## 🛠️ Tecnologías Utilizadas

  * **Python 3.x**
  * **`tkinter`** (incluido con Python): Para la interfaz gráfica de usuario.
  * **`pandas`**: Para la manipulación y gestión eficiente de los datos CSV.
  * **`Pillow`**: Para el manejo y visualización de imágenes.

-----

## 📦 Estructura del Proyecto

```
tu-proyecto/
├── dataset/
│   ├── Pokemon.csv           # Base de datos principal de Pokémon.
│   └── movimientos_pokemon.csv # Base de datos de movimientos Pokémon.
├── base_conocimiento.py      # Módulo para cargar, acceder y guardar datos de CSV.
├── interfaz.py               # Módulo principal de la GUI.
├── motor_inferencia.py       # Módulo con la lógica de negocio y procesamiento de datos.
├── reglas.py                 # Definiciones de tipos y reglas de efectividad Pokémon.
├── Pokemon.PNG               # Imagen del logo de la aplicación.
└── README.md                 # Este archivo.
```

-----

## ⚙️ Instalación y Ejecución

Sigue estos pasos para poner en marcha el sistema en tu máquina local.

### 1\. Requisitos Previos

Asegúrate de tener **Python 3.x** instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

### 2\. Clona el Repositorio (o Descarga)

Si usas Git:

```bash
git clone https://github.com/[tu-usuario]/[tu-repositorio].git
cd [tu-repositorio]
```

Si no, descarga el archivo ZIP del repositorio y extráelo en una carpeta de tu preferencia.

### 3\. Instala las Dependencias

Abre tu terminal o Símbolo del Sistema, navega hasta el directorio raíz del proyecto y ejecuta el siguiente comando:

```bash
pip install pandas Pillow
```

### 4\. Organiza los Archivos de Datos

  * Asegúrate de que la carpeta `dataset/` exista en el directorio raíz de tu proyecto.
  * Coloca `Pokemon.csv` y `movimientos_pokemon.csv` dentro de la carpeta `dataset/`.
  * Asegúrate de que `Pokemon.PNG` esté en el directorio raíz del proyecto, junto con los archivos `.py`.

### 5\. Ejecuta la Aplicación

Desde la terminal en el directorio raíz del proyecto, ejecuta:

```bash
python interfaz.py
```

La ventana principal de la aplicación debería aparecer.


## 📖 Guía de Uso

### Interfaz Principal

Al iniciar la aplicación, verás la ventana principal que te permite interactuar con todas las funcionalidades:

  * **Búsqueda de Pokémon:**
      * Ingresa el nombre de un Pokémon en el campo de texto y haz clic en "Buscar Pokémon".
      * Se mostrarán sus datos (tipos, estadísticas, mejor stat) y su efectividad defensiva.
      * También se presentarán **sugerencias de Pokémon y movimientos** para contrarrestar al Pokémon buscado, basándose en sus debilidades.
  * **Búsqueda de Movimientos:**
      * Utiliza el campo de texto específico para movimientos para ingresar el nombre de un ataque.
      * Haz clic en "Buscar Movimiento" para ver sus detalles (tipo, categoría, poder, etc.).

### Calculadora de Efectividad de Tipos

Haz clic en el botón **"Abrir Calculadora de Tipos"** para abrir una nueva ventana:

  * Selecciona uno o varios tipos de ataque utilizando las casillas de verificación.
  * Haz clic en "Calcular Efectividad" para ver cómo esos tipos atacarían a otros tipos Pokémon.

### Gestión de Pokémon

  * **Agregar Nuevo Pokémon:**
      * Haz clic en **"Agregar Nuevo Pokémon"** para abrir un formulario.
      * Rellena los detalles del nuevo Pokémon (nombre, tipos, estadísticas). El nombre debe ser único.
      * Haz clic en "Guardar Pokémon". Este Pokémon se añadirá a tu base de datos local y estará disponible para búsqueda y modificación.
  * **Modificar Pokémon:**
      * Primero, **busca el Pokémon** que deseas modificar en la interfaz principal.
      * El botón **"Modificar Pokémon" se habilitará** solo si el Pokémon buscado fue **previamente agregado por ti** (no un Pokémon original del CSV).
      * Haz clic en "Modificar Pokémon" para abrir el formulario con los datos precargados.
      * Realiza los cambios y haz clic en "Guardar Cambios".

