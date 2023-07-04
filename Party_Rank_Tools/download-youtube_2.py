from pathlib import Path
import os
import pandas as pd

# Column coordinates start at 0,0 top left
YOUTUBE_LINKS_COLUMN = 4
YOUTUBE_LINKS_LINE = 1


def download_songs(dataframe):

    for i, column in enumerate(dataframe):
        if i == YOUTUBE_LINKS_COLUMN:
            key = column
    for i, link in enumerate(dataframe[key]):
        if i <= YOUTUBE_LINKS_LINE:
            continue
        if "youtu" not in link:
            continue
        os.system(f"yt-dlp -S res,ext:mp4:m4a --recode mp4 {link}")


if __name__ == "__main__":
    sheet_path = Path(".")
    sheet_list = list(sheet_path.glob("*.ods"))

    if len(sheet_list) > 0:
        for sheet in sheet_list:

            dataframe = pd.read_excel(sheet, engine="odf")

            download_songs(dataframe)
