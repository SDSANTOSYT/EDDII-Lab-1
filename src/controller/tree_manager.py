import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import *
from .dataset_manager import *

main_tree = AVLT()

def add_film(title) -> None :
        main_tree.insert(search_movie(title)[0])

def search_in_tree(title) -> list[Film]:
    return main_tree.tree_in_list()

