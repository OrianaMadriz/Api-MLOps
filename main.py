from typing import Union
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Cargar el dataset
data = pd.read_csv('data_funciones.csv')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/peliculas_mes/{month}")
def peliculas_mes(month: str):
    # Nos quedamos solo con un dataframe con las peliculas de ese mes
    df_month = data[data['release_month'].str.lower() == month.lower()]
    
    # Obtenemos la cantidad de películas estrenadas ese mes
    cantidad_peliculas = len(df_month)
    
    # Devolvemos un diccionario con el nombre del mes y la cantidad de películas estrenadas ese mes
    return {'month': month.capitalize(), 'amount': cantidad_peliculas}

@app.get("/peliculas_dia/{day}")
def peliculas_dia(day: str):
    # Nos quedamos solo con un dataframe con las peliculas de ese día
    df_day = data[data['release_day'].str.lower() == day.lower()]
    
    # Obtenemos la cantidad de películas estrenadas ese día
    cantidad_peliculas = len(df_day)
    
    # Devolvemos un diccionario con el nombre del día y la cantidad de películas estrenadas ese día
    return {'day': day.capitalize(), 'amount': cantidad_peliculas}

@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
    # Nos quedamos solo con un dataframe con las peliculas de esa colección proporcionada
    df_collection = data[data['collection_name'] == franquicia]

    # Obtenemos la cantidad de películas en la colección
    cantidad_peliculas = len(df_collection)

    # Calculamos el promedio y el total de la ganancia para las películas de la colección
    mean_revenue = df_collection['revenue'].mean()
    total_revenue = df_collection['revenue'].sum()

    # Devolvemos un diccionario con la información
    return {
        'collection_name': franquicia,
        'movies_amount': cantidad_peliculas,
        'total_revenue': total_revenue,
        'mean_revenue': mean_revenue
    }

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
    # Nos quedamos solo con un dataframe con las peliculas de ese país proporcionado
    columnas_pais = [f'pco_name_{i}' for i in range(25)]
    df_country = data[data[columnas_pais].eq(pais).any(axis=1)]    
    
    # Obtenemos la cantidad de películas producidas en el país
    movies_amount = df_country.shape[0]
    
    # Devolvemos un diccionario con la información
    return {
        'country': pais,
        'movies_amount': movies_amount
    }

@app.get("/productoras/{productora}")
def productoras(productora: str):
    # nos quedamos solo con un dataframe con las peliculas de esa productora proporcionada
    columnas_productoras = [f'pc_name_{i}' for i in range(26)]
    df_pc = data[data[columnas_productoras].eq(productora).any(axis=1)]

    # calculamos la ganancia total de las películas de la productora
    total_revenue = df_pc['revenue'].sum()

    # contamos la cantidad de películas asociadas a la productora
    movies_amount = df_pc.shape[0]

    # devolvemos un diccionario con la información
    return {
        'production_companies': productora,
        'total_revenue': total_revenue,
        'movies_amount': movies_amount
    }

# Convertir columnas numéricas a tipos de datos apropiados
data['budget'] = pd.to_numeric(data['budget'], errors='coerce')
data['revenue'] = pd.to_numeric(data['revenue'], errors='coerce')
data['return'] = pd.to_numeric(data['return'], errors='coerce')
data['release_year'] = pd.to_numeric(data['release_year'], errors='coerce')

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Convertir columnas numéricas a tipos de datos apropiados
data['budget'] = pd.to_numeric(data['budget'], errors='coerce')
data['revenue'] = pd.to_numeric(data['revenue'], errors='coerce')
data['return'] = pd.to_numeric(data['return'], errors='coerce')
data['release_year'] = pd.to_numeric(data['release_year'], errors='coerce')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/retorno/{pelicula}")
def retorno(pelicula: str):
    # Eliminar filas duplicadas basadas en la columna 'title'
    data_unique = data.drop_duplicates(subset='title')

    # Nos quedamos solo con un dataframe con los datos de esa película proporcionada
    movie_data = data_unique[data_unique['title'] == pelicula]

    # Verificar si se encontró la película
    if len(movie_data) == 0:
        return {'error': 'Película no encontrada'}

    # Obtener los valores de las columnas de interés
    budget = movie_data['budget'].iloc[0].item()
    revenue = movie_data['revenue'].iloc[0].item()
    retur = movie_data['return'].iloc[0].item()
    release_year = movie_data['release_year'].iloc[0].item()

    # Devolver un diccionario con la información
    informacion_pelicula = {
        'pelicula': pelicula,
        'inversion': budget,
        'ganancia': revenue,
        'retorno': retur,
        'año': release_year
    }

    return informacion_pelicula