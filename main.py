from typing import Union
import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# Cargar el dataset
data = pd.read_csv('data_con_EDA.csv')

@app.get("/retorno/{pelicula}")
def recomendacion(titulo: str):
    # Obtener la película de entrada
    pelicula_entrada = df[df['title'] == titulo]

    # Crear una matriz de características utilizando TF-IDF Vectorizer para 'genres'
    tfidf_genres = TfidfVectorizer(stop_words='english')
    matriz_caracteristicas_genres = tfidf_genres.fit_transform(df['genres'].apply(lambda x: ', '.join(eval(x))))

    # Encontrar el índice de la película de entrada
    indice_genres = pelicula_entrada.index[0]

    # Calcular la similitud del coseno entre las películas basada en 'genres'
    similitud_genres = cosine_similarity(matriz_caracteristicas_genres[indice_genres], matriz_caracteristicas_genres)

    # Obtener los índices de las películas más similares basadas en 'genres'
    indices_similares_genres = similitud_genres.argsort()[0][:][::-1]

    # Obtener las películas recomendadas basadas en 'genres'
    peliculas_recomendadas_genres = df.loc[indices_similares_genres]

    # Crear una columna de similitud basada en 'genres'
    peliculas_recomendadas_genres['similitud_genres'] = similitud_genres[0, indices_similares_genres]

    # Ordenar el DataFrame por similitud basada en 'genres' de manera descendente
    df_recomendadas_genres = peliculas_recomendadas_genres.sort_values('similitud_genres', ascending=False)

    # Reiniciar los índices del DataFrame resultante
    df_recomendadas_genres.reset_index(drop=True, inplace=True)

    # Agregar la fila del título al final del dataframe
    df_recomendadas_genres.loc[len(df_recomendadas_genres)] = pelicula_entrada.iloc[0]

    # Eliminar la columna 'similitud_genres'
    df_recomendadas_genres = df_recomendadas_genres.drop('similitud_genres', axis=1)

    # Crear una matriz de características utilizando TF-IDF Vectorizer para 'title'
    tfidf_title = TfidfVectorizer(stop_words='english')
    matriz_caracteristicas_title = tfidf_title.fit_transform(df_recomendadas_genres['title'])

    # Encontrar el índice de la película de entrada en el DataFrame actualizado
    indice_title = len(df_recomendadas_genres) - 1

    # Calcular la similitud del coseno entre los títulos
    similitud_title = cosine_similarity(matriz_caracteristicas_title[indice_title], matriz_caracteristicas_title)

    # Obtener los índices de las películas más similares basadas en los títulos
    indices_similares_title = similitud_title.argsort()[0][-26:][::-1]

    # Obtener las películas recomendadas basadas en los títulos
    peliculas_recomendadas_title = df_recomendadas_genres.loc[indices_similares_title]

    # Crear una columna de similitud basada en los títulos
    peliculas_recomendadas_title['similitud_title'] = similitud_title[0, indices_similares_title]

    # Ordenar el DataFrame por similitud basada en los títulos de manera descendente
    df_recomendadas_title = peliculas_recomendadas_title.sort_values('similitud_title', ascending=False)

    # Reiniciar los índices del DataFrame resultante
    df_recomendadas_title.reset_index(drop=True, inplace=True)

    # Excluir el valor del título proporcionado del DataFrame
    df_recomendadas_title = df_recomendadas_title[df_recomendadas_title['title'] != titulo]

    # Agregar la fila del título al final del dataframe
    df_recomendadas_title.loc[len(df_recomendadas_title)] = df_recomendadas_genres.iloc[indice_title]

    # Eliminar la columna 'similitud_title'
    df_recomendadas_title = df_recomendadas_title.drop('similitud_title', axis=1)

    # Restablecer los índices del DataFrame resultante
    df_recomendadas_title.reset_index(drop=True, inplace=True)

    # Obtener las primeras 5 películas recomendadas
    df_recomendadas_title = df_recomendadas_title.head(5)

    # Obtener una lista con los títulos de las películas recomendadas
    lista_titulos = df_recomendadas_title['title'].tolist()

    return lista_titulos