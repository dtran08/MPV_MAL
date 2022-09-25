import os
# import sys
# import traceback
import json
import os.path
import requests
import difflib
from flask import jsonify
from dataGenerator import AnimeMap
from generateMALToken import *

#prompt user: MAL username and password, logout option
#parameters: log file of generated data

"""
prompt user for username/password, store to vars
automate headless navigation to MAL (do this head-on first)
on MAL site, automate the following:
-login
-click search bar
-paste anime name from data and search
-click the correct anime (how to distinguish between ovas and movies?)
-add all episodes from map to account
"""


"""
alternative: MAL API
requires the user to register for MAL API and store a client id and secret on their machine
prompt them to input their secrets and login to generate an access token
use the access token to perform api calls to update profile using map of anime (see dataGeneration.py)
extra: allow ratings and other options for adding episodes per-episode
can make the entire thing a CLI to run a command to watch the anime (or multiple), and once mpv stops, prompt to update MAL
"""  

def getAccessTokenFromFile():
    accessJson = open("token.json")
    data = json.load(accessJson)
    tokenMap = {}
    for i in data:
        tokenMap[i] = data[i]    
    return tokenMap

def setup():
    """
    Called if user wants to set up their MAL user validation (credentials/Client ID/Secret)
    """
    userClientID = input("Enter Client ID: ")
    userClientSecret = input("Enter Client Secret: ")

    print('Starting access token setup...')
    #get code challenge and put it into getting new auth url
    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorisation_url(code_challenge, userClientID)

    #after getting auth url, prompt to enter the auth code given
    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    #generate token
    token = generate_new_token(authorisation_code, code_verifier, userClientID, userClientSecret)

    print_user_info(token['access_token'])
    f = open("access_token.txt", "w")
    f.write(token['access_token'])
    f.close()
    print("Setup complete!")

def retrieveAccessToken():
    f = open("access_token.txt", "r")
    return f.read()

def main():
    if not os.path.isfile('token.json'):
        print("The file token.json was not found in local directory. Performing first-time setup...")
        setup()
    else:
        while True:
            promptSetup = input("Set up MAL API authorization? (Y/N) ")
            promptSetup = promptSetup.lower()
            if promptSetup not in ('y', 'n'):
                print("Invalid input")
                continue
            elif promptSetup == 'y':
                print("Performing setup...")
                setup()
                break
            elif promptSetup == 'n':
                break
    print("Getting access token...")
    access_token = getAccessTokenFromFile()["access_token"]

    print("Fetching recently viewed anime...")
    aniMap = AnimeMap()

    while True:
        clearFile = input("Clear recently viewed file? (Y/N) ")
        clearFile = clearFile.lower()
        if clearFile not in ('y', 'n'):
            print("Invalid input")
            continue
        elif clearFile == 'y':
            open(os.environ['HOME'] + '/.config/mpv/history.log', 'w').close()
            break
        elif clearFile == 'n':
            break

    # print(retrieveAccessToken())
    print(aniMap)

    for show in aniMap.keys():
        urlSearch = 'https://api.myanimelist.net/v2/anime'
        headersSearch = {'Authorization': 'Bearer ' + str(retrieveAccessToken()),}
        paramsSearch = {
            'q': show,
            'limit': '10',
            'fields': 'anime',
            'nsfw': '1',
        }
        # get show id
        rSearch = requests.get(urlSearch, params=paramsSearch, headers=headersSearch)
        if rSearch.json()['data'][0]['node']['title'] in show:
            animeID = rSearch.json()['data'][0]['node']['id']
            print("Found show " + rSearch.json()['data'][0]['node']['title'] + " from downloaded show " + show)
        else:
            animeID = None
        print("")
        # add episodes
        urlAdd = 'https://api.myanimelist.net/v2/anime/' + str(animeID) + '/my_list_status'
        headersAdd = {'Authorization': 'Bearer ' + str(retrieveAccessToken()),}
        dataAdd = {
            'num_watched_episodes': len(aniMap[show])
        }
        rAdd = requests.put(urlAdd, headers=headersAdd, data=dataAdd)
        print(rAdd)

main()