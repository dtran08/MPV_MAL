import sys
import os
from typing import Dict, List
import anitopy


"""
loop through log file
foreach separate line, remove the path and only keep the file name
run anitopy per line
parse data, group anime into map of series:[episodes]
"""
def AnimeMap():
    infile = os.environ['HOME'] + '/.config/mpv/history.log'
    assert os.path.exists(infile), "File was not found at " + str(infile)
    with open(infile) as mediaList:
        mediaList = mediaList.readlines()    
    for cur in range(len(mediaList)):
        mediaList[cur] = os.path.basename(mediaList[cur])
        # print(os.path.basename(show))
        # show = os.path.basename(show)

    aniMap = {}

    for cur in range(len(mediaList)):
        showdata = anitopy.parse(mediaList[cur])
        title = showdata['anime_title']
        episode = showdata['episode_number'].lstrip('0')
        if title not in aniMap:
            aniMap[title] = []
        aniMap[title].append(episode)
    return aniMap