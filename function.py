from login import Login
from conf import config, url_get
from requests import session

def song_search(s : session, name, auth = None) -> dict:
    '''
    Function for searching song;
    required param: session, name;
    return dict:{nickname, artists, uid};
    Attention: 
        There I banned the 'Live' version and make a judgement section to help user to choose the right information;
        You'd better Incoming the 'author' parameter which is called 'auth' temporarily here to improve the accuracy of the result.
    '''
    url = url_get(config('Information', 'search'))
    check_url = url_get(config('Information', 'song_check'))
    temp = s.get(url, params = {'keywords': name, 'limit': 10}, timeout = 200).json()
    # the limit param will limit the number of the search result
    if temp['code'] != 200:
        print(temp); return None
    temp_json = temp['result']['songs']
    search_result = None
    for song in temp_json:
        if 'Live' in song['name'] or (auth is not None and song['artists'][0]['name'] != auth):
            continue
        if not s.get(check_url, params = {'id': song['id']}).json()['success']:
            print('No Copyright! the song\'s id:{}'.format(song['id']))
        if input('The information:\nname:{}\nauthor:{}\nalbum:{}\ny/n? '.format(song['name'], song['artists'][0]['name'], song['album']['name'])) == 'y':
            search_result = {'nickname': song['name'], 'artists': song['artists'][0]['name'], 'uid': int(song['id'])}
            break
    if not search_result: print('Havn\'t found the song or the Cloud Music hasn\'t the CopyRight.')
    return search_result

def main():
    s = Login(session())
    print(song_search(s.login_in(), 'Raccoon City'))

if __name__ == '__main__':
    main()