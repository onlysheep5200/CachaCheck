# -*- coding : utf-8 -*-
__author__ = 'hyd'
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
import os
import sys

print "start ....."

app = QGuiApplication(sys.argv)
view = QQuickView()
view.setTitle("captcha")
view.setResizeMode(QQuickView.SizeRootObjectToView)
view.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'main.qml')))
view.show()

sys.exit(app.exec_())