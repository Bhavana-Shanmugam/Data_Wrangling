#The text in the document by <Bhavana_Shanmugam> is licensed under CC BY 3.0 https://creativecommons.org/licenses/by/3.0/us/
#The code in the document by <Bhavana_Shanmugam> is licensed under the MIT License https://opensource.org/licenses/MIT

import urllib
import urllib.request as uReq
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from time import time
from random import randint
import pickle
import requests
from requests import get

#Creating lists
names = []
imdb_ratings = []
metascores = []
genre = []
runtime = []

start_time = time()
requests = 0

headers = {"Accept-Language": "en-US, en;q=0.5; charset=UTF-8"}
i=0

start = 1
end = 0

mainCounter = 1

#IMDB URL to be accessed
parentUrl  = 'https://www.imdb.com'
childUrl = '/search/title?year=2017&title_type=feature'

#Loop created to scrape multiple pages
i=0
for i in range(10):

    if mainCounter % 200 == 0:
        #Using Pandas Framework
        movie_ratings = pd.DataFrame({
                            'Movie': names,
                            'Genre': genre,
                            'Runtime': runtime,
                            'Imdb_Rating': imdb_ratings,
                            'Metascore_Rating': metascores,
                            })

        print(movie_ratings.info())

        movie_ratings.to_csv('batch-10-' + str(mainCounter) +'.csv', index=False )
        names = []
        imdb_ratings = []
        metascores = []
        genre = []
        runtime = []


    mainUrl = parentUrl + childUrl
    response = get(mainUrl) #Fetches info from the URL

    page_html = BeautifulSoup(response.text, 'html.parser') #BeautifulSoup converts it into a soup object

    mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

    next = str(page_html.find('a',class_= 'lister-page-next next-page'))
    startIndex = next.find('href="') + 6
    endIndex = next.find('">Next')

    childUrl = next[startIndex:endIndex]

    for container in mv_containers:

        name = container.h3.a.text
        names.append(str(name).strip()) #Fetching name of the movie

        if container.strong is not None:
            imdb = float(container.strong.text)
        else:
            imdb = 0.0
        imdb_ratings.append(imdb) #Fetching IMDB Ratings

        if container.find('div', class_ = 'ratings-metascore') is not None:
            m_score = container.find('span', class_ = 'metascore').text
        else:
            m_score = 0.0
        metascores.append(int(m_score)) #Fetching Metascores Rating

        if container.find('span', class_ = 'genre') is not None:
            genreData = str(container.find('span', class_ = 'genre').text)
        else:
            genreData = 'NA'
        genre.append(str(genreData).strip()) #Fetching Genre information

        if container.find('span', class_ = 'runtime') is not None:
            run = str(container.find('span', class_ = 'runtime').text)
        else:
            run = 'NA'
        runtime.append(str(run).strip()) #Fetching runtime of the movie

    mainCounter = mainCounter + 1
    i=i+1

#Storing the values in a data frame
movie_ratings = pd.DataFrame({
                            'Movie': names,
                            'Genre': genre,
                            'Runtime': runtime,
                            'Imdb_Rating': imdb_ratings,
                            'Metascore_Rating': metascores
                            })

#Exporting the data frame contents to a CSV file
movie_ratings.to_csv('Films_list_1.csv', index=False )