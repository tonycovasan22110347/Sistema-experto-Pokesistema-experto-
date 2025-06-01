Sistema Pokexperto:
Guía de Uso: Sistema de Información y Efectividad de Pokémon
Versión: 1.0
Fecha: 31 de Mayo de 2025
1. Introducción
Bienvenido al "Sistema de Información y Efectividad de Pokémon", una aplicación de escritorio interactiva diseñada para los entusiastas de Pokémon. Esta herramienta te permitirá explorar información detallada de tus Pokémon favoritos, comprender las relaciones de efectividad entre tipos en combate, y personalizar tu propia base de datos añadiendo y modificando Pokémon.

2. Requisitos del Sistema
Para ejecutar esta aplicación, necesitarás:
•	Python: Versión 3.x (recomendado 3.8 o superior).
•	Librerías de Python: 
o	pandas: Para la gestión de datos (pip install pandas)
o	Pillow: Para la carga y visualización de imágenes PNG (pip install Pillow)
o	tkinter (Tkinter): Viene incluido con la mayoría de las instalaciones de Python.

3. Estructura del Proyecto
El sistema está organizado en los siguientes archivos y carpetas, que deben mantenerse juntos en el mismo directorio principal para su correcto funcionamiento:
•	base_conocimiento.py                    # Gestión de la base de datos (carga, guardado, etc.)
•	interfaz.py              		            # Lógica de la Interfaz Gráfica de Usuario (GUI)
•	motor_inferencia.py      	              # Procesamiento de datos y lógica principal
•	reglas.py                	              # Definición de tipos y reglas de efectividad
•	dataset/                	              # Carpeta que contiene el archivo de datos
   └── Pokemon.csv                        # Archivo CSV con la información de los Pokémon
o	Prueba.py                               # (Opcional) Script para pruebas internas del motor de inferencia

4. Preparación y Ejecución
Sigue estos pasos para poner en marcha el sistema:
1.	Asegúrate de tener Python instalado en tu sistema.
2.	Instala las librerías necesarias: Abre tu terminal o Símbolo del Sistema y ejecuta los siguientes comandos: 
o	Bash
o	pip install pandas
o	pip install Pillow

3.	Organiza los Archivos: 
o	Descarga todos los archivos .py (base_conocimiento.py, interfaz.py, motor_inferencia.py, reglas.py, Prueba.py) y la imagen Pokemon.PNG.
o	Crea una nueva carpeta llamada dataset dentro de tu directorio principal del proyecto.
o	Coloca el archivo Pokemon.csv dentro de la carpeta dataset.
o	Asegúrate de que Pokemon.PNG esté directamente en el directorio principal del proyecto, junto a los archivos .py.

4.	Ejecuta la Aplicación: 
o	Abre tu terminal o Símbolo del Sistema.
o	Navega al directorio principal de tu proyecto (donde se encuentra interfaz.py).
o	Ejecuta el siguiente comando: 
	Bash
	python interfaz.py
La ventana principal del "Buscador y Efectividad de Pokémon" debería aparecer.

5. Guía de Uso del Sistema
La aplicación principal se abre en una única ventana desde la cual puedes acceder a todas las funcionalidades.
5.1. Interfaz Principal y Búsqueda de Pokémon
 
Esta es la ventana principal desde donde interactuarás con el sistema.
[Inserta una captura de pantalla de la interfaz principal VACÍA, con el logo, el título "Sistema Pokexperto", el campo de búsqueda, y los tres botones de acción ("Abrir Calculadora de Tipos", "Agregar Nuevo Pokémon", "Modificar Pokémon" - este último deshabilitado).]
1.	Campo de Búsqueda: Ingresa el nombre de un Pokémon (por ejemplo, "Pikachu", "Charizard", "Bulbasaur") en el campo de texto etiquetado "Nombre del Pokémon:".
2.	Botón "Buscar Pokémon": Haz clic en este botón después de ingresar el nombre.
Resultados de la Búsqueda:
 
Si el Pokémon es encontrado, la interfaz se actualizará para mostrar:
•	Información del Pokémon: Nombre y Tipo(s).
•	Mejor Stat: La estadística base más alta del Pokémon.
•	Estadísticas Base: Una tabla horizontal con los valores de HP, Attack, Defense, Sp. Atk, Sp. Def y Speed.
•	Efectividad de Tipos: Una tabla detallada que muestra cómo otros tipos de ataque afectan a este Pokémon: 
o	Fuerte contra: Tipos de ataque a los que el Pokémon es resistente (recibe menos daño).
o	Débil contra: Tipos de ataque a los que el Pokémon es vulnerable (recibe más daño).
o	Inmune contra: Tipos de ataque que no le hacen daño.
o	Neutro contra: Tipos de ataque que le hacen daño normal.
Si el Pokémon no se encuentra, aparecerá un mensaje de error y la información anterior se borrará.
5.2. Calculadora de Efectividad de Tipos
 
