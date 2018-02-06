from urllib2 import urlopen
from bs4 import BeautifulSoup
import Queue
import re
import urllib2
import json
import logging
from copy import deepcopy

#add information(name and url) of all movies listed in a wikitable at a certain actor's webpage
def addMovie(table):
    movieList = []
    movie = table.find_all("tr")
    for i in range(1, len(movie)):
        if (movie[i].find('a')):
            movie_url = 'https://en.wikipedia.org' + movie[i].a["href"]
            if (movie[i].find_all('th')):
                #if the text of movie name is surrounded by <th>
                for name in movie[i].find_all('th'):
                    movie_name = name.text.split(",")[0]
            else:
                curr_text = movie[i].find_all('td')[0].text
                if (curr_text[0:3].isdigit()):
                    #if the movie name is in the second <td> element
                    for name in movie[i].find_all('td')[1]:
                        if (hasattr(name, "text")):
                            movie_name = name.text.split(",")[0]
                else:
                    #if the movie name is in the first <td> element
                    for name in movie[i].find_all('td')[0]:
                        if (hasattr(name, "text")):
                            movie_name = name.text.split(",")[0]
            movieList.append((movie_name, movie_url))
    return movieList

'''
check if a given string is start with month
return True if the string stars with any month, o/w return False
'''
def stringStartsWithMonth(str):
    if (str.startswith("January")):
        return True
    elif (str.startswith("February")):
        return True
    elif (str.startswith("March")):
        return True
    elif (str.startswith("April")):
        return True
    elif (str.startswith("May")):
        return True
    elif (str.startswith("June")):
        return True
    elif (str.startswith("July")):
        return True
    elif (str.startswith("August")):
        return True
    elif (str.startswith("September")):
        return True
    elif (str.startswith("October")):
        return True
    elif (str.startswith("November")):
        return True
    elif (str.startswith("December")):
        return True
    else:
        return False

#return the index of a string that is a month in a list of strings
def getIndexOfMonth(born_info):
    for i in range(len(born_info)):
        if (stringStartsWithMonth(born_info[i])):
            return i
    else:
        return 0


#get the born date of an actor
def getBornDate(soup):
    try:
        born_info = soup.find(text=re.compile('Born')).parent.parent.text.split()
        monthIndex = getIndexOfMonth(born_info)
        if (len(born_info[monthIndex + 1]) >= 4):
            if (monthIndex):
                born_date = (born_info[monthIndex] + " " + born_info[monthIndex + 1]).replace(",", "")
                return born_date
        else:
            if (monthIndex):
                born_date = (
                born_info[monthIndex] + " " + born_info[monthIndex + 1] + " " + born_info[monthIndex + 2]).replace(",", "")
                return born_date
    except AttributeError:
        print("born date doesn't exist")
    return ""


#add information(name and url) of all movies hidden at the html text of a certain actor's webpage
def addMovieListsWithoutWikitable(soup):
    filmList = []
    filmography = soup.find("", {"id": "Filmography"})
    if (filmography):
        node = filmography.parent
        for film in node.findNext("ul").find_all("li"):
            film_name = film.text
            if (film.find('a')):
                film_url = 'https://en.wikipedia.org' + film.a["href"]
                filmList.append((film_name, film_url))
    return filmList


#get all movies(and their url) that an actor worked in based on the url of the actor's webpage
def getMovieListOfAnActor(soup):
    table1 = soup.find("table", {"class": "wikitable sortable"})
    table2 = soup.find("table", {"class": "wikitable plainrowheaders sortable"})
    movieList = []
    if (table1 is not None):
        movieList = addMovie(table1)
    elif (table2 is not None):
        movieList = addMovie(table2)
    else:
        movieList = addMovieListsWithoutWikitable(soup)
    return movieList


#convert a number to float based on its unit
def convertUnit(value, unit):
    if (unit.find("million") != -1):
        value = float(value) * 1000000
    elif (unit.find("billion") != -1):
        value = float(value) * 1000000000
    return value


#get the release year of a movie
def getReleaseYear(infobox):
    if (infobox.find(text=re.compile('Release date'))):
        full_date = infobox.find(text=re.compile('Release date')).parent.parent.parent.find("td").text
        date_info = full_date.split()
        if (len(date_info) == 1):
            year = full_date.split()[0]
        elif (len(date_info) == 2):
            year = full_date.split()[1]
        else:
            year = full_date.split()[2]
        return year
    else:
        return ""

#get the grossing value of a movie
def getGrossingValue(boxoffice_info):
    for boxoffice in boxoffice_info.find_all("td"):
        grossing = boxoffice.text.replace(",", "").split()
        if (len(grossing) > 1):
            grossing_value_number = float(grossing[0][1:])
        else:
            grossing_value_number = float(grossing[0][1:-3])

        if (len(grossing) > 1):
            grossing_value_unit = grossing[1]
            grossing_value = convertUnit(grossing_value_number, grossing_value_unit)
        else:
            grossing_value = grossing_value_number
    return grossing_value


#get the starring casts and grossing value of a movie
def getCastsAndGrossingValue(infobox):
    castsList = []
    grossing_value_number = 0

    for info in infobox.find_all("tr"):
        for info_th in info.find_all("th"):
            if (info_th.text.startswith("Star")):
                casts_info = info_th.parent
                if (casts_info.find_all("li")):
                    for cast in casts_info.find_all("li"):
                        if (cast.find('a')):
                            actor_url = "https://en.wikipedia.org" + cast.a["href"]
                            castsList.append((cast.text, actor_url))
            elif (info_th.text.startswith("Box")):
                boxoffice_info = info_th.parent
                grossing_value_number = getGrossingValue(boxoffice_info)

    return castsList, grossing_value_number


#get the release year, starring casts and grossing value of a movie
def getMovieInfo(infobox):
    year = getReleaseYear(infobox)
    casts_queue, grossing_value = getCastsAndGrossingValue(infobox)
    return year, casts_queue, grossing_value

actorsList = {}
moviesList = {}

with open('data.json') as json_file:
    all_data = json.load(json_file)
    print(all_data)

def addEmptyUrl(x): return (x, "")

for i in range(2):
    for itemName, itemInfo in all_data[i].iteritems():
        try:
            if(itemInfo["json_class"] == "Actor"):
                actorsList[itemName] = (itemInfo["age"], map(addEmptyUrl, itemInfo["movies"]), itemInfo["total_gross"])
            if (itemInfo["json_class"] == "Movie"):
                moviesList[itemName] = (itemInfo["year"], itemInfo["box_office"], map(addEmptyUrl, itemInfo["actors"]))
        except KeyError:
            continue


print(actorsList)
print(moviesList)

#write the given dictionary into a designated json file
def writeToJason(dict, file):
    json1 = json.dumps(dict)
    f1 = open(file,"w")
    f1.write(json1)
    f1.close()

writeToJason(actorsList, "actors.json")
writeToJason(moviesList, "movies.json")

print("finished scraping")