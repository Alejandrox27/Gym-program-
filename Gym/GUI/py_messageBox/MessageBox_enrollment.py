from PyQt6 import QtWidgets, QtCore
from GUI.ui_messageBox_enrollment import *

class MessageBox_enrollment(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.drag_position = None
        
        self.inicializateMessage()
        
    def inicializateMessage(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.cancelBtn.clicked.connect(self.closeAnimation)
        self.ui.okBtn.clicked.connect(self.closeAnimation)
        
    def mousePressEvent(self, event):
        if not self.isMaximized():
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if not self.isMaximized():
            if self.drag_position is not None:
                if event.buttons() & QtCore.Qt.MouseButton.LeftButton:
                    new_position = event.globalPosition().toPoint() - self.drag_position
                    self.move(new_position)
                    event.accept()

    def mouseReleaseEvent(self, event):
        if not self.isMaximized():
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.drag_position = None
                event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)

        self.animation = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
        
    def closeAnimation(self):
        self.fade_out_animation = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.fade_out_animation.setDuration(80)  # Duración de la animación en milisegundos
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self.close)
        self.fade_out_animation.start()