import requests
import zipfile
import io
import geopandas as gpd
import pandas as pd

# Paso 1: Descargar y extraer el archivo ZIP
url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
response = requests.get(url)

# Extraer el contenido del archivo ZIP en una carpeta específica
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    z.extractall("path_to_extract")  # Cambia "path_to_extract" a la ruta deseada para extraer los archivos

# Paso 2: Leer el shapefile con GeoPandas
shapefile_path = "path_to_extract/ne_50m_admin_0_countries.shp"  # Cambia la ruta al archivo .shp extraído
gdf = gpd.read_file(shapefile_path)

# Paso 3: Filtrar y obtener las posiciones de los municipios
# Suponiendo que el shapefile contiene datos de municipios y que existe una columna 'MUNICIPIO' en ambos datasets.

# Mostrar las primeras filas para inspeccionar las columnas disponibles
print(gdf.head())

# Extraer la geometría de los municipios
municipios_geom = gdf.geometry

# Obtener las coordenadas representativas de cada municipio
municipios_coords = municipios_geom.apply(lambda x: x.representative_point().coords[:])
municipios_coords = [coords[0] for coords in municipios_coords]

# Paso 4: Relacionar con el dataset de madera movilizada
# Supón que tienes un DataFrame 'df_madera' con la columna 'MUNICIPIO' que quieres relacionar con las coordenadas

# Crear un diccionario que asocia los municipios con sus coordenadas
municipios_dict = dict(zip(gdf['MUNICIPIO'], municipios_coords))

# Simulación de un DataFrame de madera movilizada
data = {
    'MUNICIPIO': ['Bogotá', 'Medellín', 'Cali'],  # Cambia estos valores según tu dataset
    'VOLUMEN M3': [1000, 500, 800]  # Ejemplo de volumen
}
df_madera = pd.DataFrame(data)

# Agregar las coordenadas al DataFrame de madera movilizada
df_madera['coordenadas'] = df_madera['MUNICIPIO'].map(municipios_dict)

# Mostrar el DataFrame resultante
print(df_madera)
