import src.soporte as sp


contraseña = input("¿Cuál es tu contraseña?")

nombre_bbdd = input("Como quieres llamar a la base de datos o cómo se llama?")

bbdd = sp.Universidades(f"{nombre_bbdd}", f"{contraseña}")
    
bbdd.crear_bbdd()

bbdd.crear_tablas()

paises = input("¿De qué países deseas obtener la información?. Por favor, indica su nombre en inglés. Si son varios, sepáralos por comas.")

if ", " in paises:
    paises = paises.split(", ")
else:
    pass

df_universidades = bbdd.api(paises)

df_universidades = bbdd.limpieza(df_universidades)

print("Estamos sacando las coordenadas. Esto puede tardar un momento.")

df_universidades = bbdd.sacar_coordenadas(df_universidades)

bbdd.cargar_provincias(df_universidades)

bbdd.cargar_universidades(df_universidades)

print("¡Los datos se han cargado correctamente! 😊")

guardado = input("Por favor, indica la ruta y el nombre donde quieres guardar el dataframe con los datos.")

bbdd.guardar_df(df_universidades, f"{guardado}")

print("¡Los datos se han guardado correctamente en la ruta especificada! 😊")

