from interfaces import Captcha,Classifier
from impl import ByrBtCaptcha,SvmClassifier
import os.path
from cli import CliTool
def visit(arg,dirname,names):
    print dirname
    for name in names :
        if name.split('.')[1] != 'png':
            continue
        image = ByrBtCaptcha(dirname+'/'+name)
        print name
        labels,characters = image.transfer()
        arg['labels'].extend(labels)
        arg['characters'].extend(characters)


if __name__ == '__main__':
    cli = CliTool()
    cli.start()
    # t_set = dict(labels=[],characters=[])
    # os.path.walk('/Users/mac/Desktop/captcha',visit,t_set)
    #classfier = SvmClassifier()
    # classfier.train(t_set['labels'],t_set['characters'])
    # classfier.save("model.mdl")
    # classfier.load("model.mdl")
    # im = ByrBtCaptcha('/Users/mac/Desktop/captcha/test/1A6EEH.png')
    # ls,cs = im.transfer()
    # plabels,a,v = classfier.test(ls,cs)
    # captcha = []
    # for l in plabels :
    #     captcha.append(im.get_char(l))
    # captcha = ''.join(captcha)
    # print captcha