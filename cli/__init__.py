#! /usr/local/bin/python
# -*- coding:utf8 -*-
import os.path
import  argparse
from impl import SvmClassifier,ByrBtCaptcha

def visit(arg,dirname,names):
    #print dirname
        for name in names :
            if name.split('.')[1] != 'png':
                continue
            image = ByrBtCaptcha(dirname+'/'+name)
            print name
            labels,characters = image.transfer()
            arg['labels'].extend(labels)
            arg['characters'].extend(characters)

class CliTool(object):
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        self.argParser = argparse.ArgumentParser()
        #self.argParser.add_argument('run',help="运行",action="store_true")
        self.argParser.add_argument("--train",help="训练模型",action="store_true")
        self.argParser.add_argument("--test",help="测试数据",action="store_true")
        self.argParser.add_argument("--pic",help="请输入测试图片路径")
        self.argParser.add_argument("--dir",help="请输入训练数据所在路径",default="/Users/mac/Desktop/captcha")
        self.argParser.add_argument("--clearify",help="去噪声",default='')
        self.argParser.add_argument("--bicode",help="情输入图片路径",default='')
        self.argParser.add_argument("--model",help="请输入模型路径",default='/Users/mac/Desktop/CachaCheck/model.mdl')
        self.argParser.add_argument("--save",help="请输入要存储的路径",default=self.dir)
        self.args = None

    def start(self):
        self.args = self.argParser.parse_args()

        if self.args.train :
            #self._train()
            self._train()
        elif self.args.test :
            self._test()
        elif self.args.bicode :
            self._bicode()
        elif self.args.clearify :
            self._clearify()

    def _train(self):
        t_set = dict(labels=[],characters=[])
        os.path.walk(self.args.save,visit,t_set)
        classfier = SvmClassifier()
        classfier.train(t_set['labels'],t_set['characters'])
        classfier.save(self.args.save+"/model.mdl")

    def _test(self):
        if self.args.pic == '' or (not os.path.exists(self.args.pic)):
            print "请输入合法的图片路径"
            exit()
        classfier = SvmClassifier()
        classfier.load(self.args.model)
        im = ByrBtCaptcha(self.args.pic.upper())
        ls,cs = im.transfer()
        ls = [1,1,1,1,1,1]
        plabels,a,v = classfier.test(ls,cs)
        captcha = []
        for l in plabels :
            captcha.append(im.get_char(l))
        captcha = ''.join(captcha)
        print "验证码为：%s"%captcha

    def _bicode(self):
        if self.args.bicode == '' or (not os.path.exists(self.args.bicode)):
            print '请输入正确的图片路径'
            return
        captcha = ByrBtCaptcha(self.args.bicode)
        captcha._init()
        captcha._bicode(show=True)

    def _clearify(self):
        if self.args.clearify == '' or (not os.path.exists(self.args.clearify)):
            print '请输入正确的图片路径'
            return
        captcha = ByrBtCaptcha(self.args.clearify)
        captcha._init()
        captcha._bicode()
        captcha._clearify(show=True)






if __name__ == '__main__':
    cli = CliTool()
    cli.start()



