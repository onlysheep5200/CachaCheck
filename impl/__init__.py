#-*- coding:utf-8 -*-
from interfaces import Captcha,Classifier
from PIL import  Image
import os.path
from utils.svm import *
from utils.svmutil import *
class ByrBtCaptcha(Captcha):
    def __init__(self, filename=None):
        super(ByrBtCaptcha, self).__init__(filename)
        #print filename
        try :
            self.im = Image.open(filename)
            self.mode = self.im.mode
            self.raw = self.im.load()
            self.width,self.height = self.im.size
            self.basename = os.path.basename(filename).split('.')[0]
            self.symbols = []
            self.symbols.extend(Captcha.SYMBOL_NUMBER)
            self.symbols.extend(Captcha.SYMBOL_CAPITAL_CHARACTER)
            self.min_char_height = 7
            self.classes = {}
            if self.im.mode == 'L' :
                self.bicoded = True
            else :
                self.bicoded = False
            for x in range(len(self.symbols)):
                self.classes[self.symbols[x]] = x
        except Exception,e :
            print e.__unicode__()
            print "cannot open the image file"
            return

    def _init(self,show=False):
        for w in xrange(self.width):
            for h in xrange(self.height):
                if self.raw[w,h] != (0,0,0):
                    self.im.putpixel((w,h),(255,255,255))
        box = (23,14,self.width-23,self.height-15)
        self.im = self.im.crop(box)
        self._reset()
        if show :
            self.im.show()

    #return sub images
    def _divided(self):
        #print 'divided'
        #self.im.show()
        if not self.bicoded :
            return []
        #print self.im.mode
        marCol = []
        #print self.im.getpixel((0,0))
        for w in xrange(self.width):
            black_num = 0
            for h in xrange(self.height):
                if self._is_black((w,h)) :
                    black_num += 1
            marCol.append(black_num)

        breakcols = []
        breakpoints = []
        # for i in range(len(marCol)) :
        #     if self._is_breakpoint(marCol,i) :
        #         breakcols.append(i)
        #
        # print breakcols
        #
        # for x in range(0,len(breakcols),2) :
        #     p = (breakcols[x],breakcols[x+1])
        #     breakpoints.append(p)
        breakpoints = [(1,10),(19,28),(37,47),(55,64),(73,82),(91,100)]
        if len(breakpoints) < 6 :
            print len(breakpoints)
            print "divided failed"
        elif len(breakpoints) > 6 :
            widths = []
            for p in breakpoints :
                widths.append(abs(p[0]-p[1]))
            lastones = sorted(widths,lambda x,y : y-x)[6:]
            for w in lastones :
                i = widths.index(w)
                del breakpoints[i]

        #print breakpoints
        subimgs = []
        for x in breakpoints :
            sim = self.im.crop((x[0],0,x[1],self.height))
            subimgs.append(sim)
            #sim.show()
        #print "length of subimages is %d"%len(subimgs)
        return subimgs

    def _bicode(self,show=False):
        #print 'bycoded'
        self.im = self.im.convert('L')
        self._reset()
        self.bicoded = True
        self._set_color()
        if show :
            self.im.show()


    def _clearify(self,show=False):
        #print 'clearify'
        self._set_color()
        for w in range(self.width) :
            for h in range(self.height):
                if self.raw[w,h] == self.black:
                    if (w==0 and h==0) or (w==self.width-1 and h==self.height-1):
                        self.im.putpixel((w,h),self.white)
                    else :
                        if self._is_single(w,h) :
                            self.im.putpixel((w,h),self.white)
        self._reset()
        if show :
            self.im.show()

    def _reset(self):
        self.width,self.height = self.im.size
        self.raw = self.im.load()
        self.mode = self.im.mode

    def _is_black(self,point=(0,0)):
        if self.mode == 'RGB' :
            black = Captcha.RGB_BLACK
        elif self.mode == 'L' :
            black = Captcha.L_BLACK
        if self.raw[point[0],point[1]] == black :
            return True
        else:
            return False

    def _is_single(self,w,h):
        left = (w-1,h)
        right = (w+1,h)
        up = (w,h+1)
        down = (w,h-1)
        points = filter(lambda  x : x[0]>0 and x[1]>0 and x[0]<self.width and x[1]<self.height,(left,right,up,down))
        #print points
        result = True
        for x in points :
            result &= not self._is_black(x)
        return result

    def _is_breakpoint(self,marCol,pos):
        if marCol[pos] > 0 :
            return False
        left = pos -1
        right = pos+1
        if left>=0 and right<len(marCol) :
            if marCol[left]==0 and marCol[right]==0 :
                return False
            else :
                return True
        elif left<0 :
            if marCol[right] > 0 :
                return True
        else :
            if marCol[left] > 0 :
                return True
        return False

    def _set_color(self):
        if self.mode == 'RGB':
            self.black = Captcha.RGB_BLACK
            self.white = Captcha.RGB_WHITE
        #TODO:other color mode ...
        else :
            self.black = Captcha.L_BLACK
            self.white = Captcha.L_WHITE

    def _is_char(self,point):
        self._set_color()
        p1 = point[0]
        p2 = point[1]
        for i in range(p1,p2+1):
            first_black = -1
            last_black = -1
            for h in range(self.height) :
                if self.im.getpixel((i,h)) == self.black :
                    if first_black<0 :
                        first_black = h
                    if self.im.getpixel((i,h+1)) == self.white :
                        lask_black = h
                        break
            if first_black >=0 :
                if abs(first_black - last_black) > self.min_char_height :
                    return True

        return False

    def get_char(self,num):
        num = int(num)
        for x in self.classes :
            if self.classes[x] == num :
                return x




    def transfer(self):
        self._init()
        self._bicode()
        self._clearify()
        subs = self._divided()
        #subs[0].show()
        codes = list(self.basename)
        characters = []
        labels = []
        for i in range(len(codes)):
            label = self.classes[codes[i]]
            image = subs[i]
            width,height = image.size
            character = {}
            for w in range(width) :
                for h in range(height) :
                    pixel = image.getpixel((w,h))
                    if image.mode == 'L' :
                        pixel = pixel/255
                    index = w*height+h+1
                    character[index] = pixel
            characters.append(character)
            labels.append(label)
        #print characters[1]
        return labels,characters




class SvmClassifier(Classifier):
    def __init__(self):
        self.model = None

    def test(self,labels,characters):
        #super(SvmClassifier, self).test(character)
        if self.model :
            return svm_predict(labels,characters,self.model)
        return None

    def train_from_file(self, filename,args="-c 4"):
        y,x = svm_read_problem(filename)
        self.model = svm_train(y,x,args)

    def train(self,labels,characters,args = "-c 4"):
        self.model = svm_train(labels,characters,args)

    def load(self, filename):
        if os.path.exists(filename) :
            self.model = svm_load_model(filename)
        else :
            print "no such file"
            exit()

    def save(self,filename):
        if self.model :
            svm_save_model(filename,self.model)


if __name__ == '__main__' :
    captcha = ByrBtCaptcha('/Users/mac/Desktop/captcha/3HHFH3.png')
    ls,cs = captcha.transfer()
    print cs
    # classfier = SvmClassifier()
    # classfier.train(ls,cs)
    # classfier.save("model.mdl")








