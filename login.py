import requests, configparser
from hashlib import md5

'''this file is about the login;
    rule: use tuple as the information return form,
    e.g:inf = (user_name, password_md5)'''

def config() -> object:
    conf = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    conf.read('conf.ini', encoding = 'UTF-8')
    return conf

def default_count(config):
    'the config use the configparser library(is the conf variable)'
    default_phone = config.get('UserID', 'phone')
    default_password = config.get('UserID', 'pw')
    #the password has used the md5_32 type
    temp = (default_phone, default_password)
    return temp

def account_data_login():
    'get the new acoount information.'
    def password_md5_changer(pw):
        if type(pw) != 'str':
            raise TypeError
        m = md5()
        m.update(pw)
        return m.hexdigest()
    
    phone = input('Please input ur phonenumber:')
    password = input('Please input ur password(md5*32 type is better):')
    if len(password) != 32:
        password = password_md5_changer(password)
    account = (phone, password)
    return account


class Login:
    '''
    The login section.
    Incoming pramas: 
        Required prama: empty session
        login_session; user_phone(default is 0); password(default is 0)
    Functions:
        login_in(); conf_writein(); 
        classmothed: refresh_login(); check_login_status(); login_out();
    '''
    def __init__(self, session, user = 0, password = 0):
        self._user = user
        self._password = password
        self.__session = session
        self._user_data_dict = {}

    @property
    def user(self):
        return self._user
    @property
    def password(self):
        return self._password
    @property
    def user_data_dict(self):
        return self._user_data_dict
    
    conf = config()
    port = conf.get('ProxyServer', 'port')

    def login_in(self) -> object:
        conf = self.conf; port = self.port
        url = 'http://localhost:{}'.format(port) + conf.get('LoginAbout', 'login_url')
        s = requests.session()
        if input('Would u like to use the default account to login in?(y/n)')== 'y':
            account_data = default_count(conf)
        else:
            account_data = account_data_login()
        self._user = account_data[0]
        self._password = account_data[1]
        s = self.__session
        user_data = {'phone':self._user, 'md5_password':self._password}
        login_json = s.post(url, data = user_data).json()

        ##collect information
        user_cookie = login_json['cookie']
        user_id = login_json['profile']['userId']
        print('Have logged in as {}'.format(login_json['profile']['nickname']))
        self._user_data_dict = {'phone':self._user, 'pw':self._password, 'uid':user_id,'cookie':user_cookie}
        #return loginin session
        ##There, there, here u can return cookies and pass param = 'cookies' when using request section
        return s
    
    def conf_writein(self, conf_file):
        'Write the user\'s information into the config file.' 
        conf = config()
        data_dict = self._user_data_dict
        if data_dict:
            raise Exception('Need login in to collect user information firstly.')
        with open(conf_file, 'w+', encoding = 'UTF-8') as wr:
            for i in data_dict:
                conf['UserID'][i] = str(data_dict[i])
            conf.write(wr)
        return self._user_data_dict

    @classmethod
    def refresh_login(cls):
        url = 'http://localhost:{}'.format(cls.port) + (cls.conf).get('LoginAbout', 'login_rf')
        request = requests.get(url)
        return request.status_code
    
    @classmethod
    def check_login_status(cls):
        url = 'http://localhost:{}'.format(cls.port) + (cls.conf).get('LoginAbout', 'login_sta')
        status_json = requests.get(url).json()
        if status_json['data']['account'] == None:
            print('Status:Login out.')
        else:
            print('Status:Login as %s' % status_json['data']['profile']['nickname'])
   
    @classmethod
    def login_out(cls):
        url = 'http://localhost:{}'.format(cls.port) + (cls.conf).get('LoginAbout', 'logout')
        request = requests.request()
        request.get(url)


def main():
    s = requests.session()
    a = Login(s)
    a.login_in()
    a.check_login_status()
    
if __name__ == '__main__':
    main()
