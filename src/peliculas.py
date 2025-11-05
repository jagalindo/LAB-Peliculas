import csv

from typing import NamedTuple, List, Dict
from datetime import date, datetime
from pathlib import Path

Pelicula = NamedTuple(
    "Pelicula",
    [("fecha_estreno", date), 
    ("titulo", str), 
    ("director", str), 
    ("generos",List[str]),
    ("duracion", int),
    ("presupuesto", int), 
    ("recaudacion", int), 
    ("reparto", List[str])
    ]
)


def lee_peliculas(fichero: str)->List[Pelicula]:
    peliculas = []
    with open(fichero, 'r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)  # Saltar la cabecera
        for fila in lector:
            fecha_estreno, titulo, director, generos, duracion, presupuesto, recaudacion, reparto = fila
            pelicula = Pelicula(
                fecha_estreno=datetime.strptime(fecha_estreno, "%d/%m/%Y").date(),
                titulo=titulo,
                director=director,
                generos=generos.replace(', ',',').split(',') if generos else [],
                duracion=duracion,
                presupuesto=int(presupuesto),
                recaudacion=int(recaudacion),
                reparto=reparto.replace(', ',',').split(',') if reparto else []
                )
            peliculas.append(pelicula)
    return peliculas

def pelicula_mas_ganancias(peliculas:List[Pelicula], genero:str=None) -> tuple[str, int]:
    '''pelicula_mas_ganancias`: recibe una lista de tuplas de tipo `Pelicula` 
    y una cadena de texto `genero`, con valor por defecto `None`, y devuelve 
    el título y las ganancias de la película con mayores ganancias, de entre 
    aquellas películas que tienen entre sus géneros el `genero` indicado. Si 
    el parámetro `genero` es `None`, se busca la película con mayores ganancias, 
    sin importar sus géneros. Las ganancias de una película se calculan como 
    la diferencia entre la recaudación y el presupuesto. **(1 puntos)**
    '''

    pelicula_titulo = ""
    ganancias_max = 0

    for pelicula in peliculas:
        if genero in pelicula.generos or genero == None:
            ganancias = pelicula.recaudacion - pelicula.presupuesto
            if(ganancias>ganancias_max):
                ganancias_max=ganancias
                pelicula_titulo=pelicula.titulo

    return pelicula_titulo, ganancias_max

def media_presupuesto_por_genero(peliculas: List[Pelicula]) -> Dict[str, float]:
    '''`media_presupuesto_por_genero`: recibe una lista 
    de tuplas de tipo `Pelicula` y devuelve un diccionario 
    en el que las claves son los distintos géneros y los 
    valores son la media de presupuesto de las películas de 
    cada género. **(1,5 puntos)**'''

    genero_presupuesto_suma={}
    genero_presupuesto_count={}

    for pelicula in peliculas:
        presupuesto = pelicula.presupuesto
        for genero in pelicula.generos:
            if genero not in genero_presupuesto_suma:
                genero_presupuesto_suma[genero]=presupuesto
                genero_presupuesto_count[genero]=1
            else:
                genero_presupuesto_suma[genero] = genero_presupuesto_suma[genero]+presupuesto
                genero_presupuesto_count[genero] = genero_presupuesto_count[genero] +1

    genero_presupuesto_media={}
    for genero, suma in genero_presupuesto_suma.items():
        genero_presupuesto_media[genero] = suma/genero_presupuesto_count[genero]

    return genero_presupuesto_media
def peliculas_por_actor(peliculas:List[Pelicula], anyo_inicial:int=None, anyo_final:int=None):
    '''`peliculas_por_actor`: recibe una lista 
    de tuplas de tipo `Pelicula` y dos enteros 
    `año_inicial` y `año_final`, con valor por 
    defecto `None`, y devuelve un diccionario 
    en el que las claves son los nombres de los 
    actores y actrices, y los valores son el número de 
    películas, estrenadas entre `año_inicial` y `año_final` 
    (ambos incluidos), en que ha participado cada actor o actriz.
      Si `año_inicial` o `año_final` son `None`, se contarán las 
      películas sin filtrar por año inicial o final, 
      respectivamente. **(1,5 puntos)**'''
    actores_peliculas={}
    for pelicula in peliculas:
        if ( anyo_final== None or pelicula.fecha_estreno.year < anyo_final ) and ( anyo_inicial==None or pelicula.fecha_estreno.year > anyo_inicial  ):
            for actor in pelicula.reparto:
                if actor not in actores_peliculas:
                    actores_peliculas[actor] = 1
                else:
                    actores_peliculas[actor] = actores_peliculas[actor]+1

    return actores_peliculas

def actores_mas_frecuentes(peliculas:List[Pelicula], n:int, anyo_inicial:int, anyo_final:int)-> List[str]:
    '''`actores_mas_frecuentes`: recibe una lista de tuplas de tipo `Pelicula`, un entero `n` 
    y dos enteros `año_inicial` y `año_final`, con valor por defecto `None`, y devuelve una 
    lista con los `n` actores o actrices que han participado en más películas estrenadas entre 
    `año_inicial` y `año_final` (ambos incluidos). La lista de actores o actrices debe estar 
    ordenada alfabéticamente. Si `año_inicial` o `año_final` son `None`, se contarán las películas 
    sin filtrar por año inicial o final, respectivamente. Haga uso de la función `peliculas_por_actor` 
    para implementar esta función. **(1 punto)**'''

    peliculas_actor= peliculas_por_actor(peliculas, anyo_inicial, anyo_final)
    def get_value(clave):
        return peliculas_actor[clave]
    
    peliculas_actor_list=sorted(peliculas_actor.keys(), key=get_value, reverse=True)
    return peliculas_actor_list[:n]

if __name__ == '__main__':
    path = Path("./data/peliculas.csv") 
    peliculas=lee_peliculas(path)
   # print(pelicula_mas_ganancias(peliculas, "Acción"))
   # print(media_presupuesto_por_genero(peliculas))
    #print(peliculas_por_actor(peliculas))
    print(actores_mas_frecuentes(peliculas, 2, None, None))