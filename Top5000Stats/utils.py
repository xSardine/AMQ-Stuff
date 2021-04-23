import numpy as np
import itertools
import json
import re


and_exception = ["kishida..., fear..."]
coma_exception = ["shrug"]
ft_exception = ["shrug"]

manual_split = [
    (
        "masayuki yamamoto to school mates brothers",
        ("masayuki yamamoto", "school mates brothers"),
    )
]

different_name_exceptions = [
    ("minami", "minami kuribayashi"),
    ("afilia saga", "afilia saga east"),
]

decades_metadata = {}
decades_metadata["<1970"] = [0, 129]
decades_metadata[">1970"] = [130, 238]


def split_artists(artists):

    for i, split in enumerate(manual_split):
        if artists == split[0]:
            return manual_split[i][1]

    regex = []
    if artists not in and_exception:
        regex.append(" & | &|& |&")
    if artists not in coma_exception:
        regex.append(" , | ,|, |,")
    if artists not in ft_exception:
        regex.append(" ft. | ft.|ft. |ft.")
        regex.append(" feat. | feat.|feat. |feat.")

    return re.split("|".join(regex), artists)


def get_alternative_names(artist):

    for diff_entry in different_name_exceptions:
        if artist in diff_entry:
            return diff_entry
    return [artist]


def is_processed_artists(artists, processed_artists):

    for artist in artists:
        if artist in processed_artists:
            return True
    return False


def convert_dataframe_to_dictionnary(dataframe):

    dico = []
    for index, row in dataframe.iterrows():
        dico.append(
            {
                "id": index,
                "anime": row["Song"],
                "title": row["Title"],
                "artist": row["Artist"],
                "artist_ids": [],
            }
        )
    return dico


def process_artist(dfdic, artists, artist_id):

    artist_id = str(artist_id).zfill(4)

    for song in dfdic:
        for artist in artists:
            if (
                artist in split_artists(song["artist"].lower())
                and artist_id not in song["artist_ids"]
            ):
                song["artist_ids"].append(artist_id)
    return dfdic


def add_artists_ID_to_df(dataframe):

    processed_artists = []
    song_list_w_artists_ids = convert_dataframe_to_dictionnary(dataframe)
    artists_ids_mapping = []
    current_id = 0
    for artists in dataframe.Artist.values:
        artists = artists.lower()
        for artist in split_artists(artists):

            artist = get_alternative_names(artist)

            if not is_processed_artists(artist, processed_artists):

                artists_ids_mapping.append((artist, str(current_id).zfill(4)))

                song_list_w_artists_ids = process_artist(
                    song_list_w_artists_ids, artist, current_id
                )
                current_id += 1
                for alt_name in artist:
                    processed_artists.append(alt_name)

    with open("song_list_w_artists_ids.json", "w") as outfile:
        json.dump(song_list_w_artists_ids, outfile)

    with open("artists_ids_mapping.json", "w") as outfile:
        json.dump(artists_ids_mapping, outfile)


def get_most_represented_artists(song_list_w_artists_ids, nb_artist):

    with open("artists_ids_mapping.json") as json_file:
        artists_ids_mapping = json.load(json_file)

    artist_song_count = {}
    for artist in artists_ids_mapping:
        artist_song_count[artist[1]] = [artist[0], 0]

    for song in song_list_w_artists_ids:
        for artist_id in song["artist_ids"]:
            artist_song_count[artist_id][1] += 1

    output_array = []
    for key in artist_song_count.keys():
        output_array.append([key, artist_song_count[key][0], artist_song_count[key][1]])

    return sorted(output_array, key=lambda item: item[2], reverse=True)[:nb_artist]


def get_favorites_artists_ids(
    song_list_w_artists_ids, nb_artist, minimum_number_of_songs
):

    with open("artists_ids_mapping.json") as json_file:
        artists_ids_mapping = json.load(json_file)

    artist_mean_score = []
    for artist in artists_ids_mapping:

        artist_song_list = get_artist_songs(song_list_w_artists_ids, artist[1])
        if len(artist_song_list) >= minimum_number_of_songs:
            max_score, min_score, mean_score = get_list_max_min_mean(artist_song_list)
            artist_mean_score.append((artist[1], mean_score))

    artist_mean_score = sorted(
        artist_mean_score, key=lambda item: item[1], reverse=True
    )[:nb_artist]
    return [x[0] for x in artist_mean_score]


