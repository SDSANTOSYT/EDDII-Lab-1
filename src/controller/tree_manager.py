import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import *
from .dataset_manager import *

main_tree = AVLT()

# Función que añade una pelicula desde el dataset al arbol
def add_film(title) -> None :
        for film in search_movie(title):
            if film.title == title:
                main_tree.insert(film)

# Función que devuelve el arbol en forma de lista
def search_in_tree() -> list[Film]:
    return main_tree.tree_in_list()

# Función que realiza una busqueda filtrada y devuelve una lista con los resultados
def search_filter(bool_year,year: int, per: bool, bool_ingreso,ingreso: float,title)-> list[Film]:
    elements = []
    if bool_year and bool_ingreso and per:
        for film in search_in_tree():
            if ((year == film.year) and (film.dpe < film.fpe) and (float(film.fe) >= float(ingreso)) and title.lower() in film.title.lower()):
                elements.append(film)
    elif bool_year and not bool_ingreso and per:
        for film in search_in_tree():
            if ((year == film.year) and (film.dpe < film.fpe) and title.lower() in film.title.lower()):
                elements.append(film)
    elif bool_year and bool_ingreso and not per:
        for film in search_in_tree():
            if ((year == film.year) and (float(film.fe) >= float(ingreso)) and title.lower() in film.title.lower()):
                elements.append(film)
    elif bool_year and not bool_ingreso and not per:
         for film in search_in_tree():
            if (year == film.year) and title.lower() in film.title.lower():
                elements.append(film)
    elif not bool_year and bool_ingreso and per:
        for film in search_in_tree():
            if ((film.dpe < film.fpe) and (float(film.fe) >= float(ingreso)) and title.lower() in film.title.lower()):
                elements.append(film)
    elif not bool_year and bool_ingreso and not per:
        for film in search_in_tree():
            if ((float(film.fe) >= float(ingreso)) and title.lower() in film.title.lower()):
                elements.append(film)
    elif not bool_year and not bool_ingreso and per:
        for film in search_in_tree():
            if ((film.dpe < film.fpe) and title.lower() in film.title.lower()):
                elements.append(film)
    else:
        for film in search_in_tree():
            if (title.lower() in film.title.lower()):
                elements.append(film)
    return elements

