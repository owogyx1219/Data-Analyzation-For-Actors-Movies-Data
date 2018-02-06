from flask import Flask, jsonify, request
import json

app = Flask(__name__)

#Filters out all actors that do not have a certain string in their name
@app.route('/actors', methods=['GET'])
def api_filterActor():

    with open('actors.json') as json_file:
        actors_table = json.load(json_file)

    requestArg = request.args.get('name')
    or_request = requestArg.split("|")
    and_request = requestArg.split("&")

    conditions = []
    retActors = {}

    #handle the OR operator
    if(len(or_request) > 1):
        #collect all conditions from request
        for i in range(len(or_request)):
            condition = or_request[i].split("=")[-1]
            if(condition.find('"') != -1):
                condition = condition[1:-1]
            conditions.append(condition)

        #find all actors that meet one of the condition
        for actorName, actorInfo in actors_table.iteritems():
            for i in range(len(conditions)):
                if(conditions[i].isalpha()):
                    if(conditions[i] in actorName):
                        retActors[actorName] = actorInfo
                else:
                    if(int(conditions[i]) == actorInfo[0]):
                        retActors[actorName] = actorInfo
        return jsonify(retActors)

    #handle the AND operator
    elif(len(and_request) > 1):
        #collect all conditions from request
        for i in range(len(and_request)):
            condition = and_request[i].split("=")[-1]
            if (condition.find('"') != -1):
                condition = condition[1:-1]
            conditions.append(condition)

        #find all actors that meet all of the conditions
        condition_met = True
        for actorName, actorInfo in actors_table.iteritems():
            for i in range(len(conditions)):
                if (conditions[i].isalpha()):
                    if (not (conditions[i] in actorName)):
                        condition_met = False
                else:
                    if (int(conditions[i]) != actorInfo[0]):
                        condition_met = False
            if(condition_met):
                retActors[actorName] = actorInfo
        return jsonify(retActors)

    #handle the case that there is only one condition
    else:
        filterName = request.args.get('name')[1:-1]
        for actorName, actorInfo in actors_table.iteritems():
            if(filterName in actorName):
                retActors[actorName] = actorInfo
        return jsonify(retActors)


#Filters out all actors that do not have a certain string in their name
@app.route('/movies', methods=['GET'])
def api_filterMovie():

    with open('movies.json') as json_file:
        movies_table = json.load(json_file)

    or_request = request.args.get('name').split("|")
    and_request = request.args.get('name').split("&")

    conditions = []
    retMovies = {}

    #handle the OR operator
    if (len(or_request) > 1):
        #collect all conditions from request
        for i in range(len(or_request)):
            condition = or_request[i].split("=")[-1]
            if (condition.find('"') != -1):
                condition = condition[1:-1]
            conditions.append(condition)

        #find all actors that meet one of the conditions
        for movieName, movieInfo in movies_table.iteritems():
            for i in range(len(conditions)):
                if (conditions[i].isalpha()):
                    if (conditions[i] in movieName):
                        retMovies[movieName] = movieInfo
                else:
                    if (int(conditions[i]) == movieInfo[0]):
                        retMovies[movieName] = movieInfo
        return jsonify(retMovies)

    #handle the AND operator
    elif (len(and_request) > 1):
        #collect all conditions from request
        for i in range(len(and_request)):
            condition = and_request[i].split("=")[-1]
            if (condition.find('"') != -1):
                condition = condition[1:-1]
            conditions.append(condition)

        #find all actors that meet all of the conditions
        for movieName, movieInfo in movies_table.iteritems():
            for i in range(len(conditions)):
                if (conditions[i].isalpha()):
                    if (conditions[i] in movieName):
                        retMovies[movieName] = movieInfo
                else:
                    if (int(conditions[i]) == movieInfo[0]):
                        retMovies[movieName] = movieInfo
        return jsonify(retMovies)

    #handle the case that there is only one condition
    else:
        filterName = request.args.get('name')[1:-1]
        retMovies = {}
        for movieName, movieInfo in movies_table.iteritems():
            if(filterName[1:-1] in movieName):
                retMovies[movieName] = movieInfo
        return jsonify(retMovies)


#Returns the first Actor object that has correct name, displays movie attributes and metadata
@app.route('/actors/<string:name>', methods=['GET'])
def api_getActor(name):
    with open('actors.json') as json_file:
        actors_table = json.load(json_file)
    for actorName, actorInfo in actors_table.iteritems():
        if(actorName.replace(" ", "") == name.replace("_", "")):
            retActor = {actorName: actorInfo}
            return jsonify(retActor)
    return jsonify({})


#Returns the first Movie object that has correct name, displays movie attributes and metadata
@app.route('/movies/<string:name>', methods=['GET'])
def api_getMovie(name):
    with open('movies.json') as json_file:
        movies_table = json.load(json_file)
    for movieName, movieInfo in movies_table.iteritems():
        if(movieName.replace(" ", "") == name.replace("_", "")):
            retMovie = {movieName: movieInfo}
            return jsonify(retMovie)
    return jsonify({})


