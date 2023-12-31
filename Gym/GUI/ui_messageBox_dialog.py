# Form implementation generated from reading ui file 'messageBox_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(321, 177)
        Dialog.setStyleSheet("*{\n"
"background-color:transparent;\n"
"background:transparent;\n"
"    border:none;\n"
"padding:0;\n"
"margin:0;\n"
"color:#fff;\n"
"}\n"
"\n"
"#widget{\n"
"background-color:rgb(49, 55, 66);\n"
"border-radius:20px;\n"
"border-top-right-radius:0px;\n"
"}\n"
"\n"
"\n"
"#okBtn:hover{\n"
"background-color:rgb(104, 102, 122);\n"
"border-bottom-right-radius:20px;\n"
"}\n"
"\n"
"#closeMessageBtn:hover{background-color:rgb(104, 102, 122);}\n"
"\n"
"#writeTxt{\n"
"background-color:rgb(45, 46, 52);\n"
"border-radius:12px;\n"
"border:2px solid rgb(38, 38, 45);\n"
"padding:1px;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2.addWidget(self.frame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_2 = QtWidgets.QFrame(parent=self.widget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.messageLbl = QtWidgets.QLabel(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.messageLbl.setFont(font)
        self.messageLbl.setObjectName("messageLbl")
        self.verticalLayout_3.addWidget(self.messageLbl, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.writeTxt = QtWidgets.QLineEdit(parent=self.frame_4)
        self.writeTxt.setMinimumSize(QtCore.QSize(260, 10))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.writeTxt.setFont(font)
        self.writeTxt.setObjectName("writeTxt")
        self.verticalLayout_3.addWidget(self.writeTxt, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(parent=self.widget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.closeMessageBtn = QtWidgets.QPushButton(parent=self.frame_3)
        self.closeMessageBtn.setMinimumSize(QtCore.QSize(60, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.closeMessageBtn.setFont(font)
        self.closeMessageBtn.setObjectName("closeMessageBtn")
        self.horizontalLayout_2.addWidget(self.closeMessageBtn)
        self.okBtn = QtWidgets.QPushButton(parent=self.frame_3)
        self.okBtn.setMinimumSize(QtCore.QSize(60, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.okBtn.setFont(font)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout_2.addWidget(self.okBtn)
        self.verticalLayout_2.addWidget(self.frame_3, 0, QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignBottom)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.writeTxt, self.okBtn)
        Dialog.setTabOrder(self.okBtn, self.closeMessageBtn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.messageLbl.setText(_translate("Dialog", "message"))
        self.closeMessageBtn.setText(_translate("Dialog", "Cancel"))
        self.okBtn.setText(_translate("Dialog", "Ok"))
