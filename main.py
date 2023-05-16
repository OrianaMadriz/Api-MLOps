#Importamos las librerias necesarias

from typing import Union
import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Cargamos el dataset para las funciones
data = pd.read_csv('Datasets\data_funciones.csv')

@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str):
    # Nos quedamos solo con un dataframe con las peliculas de ese mes
    df_mes = data[data['mes'].str.lower() == mes.lower()]
    
    # Obtenemos la cantidad de películas estrenadas ese mes
    cantidad_peliculas = len(df_mes)
    
    # Devolvemos un diccionario con el nombre del mes y la cantidad de películas estrenadas ese mes
    return {'Mes': mes.capitalize(), 'Cantidad': cantidad_peliculas}

@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia: str):
    # Nos quedamos solo con un dataframe con las peliculas de ese dia
    df_dia = data[data['dia'].str.lower() == dia.lower()]
    
    # Obtenemos la cantidad de películas estrenadas ese dia
    cantidad_peliculas = len(df_dia)
    
    # Devolvemos un diccionario con el nombre del dia y la cantidad de películas estrenadas ese dia
    return {'Dia': dia.capitalize(), 'Cantidad': cantidad_peliculas}

@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
      # Nos quedamos solo con un dataframe con las peliculas de esa colección proporcionada
    df_franquicia = data[data['collection_name'] == franquicia]

    # Obtenemos la cantidad de películas estrenadas ese dia
    cantidad_peliculas = len(df_franquicia)
    
    # Calculamos el promedio y el total de la ganancia para las películas de la colección
    ganancia_promedio = df_franquicia['revenue'].mean()
    ganancia_total = df_franquicia['revenue'].sum()
    
    # Devolvemos un diccionario con la información
    return {
            'Franquicia': franquicia,
            'Cantidad':cantidad_peliculas,
            'Ganancia_total': ganancia_total,
            'Ganancia_promedio': ganancia_promedio
        
    }

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
   # Nos quedamos solo con un dataframe con las peliculas de ese pais proporcionado
    columnas_pais = [f'pco_name_{i}' for i in range(25)]
    df_pais = data[data[columnas_pais].eq(pais).any(axis=1)]    
    
    # Obtenemos la cantidad de películas producidas en el país
    cantidad = df_pais.shape[0]
    
    # Devolvemos un diccionario con la información
    return {
        'Pais': pais,
        'Cantidad': cantidad
    }

@app.get("/productoras/{productora}")
def productoras(productora: str):
    # Nos quedamos solo con un dataframe con las peliculas de esa productora proporcionada
    columnas_productoras = [f'pc_name_{i}' for i in range(26)]
    df_pc = data[data[columnas_productoras].eq(productora).any(axis=1)]

    # Calculamos la ganancia total de las películas de la productora
    ganancia_total = df_pc['revenue'].sum()

    # Contamos la cantidad de películas asociadas a la productora
    cantidad = df_pc.shape[0]

    # Devolvemos un diccionario con la información
    return {
        'Productora': productora,
        'Ganancia_total': ganancia_total,
        'Cantidad': cantidad
    }

# Convertimos columnas numéricas a tipos de datos apropiados
data['budget'] = pd.to_numeric(data['budget'], errors='coerce')
data['revenue'] = pd.to_numeric(data['revenue'], errors='coerce')
data['return'] = pd.to_numeric(data['return'], errors='coerce')
data['release_year'] = pd.to_numeric(data['release_year'], errors='coerce')


@app.get("/retorno/{pelicula}")
def retorno(pelicula: str):
   # Eliminamos filas duplicadas basadas en la columna 'title'
    data_unica = data.drop_duplicates(subset='title')

    # Nos quedamos solo con un dataframe con los datos de esa película proporcionada
    data_pelicula = data_unica[data_unica['title'] == pelicula]

    # Verificamos si se encontró la película
    if len(data_pelicula) == 0:
        return {'error': 'Película no encontrada'}

    # Obtenemos los valores de las columnas de interés
    inversion = data_pelicula['budget'].iloc[0].item()
    ganancia = data_pelicula['revenue'].iloc[0].item()
    retorno = data_pelicula['return'].iloc[0].item()
    anio = data_pelicula['release_year'].iloc[0].item()

    # Devolvemos un diccionario con la información
    informacion_pelicula = {
        'Pelicula': pelicula,
        'Inversion': inversion,
        'Ganancia': ganancia,
        'Retorno': retorno,
        'Anio': anio
    }

    return informacion_pelicula

