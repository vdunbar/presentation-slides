#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:26:04 2023

@author: vdunbar
"""

from bs4 import BeautifulSoup
import requests as rq
import json
from time import sleep
from random import randint
import pandas as pd

# store the request for available time stamps between 2018-01-01 and 2019-04-31
# with output to a json data structure in a variable called fem_film
fem_film = 'http://web.archive.org/cdx/search/cdx?url=femfilm.ca/&from=20180101&to=20190431&output=json'

# pass the above url to the internet archive and store the results locally
# in a variable called urls
fem_film_data = rq.get(fem_film).text

# print the fem_film_data
print(fem_film_data)

#convert fem_film_data from json to python dictionary
parse_fem_film_data = json.loads(fem_film_data)

print(parse_fem_film_data)

# list only the relevant pieces
for i in range(1, len(parse_fem_film_data)):
    print(parse_fem_film_data[i][2],parse_fem_film_data[i][1], sep='\t')
    
# build a list of urls from the data we have. We start with an empty list object
url_list = []

# then we iterate through our response from the IA and build the urls we want to scrape
for i in range(1, len(parse_fem_film_data)):
    prepend = 'https://web.archive.org/web/'
    orig_url = parse_fem_film_data[i][2]
    tstamp = parse_fem_film_data[i][1]
    wayback_link = prepend + tstamp + '/'+orig_url + 'index.php?lang=e'
    url_list.append(wayback_link)

# print the list for review
url_list

# start a counter
reqs = 0

# build empty lists to hold the repsective data
references = []
quotations = []
films = []
directors = []

for link in range(len(url_list)): # start a loop to iterate over our urls
    url = url_list[link] # grab the nth link in url_list and assign to the variable ulr
    response = rq.get(url) # request to content at the url
    sleep(randint(5,10)) # pause to be polite
    reqs += 1 # uptick the request counter
    if response.status_code == 404: # if the page does not exist, add NA as the value to the variable we're collecting
        reference = "NA"
        quotation = "NA"
        film = "NA"
        director = "NA"
    else: # if the page does not give a 404 error
        page = response.text # get the text content from the response
        page_bs = BeautifulSoup(page, 'html.parser') # create a beautiful soup object of that text
        tables = page_bs.find_all('table') # find all the tables on the page
        tables_strong = tables[1].find_all('strong') # isolate the second table and all content in it wrapped in a strong tag
        for content in tables_strong: # start a loop to interate over the tables_strong content
            reference = tables_strong[1].text # put the text in the second strong tag into a reference variable
            quotation = tables_strong[2].text # and the third into quotation
            film = tables_strong[3].text # the fourth into film
            director = tables_strong[4].text # and the fifth into director
    print(url, reference, quotation, film, director, sep = '\n') # print the output to the console
    references.append(reference) # add reference to the references list and thsame for the next 3 lines
    quotations.append(quotation)
    films.append(film)
    directors.append(director)

# write the lists with the content we've collected to a csv file
wb_output = pd.DataFrame({'url':url_list
                       ,'references':references
                       ,'quotations':quotations
                       ,'films':films
                       ,'directors':directors})
wb_output.to_csv('~/Desktop/fem_film_data.csv',index=False)
