import os


def findfile(name, ext):
    name = name.lower()
    if ext[:1] != ".":
        ext = "." + ext
    ext = ext.lower()
    docpath = os.path.dirname(os.getcwd())  # file parent dir
    for file in os.listdir(docpath):
        if file.endswith(ext):
            if file.find(name) >= 0:
                if docpath.find("/") > -1:
                    docpath = docpath + "/" + file
                else:
                    docpath = docpath + "\\" + file
                break
    if docpath.lower().find(name) >= 0 and docpath.lower().endswith(ext):
        return docpath.lower()
    else:
        return


def get_id_sec(service):
    docpath = findfile("logins", "txt")
    cid = ""
    csec = ""
    if not docpath == "":
        with open(docpath) as logindoc:
            info = [line.rstrip() for line in logindoc]
        for i in range(len(info)):
            if info[i].lower() == service.lower():
                x = info[i + 1].find(":") + 1
                cid = info[i + 1][x:]
                x = info[i + 2].find(":") + 1
                csec = info[i + 2][x:]
    return cid, csec


def create_list(list_name, sub_id, item_type, item_list):
    if item_type == "movie":
        from APIs import imdb
        list_link = imdb.create_list(list_name, item_list)
    elif item_type == "show":
        from APIs import netflix
        from APIs import hulu
        from APIs import disney
    elif item_type == "game":
        from APIs import playstation
        from APIs import xbox
        from APIs import nintendo
        from APIs import pc
    else:
        from APIs import spotify
        cid, csec = get_id_sec("spotify")
        list_link = spotify.create_list(cid, csec, list_name, sub_id, item_list)
    return list_link
