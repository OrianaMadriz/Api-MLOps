
#



<img src="imagenes/titulo.jpg" alt="Logo de la empresa" style="width: 100%;">

#
#



# PROYECTO INDIVIDUAL Nº1: Oriana Madriz
# Machine Learning Operations (MLOps)



# Cotenido:

Carpeta "pycache": es una carpeta utilizada por el intérprete de Python para almacenar archivos de código compilados en formato de caché.

Carpeta "ambiente": se refiere a un ambiente virtual, que es un entorno aislado para ejecutar aplicaciones de Python con sus propias dependencias y configuraciones.

Carpeta "Datasets": contiene las bases de datos utilizadas en los diferentes pasos del proyecto.

Carpeta "imagenes": contiene imágenes mencionadas en el archivo "readme.md" del proyecto.

"main.py": es un archivo necesario para la API de consultas. Contiene el código principal para ejecutar la API y manejar las consultas.

"Paso_1 Transformaciones y Desanidado": es un notebook que describe los pasos seguidos para realizar transformaciones y desanidado en el conjunto de datos original ("movies_dataset.csv").

"Paso_2_Preparacion de la data para crear las funciones": es un notebook que detalla los pasos seguidos para preparar y exportar la base de datos para utilizar las funciones de la API.

"Paso_3 Creacion de funciones": es un notebook donde se crean y prueban las funciones utilizadas por la API.

"Paso_4 EDA": es un notebook donde se realiza un Análisis Exploratorio de Datos teniendo en cuenta la implementación de un modelo de recomendación.

"Paso_5 Modelo de Recomendacion": es un notebook donde se desarrolla y prueba el modelo de recomendación implementado por la API.

"requirements.txt": es un archivo necesario para la plataforma Render, utilizada para implementar las consultas de la API. Este archivo especifica las dependencias requeridas para ejecutar el archivo "main.py".


### Rol a desarrollar

En mi rol como Data Scientist en esta start-up de servicios de agregación de plataformas de streaming, he asumido la responsabilidad de crear un sistema de recomendación como mi primer proyecto de Machine Learning. Sin embargo, al revisar los datos disponibles, me he dado cuenta de que la calidad y la estructura de los mismos son muy pobres. Esto incluye datos anidados y falta de transformaciones. Esta situación ha dificultado enormemente mi trabajo como Data Scientist.

Para superar estos desafíos y lograr un MVP (Minimum Viable Product), he decidido asumir el papel adicional de Data Engineer. Mi objetivo principal es llevar a cabo un rápido trabajo de Data Engineering para mejorar la madurez de los datos y establecer una base sólida para el sistema de recomendación. A continuación, detallo las tareas y responsabilidades que he asumido:

## Análisis y comprensión de los datos existentes: 
#


<p align="center">
  <img src="imagenes/Análisis y comprensión de los datos existentes.jpg" alt="Logo de la empresa">
</p>

#
Realizé un análisis exhaustivo de los datos disponibles para comprender su estructura, calidad y características. Identifiqué las deficiencias y áreas de mejora, así como los requisitos específicos necesarios para desarrollar un sistema de recomendación efectivo.

## Transformación y limpieza de los datos: 

Implementé procesos de transformación y limpieza de datos para abordar las deficiencias identificadas. Esto incluyó la normalización de datos, la corrección de valores anómalos, la resolución de datos anidados y cualquier otra transformación necesaria para mejorar la calidad y utilidad de los datos.
#

<p align="center">
  <img src="imagenes/Transformación y limpieza de los datos.jpg" alt="Logo de la empresa">
</p>


#
### Documentación y mantenimiento: 
Se han documentado todos los procesos, transformaciones y decisiones tomadas en el trabajo de Data Engineering. Esto garantizará la reproducibilidad y el mantenimiento adecuado, así como facilitará futuras mejoras y actualizaciones del sistema de recomendación.

En resumen, en mi rol combinado de Data Scientist y Data Engineer, he asumido la responsabilidad de mejorar la madurez de los datos y crear un MVP del sistema de recomendación. He trabajado diligentemente para superar los desafíos existentes y sentar las bases necesarias para el éxito del proyecto. Esto implicó realizar tareas de análisis y comprensión de los datos, transformación y limpieza de los mismos.

