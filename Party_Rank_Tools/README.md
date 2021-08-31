# Party Rank Tools

# Requirements

To use these scripts you will need python that you can download here: <https://www.python.org/downloads/>,
Make sure that it will make an environment variable for you when it will ask for it.

You also need to install ffmpeg: <https://www.ffmpeg.org/>, and set it up as an environment variable too, it is quickly explained here in the "Add ffmpeg to Windows 10 Path" section: <https://windowsloop.com/install-ffmpeg-windows-10/>

Once this is done, you need to install the python libraries I'm using for these scripts by typing this command in the CMD:

```
python -m pip install openpyxl
python -m pip install pydrive
```

# 1 - Create Party Rank Sheet

## 1.1 - Getting Expand.json

For this, you'll need an export of the expand library as a JSON, you can get it through the console of your navigator (press F12, then go on the console tab) using this call:

```js
new Listener("expandLibrary questions", (payload) => {
  console.log(payload)
}).bindListener()
socket.sendCommand({
    type: "library",
    command: "expandLibrary questions"
})
```
once this is done, you can right click the results and `expand recursively`, then you can right click again and `save as`, naming it `expand.json`

You can also DM me if you don't want to bother.

## 1.2 - Configuring the scripts

Then you need to get these scripts: `create_party_rank_sheet.py`, `google_api.py`, `download_party_rank_sheet.py` and `settings.yaml` and place them in the same folder as `expand.json`. To download them, you need to click on the script, then `raw` on the top right, and then you can right click and `save as...`.

Once you have this, you can configure the first few lines of the create_party_rank_sheet.py file to meet your needs:

```py
connect_and_upload_to_drive = True
delete_local_file_once_done = True

party_rank_name = "Nonoc"
player_list = ["EruisKawaii", "Husa", "xSardine", "etc"]
```

If you set `connect_and_upload_to_drive` to True, you will have to follow the guide on how to set up your google API credentials. (Set to False if you don't want to)

If `delete_local_file_once_done` is set to True, it will delete the created file automatically, if you only want to use those uploaded on google drive. (Set to False if you don't want to)


```py
# Filtering search
anime_search_filters = []
artist_search_filters = ["yoshino nanjou", "fripside"]
song_name_search_filters = []
# Filtering search
```
Here it will return every song in the `expand.json` file that have either `yoshino nanjou` or `fripside` as artist.

If you want every madoka song in white album:
```py
# Filtering search
anime_search_filters = ["white album"]
artist_search_filters = ["madoka yonezawa"]
song_name_search_filters = []
# Filtering search
```

## 1.3 - Setting up Google Drive API

If you wish to automatically upload each sheet to your google drive you need to follow additional steps:

You can start by following the steps described in the first 3 pages of this pdf:
<https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf>, the process changed after the 4th page, so I'll be continuing here.

Once you've done this, click on `Create Credentials`, it will brings you to a form.
For the first question, select the `Google Drive API`, the second question, select `users data`, after this, it will ask further information about your apps, since it will be only personal use, it doesn't matter and you can give it a random name. Enter you google email adress you're using to store your party ranks.

It will now ask about which personal acces you will need for your application, this script will need to login (you will still have to provide your password obviously), and create a new file in your drive, so let's add those:
- Click on `Add or Delete application domains`
- In the search filter, type `drive` and press enter
- Select the second and third elements ("Display, Modify, Update or **Create** files in your google drive")
- Go the second page and select the element right before the last one ("Connect to Google Drive")
- Press `update` at the bottom of the page

You can now press `Save and Continue`.

It will now asks you which type of application this is, it doesn't really matter, just select `Desktop App` and keep the default name.

Click `create`.

You can now click the `download` button, it will give you a `.json` that you will put in the same folder as the rest. If it is not already, rename it to `client_secrets.json`. You are now ready to start your scripts!

## 1.4 - Starting the scritps

Once you're done with this configuration, you can go in your `cmd` and get to the folder you just created using the `cd` commands:
let's say your scripts are in `C://Users/<Your_Name>/Documents/PR/`:
```
cd Documents
cd PR
```

and now you can start it:
```
python create_party_rank_sheet
```

It will create a sheet with the songs from expand filtered by your configuration, keep in mind fully uploaded stuff will not appear and still has to get taken from in game. It might also take into account songs that you don't need (i.e, angela giving you "angela aki" for example), make sure to remove those.

## Download Party Rank Sheet

Once your sheet is created, and you've added anything that is missing, and deleted anything that you don't want, you can download every song as an mp4 with the download_party_rank_sheet.py script. You can also edit the first few lines if you want to change the output path and such. You start it the same way as the previous script.

If you need to stop the process in the middle of the downloading but don't want to loose all the progress, don't worry you can quit the terminal, when you want to start again, check which line you stopped, and change the `2` in the line in the code:
```py
link_start_row = 2  # number of the row where I need to start getting links
```
to the line you want to start from. (don't forget to change it back to 2 for the next PR)

## Process Party Rank Stats

It will process the different stats from the sheets with everyone rankings in it.
