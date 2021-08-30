# Party Rank Tools

## Requirements

To use these scripts you will need python that you can download here: <https://www.python.org/downloads/>,
Make sure that it will make an environment variable for you when it will ask for it.

You also need to install ffmpeg: <https://www.ffmpeg.org/>, and set it up as an environment variable too, it is quickly explained here in the "Add ffmpeg to Windows 10 Path" section: <https://windowsloop.com/install-ffmpeg-windows-10/>

Once this is done, you need to install the python library I'm using for these scripts by typing this command in the CMD:

`python -m pip install openpyxl`

## Create Party Rank Sheet

For this, you'll need an export of the expand library as a JSON, you can get it through the console of your navigator (press F12, then go on the console tab) using this call:

```
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

Then you need to get both scripts: `create_party_rank_sheet` and `download_party_rank_sheet` and place them in the same folder as `expand.json`. For this, you need to click on the script, then `raw` on the top right, and then you can right click and `save as...`.

Once you have this, you can configure the first few lines of the create_party_rank_sheet.py file to meet your needs:

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

## Process Party Rank Stats

It will process the different stats from the sheets with everyone rankings in it.
