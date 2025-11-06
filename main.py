"""
Hicimos un Gestor de Carreras Universitarias
Estructura de datos: País / Provincia / Facultad -> CSV(s) con carreras

Funcionalidades:
- Exploración recursiva de la estructura de carpetas para encontrar CSV
- CRUD sobre carreras (añadir / editar / eliminar) en un CSV concreto
- Validaciones (duración y cupos > 0, modalidad válida)
- Estadísticas (promedio duración, cupos totales)
- Exportar listado consolidado a CSV
"""

import os,csv,sys

# Carpeta base donde están las carpetas por país/provincia/facultad.
# Mantener la estructura de ejemplo: <carpeta_del_proyecto>/Argentina/...
RUTA_BASE = os.path.join(os.path.dirname(__file__), "Argentina")

# Modalidades permitidas para una carrera
MODALIDADES = {"Presencial", "Virtual", "Mixta"}


def buscar_archivos_csv(raiz):
    """
    Recorre recursivamente la carpeta `raiz` y devuelve una lista con las
    rutas de todos los archivos que terminen en .csv
    """
    archivos = []
    for ruta_dir, dirs, files in os.walk(raiz):
        for nombre in files:
            if nombre.lower().endswith(".csv"):
                archivos.append(os.path.join(ruta_dir, nombre))
    return archivos


def leer_csv(ruta):
    """
    Lee un CSV y devuelve:
    - lista de diccionarios (filas)
    - lista de nombres de columnas (fieldnames)
    """
    with open(ruta, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        filas = list(lector)
        campos = lector.fieldnames
    return filas, campos


def escribir_csv(ruta, filas, nombres_campos):
    """
    Escribe la lista de diccionarios `filas` en el archivo `ruta`
    usando `nombres_campos` como encabezado.
    """
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=nombres_campos)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(fila)


def validar_registro(registro):
    """
    Valida que:
    - duracion_anios y cupos_anuales sean enteros > 0
    - modalidad esté en MODALIDADES
    - id y nombre_carrera no estén vacíos
    Devuelve (True, "") si OK, o (False, "mensaje") si hay error.
    """
    try:
        dur = int(registro.get("duracion_anios", ""))
        cup = int(registro.get("cupos_anuales", ""))
        if dur <= 0 or cup <= 0:
            return False, "duracion_anios y cupos_anuales deben ser > 0"
    except Exception:
        return False, "duracion_anios y cupos_anuales deben ser enteros"
    if registro.get("modalidad") not in MODALIDADES:
        return False, f"modalidad debe ser una de {MODALIDADES}"
    if not registro.get("id") or not registro.get("nombre_carrera"):
        return False, "id y nombre_carrera no pueden estar vacíos"
    return True, ""


def listar_todas_las_carreras():
    """
    Recorre todos los CSV y muestra por consola cada carrera encontrada
    junto con el archivo origen.
    """
    archivos = buscar_archivos_csv(RUTA_BASE)
    todas = []
    for ruta in archivos:
        filas, campos = leer_csv(ruta)
        for f in filas:
            f["_archivo_origen"] = ruta
            todas.append(f)
    if not todas:
        print("No se encontraron carreras.")
        return
    # Imprime cada registro de forma legible
    for r in todas:
        print(f'{r.get("id")} | {r.get("nombre_carrera").title()} | {r.get("duracion_anios")} años | '
              f'{r.get("cupos_anuales")} cupos | {r.get("modalidad")} | {r.get("_archivo_origen")}')


def seleccionar_csv():
    """
    Muestra al usuario la lista de CSV disponibles y le permite elegir uno.
    Devuelve la ruta seleccionada o None si canceló/seleccionó inválido.
    """
    archivos = buscar_archivos_csv(RUTA_BASE)
    if not archivos:
        print("No hay archivos CSV en la estructura de carpetas.")
        return None
    print("Elija un archivo CSV donde operar:")
    for i, ruta in enumerate(archivos, 1):
        print(f"{i}) {ruta}")
    elec = input("Número (Enter para cancelar): ").strip()
    if not elec:
        return None
    try:
        idx = int(elec) - 1
        return archivos[idx]
    except Exception:
        print("Selección inválida.")
        return None


def agregar_carrera():
    """
    Agrega una nueva carrera al CSV seleccionado.
    Pide al usuario el valor para cada columna (según el header).
    """
    ruta = seleccionar_csv()
    if not ruta:
        return
    filas, campos = leer_csv(ruta)
    nuevo = {}
    for campo in campos:
        if campo=="modalidad":
            valor = input(f"{campo}: ").strip().title()
        else:
            valor = input(f"{campo}: ").strip()
        nuevo[campo] = valor
    ok, msg = validar_registro(nuevo)
    if not ok:
        print("Error de validación:", msg)
        return
    filas.append(nuevo)
    escribir_csv(ruta, filas, campos)
    print("Carrera añadida.")