#write the dictionary into a jason file
def writeToJason(dict, file):
    json1 = json.dumps(dict)
    f1 = open(file, "w")
    f1.write(json1)
    f1.close()


#change attribute of an actor in the jason file by Leveraging PUT requests
@app.route('/actors', methods=['PUT'])
def updateActor():
    request.get_data()
    data_info = request.data.split(" ")
    update_info = data_info[-2][2:-2]
    update_key_value = update_info.split(":")
    update_key = update_key_value[0][1:-1]
    update_value = update_key_value[1]
    actorName = data_info[-1].split("/")[-1].replace("_", " ")

    with open('actors.json') as json_file:
        actors_table = json.load(json_file)
    for actor_name, actorInfo in actors_table.iteritems():
        if(actor_name == actorName):
            if(update_key == "total_gross"):
                actorInfo[2] = int(update_value)
            elif(update_key == "age"):
                actorInfo[0] = int(update_value)

    writeToJason(actors_table, "actors.json")
    return("updated actor's" + " " + update_key + " to " + update_value)


#change attribute of an movie in the jason file by Leveraging PUT requests
@app.route('/movies', methods=['PUT'])
def updateMovie():
    request.get_data()
    data_info = request.data.split(" ")
    update_info = data_info[-2][2:-2]
    update_key_value = update_info.split(":")
    update_key = update_key_value[0][1:-1]
    update_value = update_key_value[1]
    movieName = data_info[-1].split("/")[-1].replace("_", " ")

    with open('movies.json') as json_file:
        movies_table = json.load(json_file)
    for movie_name, movieInfo in movies_table.iteritems():
        if(movie_name == movieName):
            if(update_key == "year"):
                movieInfo[0] = int(update_value)
            if(update_key == "box_office"):
                movieInfo[1] = int(update_value)

    writeToJason(movies_table, "movies.json")
    return("updated movie's" + " " + update_key + " to " + update_value)


#delete an Actor Object in the backend by Leveraging DELETE requests
@app.route('/actors', methods=['DELETE'])
def removeActor():
    request.get_data()
    data_info = request.data.split(" ")[-1]
    actorName = data_info.split("/")[-1].replace("_", " ")

    with open('actors.json') as json_file:
        actors_table = json.load(json_file)

    del actors_table[actorName]

    writeToJason(actors_table, "actors.json")
    return ("removed" + " " + actorName)


#delete an Movie Object in the backend by Leveraging DELETE requests
@app.route('/movies', methods=['DELETE'])
def removeMovie():
    request.get_data()
    data_info = request.data.split(" ")[-1]
    movieName = data_info.split("/")[-1].replace("_", " ")

    with open('movies.json') as json_file:
        movies_table = json.load(json_file)

    del movies_table[movieName]

    writeToJason(movies_table, "movies.json")
    return ("removed" + " " + movieName)


#add an Actor Object in the backend by Leveraging POST requests
@app.route('/actors', methods=['POST'])
def addActor():
    request.get_data()
    table = []
    data_info = request.data.split("'{")[-1].split("}'")[0].split(",")
    newActorName = ""

    #parse the information of the new actor and add them to table
    for i in range(len(data_info)):
        key_value = data_info[i].split(":")
        key = key_value[0].replace('"', '').replace(" ", "")
        value = key_value[1]

        if(key == "name"):
            newActorName = value[1:-1]
        elif(key == "total_gross" or key == "age"):
            table.insert(len(table), int(value.replace(" ", "")))
        else:
            table.insert(len(table), value[1:-1])

    with open('actors.json') as json_file:
        actors_table = json.load(json_file)

    #update backend
    actors_table[newActorName] = table
    writeToJason(actors_table, "actors.json")

    return ("added actor: " + newActorName)


#add an Movie Object in the backend by Leveraging POST requests
@app.route('/movies', methods=['POST'])
def addMovie():
    request.get_data()
    table = []
    data_info = request.data.split("'{")[-1].split("}'")[0].split(",")
    newMovieName = ""

    #parse the information of the new movie and add them to table
    for i in range(len(data_info)):
        key_value = data_info[i].split(":")
        key = key_value[0].replace('"', '').replace(" ", "")
        value = key_value[1]

        if(key == "name"):
            newMovieName = value[1:-1]
        elif(key == "box_office" or key == "year"):
            table.insert(len(table), int(value.replace(" ", "")))
        else:
            table.insert(len(table), value)

    with open('movies.json') as json_file:
        movies_table = json.load(json_file)

    #update backend
    movies_table[newMovieName] = table
    writeToJason(movies_table, "movies.json")

    return ("added actor: " + newMovieName)

if __name__ == '__main__':
    app.run(debug=True, port=8002)
