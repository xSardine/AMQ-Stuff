# Husa's Sheet mp4 downloader

# What it does
Download every webm in Husa's sheet as an mp4

# Usage
## What to download
If you don't have ffmpeg installed, download it, and configure it as an environment variable

If you don't have python installed, download it, and configure it as an environment variable

Then in the cmd, use `pip install openpyxl`

Download your sheet from google sheet: `File` → `Download` → `Microsoft Excel (.xlsx)` and move it into the same folder as the one containing the .py file

## How to use it
Every time you use a new sheet, you need to change some values and make sure they are still right. This version is for the Angela PR. 

You can find what you need to change at the start of the python file.

- `sheet_tab_name = "ark1"`  -> name of the sheet (bottom left)
- `link_start_row = 2` -> the row where your webm start appearing in your sheet
- `link_position_column = 3`  -> position of the column containing webms in the sheet
- `output_path = Path("mp4")` -> name of the folder you want your files to be saved (here it is <current_directory/mp4/>)

Once you're done, double click it, **or** right click -> open with python
**or** run the command `python3 husa_sheet_downloader.py`

### Customization:

You can change the command you want to be done to the webm by searching the `command` variable (ctrl+f -> command)
Currently, it convert the webm to an mp4, but you can modify it by changing the command just like you would do with ffmpeg while keeping the same format as the current one.