def buscar_por_id(id_buscar):
    """
    Busca una carrera por su ID en todos los CSV.
    Si la encuentra devuelve: (ruta_archivo, filas, campos, registro)
    Si no la encuentra devuelve: (None, None, None, None)
    """
    archivos = buscar_archivos_csv(RUTA_BASE)
    for ruta in archivos:
        filas, campos = leer_csv(ruta)
        for fila in filas:
            if fila.get("id") == id_buscar:
                return ruta, filas, campos, fila
    return None, None, None, None


def editar_carrera():
    """
    Edita una carrera buscándola por ID. Pide campo por campo (salteo id).
    """
    id_ = input("ID de la carrera a editar: ").strip()
    ruta, filas, campos, registro = buscar_por_id(id_)
    if not ruta:
        print("No encontrada.")
        return
    print("Registro actual:")
    print(registro)
    for campo in campos:
        if campo == "id":
            continue  # no permitir editar el id por simplicidad
        nuevo = input(f"{campo} [{registro.get(campo)}]: ").strip()
        if nuevo:
            registro[campo] = nuevo
    ok, msg = validar_registro(registro)
    if not ok:
        print("Error de validación:", msg)
        return
    escribir_csv(ruta, filas, campos)
    print("Actualizada.")


def eliminar_carrera():
    """
    Elimina una carrera por su ID (pide confirmación).
    """
    id_ = input("ID de la carrera a eliminar: ").strip()
    ruta, filas, campos, registro = buscar_por_id(id_)
    if not ruta:
        print("No encontrada.")
        return
    confirma = input(f"Confirmar eliminar {id_} (s/N): ").strip().lower()
    if confirma != "s":
        print("Cancelado.")
        return
    filas_nuevas = [f for f in filas if f.get("id") != id_]
    escribir_csv(ruta, filas_nuevas, campos)
    print("Eliminada.")


def estadisticas():
    """
    Calcula y muestra estadísticas simples sobre todas las carreras:
    - cantidad de carreras
    - cupos totales
    - duración media en años
    """
    archivos = buscar_archivos_csv(RUTA_BASE)
    total_carreras = 0
    total_cupos = 0
    total_duracion = 0
    for ruta in archivos:
        filas, campos = leer_csv(ruta)
        for f in filas:
            try:
                total_carreras += 1
                total_cupos += int(f.get("cupos_anuales", 0))
                total_duracion += int(f.get("duracion_anios", 0))
            except Exception:
                # Si hay datos mal formateados, los ignoramos en la estadística
                pass
    if total_carreras == 0:
        print("No hay datos.")
        return
    print(f"Carreras: {total_carreras}")
    print(f"Cupos totales: {total_cupos}")
    print(f"Duración media (años): {total_duracion / total_carreras:.2f}")


def exportar_consolidado():
    """
    Exporta todas las carreras encontradas en un único CSV cuyo nombre
    se solicita al usuario.
    """
    archivos = buscar_archivos_csv(RUTA_BASE)
    salida = []
    nombres_campos = None
    for ruta in archivos:
        filas, campos = leer_csv(ruta)
        if nombres_campos is None:
            nombres_campos = campos
        for f in filas:
            f["_archivo_origen"] = ruta
            salida.append(f)
    if not salida:
        print("Nada para exportar.")
        return
    destino = input("Nombre de archivo de salida (ej: consolidado.csv): ").strip()
    if not destino:
        print("Cancelado.")
        return
    # combinamos los campos originales + campo _archivo_origen
    fnames = list(nombres_campos) + ["_archivo_origen"]
    with open(destino, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=fnames)
        escritor.writeheader()
        for fila in salida:
            escritor.writerow(fila)
    print(f"Exportado a {destino}")


def imprimir_menu():
    """
    Muestra el menú principal al usuario.
    """
    print("""\n--- Gestor de Carreras Universitarias ---
1) Listar todas las carreras
2) Añadir carrera (en un CSV existente)
3) Editar carrera (por id)
4) Eliminar carrera (por id)
5) Estadísticas
6) Exportar consolidado a CSV
7) Salir
""")


def main():
    """
    Punto de entrada del programa.
    Verifica que exista la carpeta base y muestra el menú en bucle.
    """
    if not os.path.exists(RUTA_BASE):
        print("No se encontró la carpeta base:", RUTA_BASE)
        sys.exit(1)
    while True:
        imprimir_menu()
        opcion = input("Opción: ").strip()
        match opcion:
            case "1":
                listar_todas_las_carreras()
            case "2": 
                agregar_carrera()
            case "3":
                editar_carrera()
            case "4":
                eliminar_carrera()
            case "5":
                estadisticas()
            case "6":
                exportar_consolidado()
            case "7":
                print("Terminando codigo... Chau")
                break
            case _:
                print("Opcion invalida.")

if __name__ == "__main__":
    main()