# Cargamos el dataset para aplicar el modelo
df = pd.read_csv('Datasets\data_modelo.csv')

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    
    #Si el titulo ingresado no esta en los titulos del dataset devolvemos el mensaje "No se tienen datos del titulo ingresado"
    if titulo not in df['title'].values:
        return {'mensaje': "No se tienen datos del titulo ingresado" }
    else:

        # Creamos una instancia de TfidfVectorizer para los géneros
        tfidf_genres = TfidfVectorizer(tokenizer=lambda x: eval(x), lowercase=False)

        # Creamos la matriz de características para los géneros
        matriz_caracteristicas_genres = tfidf_genres.fit_transform(df['genres'].apply(str))

        # Encontramos el índice de la película de entrada en el DataFrame actualizado
        indice_genres = df[df['title'].str.contains(titulo, case=False)].index[0]

        # Calculamos la similitud del coseno entre los géneros
        similitud_genres = cosine_similarity(matriz_caracteristicas_genres[indice_genres], matriz_caracteristicas_genres)

        # Obtenemos los índices de las películas más similares basadas en los géneros
        indices_similares_genres = similitud_genres.argsort()[0][:][::-1]

        # Obtenemos las películas recomendadas basadas en los géneros
        peliculas_recomendadas_genres = df.loc[indices_similares_genres]

        # Creamos una columna de similitud basada en los géneros
        peliculas_recomendadas_genres['similitud_genres'] = similitud_genres[0, indices_similares_genres]

        # Ordenamos el DataFrame por similitud basada en los géneros de manera descendente
        df_recomendadas_genres = peliculas_recomendadas_genres.sort_values('similitud_genres', ascending=False)

        # Reiniciamos los índices del DataFrame resultante
        df_recomendadas_genres.reset_index(drop=True, inplace=True)

        # Excluimos el valor de los géneros de la película de entrada del DataFrame
        df_recomendadas_genres = df_recomendadas_genres[df_recomendadas_genres['title'] != titulo]

        # Filtramos las películas con similitud de géneros mayor a cero
        df_recomendadas_genres = df_recomendadas_genres[df_recomendadas_genres['similitud_genres'] > 0]

        # Obtenemos las primeras 5 películas recomendadas sin repeticiones
        df_recomendadas_genres = df_recomendadas_genres.drop_duplicates(subset=['title'])

        # Agregamos la fila correspondiente al título proporcionado al final del DataFrame
        fila_titulo_proporcionado = df[df['title'] == titulo]
        df_recomendadas_genres = pd.concat([df_recomendadas_genres, fila_titulo_proporcionado])

        # Reiniciamos los índices del DataFrame resultante
        df_recomendadas_genres.reset_index(drop=True, inplace=True)

        # Creamos una matriz de características utilizando TF-IDF Vectorizer para 'title'
        tfidf_title = TfidfVectorizer(stop_words='english')
        matriz_caracteristicas_title = tfidf_title.fit_transform(df_recomendadas_genres['title'])

        # Encontramos el índice de la película de entrada en el DataFrame actualizado
        indice_title = len(df_recomendadas_genres) - 1

        # Calculamos la similitud del coseno entre los títulos
        similitud_title = cosine_similarity(matriz_caracteristicas_title[indice_title], matriz_caracteristicas_title)

        # Obtenemos los índices de las películas más similares basadas en los títulos
        indices_similares_title = similitud_title.argsort()[0][:][::-1]

        # Obtenemos las películas recomendadas basadas en los títulos
        peliculas_recomendadas_title = df_recomendadas_genres.loc[indices_similares_title]

        # Creamos una columna de similitud basada en los títulos
        peliculas_recomendadas_title['similitud_title'] = similitud_title[0, indices_similares_title]

        # Ordenamos el DataFrame por similitud basada en los títulos de manera descendente
        df_recomendadas_title = peliculas_recomendadas_title.sort_values('similitud_title', ascending=False)

        # Reiniciamos los índices del DataFrame resultante
        df_recomendadas_title.reset_index(drop=True, inplace=True)

        # Excluimos el valor del título proporcionado del DataFrame
        df_recomendadas_title = df_recomendadas_title[df_recomendadas_title['title'] != titulo]

        # Obtenemos las películas recomendadas sin repeticiones
        df_recomendadas_title = df_recomendadas_title.drop_duplicates(subset=['title'])

        # Obtenemos una lista de los títulos recomendados
        lista_recomendados = df_recomendadas_title['title'].tolist()

        # Creamos el diccionario de salida
        recomendaciones = {'lista recomendada': lista_recomendados[:5]}

        return recomendaciones