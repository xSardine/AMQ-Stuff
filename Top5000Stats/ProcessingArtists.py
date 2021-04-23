import utils
from pathlib import Path
import pandas as pd
  
if __name__ == "__main__":
    sheet_path = Path(".")
    sheet_list = list(sheet_path.glob("**/*.ods"))

    if len(sheet_list) > 0:
        dataframe = pd.read_excel(sheet_list[0], engine="odf")
        artists = utils.add_artists_ID_to_df(dataframe)
