import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

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


#find grossing value of a movie given the name of the movie
def findGrossingOfAMovie(movie_name):
    return movies_table[movie_name][1]


#find movies an actor has worked in given the name of the actor
def findMoviesOfAnActor(actor_name):
    return actors_table[actor_name][1]


#find the starring actors of a movie given the name of the movie
def findActorsInAMovie(movie_name):
    return movies_table[movie_name][2]


#find all movies that were released on the given year
def findMoviesInAGivenYear(year):
    movieList = []
    for movie, movie_info in movies_table.iteritems():
        if (movie_info[0] == year):
            movieList.append(movie)
    return movieList


#find all actors who were born in the given year
def findActorsInAGivenYear(year):
    actorList = []
    for actor, actor_info in actors_table.iteritems():
        if(actor_info[0].split(" ")[-1] == year):
            actorList.append(actor)
    return actorList


#find the index of entry oldestActorsList where the entry is the first entry whose year is smaller than actor_year
def findReplaceIndex(actor_year, oldestActorsList):
    for i in range(len(oldestActorsList)):
        if (actor_year < oldestActorsList[i][1]):
            return i
    return -1


#find the n oldest actors
def findOldestActors(n):
    oldestActorsList = [("", 2020)] * n
    for actor, actor_info in actors_table.iteritems():
        actor_year = actor_info[0].split(" ")[-1]
        if(actor_year.isdigit()):
            actor_year = int(actor_year)
            index = findReplaceIndex(actor_year, oldestActorsList)
            #replace the youngest actor(a1) in oldestActorsList with the new one if there's an actor older than a1
            if(index != -1):
                oldestActorsList.remove(oldestActorsList[index])
                oldestActorsList.append((actor, actor_year))
    return oldestActorsList


#Calculate the connections of each actors and store the information in Actors
Actors = []
for actorName, actorInfo in actors_table.iteritems():
    movieListOfAnActor = findMoviesOfAnActor(actorName)
    connection_count = 0
    for movieIndex in range(len(movieListOfAnActor)):
        try:
            actorsInAMovie = findActorsInAMovie(movieListOfAnActor[movieIndex][0])
            #for each movie that the actor worked in , count the number of actors in this movie
            for actorIndex in range( len(actorsInAMovie) ):
                if(actorsInAMovie[actorIndex][0] != actorName):
                    connection_count += 1
        except KeyError:
            continue
    Actors.append((actorName, connection_count))
print(Actors)
Actors.sort(key=lambda x:x[1])
print(Actors)


#select top 10 actors with highest connections
ActorsName = []
ActorsConnections = []
for i in range(len(Actors)-10, len(Actors)):
    ActorsName.append(Actors[i][0])
    ActorsConnections.append(Actors[i][1])


#plot top 10 actors that has most connections with other actors
colors = cm.rainbow(np.linspace(0,1,10))
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1)
plt.pie(ActorsConnections, explode=explode, labels=ActorsName, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title("Top 10 Hub Actors")
plt.show()

#calculate the grossing value of actors based on age(not age group)
ageToGrossValueTable = {}
for actorName, actorInfo in actors_table.iteritems():
    actorAge = actorInfo[0]
    actorGross = actorInfo[2]
    if(actorAge in ageToGrossValueTable):
        ageToGrossValueTable[actorAge] += actorGross
    else:
        ageToGrossValueTable[actorAge] = actorGross

#plot the grossing values of each age
ax = plt.subplot()
ax.bar(ageToGrossValueTable.keys(), ageToGrossValueTable.values(), width = 1, align='center')
ax.autoscale(tight=True)
plt.show()

#divide different ages into differene age groups
grossByAgeGroup = {"20-29": 0, "30-39": 0, "40-49": 0, "50-59": 0, "60-69": 0, "70-79": 0, "80-89": 0, "90-99": 0}
for age, gross in ageToGrossValueTable.iteritems():
    if(age >= 20 and age <= 29):
        grossByAgeGroup["20-29"] += gross
    elif(age >= 30 and age <= 39):
        grossByAgeGroup["30-39"] += gross
    elif (age >= 40 and age <= 49):
        grossByAgeGroup["40-49"] += gross
    elif (age >= 50 and age <= 59):
        grossByAgeGroup["50-59"] += gross
    elif (age >= 60 and age <= 69):
        grossByAgeGroup["60-69"] += gross
    elif (age >= 70 and age <= 79):
        grossByAgeGroup["70-79"] += gross
    elif (age >= 80 and age <= 89):
        grossByAgeGroup["80-89"] += gross
    elif (age >= 90 and age <= 99):
        grossByAgeGroup["90-99"] += gross

#store information about grossing value of each age group in ageGroupGross
ageGroup = []
ageGroupGross = []
for group, grossing in grossByAgeGroup.iteritems():
    ageGroup.append(group)
    ageGroupGross.append(grossing)

#plot the pie graph that shows the relations between age group and the grossing values sum of actors in this age group
fig = plt.figure(4, figsize=(10,10))
ax = fig.add_subplot(211)
colors = cm.rainbow(np.linspace(0,1,8))
pieChart = ax.pie(ageGroupGross, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
ax.axis('equal')

#plot the legend of the pie graph
ax2 = fig.add_subplot(212)
ax2.axis("off")
ax2.legend(pieChart[0], ageGroup, loc="center")

plt.title("Grossing Of Different Age Groups")
plt.show()
