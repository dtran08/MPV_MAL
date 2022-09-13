Currently, this contains the code needed to record episode names in a log file when opened in mpv only.

To do this, take the save.lua script and drop it into /home/username_here/.config/mpv/scripts/

When running a file in mpv, it will log it into a file called history.log

Uses anitopy (python library: https://github.com/igorcmoura/anitopy) to parse filename

Uses selenium 4.4.3

To Do:
-Load MAL database and do initial testing
-Headless browsing on MAL
-Configure parsing to load into MAL database