import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import *
import csv

def search_movie(title: str) -> list[Film] :
    films = []
    with open('src/dataset_movies.csv',"r",encoding="utf-8") as dataset:
        reader = csv.reader(dataset)
        next(reader)
        for line in reader:
            if title.lower() in line[0].lower():
                print(line)
                films.append(Film(line[0],line[1],line[2],line[3],line[4],line[5],line[6]))
        return films


