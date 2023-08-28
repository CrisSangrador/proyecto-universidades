### Importación de las librerías necesarias

import requests
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import mysql.connector

# -*- coding: utf-8 -*-



class Universidades:

    # Creación de base de datos

    """Esta clase va a recibir dos parámetros, que son el nombre de la base de datos que se quiere crear
    y la contraseña para poder crearla"""
    
    def __init__(self, nombre_bbdd, contraseña):

        self.nombre_bbdd = nombre_bbdd
        self.contraseña = contraseña

    # método para crear la BBDD 
    def crear_bbdd(self):

        """Esta función recibe los parámetros del método constructor. Crea la base de datos si no existía
        con anterioridad y, si no, devuelve un mensaje de que no se ha podido crear."""

        mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password=f'{self.contraseña}') 
        mycursor = mydb.cursor()

        print("La conexión se ha realizado con éxito.")

        try:
            mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.nombre_bbdd};")


            print(f"La base de datos {self.nombre_bbdd} se ha creado con éxito o ya existía anteriormente.")
            
        except:

            print(f"La base de datos {self.nombre_bbdd} no se ha podido crear.")


    def crear_tablas(self):

        """Esta función recibe los parámetros del método constructor. Crea las tablas de
        la base de datos si no existían con anterioridad y, si no, devuelve un mensaje avisando de que
        no se ha podido crear."""


        mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password=f'{self.contraseña}') 
        mycursor = mydb.cursor()


        query1 = f"""CREATE TABLE IF NOT EXISTS `{self.nombre_bbdd}`.`países` (
                    `idestado` INT NOT NULL AUTO_INCREMENT,
                    `nombre_país` VARCHAR(45) NOT NULL,
                    `nombre_provincia` VARCHAR(45) NOT NULL,
                    `latitud` DECIMAL (10, 7) NULL,
                    `longitud` DECIMAL (10, 7) NULL,
                    PRIMARY KEY (`idestado`));"""
        
        query2 = f"""CREATE TABLE IF NOT EXISTS `{self.nombre_bbdd}`.`universidades` (
                    `id_universidad` INT NOT NULL AUTO_INCREMENT,
                    `nombre_universidad` VARCHAR(100) NULL,
                    `pagina_web` VARCHAR(100) NULL,
                    `países_idestado` INT NOT NULL,
                    PRIMARY KEY (`id_universidad`),
                    INDEX `fk_universidades_países_idx` (`países_idestado` ASC) VISIBLE,
                    CONSTRAINT `fk_universidades_países`
                        FOREIGN KEY (`países_idestado`)
                        REFERENCES `{self.nombre_bbdd}`.`países` (`idestado`)
                        ON DELETE NO ACTION
                        ON UPDATE NO ACTION); """   

        try:
            
            mycursor.execute(query1)
            mycursor.execute(query2)
            mydb.commit()
            print("Las tablas de la base de datos se han podido crear correctamente.")

        except mysql.connector.Error as err:

            print("No se han podido crear las tablas de la base de datos.")
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg) 

    # Extracción

    def api(self, paises):

 

        """Esta función recibe un único parámetro, que será un string o una lista de strings con el nombre del país o países (en inglés) de los que se quiere
        obtener información. Se realizará la extracción de los datos de los países indicados, y devolverá un DataFrame
        con la información obtenida. En caso de que hubiera algún error, devolverá el número del error y el motivo."""

        if isinstance(paises, str): # Comprueba si el parámetro introducido es un string. 

            url = f"http://universities.hipolabs.com/search?country={paises}" 

            response = requests.get(url)

            code = response.status_code # Devuelve el código de la extracción de datos

            reason = response.reason # Devuelve el motivo.

            if code == 200: # Comprueba que el código de la extracción sea 200, es decir, que haya ocurrido correctamente.

                print(f"Información de {paises} obtenida correctamente, se va a convertir en DataFrame.")

                df =  pd.json_normalize(response.json())

                return df # Devuelve el DataFrame con la información del país indicado. 
            
            else: 
                return f"Error: {code}, {reason}." # Si no, devuelve el código de error y el motivo.
        
        elif isinstance(paises, list):  # Comprueba si el parámetro introducido es una lista.

            df_universidades = pd.DataFrame() #Se crea un DataFrame vacío para ir uniendo los resultados por cada país de la lista introducida.

            for pais in paises: 

                url = f"http://universities.hipolabs.com/search?country={pais}"

                response = requests.get(url) 

                code = response.status_code # Devuelve el código de la extracción de datos

                reason = response.reason # Devuelve el motivo.

                if code == 200: # Comprueba que el código de la extracción sea 200, es decir, que haya ocurrido correctamente.

                    print(f"Información de {pais} obtenida correctamente, se va a convertir en DataFrame.")

                    df =  pd.json_normalize(response.json())

                    df_universidades = pd.concat([df_universidades, df], axis = 0) # Se unen los resultados en el DataFrame creado

                else: 
                    return f"Error: {code}, {reason}."
                
            
            return df_universidades # Devuelve el DataFrame con la información de los paises indicados si se ha podido crear. Fuera del bucle para
                                    # que se pueda completar el bucle. 
        
        else:
            print("Por favor, introduzca un único país o una lista de paises (en inglés).")

    
    # 2. Limpieza

    def limpieza(self, dataframe):

        """Esta función recibe como parámetro el nombre del dataframe a limpiar.
            Devuelve el dataframe con el nombre de las columnas cambiadas ("-" ahora es "_"), y elimina una columna redundante. Además,
            realiza el explode a la columna "web_pages, elimina los duplicados de la columna  "name", imputa los nulos de
            la columna "state_province" por la categoría "Unknown". Asimismo, cambia los estados por el nombre completo. 
            Devuelve el dataframe con los datos aplicados. """

        nuevas_columnas = {col : col.replace("-", "_") for col in dataframe.columns} # Se crea un diccionario con los nombres antiguos como key, y 
                                                                                    #los nuevos nombres como value.

        dataframe.rename(columns = nuevas_columnas, inplace = True) # Se realiza el cambio del nombre de las columnas.
            
        dataframe.drop("domains", axis = 1, inplace = True) # Se elimina la columna de domains.

        dataframe = dataframe.explode("web_pages") # Se realiza el explode para la columna de "web_pages"

        dataframe.drop_duplicates(subset = "name", inplace = True) # Se eliminan los duplicados en la columna "name"

        dataframe["state_province"].fillna("Unknown", inplace = True)

        dataframe["state_province"] = dataframe["state_province"].replace("NV", "Nevada").replace("TX", "Texas").replace("IN", "Indianapolis").replace("CA", "California").replace("VA", "Virginia").replace("NY", "New York")
            
        dataframe["state_province"] = dataframe["state_province"].replace("New York, NY", "New York").replace("MI", "Michigan").replace("GA", "Georgia").replace("ND", "North Dakota").replace("Ciudad Autónoma de Buenos Aires", "Buenos Aires")
        
        # Se realizan varias modificaciones a la columna "state_province", imputando los nulos por una nueva categoría y reemplazando los nombres de estados
        # por otros nombres más claros. El replace se podría haber hecho una única línea de código, pero quedaba muy larga, así que he 
        # optado por partirla en dos. 
        
        dataframe["name"] = dataframe["name"].str.replace('"', '') # Hay algunas universidades que tienen dobles comillas en sus nombres, lo que impide su inserción en la base de datos. 
                                                                    #Lo solucionamos aquí para evitar problemas en la futura inserción
    

        return dataframe # Se devuelve el dataframe con los cambios aplicados 
        
    def sacar_coordenadas(self, dataframe):
        
        """Esta función recibe dos parámetros, que es el nombre del dataframe y el nombre de la columna sobre la que se quieren sacar las coordenadas.
        Se utiliza la librería de Geopy para conseguir la latitud y la longitud de los lugares indicados. 
        Devuelve el DataFrame con dos columnas nuevas, "lat" y "long", que contienen las coordenadas en función del lugar de la columna indicada."""

        lista_estados = list(dataframe["state_province"].unique()) # Primero, se crea una lista con los valores únicos de esa columna.

        df_localizacion = pd.DataFrame(columns = ["state_province", "lat", "long"]) # Se crea un datagrame vacío para poder introducir los datos. 

        for estado in lista_estados: 

            if estado != "Unknown":  
                geo = Nominatim(user_agent = "nombre")
                localizacion = geo.geocode(f"{estado}")
                state = f"{estado}"
                latitud = localizacion[1][0]
                longitud = localizacion[1][1]

                df_localizacion.loc[len(df_localizacion.index)] = [state, latitud, longitud] #Se añaden los datos sacados de Geopy en la última fila del DataFrame creado.
            
            else: # Si el estado/lugar entra en la categoría creada previamente de "Unknown", entonces las coordenadas se convertirán a un nulo de NumPY.
                
                state = f"{estado}"
                latitud = np.nan
                longitud = np.nan
                
                df_localizacion.loc[len(df_localizacion.index)] = [state, latitud, longitud]
            
        dataframe = pd.merge(dataframe, df_localizacion, on = "state_province", how = "left")

        return dataframe
    
    def guardar_df(self, dataframe, ruta_nombre):

        """Esta función recibe dos parámetros, que son el nombre del dataframe a guardar y la ruta donde se quiere guardar. 
        Guarda el archivo tanto en .pkl como en .csv"""

        dataframe.to_csv(f"{ruta_nombre}.csv")
        dataframe.to_pickle(f"{ruta_nombre}.pkl")

    def cargar_provincias(self, dataframe):

        """Esta función recibe como parámetro un DataFrame para cargar los datos correspondientes de país, 
        estado, latitud y longitud a la tabla de "países" de la base de datos creada. 
        Primero comprueba que no esté ya insertada en la base de datos y, si no lo está, 
        la inserta; de lo contrario, avisa al usuario de que ya está ese registro en la 
        tabla"""

        df_provincias = dataframe[["country", "state_province", "lat", "long"]].drop_duplicates()
        # Creamos un DataFrame con las columnas que nos interesan del DataFrame 
        # especificado al llamar a la función, y quitamos los duplicados por si acaso.

        mydb = mysql.connector.connect(user="root",
                                    password= f"{self.contraseña}",
                                    host="localhost", 
                                    database=f"{self.nombre_bbdd}")
        mycursor = mydb.cursor()
    
        for indice, fila in df_provincias.iterrows(): # Iteramos por cada una de las filas del DataFrame creado

            try: # Chequeamos que no haya ningún registro que coincida en estado y país

                check_provincia = f"""SELECT idestado FROM países 
                                    WHERE nombre_provincia = "{fila['state_province']}" AND nombre_país = "{fila['country']}";"""
                mycursor.execute(check_provincia)
                existe_provincia = mycursor.fetchone()
                

                if not existe_provincia: #Si no existe un registro, lo inserta

                    query_provincia = f"""INSERT INTO países (nombre_país, nombre_provincia, latitud, longitud) 
                                            VALUES ("{fila['country']}", "{fila['state_province']}", 
                                            {'NULL' if pd.isna(fila['lat']) else fila['lat']},
                                            {'NULL' if pd.isna(fila['long']) else fila['long']}); 
                                            """
                                            # Hay algunos nulos, así que indicamos que ponga NULL en la base de datos
                                            #para que no haya errores. 
                    
                    mycursor.execute(query_provincia)
                    mydb.commit()

                else: # Si existe, devuelve que ya existe.
                    print(f"Ya existe la provincia {fila['state_province']} en la base de datos.")

            
            except mysql.connector.Error as err: #Si hay un error, devuelve el código y el mensaje.

                print("No se han podido cargar las provincias a la base de datos.")
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)          


    def cargar_universidades(self, dataframe):

        """Esta función recibe como parámetro un DataFrame para cargar los datos correspondientes de nombre de 
        la universidad, su página web, el país y el estado a la tabla de "universidades" de la base de datos creada. 
        Primero comprueba que no esté ya insertada en la base de datos y, si no lo está, la inserta; de lo contrario, avisa al usuario de que ya está ese registro en la 
        tabla. Además, comprueba el id correspondiente a la ciudad y país, para añadirlo a la tabla "universidades"
        como *foreing key*"""


        df_universidad = dataframe[["name", "web_pages", "country", "state_province"]].drop_duplicates()
                # Creamos un DataFrame con las columnas que nos interesan del DataFrame 
                # especificado al llamar a la función, y quitamos los duplicados por si acaso.


        mydb = mysql.connector.connect(user="root",
                                    password= f"{self.contraseña}",
                                    host="localhost", 
                                    database=f"{self.nombre_bbdd}")
        mycursor = mydb.cursor()
        
        for indice, fila in df_universidad.iterrows(): # Iteramos por cada una de las filas del DataFrame creado

            try: # Chequeamos que no haya ningún registro que coincida en nombre de universidad

                check_universidad = f"""SELECT id_universidad FROM universidades 
                                        WHERE nombre_universidad = "{fila['name']}"; 
                                        """
                mycursor.execute(check_universidad)
                existe_universidad = mycursor.fetchone()
                    
                if not existe_universidad: #Si no existe un registro, continua

                    try: # Obtiene el ID del estado correspondiente en la tabla de "paises" y lo inserta
                        # como foreign key con el resto de datos de nombre y página web.

                        check_provincia = f"""SELECT idestado FROM países 
                                            WHERE nombre_provincia = "{fila['state_province']}" AND nombre_país = "{fila['country']}";"""
                                            
                        mycursor.execute(check_provincia)

                        id_estado = mycursor.fetchone()[0]
        
                        query_universidad = f"""INSERT INTO universidades (nombre_universidad, pagina_web, países_idestado) 
                                                VALUES ("{fila['name']}", "{fila['web_pages']}", "{id_estado}");
                                                """
                                
                        mycursor.execute(query_universidad)
                        mydb.commit() 
                    
                    except mysql.connector.Error as err: # Si no puede obtener el ID del estado
                                                            #devuelve los errores

                        print("No se ha podido  obtener el ID de la provincia.")
                        print(err)
                        print("Error Code:", err.errno)
                        print("SQLSTATE", err.sqlstate)
                        print("Message", err.msg)     

                else: # Si sí existe la universidad en esa tabla, devuelve que ya existe.

                    print(f"Ya existe la universidad {fila['name']} en la base de datos.")

                
            except mysql.connector.Error as err:

                print("No se han podido cargar las universidades a la base de datos.")
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)       
