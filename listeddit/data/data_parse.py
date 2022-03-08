import urllib, json, re


def get_type(comment):
    bodytext = comment.body.lower()
    songs = ["song", "music", "audio"]
    movies = ["movie", "film"]
    shows = ["show", "TV"]
    games = ["game"]
    type = "that"  # default value
    if any(keyword in bodytext for keyword in songs) or bodytext.lower()=="listplease!":
        type = "song"
    elif any(keyword in bodytext for keyword in movies):
        type = "movie"
    elif any(keyword in bodytext for keyword in shows):
        type = "show"
    elif any(keyword in bodytext for keyword in games):
        type = "game"
    else:
        pos1 = bodytext.find("[")
        pos2 = bodytext.find("]")
        if pos2 > pos1 > -1:
            type = bodytext[pos1 + 1:pos2]
    if type == "":  # try to figure out from post title
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
    name = "Reddit thread " + sub.id  # TODO: Make this fancier / more descriptive
    return name


def get_title_YT(vidlink):
    title = ""
    try:
        params = {"format": "json", "url": vidlink}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string
        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            title = data['title']
    except Exception:
        pass
    return title


def strip_extra(text, delim):
    words = text.split()
    pos1 = 0
    for j in range(len(words)):  # find position of delim
        if words[j] is delim:
            pos1 = j
            break
    if pos1 is 0:  # might be mashed against preceding/following word
        for j in range(len(words)):
            if words[j].find(delim) > -1:
                pos1 = j
                break
    pos2 = 0
    j = pos1
    bOneFound = False
    if text.find("\"") > -1:
        while j < len(words):
            if words[j][-1] is "\"":  # word ends with quotes
                pos2 = j
                break
            j = j + 1
    if pos2 is 0:
        j = pos1  # reset j
        while j < len(words):  # find end of title/artist snippet
            if words[j].istitle():
                pos2 = j + 1
            elif len(words[j]) > 3:
                if bOneFound:  # not proper case
                    break
                else:
                    bOneFound = True
                    pos2 = j + 1
            j = j + 1
    if pos2 is 0:
        pos2 = len(words)
    j = pos1
    pos1 = 0
    if text.find("\"") > -1:
        while j > -1:
            if words[j][0] is "\"":
                pos1 = j
                break
            j = j - 1
    if pos1 is 0:
        while j > -1:  # find beginning of title/artist snippet
            if words[j].istitle():
                pos1 = j
            elif len(words[j]) > 3:
                break
            j = j - 1
    return " ".join(words[pos1:pos2])


def get_songs(comments_raw):
    songs = []
    for comment in comments_raw:
        if not hasattr(comment, "body"):  # "More Comments" has no body
            continue
        #print("2: " + comment.body[:25])
        txt = comment.body
        for line in txt.splitlines():
            songfound = False
            if line.lower().find("youtu") > -1:  # youtube link (easy)
                pos1 = line.find("[")
                pos2 = line.find("]")
                if pos1 > -1 and pos2 > -1:  # youtube link with description
                    if pos2 > pos1:  # CYA
                        titleYT = line[pos1 + 1:pos2]
                        if not titleYT.lower().find("youtu"):  # link was typed properly
                            songs.append(titleYT.strip())  # use link description
                            songfound = True
                if not songfound:  # just a youtube link, no description
                    for word in line.split():
                        if word.lower().startswith("youtu"):
                            titleYT = get_title_YT(word)
                            if titleYT is "":
                                continue
                            pos1 = titleYT.lower().find("(official")
                            if pos1 > 1:  # remove "(official video)" or similar
                                titleYT = titleYT[:pos1]
                            if len(titleYT) > 0:
                                songs.append(titleYT.strip())
            elif line.lower().find(" by ") > -1 or line.find("-") > -1:  # title by/- artist (commone)
                line = line.replace("”", "\"")
                line = line.replace("“", "\"")
                if line.lower().find(" by ") > -1:
                    delim = " by "
                else:
                    delim = " - "
                    if line.lower().count(delim) is 0:  # trim spaces
                        delim = delim.strip()
                split_line = re.split("[;,.]", line)  # in case multiple were listed
                for i in range(len(split_line)):
                    if len(split_line[i]) < 2:  # too short -> maybe was acronym?
                        split_line[i] = split_line[i - 1] + split_line[i]
                    elif split_line[i][:2] == "\" ":  # comma was potentially in title
                        split_line[i] = split_line[i - 1] + split_line[i]
                    elif split_line[i][:2] == "by":  # comma potentially between title/artist
                        split_line[i] = split_line[i - 1] + split_line[i]
                    if split_line[i].lower().find(" by ") > -1 or split_line[i].find("-") > -1:
                        if split_line[i].find(" by ") > -1:
                            split_line[i] = strip_extra(split_line[i], "by")
                        else:
                            split_line[i] = strip_extra(split_line[i], "-")
                        split_line[i] = split_line[i].replace("-", "")  # remove dashes
                        # split_line[i] = split_line[i].replace("\"", "") #remove quotes
                        songs.append(split_line[i].strip())
            else:  # weird/annoying format
                if len(line) > 100:
                    continue
                line = line.replace("-", "")  # remove dashes
                line = line.replace("\"", "")  # remove quotes
                pos1 = line.find(".")
                if pos1 > -1:
                    songs.append(line[:pos1].strip())
                else:
                    songs.append(line.strip())  # TODO: parse
    #print("3: " + str(len(songs)))
    songs = list(dict.fromkeys(songs))  # remove duplicates
    #print("4: " + str(len(songs)))
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
