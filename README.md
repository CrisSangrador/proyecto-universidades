# Proyecto API de universidades

### Descripción del proyecto:

Este proyecto contiene los ejercicios de evaluación del segundo sprint del segundo módulo del bootcamp de *Data Analytics*, cuya motivación es la de demostrar los conocimientos alcanzados a lo largo de este sprint.  


Este proyecto tiene como objetivo identificar todas las universidades ubicadas en tres países específicos: **Estados Unidos, Canadá y Argentina**. Para llevar a cabo esta tarea, utilizaremos la API de ["Universities Hipolab"](https://github.com/Hipo/university-domains-list), una fuente confiable y completa de información sobre las universidades en todo el mundo. Con la ayuda de esta API, podemos acceder a una gran cantidad de datos relevantes, incluyendo el nombre de la universidad, la ciudad donde esta ubicada, el nombre de la institución y otra información importante que nos permitirá llevar a cabo un análisis detallado. 

### Estructura del proyecto:

Este proyecto presenta la siguiente estructura:

- Directorio `notebooks`: En este directorio se encuentran los siguientes notebooks:
    - `evaluacion_2.ipynb`: Contiene los ejercicios resueltos de la evaluación.
    - `clase_extraccion_limpieza.ipynb`: Contiene una Clase que permite extraer los datos de la API, así como su conversión a DataFrame la limpieza de los datos según los criterios establecidos en la evaluación. 
    - `clase_carga.ipynb`: Contiene una Clase que permite crear una nueva base de datos con dos tablas, países y universidades, según los criterios establecidos en la evaluación. Además, permite la carga de los datos contenidos en un DataFrame (como el creado el `clase_extraccion_limpieza.ipynb`) a la base de datos creada.

- Directorio `data`, que contiene el resultado de la extracción y la limpieza de datos, guardado tanto en formato `.csv` como en `.pkl`.

- Directorio `sql`, que contiene:
    - `script_bbdd_universidades`: Script de la creación de la base de datos en MySQL.
    -  `imagen_esquema_bbdd.png`: Imagen que recoge la relación entre las dos tablas creadas en la base de datos. 

- Directorio `src`, que contiene:
    - `soporte.py`, contiene las dos Clases (guardadas en `clase_extraccion_limpieza.ipynb` y `clase_carga.ipynb`) unificada en una sola.

- Archivo `main.py`, a través del cual se puede ejecutar la Clase guardada en el archivo `soporte.py` a través de la terminal. 


### Librerías y herramientas utilizadas a lo largo del proyecto:

*Click en el nombre de cada una para acceder a su documentación.*

- [`NumPy`](https://numpy.org/doc/stable/user/), para poder trabajar con los nulos..
- [`Pandas`](https://pandas.pydata.org/docs/user_guide/index.html), para poder trabajar con DataFrames. 
- [`Requests`](https://requests.readthedocs.io/en/latest/), para poder realizar la llamada a la API y sacar información.
- [`MySQL Connector`](https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html), para poder conectarse a MySQL y trabajar sobre las bases de datos a través del código de Python.
- [`Geopy`](https://geopy.readthedocs.io/en/stable/), para poder trabajar con localizaciones, coordenadas, etc.