Mi objetivo principal fué lograr un MVP funcional en el transcurso de una semana, por lo que trabajé con determinación y enfoque para cumplir con los plazos establecidos. Además, busqué oportunidades para mejorar y optimizar los procesos de Data Engineering a medida que avanzó el proyecto, asegurando así una base sólida y escalable para futuras iteraciones y mejoras del sistema de recomendación.

Estoy consciente de los desafíos y la presión que conllevó este rol combinado de Data Scientist y Data Engineer, pero me  comprometí a afrontarlos de manera proactiva y resolverlos de manera efectiva. Utilicé mis habilidades técnicas y conocimientos en ambas áreas para llevar a cabo con éxito este proyecto y contribuir al crecimiento y éxito de la start-up.

## Propuesta de trabajo
#

<p align="center">
  <img src="imagenes/Propuesta de trabajo.png" alt="Logo de la empresa">
</p>


#
En este proyecto de MVP, nos enfocamos en la rapidez y la eficiencia de las transformaciones de datos necesarias.  A continuación se presenta la descripción de las tareas y los logros requeridos y alcanzados en el proyecto:

### Desanidamiento de campos anidados: 
Para poder utilizar los campos "belongs_to_collection", "production_companies" entre otros, se requerió desanidarlos. Esto implicó extraer los valores de diccionarios o listas presentes en cada fila y volver a unirlos al dataset. En caso de no ser necesario desanidarlos, se buscó una alternativa para acceder a esos datos sin necesidad de desanidarlos.

### Relleno de valores nulos: 
Los campos "revenue" y "budget" que presentaron valores nulos han sido rellenados con el número 0. Esto garantizó que no hubieran valores faltantes en estos campos y facilitó el cálculo del retorno de inversión.

### Eliminación de valores nulos en el campo "release_date":
 Los registros que tuvieron valores nulos en el campo "release_date" fueron eliminados. Esto aseguró que todos los registros tuvieran una fecha de estreno válida y consistente.

### Formato de fecha y creación de columna "release_year":
Los valores de fecha en el campo "release_date" fueron cambiados al formato AAAA-mm-dd. Además, se creó una nueva columna llamada "release_year" donde se extrajo el año de la fecha de estreno.

### Creación de columna de retorno de inversión: 
Se creó una columna llamada "return" donde se calculó el retorno de inversión dividiendo los campos "revenue" y "budget". En caso de no haber datos disponibles para el cálculo, se asignó el valor 0.

### Eliminación de columnas no utilizadas: 
Las columnas "video", "imdb_id", "adult", "original_title", "vote_count", "poster_path" y "homepage" que no serán utilizadas en el proyecto han sido eliminadas del dataset. Esto permitió reducir el tamaño del dataset y optimizar el rendimiento.

Estos requerimientos de transformación han sido enfocados en lograr un MVP funcional de manera rápida y eficiente. Una vez realizados, se llevó a cabo las transformaciones necesarias para preparar los datos y avanzar en la implementación del sistema de recomendación.

### Análisis exploratorio de los datos (EDA)
#

<p align="center">
  <img src="imagenes/Análisis exploratorio de los datos (EDA).png" alt="Logo de la empresa">
</p>

#

Se ha realizado un análisis exploratorio de los datos después de haberlos limpiado. Durante el análisis, se han investigado las relaciones entre las variables del dataset, se han identificado outliers o anomalías y se han descubierto patrones interesantes que podrían ser útiles en análisis posteriores.

Una de las visualizaciones destacadas en el EDA es la nube de palabras, que muestra las palabras más frecuentes en los títulos de las películas. Esta información pudo ser utilizada para mejorar el sistema de recomendación.

### Desarrollo de la API:
#

<p align="center">
  <img src="imagenes/Desarrollo de la API.png" alt="Logo de la empresa">
</p>


