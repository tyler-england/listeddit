import spotipy
from fuzzywuzzy import fuzz


def get_playlist_id(sp, un, list_name):
    playlist_id = ""
    playlists = sp.user_playlists(un)
    for playlist in playlists["items"]:
        if playlist["name"] == list_name:
            playlist_id = playlist['id']
            break
    return playlist_id


def create_list(list_name, song_info):
    sp_cid = "4d36c529bdd045d285debd8ed83a701c"  # client ID
    sp_csec = "a260a7412b3542aba3e0f2bcfe8a9bc1"  # client secret
    sp_uri = "http://localhost:8080"
    sp_scope = "playlist-modify-private,playlist-modify-public"
    # sp_cache = '.spotipyoauthcache'
    sp_un = "374oo3vji0f3aexvb4l423n63"

    auth_mgr = spotipy.SpotifyOAuth(sp_cid, sp_csec, sp_uri, None, sp_scope, None, sp_un)
    # sp = spotipy.oauth2.SpotifyOAuth(sp_cid, sp_csec, sp_uri, None, sp_scope, sp_cache, sp_un)
    sp = spotipy.Spotify(auth_manager=auth_mgr)
    playlist_name = list_name
    playlist_description = 'description for test playlist'
    track_ids = []
    list_url = ""
    for i in range(len(song_info)):
        if len(song_info[i]) > 0:
            try:
                print(song_info[i])
                results = sp.search(q=song_info[i], limit=5, type="track")
                if results["tracks"]["total"] > 0:
                    max_match = 0
                    for j in range(len(results["tracks"]["items"])):  # for the search results
                        cmptxt = results['tracks']['items'][j]['name']  # title
                        cmptxt = cmptxt + " " + results['tracks']['items'][j]['artists'][0]['name']  # add artist
                        match = fuzz.token_set_ratio(cmptxt, song_info[i])  # similarity between result & comment
                        if match > max_match:  # closer match on title/artist
                            max_match = match
                            max_ind = j
                    if max_match > 0:
                        track_ids.append(results['tracks']['items'][max_ind]['id'])  # append track id
            except Exception as e:
                print(song_info[i] + "--" + str(e))
                continue
    track_ids = list(dict.fromkeys(track_ids))  # remove duplicates
    if len(track_ids) > 0:
        track_ids = track_ids[:99]  # 100 max per spotify
        new_playlist = sp.user_playlist_create(sp_un, playlist_name, public=True, description=playlist_description)
        list_id = get_playlist_id(sp, sp_un, playlist_name)
        list_url = "open.spotify.com/playlist/" + list_id
        sp.playlist_add_items(list_id, track_ids)
    return list_url
