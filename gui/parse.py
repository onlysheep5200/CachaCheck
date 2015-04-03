from PyQt5.QtCore import QUrl
url = QUrl("file:///.file/id=6571367.36737433")
f = url.toLocalFile()
print f
#print url.toString()
