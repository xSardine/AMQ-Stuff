import pandas as pd
from pathlib import Path
import utils
import utils

def most_represented_artists(dataframe, nb_artists):

    artists_list = utils.get_most_represented_artists(dataframe, nb_artists)
    file_text = (
        "------------------------ Most represented artists ------------------------\n"
    )
    for artist in artists_list:

        artist_song_list = utils.get_artist_songs(dataframe, artist[0])
        max_score, min_score, mean_score = utils.get_list_max_min_mean(artist_song_list)

        file_text += "---" + " / ".join(artist[1]) + "---\n"
        file_text += "max_score: " + str(max_score) + "\n"
        file_text += "min_score: " + str(min_score) + "\n"
        file_text += "mean_score: " + str(mean_score) + "\n"
        file_text += "number of songs: " + str(len(artist_song_list)) + "\n\n"

        for song in artist_song_list:
            file_text += (
                str(song["score"])
                + ": "
                + song["anime"]
                + " - "
                + song["title"]
                + " by "
                + song["artist"]
                + "\n"
            )

        file_text += "\n"

    file_text += "\n\n\n\n\n\n\n"

    return file_text


def most_favorite_artists(dataframe, nb_artists, minimum_number_of_songs):

    fav_artists_ids = utils.get_favorites_artists_ids(
        dataframe, nb_artists, minimum_number_of_songs
    )

    file_text = (
        "------------------------ Favorite Artists (minimum "
        + str(minimum_number_of_songs)
        + " songs) ------------------------\n"
    )

    for artist_id in fav_artists_ids:

        artist_song_list = utils.get_artist_songs(dataframe, artist_id)
        max_score, min_score, mean_score = utils.get_list_max_min_mean(artist_song_list)

        file_text += "---" + " / ".join(utils.get_artist_names(artist_id)) + "---\n"
        file_text += "max_score: " + str(max_score) + "\n"
        file_text += "min_score: " + str(min_score) + "\n"
        file_text += "mean_score: " + str(mean_score) + "\n"
        file_text += "number of songs: " + str(len(artist_song_list)) + "\n\n"

        for song in artist_song_list:
            file_text += (
                str(song["score"])
                + ": "
                + song["anime"]
                + " - "
                + song["title"]
                + " by "
                + song["artist"]
                + "\n"
            )
        file_text += "\n\n"

    file_text += "\n\n\n\n\n\n\n"

    return file_text


def least_favorite_artists(dataframe, nb_artists, minimum_number_of_songs):

    least_fav_artists_ids = utils.get_least_favorites_artists_ids(
        dataframe, nb_artists, minimum_number_of_songs
    )

    file_text = (
        "------------------------ Least Favorite Artists (minimum "
        + str(minimum_number_of_songs)
        + " songs) ------------------------\n"
    )

    for artist_id in least_fav_artists_ids:

        artist_song_list = utils.get_artist_songs(dataframe, artist_id)
        max_score, min_score, mean_score = utils.get_list_max_min_mean(artist_song_list)

        file_text += "---" + " / ".join(utils.get_artist_names(artist_id)) + "---\n"
        file_text += "max_score: " + str(max_score) + "\n"
        file_text += "min_score: " + str(min_score) + "\n"
        file_text += "mean_score: " + str(mean_score) + "\n"
        file_text += "number of songs: " + str(len(artist_song_list)) + "\n\n"

        for song in artist_song_list:
            file_text += (
                str(song["score"])
                + ": "
                + song["anime"]
                + " - "
                + song["title"]
                + " by "
                + song["artist"]
                + "\n"
            )
        file_text += "\n\n"

    file_text += "\n\n\n\n\n\n\n"

    return file_text


def full_sorted_list(dataframe, activate_full_sorted_list):

    song_list = utils.get_full_sorted_song_list(dataframe)
    max_score, min_score, mean_score = utils.get_list_max_min_mean(song_list)

    file_text = "------------------------ Global Stats ------------------------\n"

    file_text += "max_score: " + str(max_score) + "\n"
    file_text += "min_score: " + str(min_score) + "\n"
    file_text += "mean_score: " + str(mean_score) + "\n"
    file_text += "number of songs: " + str(len(song_list)) + "\n\n"

    if activate_full_sorted_list:

        file_text += (
            "------------------------ Full Sorted List ------------------------\n"
        )
        for song in song_list:
            file_text += (
                str(song["score"])
                + ": "
                + song["anime"]
                + " - "
                + song["title"]
                + " by "
                + song["artist"]
                + "\n"
            )
        file_text += "\n\n\n\n\n\n\n"

    return file_text


def score_counting(dataframe, precision):

    file_text = (
        "------------------------ Sorted score counter with precision "
        + str(precision)
        + " ------------------------\n"
    )
    score_counting = utils.score_counting(dataframe, precision)

    for score in score_counting:
        file_text += str(score[0]) + ": " + str(score[1]) + "\n"
    file_text += "\n\n\n\n\n\n\n"
    return file_text


def decades_stats(dataframe):

    file_text = "------------------------ Stats per decade ------------------------\n"
    for decade in utils.get_decades_stats(dataframe):
        file_text += "---" + decade["decade"] + "---\n"
        file_text += "max_score: " + str(decade["max"]) + "\n"
        file_text += "min_score: " + str(decade["min"]) + "\n"
        file_text += "mean_score: " + str(decade["mean"]) + "\n"
        file_text += "number of songs: " + str(decade["nb_songs"]) + "\n\n"
    file_text += "\n\n\n\n\n\n\n"
    return file_text

if __name__ == "__main__":

    # Config
    activate_global_stats = True
    activate_favorite_artists = True
    activate_least_favorite_artists = True
    activate_most_represented_artists = True
    activate_full_sorted_list = True
    activate_score_counting = True
    activate_decades_stats = True

    nb_artists = 10
    minimum_amount_of_songs = 3

    sheet_path = Path(".")
    for sheet in list(sheet_path.glob("**/*.ods")):

        file_text = ""

        dataframe = pd.read_excel(sheet, engine="odf")
        dataframe = utils.add_scores_to_song_list_w_ids(dataframe)

        if activate_global_stats:
            file_text += full_sorted_list(dataframe, activate_full_sorted_list)

        if activate_favorite_artists:
            file_text += most_favorite_artists(dataframe, nb_artists, minimum_amount_of_songs)

        if activate_favorite_artists:
            file_text += least_favorite_artists(dataframe, nb_artists, minimum_amount_of_songs)

        if activate_most_represented_artists:
            file_text += most_represented_artists(dataframe, nb_artists)

        if activate_score_counting:
            file_text += score_counting(dataframe, 1)
            file_text += score_counting(dataframe, 0.1)

        if activate_decades_stats:
            file_text += decades_stats(dataframe)

        
        with open(sheet.with_suffix(".txt"), "w", encoding="utf-8") as writer:
            writer.write(file_text)
