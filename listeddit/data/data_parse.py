# imports

def get_type(comment):
    bodytext = comment.body.lower()
    songs = ["song", "music", "audio"]
    movies = ["movie", "film"]
    shows = ["show", "TV"]
    games = ["game"]
    type = "song"  # default value
    if any(keyword in bodytext for keyword in songs):
        type = "song"
    elif any(keyword in bodytext for keyword in movies):
        type = "movie"
    elif any(keyword in bodytext for keyword in shows):
        type = "show"
    elif any(keyword in bodytext for keyword in games):
        type = "game"
    else:  # try to figure out from post title
        sub = comment.submission
        bodytext = sub.title
        if any(keyword in bodytext for keyword in songs):
            type = "song"
        elif any(keyword in bodytext for keyword in movies):
            type = "movie"
        elif any(keyword in bodytext for keyword in shows):
            type = "show"
        elif any(keyword in bodytext for keyword in games):
            type = "game"
    return type


def get_name(sub):
    name="Reddit thread " + sub.id #TODO: Make this fancier / more descriptive
    return name


def get_songs(comments_raw):
    songs = []
    songs.append("fire to the rain")
    songs.append("we didn't start the fire")
    songs.append("outta your mind")
    songs.append("it's raining men")
    # TODO: figure out which part of each element is a song -> create array
    return songs


def get_movies(comments_raw):
    movies = []
    # TODO: figure out which part of each element is a movie - >create array (old versions vs. remakes?)
    return movies


def get_shows(comments_raw):
    shows = []
    # TODO: figure out which part of each element is a show -> create array
    return shows


def get_games(comments_raw):
    games = []
    # TODO: figure out which part of each element is a game -> create array
    return games
