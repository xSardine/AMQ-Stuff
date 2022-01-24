# Party Rank Tools

- For Tools to create the Sheet itself automatically, and/or download every webm/mp4 needed, DM me on discord.

- Process Stats will output some stats such as how much people got their ranking close to the final result, or the affinity between people.

- Upload Party Rank will take as input a sheet you need to send to the player, and the list of player, and will automatically upload everything to your Google Drive.

# Requirements

To use these scripts you will need python that you can download here: <https://www.python.org/downloads/>,
Make sure that it will make an environment variable for you when it will ask for it.

Once this is done, you need to install the python libraries I'm using for these scripts by typing this command in the CMD:

- For process_stats.py:
```
python -m pip install matplotlib
python -m pip install pandas
python -m pip install scipy
```

- For upload_party.py:
```
python -m pip install openpyxl
python -m pip install pydrive
```

# Download and Start a script (Windows)

To download one of the scripts, you need to click on it on github, it will open the content. Click on `raw` at the top right of your screen. You can then `right click` and press `save as`.

To start it you can either:
- `Alt + Right click` the folder containing the script and select `Open Powershell`
- Type `cmd` in your windows search bar and open the command line interpretor. Then use the `cd` function to move into the folder containing the script. (i.e, if the script is in `Documents/PR_Tools/script.py`, then you use `cd Documents\PR_Tools\`)
  
After you've done one of these two steps, you can then type in the cmd:
```
python name_of_the_script.py
```

# Process Party Stats

exampleSheet.ods is a minimal sheet for which the script should work, just replicate it with your PR. You can have stuff on the left and the right of this minimal information (like ids, song names, totals, ...) as long as you change the variables to the right values, however nothing should be on the top or the bottom.

If the players `ranked` the songs, then you need to use `process_party_rank_stats.py`, otherwise, if they `rated` the songs, you need to use `process_party_rate_stats.py`

Place the `PR final sheets` you want stats from in the same folder as the script. Open the script with an editor and put the right amount of people in the `NB_PLAYERS` variable.

You can then start the script and it will output a .txt file and an image in that same folder.

# 2. Upload Party Rank

## 2.1 Setting up Google Drive API

*might be outdated, search on google to help you do that*

If you wish to automatically upload each sheet to your google drive you need to follow additional steps:

You can start by following the steps described in the first 3 pages of this pdf:
<https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf>, the process changed after the 4th page, so I'll be continuing here.

Once you've done this, click on `Create Credentials`, it will brings you to a form.
For the first question, select the `Google Drive API`, the second question, select `users data`, after this, it will ask further information about your apps, since it will be only personal use, it doesn't matter and you can give it a random name. Enter you google email adress you're using to store your party ranks.

It will now ask about which personal acces you will need for your application, this script will need to login (you will still have to provide your password obviously), and create a new file in your drive, so let's add those:
- Click on `Add or Delete application domains`
- In the search filter, type `drive` and press enter
- Select the second and third elements ("Display, Modify, Update or **Create** files in your google drive")
- Go to the second page and select the element right before the last one ("Connect to Google Drive")
- Press `update` at the bottom of the page

You can now press `Save and Continue`.

It will now asks you which type of application this is, it doesn't really matter, just select `Desktop App` and keep the default name.

Click `create`.

You can now click the `download` button, it will give you a `.json` that you will put in the same folder as the rest. You can find your `Client ID` and `Client Secret` in that file, copy and paste them in their respective field in the `settings.yaml` file. You can now delete the `.json` file downloaded previously.

Final step: on the google project interface, on the left, below `logins`, click on `OAuth Consent Screen`, and on this page, click on `Add user`. Type the email adress you will be using to store these Party Ranks sheets.

You're now good to go!

You will have to use your logins the first time, they will then be stored in a new file created in the folder: `credentials.json`. Don't worry, they are securely stored (Hashed, not in plain sight). As long as you have this file in the folder, you won't have to login again.

## 2.2 Uploading every user custom sheet to google drive

- Place the script and the sheet you need to upload in the same folder.
- Edit the first few lines to meet your PR configuration
- You can then upload a sheet per user into google drive with this command in your cmd:
```
python upload_party_rank_sheet.py
```
By default, the files will be uploaded in `~/Party Ranks/PR_Name/files.xlsx`.

(example for Nonoc: `~/Party Ranks/Nonoc/Nonoc Anime Songs Sheets (User).xlsx`)