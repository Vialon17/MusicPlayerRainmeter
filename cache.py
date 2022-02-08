import pickle, os
from conf import config

temp_bannd_endswith = ('.jpg', '.lrc')
songslib = config('Local', 'songslib')
cachelib = config('Local', 'cache')

def endswith_judge(endswith_tuple : tuple, filename : str) -> bool:
    '''
    To judge the filetype if we need.
    for example: ('.jpg', '.png') and filename: temp.jpg,
    then the function will return True.
    '''
    for endswith in endswith_tuple:
        if filename[-4:] == endswith: return True
    return False

def songlib_pickle():
    songslib_cache = {}
    for dir in os.listdir(songslib):
        dirpath = os.path.join(songslib + '\\' + dir)
        if dir == 'Cache': continue
        if os.path.isdir(dirpath):
            temp_filelist = []
            for filename in os.listdir(dirpath):
                if not endswith_judge(temp_bannd_endswith, filename):
                    temp_filelist.append(filename)
            songslib_cache[dir] = temp_filelist
    with open(cachelib + '\\SongsLibCache.pkl', 'wb+') as songslib_cache_file:
        pickle.dump(songslib_cache, songslib_cache_file)
    print('Have write in songslibrary cache.')


def main():
    print(songlib_pickle())

if __name__ == '__main__':
    main()
