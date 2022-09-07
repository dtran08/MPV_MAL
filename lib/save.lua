-- https://github.com/mpv-player/mpv/blob/master/DOCS/man/lua.rst for docs
-- set a local variable HISTFILE to a string
-- this string will be either APPDATA or HOME envvars (nil or /home/doug respectively), and concatenate /mpv/history.log
local HISTFILE = (os.getenv('APPDATA') or os.getenv('HOME')..'/.config')..'/mpv/history.log';

-- when file-loaded state, call this function
-- TO DO: make sure that when we load MAL database, parse correctly to match up episode names and anime titles
mp.register_event('file-loaded', function()
    local title, fp;
    -- get title of media
    title = mp.get_property('media-title');
    title = (title == mp.get_property('filename') and '' or (' (%s)'):format(title));
    -- title = ''; -- uncomment here

    -- open the log file and write the timestamp and title, then close it
    fp = io.open(HISTFILE, 'a+');
    fp:write(('%s%s\n'):format(mp.get_property('path'), title));
    fp:close();
end);

-- mp.register_event('idle', function()
--     local fp, last;
--     local pos;

--     fp = io.open(HISTFILE, 'r');
--     last = '';

--     if not fp then
--         return
--     end

--     fp:seek('end', -200);

--     for line in fp:lines() do
--         last = line;
--     end;

--     fp:close();

--     pos = last:find(']');
--     last = last:sub(pos + 2);

--     mp.commandv('loadfile', last);
-- end);