import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import *
from .dataset_manager import *

main_tree = AVLT()

def add_film(title) -> None :
    for film in search_movie(title):
        main_tree.insert(film)

