from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects


# -------- Mandatory settings --------

# ranking or rating
SCORING_METHOD = "ranking"

# the column at which players scores start appearing (first column in the sheet = 1)
START_COLUMN_PLAYER = 9

# the line at which players names start appearing (first line in the sheet = 1)
START_LINE_PLAYER = 1

# -------- Recommended settings --------

# Party Rank names, used to name the files created and display the PR name within them
# If name is just <""> then it will default to the filesheet name
PARTY_RANK_NAME = ""

# Necessary if you have stuff at the right of players scores grid in the sheet
# if 0 = setting ignored and will work if nothing is on the right
NB_PLAYERS = 14

# Necessary if you have stuff at the bottom of players scores grid in the sheet
# if 0 = setting ignored and will work if nothing is on the bottom
NB_SONGS = 0


# -------- Optional settings --------
# Number of songs to weight for the distance from average
# i.e if 3: the top 3 of a player will weight more when considering their distance from average score
TOP_SONGS_WEIGHT = 0


# -------- Affinity Grid Style settings --------
# Police size of affinity numbers
AFFINITY_NUMBERS_POLICE_SIZE = 4.5

# Width of the shadow outlining affinity numbers
NUMBERS_OUTLINE_WIDTH = 0.8

# Labels police size (player names on axis')
LABEL_POLICE_SIZE = 8


START_LINE_PLAYER -= 1
START_COLUMN_PLAYER -= 1


def get_song_average(song):
    return song[START_COLUMN_PLAYER : START_COLUMN_PLAYER + NB_PLAYERS].mean()


def process_distance_from_average(dataframe):
    """
    topWeight = Which songs should be weighted
    topWeight = O: no weight
    topWeight = 5: the top 5 songs of the player will be weighted more (1 being even more weighted than 5, etc...))
    """

    rankers = list(dataframe.keys())

    currentMeanDistance = {}
    max_len_ranker_name = 0
    for ranker in rankers:
        currentMeanDistance[ranker] = 0
        if len(str(ranker)) > max_len_ranker_name:
            max_len_ranker_name = len(str(ranker))

    for index, song in dataframe.iterrows():
        for i, ranker in enumerate(rankers):
            if i < TOP_SONGS_WEIGHT:
                currentMeanDistance[ranker] += (
                    abs(song.mean() - song[ranker]) * TOP_SONGS_WEIGHT + 1 - i
                )
            else:
                currentMeanDistance[ranker] += abs(song.mean() - song[ranker])

    for ranker in currentMeanDistance:
        currentMeanDistance[ranker] = currentMeanDistance[ranker] / (index + 1)

    currentMeanDistance = dict(
        sorted(currentMeanDistance.items(), key=lambda item: item[1])
    )

    optional = (
        f"(with top {TOP_SONGS_WEIGHT} songs weighted)" if TOP_SONGS_WEIGHT > 1 else ""
    )
    ultimate_taste = f"Distance from Average {optional}\n"
    for ranker in currentMeanDistance:
        ultimate_taste += f"{ranker}: {'-' * (max_len_ranker_name - len(str(ranker)))} {round(currentMeanDistance[ranker], 2)}\n"
    ultimate_taste += "\n"

    return ultimate_taste


