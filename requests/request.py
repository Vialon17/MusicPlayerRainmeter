import requests
from configparser import ConfigParser

# get information from config folder
conf = ConfigParser()
conf.read(".\config\setting.ini", encoding = 'utf8')


def check_server() -> bool:
    '''
    check local CloudMusicApi Nodejs server status
    '''
    port = conf['ProxyServer']['port']
    return True if requests.get('http://localhost:{0}'.format(port)).status_code == 200 else False


class User:
    '''
    the user part
    '''
    basic_url = 'http://localhost:{0}'.format(conf['ProxyServer']['port'])

    def __init__(self):
        self._data = {}
    
    def __str__(self):
        pass
    
    def login(self, way: int) -> object:
        '''
        Necessary Parameter:
            `way`: 1 -> phone, 2 -> email, 3-> qr;
        '''
        urls = {
            1:conf['LoginAbout']['login_url_phone'], 
            2:conf['LoginAbout']['login_url_email'], 
            3:conf['LoginAbout']['login_url_qr']
            }
        login_url = urls[way]

if __name__ == '__main__':
    print(check_server())