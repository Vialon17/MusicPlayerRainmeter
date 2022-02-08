import requests, os, pickle, time
from conf import config, url_get
from cache import songlib_pickle
from login import Login

valid_period = config('Setting', 'update_period')

def check_local_song(songname : str) -> dict:

    '''
    to check if song exist in local songslib folder.
    return the result:
        {'folder_name': ['song1_name','song2_name']}...
    attention: the check case sensitive
    '''

    result = {}
    songslib_cachefile = config('Local', 'cache') + '\SongsLibCache.pkl'
    time_period = int(time.time() - os.path.getmtime(songslib_cachefile))
    if os.path.exists(songslib_cachefile) != True and (time_period//86400 >= valid_period):
        songlib_pickle()
    with open(songslib_cachefile, 'rb') as cache:
        songlib_cache = pickle.load(cache)
    for key, value in songlib_cache.items():
        temp_list = []
        for filename in value:    
            if songname in filename:
                temp_list.append(filename)
        if temp_list == []:
            continue
        result[key] = temp_list
    return result

def download_check(cache, object):
    '''
    Check the local cache library and file brfore download to avoid possible mistake.
    '''
    pass

class Song:
    '''
    Required minimum parameters:song's id and user session.
    
    '''
    def __init__(self, session, id, name = None, artist = None, **kwarg):
        self._id = id
        self._session = session
        self._name = name
        self._filetype = 'mp3'
        self._artist = artist
        self._other = {}
        for key, value in kwarg:
            self._other[key] = value
        if self._artist is None:
            self.song_inf()

    @property
    def id(self):
        return self._id
    
    @property
    def artist(self):
        return self._artist
    
    @property
    def album(self):
        return self._album

    def song_inf(self) -> dict:
        '''
        Function return song information, need song's id parameter.
        return syntax:
                    {'nickname': '', 'sn': '보여줄게', 'ar': 'Ailee', 'uid': 310680566, 'br': 2307, 'fn': '보여줄게_Ailee.wav', 'alb': 'Invitation ', 'cid': ''}
        There has set the class's attributes:
            song's arthor: self.artist
            song's name: self.name
            song.album: self.album
            song.pictiureURL: self.picURL
        '''
        url = url_get(config('Information', 'song_inf'))
        temp_json = self._session.get(url, params = {'ids':self._id}).json()
        if temp_json['songs'] is None:
            print('Haven\'t found the song %s' % self._id)
            return None
        information = dict(song_inf := temp_json['songs'][0])
        self._name = song_inf['name']
        self._artist = song_inf['ar'][0]['name']
        self._album = song_inf['al']['name']
        self._picURL = song_inf['al']['picUrl']
        return information

    
    def download_url_get(self) -> str:
        '''
        Just get the download URL from NetCloud music API.
        '''
        download_url_getter = url_get(config('Information', 'download_url'))
        s = self._session
        temp_json = s.get(download_url_getter, params = {'id':self._id}).json()
        download_url = temp_json['data']['url']
        self._filetype = temp_json['data']['type']
        if download_url is None:
            print('Missing resources in NetCloud.')
        return download_url

    def download(self, url, cachelib) -> str:
        '''
        Download song and write into cache_file.
        Return the filename str.
        '''
        filename = self._name + '.' + self._filetype
        song_temp = self._session.get(url).content
        with open(cachelib + '\\' + filename, 'wb') as writedown:
            writedown.write(song_temp)
        print(f'Have downloaded into the file:{filename} in {cachelib} folder.')
        return filename
    
    def download_pic(self, cachelib) -> str:
        'Download song picture and write into cache_file.'
        if self._picURL is None:
            self.song_inf()
        filename = self._name + self._picURL[-4:]
        pic_temp = self._session.get(self._picURL, verify = False).content
        with open(cachelib + '\\' + filename, 'wb') as writedown:
            writedown.write(pic_temp)
        print(f'Have downloaded into the file:{filename} in {cachelib} folder.')
        return filename

    def download_lyric(self, cachelib) -> str:
        'Download song lyric and write into cache_file.'
        lyric_url = url_get(config('Information', 'song_lyric'))
        temp_json = self._session.get(lyric_url, params = {'id': self._id}).json()
        if temp_json['code'] != 200:
            print('Error with Code:{}' % temp_json['code']); return None
        if self._name is None:
            self.song_inf()
        filename = self._name + '.lrc'
        with open(cachelib + '\\' + filename, 'w+', encoding = 'UTF-8') as writedown:
            for lrc in temp_json:
                if type(temp_json[lrc]) != dict or 'lyric' not in temp_json[lrc]: continue
                writedown.write(temp_json[lrc]['lyric'])
        print(f'Have downloaded into the file:{filename} in {cachelib} folder.')
        return filename

def main():
    user = Login(requests.session())
    s = user.login_in()
    song_id = 35440252
    song1 = Song(s, song_id)
    cachelib = 'E:\Songs\Cache'
    print(song1.download_lyric(cachelib))

if __name__ == '__main__':
    main()