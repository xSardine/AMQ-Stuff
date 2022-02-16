# Party Rank Tools

- For Tools to create the Sheet itself automatically, and/or download every webm/mp4 needed, DM me on discord.

- Process Stats will output some stats such as how much people got their ranking close to the final result, or the affinity between people.

- Upload Party Rank will take as input a sheet you need to send to the player, and the list of player, and will automatically upload everything to your Google Drive. (You'll still have to send them the link to their sheet)

# Requirements

To use these scripts you will need python that you can download here: <https://www.python.org/downloads/>,
Make sure that it will make an environment variable for you when it will ask for it.

Once this is done, you need to install the python libraries for the script you want to use. Type this command in the CMD:

- For process_PR_stats.py:
```
python -m pip install matplotlib pandas scipy odfpy
```

- For upload_party.py:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

# Download and Start a script (Windows)

To download one of the scripts, you need to click on it on github, it will open the content. Click on `raw` at the top right of your screen. You can then `right click` and press `save as`.

To start it you can either:
- `Alt + Right click` the folder containing the script and select `Open Powershell`
- or type `cmd` in your windows search bar and open the command line interpretor. Then use the `cd` function to move into the folder containing the script. (i.e, if the script is in `Documents/PR_Tools/script.py`, then you use `cd Documents\PR_Tools\`)
  
After you've done one of these two steps, you can then type in the cmd:
```
python name_of_the_script.py
```

# Process Party Stats

exampleSheet.ods is a minimal sheet for which the script should work, just replicate it with your PR. You can have stuff on the left of the player grid as long as you fill in correctly the variables `START_COLUMN_PLAYER` and `START_LINE_PLAYER` to the right values within the script.

However, if you want to have stuff on the bottom of your sheet, then you'll need to update `NB_SONGS` variable for each PR. If you want stuff on the right of the PR, then you'll need to update `NB_PLAYERS`. These variables are used as coordinates to isolate the "player score grid" from the rest of the sheet to simulate the format of exampleSheet.ods.

Place the `PR final sheets` in the same folder as the script. Open the script with an editor and edit the different settings/variables to meet your sheet formats and the current PR.

You can then start the script and it will output a .txt file and an image in that same folder.

# 2. Upload Party Rank

## 2.1 Setting up Google Drive API

*might be outdated, search on google to help you do that*

If you wish to automatically upload 1 sheet per user to your google drive you need to follow additional steps, **this is only worth if you intend to do a lot of PR or PRs with a lot of people**:

You'll want to open your google cloud platform:
<https://console.developers.google.com/home/>
In the search bar, type `Google Drive API` and press enter. Wait a few seconds, once it is activated, click on `Create Credentials` on the top right.

It will ask how you will use the API, select user data as we will manage our own data. Press Next. It will ask more information about the application, since it's for personnal use, it doesn't really matter, just enter some random names for the necessary fields and enter your email.

It will now ask about which personal acces you will need for your application, this script will need to login (you will still have to provide your password when using it obviously), and create a new file in your drive, so let's add those:
- Click on `Add or Delete application domains`
- In the search filter, type `drive` and press enter
- Select the second and third elements ("Display, Modify, Update or **Create** files in your google drive")
- Go to the second page and select the element right before the last one ("Connect to Google Drive")
- Press `update` at the bottom of the page

You can now press `Save and Continue`.

It will now asks you which type of application this is, it doesn't really matter, just select `Desktop App` and keep the default name.

Click `create`.

You can now click the `download` button, it will give you a `.json` that you will put in the same folder as the rest. Rename this file `credentials.json`.

Final step: Go back to the menu on the top left of your screen, select `API and services`, select `OAuth Consent Screen`, scroll down a little and click on `Add User`. Enter the email related to the Google Drive account you will use to store your sheets. Press save twice and you're done.


## 2.2 Uploading every user custom sheet to google drive

- Place the script and the sheet you need to upload in the same folder.
- Edit the first few lines to meet your PR configuration
- You can then upload a sheet per user into google drive with this command in your cmd:
```
python upload_party_rank_sheet.py
```
You will have to use your logins the first time. A new file `token.json` will be created and will let you use the script without logging in as long as it is in the folder.

By default, the files will be uploaded in `~/<file_name> PR/<file_name> (<user_name>).extension`.

(example for the file name "Nonoc.ods": `~/Nonoc PR/Nonoc (User).ods`)