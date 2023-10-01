from PyQt6 import QtWidgets, QtCore
from GUI.ui_messagebox_copy import *

class MessageBox_copy(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.drag_position = None
        self.inicializateMessage()
        
    def inicializateMessage(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def showEvent(self, event):
        super().showEvent(event)

        self.animation = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.finished.connect(self.startCloseAnimation)
        self.animation.start()

    def startCloseAnimation(self):
        QtCore.QTimer.singleShot(700, self.closeAnimation)

    def closeAnimation(self):
        self.fade_out_animation = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.fade_out_animation.setDuration(80)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self.close)
        self.fade_out_animation.start()