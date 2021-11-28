mshift's S/A script that me and Husa modified to keep only the songCounter part

## Song Count + Guess Rate
It might not be 100% legal because you're scrapping AMQ database, but Husa made it public, so I might as well. ~~don't worry, you can use it no one cares~~

If you're one of the few people that uses the S/A script as well, do not use that version yet.

## Installation

- Install Node.js
Go to https://nodejs.org/en/ , download the recommended version and install it

- Download the files in this directory (click on them, raw, right click, download)

- Download the necessary modules by extracting node_modules.zip

- Add the tampermonkey_script.js in Tampermonkey

- Open the powershell in the directory: Shift + Right-Click on the folder 'songHistory' then 'Open PowerShell window here'

 
The preparation should be done, you can now start the server and start playing AMQ.

To start the server: `node index.js` in the shell window
You should see a message that the HTTP server is listening. Make sure to keep this window open whenever you're playing AMQ

If either:
The song name or the artist change/get fixed, it will reset the song count and guess rate as it will detect is as a whole new song, it's "normal" as that's how mshift's script work. Maybe i'll improve that someday. (no)

