def create_list(list_name, item_type, item_list):
    if item_type is "movie":
        from listeddit.APIs import imdb
        list_link = imdb.create_list(list_name, item_list)
    elif item_type is "show":
        from listeddit.APIs import netflix
        from listeddit.APIs import hulu
        from listeddit.APIs import disney
    elif item_type is "game":
        from listeddit.APIs import playstation
        from listeddit.APIs import xbox
        from listeddit.APIs import nintendo
        from listeddit.APIs import pc
    else:
        from listeddit.APIs import spotify
        list_link = spotify.create_list(list_name, item_list)
    return list_link
