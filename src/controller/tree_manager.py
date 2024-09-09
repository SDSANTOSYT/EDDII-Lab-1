import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import *
from .dataset_manager import *

main_tree = AVLT()

# Función que añade una pelicula desde el dataset al arbol
def add_film(title) -> None :
        main_tree.insert(search_movie(title)[0])

# Función que devuelve el arbol en forma de lista
def search_in_tree(title) -> list[Film]:
    return main_tree.tree_in_list()

# Función que realiza una busqueda filtrada y devuelve una lista con los resultados
def search_filter(bool_year,year: int, per: bool, bool_ingreso,ingreso: float,title)-> list[Film]:
    elements = []
    if bool_year and bool_ingreso and per:
        for film in search_in_tree():
            if ((year == Film.year) and (film.dpe < film.fpe) and (film.fe >= ingreso) and title in film.title):
                elements.append(Film)
    elif bool_year and not bool_ingreso and per:
        for film in search_in_tree():
            if ((year == Film.year) and (film.dpe < film.fpe) and title in film.title):
                elements.append(Film)
    elif bool_year and bool_ingreso and not per:
        for film in search_in_tree():
            if ((year == Film.year) and (film.fe >= ingreso) and title in film.title):
                elements.append(Film)
    elif bool_year and not bool_ingreso and not per:
         for film in search_in_tree():
            if (year == Film.year) and title in film.title:
                elements.append(Film)
    elif not bool_year and bool_ingreso and per:
        for film in search_in_tree():
            if ((film.dpe < film.fpe) and (film.fe >= ingreso) and title in film.title):
                elements.append(Film)
    else:
        for film in search_in_tree():
            if (title in film.title):
                elements.append(Film)
    return elements
