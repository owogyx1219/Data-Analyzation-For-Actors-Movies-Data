import json
import random
from random import randint
'''
load data from json file for the table contains relations between movies and actors. 
If an actors participated a certain movie or a movie has a certain actor as it starring,
then a key-value pair(either movie:actor or actor:movie) is stored in the dictionary 
'''
with open('relations.json') as json_file1:
    relations_table = json.load(json_file1)

'''
load data for actors, each entry contains information about a certain actor/actress, including 
his/her born date of the actor and the movies he/she worked in
'''
with open('actors.json') as json_file2:
    actors_table = json.load(json_file2)

'''
load data for movies, each entry contains information about a certain movie, including 
the release date, box office and starring actors
'''
with open('movies.json') as json_file3:
    movies_table = json.load(json_file3)

#check for a certain actor, if the movie starring casts also contains him/her
actor_name = "Orlando Bloom"
ob = relations_table[actor_name]
for elem in movies_table["Lord of the Rings: The Two Towers"][2]:
    if(elem[0] == actor_name):
        print("True")
print(ob)

elem, elemList = random.choice(list(relations_table.items()))
print(elem)
print(elemList)

if( len(elemList) > 1):
    choice = random.choice(elemList)
    print(choice[0])
    try:
         actorList = actors_table[choice[0]][1]
         if elem in actorList:
            print(True)
    except KeyError:
        print("Key doesn't exist")
    try:
         movieList = movies_table[choice[0]][2]
         if elem in movieList:
            print(True)
    except KeyError:
        print("Key doesn't exist")