#
Para disponibilizar los datos de la empresa, se ha implementado una API utilizando el framework FastAPI. Se han creado 6 funciones para los endpoints que se consumirán en la API, cada una con su respectivo decorador @app.get('/'):

#### peliculas_mes(mes):
Permite ingresar el nombre del mes como parámetro y devuelve la cantidad histórica de películas estrenadas en ese mes.

#### peliculas_dia(dia): 
Permite ingresar el nombre del día de la semana (respetando acentuación) como parámetro y devuelve la cantidad histórica de películas estrenadas en ese día.

#### franquicia(franquicia): 
Permite ingresar el nombre de una franquicia (respetando las mayúsculas de nombre propio) y devuelve la cantidad de películas de esa franquicia, la ganancia total y el promedio de ganancias.

#### peliculas_pais(pais): 
Permite ingresar el nombre de un país (respetando las mayúsculas de nombre propio) y devuelve la cantidad de películas producidas en ese país.

#### productoras(productora): 
Permite ingresar el nombre de una productora, (respetando las mayúsculas de nombre propio), y devuelve la ganancia total y la cantidad de películas producidas por esa productora.

#### retorno(pelicula):
Permite ingresar el nombre de una película (respetando las mayusculas de nombre propio) y devuelve la inversión, la ganancia, el retorno y el año de lanzamiento de la película.


### Sistema de recomendación

Una vez que los datos se han vuelto consumibles a través de la API y se ha realizado un análisis exhaustivo de los mismos, se ha implementado un modelo de machine learning para crear un sistema de recomendación de películas. El sistema se basa en encontrar la similitud de generos entre una película dada y el resto de películas, y devuelve una lista ordenada de las 5 películas más similares. Esta funcionalidad ha sido implementada como una función adicional en la API y se ha llamado recomendacion('titulo')

### Deployment

Para desplegar la API, se ha utilizado el servicio Render que ha permitido que la API sea consumida desde la web. Otra opción considerada fue Railway, pero finalmente se optó por Render por su conveniencia. A continuacion se mencionan algunos ejmeplos:

#### link general a la API
https://api-peliculas-tfyb.onrender.com

#### peliculas_mes(enero): 
https://api-peliculas-tfyb.onrender.com/peliculas_mes/enero

#### peliculas_dia(miércoles):
https://api-peliculas-tfyb.onrender.com/peliculas_dia/miércoles

#### franquicia(Toy Story Collection): 
https://api-peliculas-tfyb.onrender.com/franquicia/Toy%20Story%20Collection

#### peliculas_pais(United Kingdom): 
https://api-peliculas-tfyb.onrender.com/peliculas_pais/United%20Kingdom

#### productoras(Paramount Pictures):  
https://api-peliculas-tfyb.onrender.com/productoras/Paramount%20Pictures

#### retorno(Avatar):  
https://api-peliculas-tfyb.onrender.com/retorno/Avatar

#### recomendacion(Batman):
https://api-peliculas-tfyb.onrender.com/recomendacion/Batman



### Video
#

<p align="center">
  <img src="imagenes/Video.jpg" alt="Logo de la empresa">
</p>


#
Se ha creado un video (https://drive.google.com/drive/folders/1VHV8HH37hd34l-9Ks3kd0k89kX6jlcwd) para demostrar el funcionamiento de las consultas propuestas en la API y para mostrar los resultados obtenidos con el modelo de machine learning de recomendacion. El video permite al equipo comprender de manera clara y concisa cómo se utilizan las herramientas y los logros alcanzados en el proyecto. 

### Fuente de datos

Dataset (movies_dataset.csv): Archivo con los datos que requieren ser procesados, tengan en cuenta que hay datos que estan anidados (un diccionario o una lista como valores en la fila).
Diccionario de datos (Diccionario de Datos - Movies -.csv): Diccionario con algunas descripciones de las columnas disponibles en el dataset.

### Use estas herramientas

FastApi

Uvicorn

Python

Pandas

Numpy

Scikit-learn

Entre otras

Gracias por llegar hasta aca! Cualquiero duda o consulta no dudes en escribir orianamadriz29@gmail.com


