from pathlib import Path
import pandas as pd
import numpy as np
from scipy import spatial
import matplotlib
import matplotlib.pyplot as plt
from sklearn import preprocessing

  

def get_song_average(song):
    return song[5:].mean()

def process_tastes_average(dataframe, ignore):

    currentMeanDistance = {}
    for key in dataframe.keys()[5:]:
        currentMeanDistance[key] = 0
    
    for index, song in dataframe.iterrows():
        average = get_song_average(song)
        if index < ignore:
            for ranker in song.keys()[5:]:
                currentMeanDistance[ranker] += abs(average - song[ranker])
    
    for key in currentMeanDistance:
        currentMeanDistance[key] = currentMeanDistance[key] / ignore
    
    currentMeanDistance = dict(sorted(currentMeanDistance.items(), key=lambda item: item[1]))

    msg = "Who has the ultimate tastes (distance from average)"
    if ignore != 70:
        msg += " | Only taking into account top" + str(ignore)
    print(msg)
    for key in currentMeanDistance:
        print(key + ": ", currentMeanDistance[key])
    print("\n\n")


def process_tastes_rank(dataframe, ignore):

    currentMeanDistance = {}
    for key in dataframe.keys()[5:]:
        currentMeanDistance[key] = 0
    
    for index, song in dataframe.iterrows():
        if index < ignore:
            for ranker in song.keys()[5:]:
                currentMeanDistance[ranker] += abs(index - song[ranker])
    
    for key in currentMeanDistance:
        currentMeanDistance[key] = currentMeanDistance[key] / ignore
    
    currentMeanDistance = dict(sorted(currentMeanDistance.items(), key=lambda item: item[1]))

    msg = "Who has the ultimate tastes (distance from rank)"
    if ignore != 70:
        msg += " | Only taking into account top" + str(ignore)
    print(msg)
    for key in currentMeanDistance:
        print(key + ": ", currentMeanDistance[key])
    print("\n\n")


def plot_affinity(affinity, rankers):
    fig, ax = plt.subplots()
    im = ax.imshow(affinity)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(rankers)))
    ax.set_yticks(np.arange(len(rankers)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(rankers)
    ax.set_yticklabels(rankers)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(rankers)):
        for j in range(len(rankers)):
            text = ax.text(j, i, round(1 - affinity[i, j], 2),
                        ha="center", va="center", color="w")

    ax.set_title("Affinity between players")
    fig.tight_layout()
    plt.show()

def print_affinity(affinity, rankers):
    for index, ranker in enumerate(affinity):
        idx = np.argpartition(-ranker, -5)[-5:]
        indices = idx[np.argsort((ranker)[idx])]
        print(rankers[index])
        for indice in indices[1:]:
            print("BFF: " + rankers[indice])
        
        idx = np.argpartition(ranker, -4)[-4:]
        indices = idx[np.argsort((-ranker)[idx])]
        for indice in indices:
            print("Worst ennemy: " + rankers[indice])
        print()
    print("\n\n")


def process_cosine_affinity(dataframe, ignored_players=[]):

    rankers = []
    for ranker in dataframe.keys()[5:]:
        if ranker not in ignored_players:
            rankers.append(ranker)

    affinity = np.zeros((14 - len(ignored_players), 14 - len(ignored_players)))

    for ranker in dataframe.keys()[5:]:
        for ranker2 in dataframe.keys()[5:]:
            if ranker not in ignored_players and ranker2 not in ignored_players:
                affinity[rankers.index(ranker)][rankers.index(ranker2)] = spatial.distance.cosine(np.array(dataframe[ranker]), np.array(dataframe[ranker2]))

    print_affinity(affinity, rankers)
    plot_affinity(affinity, rankers)


def process_rank_affinity(dataframe, ignored_players=[]):

    rankers = []
    for ranker in dataframe.keys()[5:]:
        if ranker not in ignored_players:
            rankers.append(ranker)

    affinity = np.zeros((14 - len(ignored_players), 14 - len(ignored_players)))

    for ranker in dataframe.keys()[5:]:
        for ranker2 in dataframe.keys()[5:]:
            if ranker not in ignored_players and ranker2 not in ignored_players:
                affinity[rankers.index(ranker)][rankers.index(ranker2)] += np.sum(abs(np.array(dataframe[ranker]) - np.array(dataframe[ranker2])))
    affinity = preprocessing.normalize(affinity)
    print_affinity(affinity, rankers)
    plot_affinity(affinity, rankers)
 
if __name__ == "__main__":
    sheet_path = Path(".")
    sheet_list = list(sheet_path.glob("**/*.ods"))

    ignoring = [70]

    if len(sheet_list) > 0:
        dataframe = pd.read_excel(sheet_list[0], engine="odf")
        for ignored in ignoring:
            process_tastes_average(dataframe, ignored)

        for ignored in ignoring:
            process_tastes_rank(dataframe, ignored)

        process_cosine_affinity(dataframe, [])
        process_rank_affinity(dataframe, [])
