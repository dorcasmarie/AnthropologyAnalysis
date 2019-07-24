import pandas as pd
import requests
import requests_cache
import sqlite3
import time
import json
import configparser
import re

data = pd.read_csv('data_clean.csv', sep='\t')

oclc_nums = data["oclc_number"].tolist()

db_filename = '/Users/washids/Dev/Anthropology/ClusterPython/WorldCatData.db'

connection = sqlite3.connect(db_filename)
c = connection.cursor()

requests_cache.install_cache('oclc_cache', backend='sqlite', expire_after=1814400) #expires after 3 weeks

errors = []
config = configparser.ConfigParser()
config.read('WorldCatAPI.ini')
location = config['WorldCatAPI']['location']
wskey = config['WorldCatAPI']['wskey']
for i, num in enumerate(oclc_nums):
    print("Pulling: ", str(i))
    url = str('http://www.worldcat.org/webservices/catalog/content/libraries/' + str(num) + '?')
    params = {'location': location,
              'wskey': wskey,
              'format': 'json'}
    response = requests.get(url, params=params, timeout=30) #times out after 30 seconds
    # title, author, publisher, date, OCLCnumber, library, institutionName, city, state, postalCode, distance
    content = response.content.decode() #this step is required to reformat the json
    #formatted = re.sub('\\[', '[', content)
    formatted = re.sub(r"\\]", "]", content) #reformat json
    formatted = re.sub(r"\"ARTeHIS \"Archéologie, Terre, Histoire, Sociétés\"",
                       "\"ARTeHIS, Archéologie, Terre, Histoire, Sociétés", formatted) #reformat json
    formatted = re.sub(r"Biblioteca \"Guido Horn d\'Arturo\" dell\'Universita\' e dell\'",
                       "Biblioteca \'\'Guido Horn d\'Arturo\'\' dell\'Universita\' e dell\'", formatted)
        #res_obj = response.json()
    print(formatted) #printing because I'm getting badly formmatted json from the API
    res_obj = json.loads(formatted) #load json
    #don't forget to clear the BOOKS and libraries tables in the WORLDCAT database if you run again
    try: #this is to create the books table
        create_sql = """INSERT INTO BOOKS (
            title,
            author,
            publisher,
            date_pub,
            oclc_number
        ) VALUES (?,?,?,?,?);"""
        c.execute(create_sql, (res_obj['title'], res_obj['author'], res_obj['publisher'], res_obj['date'], res_obj['OCLCnumber']))
        book_id = c.lastrowid
        connection.commit()

        for library in res_obj['library']: #this is to create the libraries table

            create_sql = """INSERT INTO libraries (
                institution_name,
                city,
                us_state,
                country,
                postal_code,
                oclc_symbol,
                distance,
                book_number
             ) VALUES (?,?,?,?,?,?,?,?);"""

            c.execute(create_sql, (library['institutionName'], library['city'], library['state'], library['country'], library['postalCode'], library['oclcSymbol'], library['distance'], book_id))
        connection.commit()
    except Exception as e:
        print(e)
        errors.append(num)

print(errors)
now = time.ctime(int(time.time()))
print("Time: {0} / Used Cache: {1}".format(now, response.from_cache))
