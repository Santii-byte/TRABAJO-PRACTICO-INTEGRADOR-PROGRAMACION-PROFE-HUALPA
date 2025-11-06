
# Ejercicio Final Integrador: Gestión Jerárquica de Datos

**Materia:** Programación 

**Tema:** Persistencia jerárquica y manejo de archivos CSV en Python

---

## Estructura de datos

El proyecto utiliza una **estructura de persistencia jerárquica** basada en directorios, que representa la relación entre  **país, provincia y facultad** .

Cada carpeta contiene archivos CSV donde se almacenan las carreras correspondientes.

```
Argentina/
│
├── Buenos_Aires/
│   ├── UBA/
│   │   └── uba_ingenieria.csv
│   └── UNLP/
│       └── unlp_ciencias.csv
│
└── Cordoba/
    └── UNC/
        └── unc_carreras.csv
```

* **Nivel 1:** País
* **Nivel 2:** Provincia
* **Nivel 3:** Facultad
* **Nivel 4 (hojas):** Archivos CSV con las carreras (datos persistentes)

Cada archivo CSV mantiene la siguiente estructura de columnas:

`id, nombre_carrera, duracion_anios, cupos_anuales, modalidad`

---

## Lógica de filtrado y almacenamiento

El sistema **recorre recursivamente** toda la jerarquía de carpetas, detectando automáticamente los archivos `.csv` que contengan carreras.

Este enfoque permite:

1. **Filtrar y acceder a datos específicos** según su ubicación (por país, provincia o facultad).
2. **Mantener independencia entre entidades** , ya que cada facultad tiene su propio archivo.
3. **Persistir los cambios directamente en los CSV** , garantizando que los datos se conserven después de cerrar el programa.

> El recorrido recursivo se realiza con funciones que usan `os.walk()`
>
> para explorar todas las subcarpetas a partir de la raíz `Argentina/`.

---

## Instrucciones de uso

### Requisitos

* Python 3.8 o superior
* No requiere librerías externas

### Ejecución

1. Descomprimir el archivo `universidades_project.zip`
2. Abrir una terminal dentro de la carpeta `universidades_project`
3. Ejecutar el programa principal:
   ```bash
   python3 main.py
   ```
4. Navegar por el menú interactivo:

```
--- Gestor de Carreras Universitarias ---
1) Listar todas las carreras
2) Añadir carrera (en un CSV existente)
3) Editar carrera (por ID)
4) Eliminar carrera (por ID)
5) Estadísticas
6) Exportar consolidado a CSV
7) Salir
```

---

## Validaciones implementadas

* `duracion_anios` y `cupos_anuales` deben ser **enteros positivos**
* `modalidad` debe pertenecer a: **Presencial, Virtual o Mixta**
* `id` y `nombre_carrera` no pueden estar vacíos

---

## Estadísticas disponibles

El sistema puede calcular:

* Cantidad total de carreras
* Total de cupos anuales
* Promedio de duración de las carreras (en años)

---

## Persistencia jerárquica

Cada operación (agregar, eliminar o modificar) se aplica directamente sobre el archivo CSV correspondiente, garantizando la  **persistencia de datos** .

Al iniciar el programa, se  **vuelven a leer todos los CSV** , manteniendo la información actualizada.

Este modelo simula un **sistema de almacenamiento descentralizado** donde las facultades son unidades autónomas de datos, y el programa principal actúa como un  **agregador jerárquico** .

---

## Autores

Proyecto desarrollado por Santino Barone y Maximo Quiroga