def get_least_favorites_artists_ids(
    song_list_w_artists_ids, nb_artist, minimum_number_of_songs
):

    with open("artists_ids_mapping.json") as json_file:
        artists_ids_mapping = json.load(json_file)

    artist_mean_score = []
    for artist in artists_ids_mapping:

        artist_song_list = get_artist_songs(song_list_w_artists_ids, artist[1])
        if len(artist_song_list) >= minimum_number_of_songs:
            max_score, min_score, mean_score = get_list_max_min_mean(artist_song_list)
            artist_mean_score.append((artist[1], mean_score))

    artist_mean_score = sorted(artist_mean_score, key=lambda item: item[1])[:nb_artist]
    return [x[0] for x in artist_mean_score]


def get_artist_songs(song_list_w_artists_ids, artist_id):

    song_list = []
    for song in song_list_w_artists_ids:
        for c_artist_id in song["artist_ids"]:
            if artist_id == c_artist_id:
                song_list.append(song)
    return sorted(song_list, key=lambda item: item["score"], reverse=True)


def get_full_sorted_song_list(song_list_w_artists_ids):
    return sorted(song_list_w_artists_ids, key=lambda item: item["score"], reverse=True)


def get_list_max_min_mean(song_list):

    min_score = 11
    max_score = -1
    total_score = 0

    for song in song_list:
        if song["score"] < min_score:
            min_score = song["score"]
        if song["score"] > max_score:
            max_score = song["score"]
        total_score += song["score"]

    return (
        max_score,
        min_score,
        round(total_score / len(song_list), 3),
    )


def add_scores_to_song_list_w_ids(dataframe):

    with open("song_list_w_artists_ids.json") as json_file:
        song_list_w_artists_ids = json.load(json_file)

    output_dict = []

    for index, row in dataframe.iterrows():
        for song in song_list_w_artists_ids:
            if song["id"] == index:
                song["score"] = row["Score"]
    return song_list_w_artists_ids


def get_artist_names(artist_id):

    with open("artists_ids_mapping.json") as json_file:
        artists_ids_mapping = json.load(json_file)

    for artist in artists_ids_mapping:
        if artist[1] == artist_id:
            return artist[0]
    return ""


def score_counting(song_list_w_artists_ids, precision):

    # Counting number of occurence of each score
    if precision == 0.1:

        scores_counter = {}
        for i in range(10):
            for j in range(10):
                key = round(i * 1 + j * 0.1, 1)
                scores_counter[key] = 0
        scores_counter[10.0] = 0

        for song in song_list_w_artists_ids:
            scores_counter[song["score"]] += 1

        sorted_dict = dict(
            sorted(scores_counter.items(), key=lambda item: item[1], reverse=True)
        )

        output_array = []
        for x in sorted_dict:
            output_array.append((x, sorted_dict[x]))
        return output_array

    elif precision == 1:

        scores_counter = {}
        for i in range(11):
            scores_counter[i] = 0

        for song in song_list_w_artists_ids:
            scores_counter[int(song["score"])] += 1

        sorted_dict = dict(
            sorted(scores_counter.items(), key=lambda item: item[1], reverse=True)
        )

        output_array = []
        for x in sorted_dict:
            output_array.append((x, sorted_dict[x]))
        return output_array


def get_decades_stats(song_list_w_artists_ids):

    output_decade = []
    for key in decades_metadata.keys():

        decade_list_song = song_list_w_artists_ids[
            decades_metadata[key][0] : decades_metadata[key][1]
        ]

        max_score, min_score, mean_score = get_list_max_min_mean(decade_list_song)

        output_decade.append(
            {
                "decade": key,
                "max": max_score,
                "min": min_score,
                "mean": mean_score,
                "nb_songs": len(decade_list_song),
            }
        )

    return sorted(output_decade, key=lambda item: item["mean"], reverse=True)

