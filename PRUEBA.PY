# Cargar el dataset
df = pd.read_csv('data_con_EDA.csv')

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    df = pd.read_csv('data_con_EDA.csv')
    columnas_deseadas = ['genres',"title"]
    df = df[columnas_deseadas]
    df.drop_duplicates(subset=["title"], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['title'] = df['title'].astype(str)

    pelicula_entrada = df[df['title'].str.contains(titulo, case=False)]


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
    indices_similares_genres = similitud_genres.argsort()[0][-90:][::-1]

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

    #Eliminar la columna 'similitud_genres'
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

    # Obtener una lista de los títulos recomendados
    lista_recomendados = df_recomendadas_title['title'].tolist()

    # Crear el diccionario de salida
    recomendaciones = {'lista recomendada': lista_recomendados}

    return recomendaciones  