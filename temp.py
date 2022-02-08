# This file is just for test privately.
import os, random, math, configparser, hashlib, itertools

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

def getStrAsMD5(parmStr):
    #1、参数必须是utf8
    #2、python3所有字符都是unicode形式，已经不存在unicode关键字
    #3、python3 str 实质上就是unicode
    if isinstance(parmStr,str):
        # 如果是unicode先转utf-8
        parmStr=parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()


def judge(num, judge_list, return_list):
    len_judge = len(judge_list)
    len_return = len(return_list)
    if len_judge - len_return < 0:
        for i in range(abs(len_return - len_judge)):
            judge_list.append(judge_list[-1])
    else:
        for j in range(abs(len_return - len_judge)):
            return_list.append(return_list[-1])
    for k in range(len(judge_list)):
        if num == judge_list[k]:
            return return_list[k]
    raise Exception('Havn\'t found valid key.')


class Card():

    def __init__(self, num, suite):
        self._num = int(num)
        if self._num not in range(1, 14):
            raise Exception('Card Key Error!')
        self._suite = suite
    
    @property
    def num(self):
        return self._num
    
    @property
    def suite(self):
        return self._suite
    
    def __str__(self):
        surface_num = self._num
        if self._num not in range(2, 11):
            face = ['A', 'J', 'Q', 'K']
            face_num = [1, 11, 12, 13]
            for i in range(len(face_num)):
                if surface_num == face_num[i]:
                    surface_num = face[i]
        string = '%s%s' % (self._suite, surface_num)
        return string

    def include_show(self):
        return self._suite, self._num

class Poker:
    
    def __init__(self):
        self._num = [x for x in range(1, 14)]
        self._suite = ['Heart♠', 'Spade♥', 'Club♣', 'Diamond♦']

    def shuffle(self) -> list:
        deck = []
        temp = input('Dose the Poker need jokers?(y/n)')
        if temp == 'y':
            deck += ['JOKER', 'Joker']
        for i in itertools.product(self._suite, self._num):
            temp = i[0] + str(i[1])
            deck.append(temp)
        random.shuffle(deck)
        return deck

    def next(self, deck: list, left_cards_num: int) -> tuple:
        left_cards = deck[-left_cards_num:]
        deck = deck[:-left_cards_num]
        print(deck, len(deck))
        for i in range(len(deck)):
            yield deck.pop(0)

def poker_temp():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    b = ['Heart♠', 'Spade♥', 'Club♣', 'Diamond♦']
    poker = Poker()
    deck = poker.shuffle()
    left_cards_num = 3
    left_cards = deck[-left_cards_num:]
    people_num = 3
    temp1, temp2, temp3 = [], [], []
    temp_num = 0
    for i in poker.next(deck, 3):
        temp_num += 1
        if temp_num in range(1, 54, people_num):
            temp1.append(i)
        if temp_num in range(2, 54, people_num):
            temp2.append(i)
        if temp_num in range(3, 54, people_num):
            temp3.append(i)
    print(temp1, len(temp1), temp2, len(temp2), temp3, len(temp3))

def abc():
    def __str__(self):
        return 'this is a function'
    pass

def change_int(x:int):
    str = ''
    temp = x
    while temp != 0:
        if temp % 2 == 1:
            str += '1'
        else: str += '0'
        temp = temp//2
    print(str)

class Temmp:
    @classmethod
    def test(self):
        return '123'

def main():
    A = Temmp()
    print(A.test(), Temmp.test())

if __name__ == '__main__':
    main()
