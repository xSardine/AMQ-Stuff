from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

START_COLUMN_PLAYER = 0  # the column at which players start appearing
NB_PLAYERS = 10


def get_song_average(song):
    return song[START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS].mean()


def process_tastes_average(dataframe, topWeight=0):
    """
    topWeight = Which songs should be weighted
    topWeight = O: no weight
    topWeight = 5: the top 5 songs of the player will be weighted more (1 being even more weighted than 5, etc...)) 
    """

    currentMeanDistance = {}
    for key in dataframe.keys()[START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS]:
        currentMeanDistance[key] = 0

    for index, song in dataframe.iterrows():
        average = get_song_average(song)
        for ranker in song.keys()[
            START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS
        ]:

            if song[ranker] < topWeight + 1:
                currentMeanDistance[ranker] += abs(average - song[ranker]) * (
                    topWeight + 2 - song[ranker]
                )
            else:
                currentMeanDistance[ranker] += abs(average - song[ranker])

    for key in currentMeanDistance:
        currentMeanDistance[key] = currentMeanDistance[key] / (index + 1)

    currentMeanDistance = dict(
        sorted(currentMeanDistance.items(), key=lambda item: item[1])
    )

    optional = f" with top {topWeight} songs weighted" if topWeight > 1 else ""
    ultimate_taste = f"Who has the ultimate tastes (distance from average{optional})\n"
    for key in currentMeanDistance:
        ultimate_taste += f"{key}: {round(currentMeanDistance[key], 2)}\n"
    ultimate_taste += "\n"

    return ultimate_taste


def plot_affinity(affinity, rankers, PR_name):
    fig, ax = plt.subplots()
    im = ax.imshow(affinity, cmap="YlGn_r", vmin=0, vmax=1)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(rankers)))
    ax.set_yticks(np.arange(len(rankers)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(rankers)
    ax.set_yticklabels(rankers)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(rankers)):
        for j in range(len(rankers)):
            ax.text(
                j,
                i,
                f"{int(round(1 - affinity[i, j], 2) * 100)}%",
                ha="center",
                va="center",
                color="w",
                size=4.5,
            )

    ax.set_title(PR_name)
    fig.tight_layout()
    plt.savefig(f"{PR_name}_Affinity.png", dpi=199)


def NormalizeData(data, nb_songs):
    return (data - 0) / (nb_songs * 10 - 0)


def process_affinity(dataframe):

    rankers = []
    for ranker in dataframe.keys()[
        START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS
    ]:
        rankers.append(ranker)

    affinity = np.zeros((NB_PLAYERS, NB_PLAYERS))

    for ranker in dataframe.keys()[
        START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS
    ]:
        for ranker2 in dataframe.keys()[
            START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS
        ]:
            rating1 = np.array(dataframe[ranker])
            rating2 = np.array(dataframe[ranker2])
            for i, rating in enumerate(rating1):
                affinity[rankers.index(ranker)][rankers.index(ranker2)] += abs(
                    rating - rating2[i]
                )

    affinity = NormalizeData(affinity, len(rating1))
    return affinity, rankers


if __name__ == "__main__":
    sheet_path = Path(".")
    sheet_list = list(sheet_path.glob("*.ods"))

    if len(sheet_list) > 0:
        for sheet in sheet_list:
            dataframe = pd.read_excel(sheet, engine="odf")
            PR_name = str(sheet).split(" ")[0]
            f = open(f"{PR_name}_ultimate_tastes.txt", "w")
            f.write(f"{sheet.name}\n\n")
            f.write(process_tastes_average(dataframe))
            f.write(process_tastes_average(dataframe, topWeight=3))
            f.close()

            affinity, rankers = process_affinity(dataframe)
            plot_affinity(affinity, rankers, PR_name)