Esta funcionalidad te permite calcular la efectividad de uno o más tipos de ataque combinados.
1.	Botón "Abrir Calculadora de Tipos": Haz clic en este botón en la ventana principal. Se abrirá una nueva ventana.
2.	Seleccionar Tipos de Ataque: En la nueva ventana, marca las casillas de verificación correspondientes a los tipos de ataque que deseas calcular. Puedes seleccionar uno o varios tipos.
3.	Botón "Calcular Efectividad": Haz clic en este botón para ver los resultados.

Resultados del Cálculo:
La tabla de resultados mostrará contra qué tipos son:
•	Efectivos contra: Tipos a los que los tipos seleccionados hacen el doble de daño.
•	Poco efectivos contra: Tipos a los que los tipos seleccionados hacen la mitad de daño.
•	Sin efecto contra: Tipos a los que los tipos seleccionados no hacen daño.
•	Neutros contra: Tipos a los que los tipos seleccionados hacen daño normal.
5.3. Agregar Nuevo Pokémon
 
Puedes extender la base de datos local del sistema añadiendo tus propios Pokémon.
1.	Botón "Agregar Nuevo Pokémon": Haz clic en este botón en la ventana principal. Se abrirá una nueva ventana de formulario.
[Inserta una captura de pantalla de la ventana "Agregar Nuevo Pokémon", con los campos de entrada vacíos o con valores predeterminados.]
2.	Rellenar el Formulario: 
o	Nombre: Ingresa el nombre único del nuevo Pokémon.
o	Tipo 1: Selecciona el tipo principal del Pokémon de la lista desplegable.
o	Tipo 2: Opcional. Selecciona un segundo tipo si aplica, o déjalo en blanco.
o	HP, Attack, Defense, Sp. Atk, Sp. Def, Speed: Ingresa los valores numéricos enteros para cada estadística.
3.	Botón "Guardar Pokémon": Haz clic para añadir el Pokémon a la base de datos. 
o	Si los datos son válidos, recibirás un mensaje de éxito y la ventana se cerrará. El Pokémon se guardará en Pokemon.csv.
o	Si hay errores (ej. nombre duplicado, valores no numéricos), aparecerá un mensaje de error.
4.	Verificar el Pokémon Añadido: Puedes buscar el Pokémon recién agregado en la interfaz principal para confirmar que ha sido añadido correctamente.
5.4. Modificar Pokémon
 
Esta función te permite editar la información de los Pokémon que tú mismo has agregado al sistema. Los Pokémon originales del archivo Pokemon.csv no pueden ser modificados.
1.	Buscar el Pokémon a Modificar: En la interfaz principal, busca el nombre del Pokémon que deseas modificar. Importante: Solo los Pokémon que fueron previamente añadidos por el usuario (mediante la función "Agregar Nuevo Pokémon") pueden ser modificados.
[Inserta una captura de pantalla de la interfaz principal con un Pokémon agregado por el usuario buscado (ej. "MiPokemon"), y el botón "Modificar Pokémon" HABILITADO.]
2.	Botón "Modificar Pokémon": Si el Pokémon buscado es un Pokémon agregado por el usuario, este botón se habilitará. Haz clic en él.
[Inserta una captura de pantalla de la ventana "Modificar Pokémon" precargada con los datos de un Pokémon editable.]
3.	Editar el Formulario: La ventana de modificación se abrirá precargada con los datos actuales del Pokémon. Realiza los cambios necesarios en cualquiera de los campos.
4.	Botón "Guardar Cambios": Haz clic para aplicar las modificaciones. 
o	Si los cambios son válidos, recibirás un mensaje de éxito y la ventana se cerrará. Los cambios se guardarán en Pokemon.csv.
o	Si hay errores (ej. nombre duplicado con otro Pokémon, valores no numéricos), aparecerá un mensaje de error.
5.	Verificar Cambios: El sistema automáticamente refrescará la búsqueda del Pokémon en la interfaz principal para mostrar los datos actualizados.

6. Consideraciones y Solución de Problemas
•	Archivo Pokemon.csv faltante o corrupto: Si el sistema no puede encontrar o leer Pokemon.csv en la carpeta dataset, intentará crear uno nuevo con encabezados vacíos. Asegúrate de que el archivo exista y esté en la ruta correcta.
•	Imagen Pokemon.PNG no encontrada: Si la imagen del logo no se carga, verifica que Pokemon.PNG esté en el mismo directorio que interfaz.py.
•	Problemas con Pillow: Si recibes errores relacionados con imágenes, asegúrate de haber instalado Pillow correctamente (pip install Pillow).
•	Valores de Estadísticas: Asegúrate de ingresar solo números enteros positivos para las estadísticas del Pokémon.
•	Nombres Duplicados: El sistema no permite agregar o modificar un Pokémon si su nombre (insensible a mayúsculas/minúsculas) ya existe en la base de datos para otro Pokémon.
