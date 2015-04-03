# -*- coding : utf-8 -*-
from PyQt5.QtCore import QUrl,QCoreApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlEngine,QQmlComponent
import os
import sys

app = QGuiApplication(sys.argv)
engine = QQmlEngine()
component = QQmlComponent(engine)
component.loadUrl(QUrl("main.qml"))
top = component.create()
if top :
    top.show()



sys.exit(app.exec_())