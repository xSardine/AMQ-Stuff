# Saro Top 5000 Stats

# What it does
It is currently in development: the code is ugly, the output is ugly, everything is ugly, it might not even work, there's still 8 months before the end, so I take my time.
This repository is useless to you if you're not part of Saro's cursed openings party rank.

Currently, the script let you get a bunch of stats regarding your scorings.

# Usage
## **How to download it**

There is two way 

**either**:
- Download python: <https://www.python.org/downloads/>
- Download the code: <https://downgit.github.io/#/home?url=https://github.com/xSardine/AMQ-Stuff/tree/main/Top5000Stats>
- Download your sheet from google sheet: `File` → `Download` → `OpenDocument Format (.ods)` and move it into the `Top5000Stats` folder newly created.

**or** :
- Only do the third point and send it to me via DM if you don't want to download python and the code. I'll run it for you.

~~The more people do the first version the less work I have to do~~

## **How to use it**

- Double click on `ProcessingArtists.py`, this will make a mapping to automatically assign an ID to each artist.
- Double click on `ProcessingUserList.py`, this will generate a `.txt` file containing all sorts of stats.
- If there's any errors, DM me, I didn't test it from a new environment, and some libraries might be missing.

The best way to navigate through this cursed `.txt` is to CTRL+F your way with these keywords:
- **Global Stats**: Stats concerning your entire list
- **Full Sorted List**: Your entire list, but sorted by score in descending order
- **Most Favorite Artists**: Your top 10 most favorite artists (must have at least 3 songs)
- **Least Favorite Artists**: Your top 10 least favorite artists (must have at least 3 songs)
- **Most represented artists**: Starts concerning the top 10 artists with the most songs
- **Sorted Score Counter**: Count the amount of times you've given a particular score. Come with two precisions: 1.0 and 0.1
- **Stats per decade**: Stats concerning each decades


## **Customize it**

You can customize some settings in `ProcessingUserList.py`:
- You can choose to not print some of the stats by replacing the `True` value with `False` of the `activate_<particular_stats>` attribute. For example, if you want to remove the full sorted list, you can replace `activate_full_sorted_list = True` with `activate_full_sorted_list = False`
- You can change the amount of artists printed for the most/least favorite artists as well as the most represented artists by changing `nb_artists = 10` with `nb_artists = <new_number>`
- You can change the minimal amount of songs an artist need to be taken into account in the most/least favorite artists by changing `minimum_amount_of_songs = 3` with `minimum_amount_of_songs = <new_number>`.

## If you want to help me

This algorithm automatically maps an artist with a given ID, that way I can easily get every song for a given artists. However I can't **fully** automate it.

- 85% is automated: Basic artists
- 10% is semi-automated: Artists that have multiple names or that Saro typo'd                                                 (i.e. Afilia Saga / Afilia Saga East)
- another 2% is semi-automated: Artists that contains "&" or "," in their name                                                    (ie. Kishida Kyodan &THE Akeboshi Rockets)
- 3% will need to be manual: Different artists with the same name                                                                       (i.e. Minami (DomexKano) / Minami (Kuribayashi))

For the 2 middle cases, if you find an artist or combo of artists that I've yet to add to my exceptions in `ProcessingArtists.py`, you can DM me on Discord.

For the last case, I'll probably do them at the end, or later. It's not yet implemented. However, I'll still take the artists you can find.

I'll also take a reminder when we cross a new decade and at which song.