def plot_affinity(affinity, rankers, PR_name):
    fig, ax = plt.subplots()
    ax.imshow(affinity)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(rankers)))
    ax.set_yticks(np.arange(len(rankers)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(rankers)
    ax.set_yticklabels(rankers)

    ax.tick_params(axis="both", labelsize=LABEL_POLICE_SIZE)

    # Rotate the x tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(rankers)):
        for j in range(len(rankers)):
            ax.text(
                j,
                i,
                f"{int(round(1 - affinity[i, j], 2) * 100)}",
                ha="center",
                va="center",
                color="w",
                size=AFFINITY_NUMBERS_POLICE_SIZE,
                path_effects=[
                    PathEffects.withStroke(
                        linewidth=NUMBERS_OUTLINE_WIDTH, foreground="black"
                    )
                ],
            )

    ax.set_title(f"{PR_name}\nAffinity Between People")
    fig.tight_layout()
    plt.savefig(f"{PR_name}_Affinity.png", dpi=199)


def NormalizeData(data, nb_songs):
    # normalize data for ratings affinity
    return (data - 0) / (nb_songs * 10 - 0)


def compute_similarity(vector1, vector2):
    if len(vector1) != len(vector2):
        print("Similary func got two vectors of different sizes")
        return 0

    weights = np.ones(len(vector1))

    simVector1 = []
    simVector2 = []
    for song in range(len(vector1)):
        # weight = 10 if song < len(vector1) / 2 else 1
        weight = 1

        v1 = list(np.zeros(len(vector1)))
        v1[int(vector1[song]) - 1] = weight

        v2 = list(np.zeros(len(vector2)))
        v2[int(vector2[song]) - 1] = weight

        simVector1 += v1
        simVector2 += v2

    return 1 - np.dot(simVector1, simVector2) / (
        np.linalg.norm(simVector1) * np.linalg.norm(simVector2)
    )


def process_ranking_affinity(dataframe):
    """
    Process affinity between players using cosine similarity
    """

    rankers = list(dataframe.keys())

    affinity = np.zeros((len(rankers), len(rankers)))

    for i, ranker in enumerate(rankers):
        for j, ranker2 in enumerate(rankers):
            affinity[i][j] = compute_similarity(
                list(dataframe[ranker]), list(dataframe[ranker2])
            )

    return affinity, rankers


def process_rating_affinity(dataframe):
    """
    Process affinity between players using score diffences sums
    cosine should technilly also works for ratings, but I feel like it's not very good
    """

    rankers = list(dataframe.keys())

    affinity = np.zeros((len(rankers), len(rankers)))

    for i, ranker in enumerate(rankers):
        for j, ranker2 in enumerate(rankers):
            affinity[i][j] = sum(abs(dataframe[ranker] - dataframe[ranker2]))

    affinity = NormalizeData(affinity, dataframe.shape[0])

    return affinity, rankers


def process_ranking_stats(dataframe):
    """
    process stats for a rating PR
    - Players distance from average
    - Number of Greens & Reds
    """

    rankers = list(dataframe.keys())

    greensCounter = {}
    redsCounter = {}
    max_len_ranker_name = 0
    for ranker in rankers:
        greensCounter[ranker] = redsCounter[ranker] = 0
        if len(str(ranker)) > max_len_ranker_name:
            max_len_ranker_name = len(str(ranker))

    for index, song in dataframe.iterrows():
        for ranker in rankers:
            if song[ranker] == song.min():
                greensCounter[ranker] += 1
            if song[ranker] == song.max():
                redsCounter[ranker] += 1

    greensCounter = dict(
        sorted(greensCounter.items(), key=lambda item: item[1], reverse=True)
    )

    marble_string = "Greens & Reds\n"
    for ranker in greensCounter:
        marble_string += f"{ranker}: {'-' * (max_len_ranker_name - len(str(ranker)))} {greensCounter[ranker]} Greens & {redsCounter[ranker]} Reds\n"
    marble_string += "\n"
    return marble_string


def process_rating_stats(dataframe):
    """
    process stats for a rating PR
    - Players distance from average
    - Number of Greens & Reds
    - Number of 10s
    - Average score
    """

    rankers = list(dataframe.columns)

    average_score = {ranker: round(dataframe[ranker].mean(), 2) for ranker in rankers}
    total_score = {ranker: dataframe[ranker].sum() for ranker in rankers}
    greens_counter = {ranker: 0 for ranker in rankers}
    reds_counter = {ranker: 0 for ranker in rankers}
    tens_counter = {ranker: 0 for ranker in rankers}
    max_len_ranker_name = max(len(ranker) for ranker in rankers)

    for _, song in dataframe.iterrows():
        for ranker in rankers:
            if song[ranker] == song.max():
                greens_counter[ranker] += 1
            if song[ranker] == song.min():
                reds_counter[ranker] += 1
            if song[ranker] == 10:
                tens_counter[ranker] += 1

    sorted_average_score = dict(
        sorted(average_score.items(), key=lambda item: item[1], reverse=True)
    )

    marble_string = "Averages (Totals): (Sorted by Highest to Lowest)\n"
    for ranker, score in sorted_average_score.items():
        padding = "-" * (max_len_ranker_name - len(ranker))
        marble_string += f"{ranker}: {padding} {score} ({total_score[ranker]})\n"
    marble_string += "\n"

    marble_string += "Greens, Reds & 10/10s (Sorted by Averages)\n"
    for ranker, greens in greens_counter.items():
        padding = "-" * (max_len_ranker_name - len(ranker))
        marble_string += f"{ranker}: {padding} {greens} Greens, {reds_counter[ranker]} Reds & {tens_counter[ranker]} 10/10s\n"
    marble_string += "\n"

    return marble_string


def process_stats(dataframe, PR_name):
    """
    Write some stats in a text file:
    - Players distance from average
    - Number of Greens & Reds
    if scoring method is rating, also add:
    - Number of 10s
    - Average score
    """

    f = open(f"{PR_name}_stats.txt", "w")
    f.write(process_distance_from_average(dataframe))
    if SCORING_METHOD == "ranking":
        f.write(process_ranking_stats(dataframe))
    if SCORING_METHOD == "rating":
        f.write(process_rating_stats(dataframe))
    f.close()


def cut_df_scoring_grid(dataframe):
    # Cut the dataframe scoring grid using START_COLUMN_PLAYER START_LINE_PLAYER NB_PLAYERS NB_SONGS coordinates settings

    if NB_SONGS:
        dataframe = dataframe.drop(range(NB_SONGS, dataframe.shape[0]), axis=0)

    if START_LINE_PLAYER:
        dataframe = dataframe.drop(range(START_LINE_PLAYER), axis=0)

    if START_COLUMN_PLAYER:
        dataframe = dataframe.drop(
            dataframe.columns[range(START_COLUMN_PLAYER)], axis=1
        )
    if NB_PLAYERS:
        dataframe = dataframe.drop(
            dataframe.columns[range(NB_PLAYERS, dataframe.shape[1])], axis=1
        )

    return dataframe


if __name__ == "__main__":
    sheet_path = Path(".")
    sheet_list = list(sheet_path.glob("*.ods"))

    if len(sheet_list) > 0:
        for sheet in sheet_list:
            # Get the dataframe and cut the scoring grid using PR settings
            dataframe = pd.read_excel(sheet, engine="odf")
            dataframe = cut_df_scoring_grid(dataframe)
            print(
                "\nScore grid based on the settings you entered, check if it's correct!\n"
            )
            print(dataframe)

            PR_name = PARTY_RANK_NAME if PARTY_RANK_NAME else sheet.name

            # Write some stats in a text file
            process_stats(dataframe, PR_name)

            if SCORING_METHOD == "ranking":
                affinity, rankers = process_ranking_affinity(dataframe)
            else:
                affinity, rankers = process_rating_affinity(dataframe)

            plot_affinity(affinity, rankers, PR_name)
