import httplib
import json

httpServ = httplib.HTTPConnection("127.0.0.2", 80)
httpServ.connect()

#test filter actor request
httpServ.request('GET', "/actors?name='Bob'")
actor_name = "Bob"

response = httpServ.getresponse()
with open('actors.json') as json_file:
    actors_table = json.load(json_file)
if response.status == httplib.OK:
    print(actor_name)
    for actorName, actorInfo in actors_table.iteritems():
        if(actor_name in actorName):
            print(actorName)
            print(actorInfo)


# test filter actor request
httpServ.request('GET', "/movies?name='sleeping'")
movie_name = "sleeping"

response = httpServ.getresponse()
with open('movies.json') as json_file:
    movies_table = json.load(json_file)
if response.status == httplib.OK:
    print(movie_name)
    for movieName, movieInfo in movies_table.iteritems():
        if (movie_name in movieName):
            print(movieName)
            print(movieInfo)



#test get actor request
httpServ.request('GET', "/actors/Bruce_Willis")
actor_name = "Bruce_Willis"

response = httpServ.getresponse()
with open('actors.json') as json_file:
    actors_table = json.load(json_file)
if response.status == httplib.OK:
    print(actor_name)
    for actorName, actorInfo in actors_table.iteritems():
        if(actorName.replace(" ", "") == actor_name.replace("_", "")):
            print(actorName)
            print(actorInfo)



# test filter movie request
httpServ.request('GET', "/movies/Rock_the_Kasbah")
movie_name = "Rock_the_Kasbah"

response = httpServ.getresponse()
with open('movies.json') as json_file:
    movies_table = json.load(json_file)
if response.status == httplib.OK:
    print(movie_name)
    for movieName, movieInfo in movies_table.iteritems():
        if (movieName.replace(" ", "") == movie_name.replace("_", "")):
            print(movieName)
            print(movieInfo)


httpServ.close()