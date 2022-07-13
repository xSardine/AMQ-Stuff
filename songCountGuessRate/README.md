mshift's S/A script that me and Husa modified to keep only the songCounter part

It will display the number of time a song have appeared and your guess rate on it in the song info box.

## Song Count + Guess Rate

If you're one of the few people that uses the S/A script as well, do not use this as idk if they are compatible.

## Installation

- Install [tampermonkey](https://www.tampermonkey.net/) if you don't have it already

- Install [Node.js](https://nodejs.org/en/), download the recommended version

- Download the [node_modules.zip](https://github.com/xSardine/AMQ-Stuff/raw/main/songCountGuessRate/node_modules.zip), and the [index.js script](https://raw.githubusercontent.com/xSardine/AMQ-Stuff/main/songCountGuessRate/index.js) (right click → save as) from this repository. Place them in the same directory and extract the `node_modules.zip` archive.

- Add the [tampermonkey_script](https://github.com/xSardine/AMQ-Stuff/raw/main/songCountGuessRate/tampermonkey_script.user.js) in Tampermonkey

The preparation should be done, you can now start the local server and start playing AMQ.
This server will be called at the end of each song and save your stats on the songs, it will then send it back to the userscript that will display the information on the song info box.

To start the local server:

- Open the powershell in the directory: `Shift + Right-Click` on the folder where your files are located, then click `Open PowerShell window here`
- Type `node index.js` in the shell window

You should see a message that the HTTP server is listening. Make sure to keep this window open whenever you're playing AMQ

### Known issue

If the song name or the artist change/get fixed, it will reset the song count and guess rate as it will detect is as a whole new song. I could technically fix this, but I'm not sure it's worth it. So it won't be anytime soon.
If somehow a song for which you had a lot of plays and you wish to keep your data happens to be one of the like 20 songs updated each months out of 28 000, you can work around this problem by using database editing tools to update the song name and artist directly on your local database. [SQLite Browser](https://sqlitebrowser.org/) for example would let you do that.
