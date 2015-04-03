#-*- coding:utf-8 -*-
class Captcha (object) :
    RGB_BLACK = (0,0,0)
    RGB_WHITE = (255,255,255)
    L_BLACK = 0
    L_WHITE = 255
    SYMBOL_NUMBER = ['1','2','3','4','5','6','7','8','9','0']
    SYMBOL_CAPITAL_CHARACTER = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    def __init__(self,filename=None):
        pass
    def _init(self,show=False):
        pass
    def _bicode(self,show=False):
        pass
    def _clearify(self,show=False):
        pass
    def _divided(self):
        pass
    def transfer(self):
        pass


class Classifier(object) :
    '''
        ML partion, training and testing
    '''
    def train(self,filename):
        pass

    def load(self,filename):
        pass

    def test(self,character):
        pass

    def save(self,filename):
        pass


