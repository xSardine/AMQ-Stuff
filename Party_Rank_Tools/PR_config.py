party_rank_name = "Coorie"
player_list = ["EruisKawaii", "Husa", "xSardine", "etc"]

# Filtering search
anime_search_filters = []
artist_search_filters = ["coorie", ["rino", True]]
song_name_search_filters = []

# If set to True, the song will need to fit every type of filter (it still "or" inside the filter themselves tho),
# if set to False, the song will need to fit at least one of these filters (i.e: either the artist filter, song name filter, or anime filter)
and_filter = True

# If set to True, it will only take the first instance of a song,
# meaning that if a further instance is a longer sample, it will ignore it anyway
filter_duplicate = False

# You can also set a filter to have to match the exact name (not case sensitive) by giving it the "True" statue.
# I.E, if you want "mpi" to match the exact artist to avoid catching Empire as well in a Sawano Ranking:
# artist_search_filters = ["mika kobayashi", "eliana", ["mpi", True]]
# or for Minami and every other Minami (Minami Takahashi etc...):
# artist_search_filters = ["minami kuri", ["minami", True]] (this will still catch domexkano tho, since it's the exact same name)

# Filtering search


"""
Some Usage example:

_______________________________________________________________
"exact name" example
Song that are called "Yakusoku" Party Rank
Not setting the True value to "yakusoku" here would find every song with yakusoku in it such as "Madoromi no Yakusoku"

anime_search_filters = []
artist_search_filters = []
song_name_search_filters = [["yakusoku", True]]
and_filter = (doesn't matter since only one filter used)
_______________________________________________________________

_______________________________________________________________
another "Exact match" filter example
Here it will try to find any artist with "minami kuri" in it (i.e, minami kuribayashi)
but also every artist that are exactly named "minami" (not case sensitive, i.e "Minami" and not Minami Takahashi and the rest)

anime_search_filters = []
artist_search_filters = ["minami kuri", ["minami", True], "w/e her name is in GPX"]
song_name_search_filters = []
and_filter = (doesn't matter since only one filter used)
_______________________________________________________________

_______________________________________________________________
"And filter" example
Here it will search for every song in white album that are sang by madoka yonezawa
if for some reasons you wanted every white album song and every madoka yonezawa (not particularly from white album), 
you would have to set "and_filter = False"

anime_search_filters = ["white alb"]
artist_search_filters = ["madoka"]
song_name_search_filters = []
and_filter = True
_______________________________________________________________

_______________________________________________________________
Hard settings example
Trying to get the most sawano composed songs while avoiding what you don't need:

anime_search_filters = ["Brighter than", "Zodiac War"]
artist_search_filters = [
    "Sawano",
    "Gemie",
    "Aimee Black",
    "Mika kobayashi",
    "benjamin anderson",
    ["mpi", True],   # avoiding Empire
    "david whit",       
    ["laco", True],  # avoiding galaco
    "eliana",
]
song_name_search_filters = ["Harmonious", "vogel im kaf"]
and_filter = False

/!\ It might be missing some, I did that by memory
_______________________________________________________________

"""
