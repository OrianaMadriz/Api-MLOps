from typing import Union
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Cargar el dataset
data = pd.read_csv('data_funciones.csv')

@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str):
    # nos quedamos solo con un dataframe con las peliculas de ese mes
    df_mes = data[data['mes'].str.lower() == mes.lower()]
    
    # obtenemos la cantidad de películas estrenadas ese mes
    cantidad_peliculas = len(df_mes)
    
    # devolvemos un diccionario con el nombre del mes y la cantidad de películas estrenadas ese mes
    return {'Mes': mes.capitalize(), 'Cantidad': cantidad_peliculas}

@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia: str):
    # nos quedamos solo con un dataframe con las peliculas de ese dia
    df_dia = data[data['dia'].str.lower() == dia.lower()]
    
    # obtenemos la cantidad de películas estrenadas ese dia
    cantidad_peliculas = len(df_dia)
    
    # devolvemos un diccionario con el nombre del dia y la cantidad de películas estrenadas ese dia
    return {'Dia': dia.capitalize(), 'Cantidad': cantidad_peliculas}

@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
      # nos quedamos solo con un dataframe con las peliculas de esa colección proporcionada
    df_franquicia = data[data['collection_name'] == franquicia]

    # obtenemos la cantidad de películas estrenadas ese dia
    cantidad_peliculas = len(df_franquicia)
    
    # calculamos el promedio y el total de la ganancia para las películas de la colección
    ganancia_promedio = df_franquicia['revenue'].mean()
    ganancia_total = df_franquicia['revenue'].sum()
    
    # devolvemos un diccionario con la información
    return {
            'Franquicia': franquicia,
            'Cantidad':cantidad_peliculas,
            'Ganancia_total': ganancia_total,
            'Ganancia_promedio': ganancia_promedio
        
    }

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
   # nos quedamos solo con un dataframe con las peliculas de ese pais proporcionado
    columnas_pais = [f'pco_name_{i}' for i in range(25)]
    df_pais = data[data[columnas_pais].eq(pais).any(axis=1)]    
    
    # obtenemos la cantidad de películas producidas en el país
    cantidad = df_pais.shape[0]
    
    # devolvemos un diccionario con la información
    return {
        'Pais': pais,
        'Cantidad': cantidad
    }

@app.get("/productoras/{productora}")
def productoras(productora: str):
    # nos quedamos solo con un dataframe con las peliculas de esa productora proporcionada
    columnas_productoras = [f'pc_name_{i}' for i in range(26)]
    df_pc = data[data[columnas_productoras].eq(productora).any(axis=1)]

    # calculamos la ganancia total de las películas de la productora
    ganancia_total = df_pc['revenue'].sum()

    # contamos la cantidad de películas asociadas a la productora
    cantidad = df_pc.shape[0]

    # devolvemos un diccionario con la información
    return {
        'Productora': productora,
        'Ganancia_total': ganancia_total,
        'Cantidad': cantidad
    }

# Convertir columnas numéricas a tipos de datos apropiados
data['budget'] = pd.to_numeric(data['budget'], errors='coerce')
data['revenue'] = pd.to_numeric(data['revenue'], errors='coerce')
data['return'] = pd.to_numeric(data['return'], errors='coerce')
data['release_year'] = pd.to_numeric(data['release_year'], errors='coerce')


@app.get("/retorno/{pelicula}")
def retorno(pelicula: str):
   # Eliminar filas duplicadas basadas en la columna 'title'
    data_unica = data.drop_duplicates(subset='title')

    # Nos quedamos solo con un dataframe con los datos de esa película proporcionada
    data_pelicula = data_unica[data_unica['title'] == pelicula]

    # Verificar si se encontró la película
    if len(data_pelicula) == 0:
        return {'error': 'Película no encontrada'}

    # Obtener los valores de las columnas de interés
    inversion = data_pelicula['budget'].iloc[0].item()
    ganancia = data_pelicula['revenue'].iloc[0].item()
    retorno = data_pelicula['return'].iloc[0].item()
    anio = data_pelicula['release_year'].iloc[0].item()

    # Devolver un diccionario con la información
    informacion_pelicula = {
        'Pelicula': pelicula,
        'Inversion': inversion,
        'Ganancia': ganancia,
        'Retorno': retorno,
        'Anio': anio
    }

    return informacion_pelicula