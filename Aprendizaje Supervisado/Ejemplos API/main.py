# Ejemplo de uso de una API en Python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from base_model import BaseModel
import requests
import json
from videojuego_rawg import Videojuego_rawg
from datetime import datetime
import time


def insertar_videojuego(id, nombre, fecha_lanzamiento, imagen, valoracion):
    with Session(engine) as session:  # Crear una sesión para interactuar con la base de datos
        # Consulta para verificar si el videojuego ya existe
        select_stmt = select(Videojuego_rawg).filter_by(id == id)
        # devuelve todas las filas que cumplen la condición de que se repite el id
        existe = session.scalars(select_stmt).all()
        nuevo_videojuego = {}
        if len(existe) == 0:
            nuevo_videojuego = Videojuego_rawg(
                id=id,
                nombre=nombre,
                fecha_lanzamiento=fecha_lanzamiento,
                imagen=imagen,
                valoracion=valoracion
            )
        # Agregar el nuevo videojuego a la sesión
        session.add(nuevo_videojuego)
        session.commit()  # Confirmar los cambios en la base de datos
        print(f"Videojuego insertado: {nuevo_videojuego}")


# Paso 1: Crear la base de datos de ejemplo
# Conexión a una base de datos SQLite. True para el ver el log de SQL, False para no verlo.
engine = create_engine(
    "sqlite+pysqlite:///ejemplo_api.db", echo=True, future=True)
# Crear las tablas en la base de datos según los modelos definidos.
BaseModel.metadata.create_all(engine)


# Paso 2: Obtener datos de la API y almacenarlos en la base de datos
videojuegos = []
key = "tu_api_key_aqui"  # Reemplaza con tu clave de API válida
pagina_inicial = 1
pagina_final = 2  # Número de páginas a obtener
page_size = 100  # Limitar a 100 resultados por página


for pagina in range(pagina_inicial, pagina_final + 1):
    # URL de la API RAWG para obtener videojuegos
    url = f"https://api.rawg.io/api/games?key={key}&page={pagina}&page_size={page_size}"
    cabeceras = {}
    # Establecer un User-Agent personalizado
    cabeceras["User-Agent"] = "MiAplicacion/1.0"
    response = requests.get(url)  # Realizar la solicitud GET a la API
    if response.status_code == 200:
        # Cargar la respuesta JSON (diccionario de Python)
        json_data = json.loads(response.text)
        # Extraer la lista de resultados de videojuegos
        resultados = json_data["results"]
        # Paso 3: Iterar sobre cada videojuego en los resultados e insertar en la base de datos
        for resultado in resultados:
            id = resultado["id"]
            nombre = resultado["name"]
            fecha_lanzamiento = datetime.strptime(
                resultado["released"], "%Y-%m-%d").year if resultado["released"] else None
            imagen = resultado.get("background_image", None)
            valoracion = resultado.get("rating", 0.0)
            insertar_videojuego(
                id, nombre, fecha_lanzamiento, imagen, valoracion)

    else:
        print(f"Error al obtener datos de la API: {response.status_code}")

    if pagina != pagina_final:
        # Esperar 5 segundos entre solicitudes para respetar los límites de la API
        time.sleep(5)
