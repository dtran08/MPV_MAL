WIP application to save anime episodes played in mpv and update a user's MyAnimeList profile with the amount of episodes watched.

Currently supported on Unix systems.
Uses anitopy (python library: https://github.com/igorcmoura/anitopy) to parse filename for anime metadata.
Uses MyAnimeList API to search for and update your profile.

You will need a script to record episode names in a log file when opened in the mpv media player.
To do this, take the `save.lua` script and drop it into /home/username_here/.config/mpv/scripts/ (TO DO: automatically drop into user's mpv config path)
When running a file in mpv, it will log it into a file called history.log

Make sure your anime files are titled properly! The filename must include the same or similar name as what is found on MAL. The MAL API should also accept the English form of the anime as well, so no need to worry about romanji to English formatting.

First Time Setup:
-Run `automation.py`
-If this is the first time setting up your MAL account, you will be prompted to enter your client ID and client secret. Store these values accordingly. (TO DO: have user store in formatted json file and read from that)
-You will be prompted to click a link to authorize your account for access token creation. After clicking "Allow", copy the token in the url (format: `https://github.com/dtran08/MPV_MAL?code=token_here`)
-The script will automatically create a file called `access_token.txt` containing your access token. It will read from this file when calling any endpoints.

Normal Run:
-Watch anime in mpv. The `save.lua` script will automatically log all anime watched.
-Run `automation.py`
-Type y/n to set up the MAL API authorization again (if your client ID and client secret change, you will need to do this).
-Type y/n to clear your mpv log history file (this is recommended as the MAL API accepts *amounts* of episodes, rather than episode numbers).
-Assuming that your anime files have accurate naming conventions similar/same to the MAL database, the API will add the *first* result found on its search query to your account, as well as the amount of episodes watched.