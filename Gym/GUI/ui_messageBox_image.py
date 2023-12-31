# Form implementation generated from reading ui file 'messageBox_image.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(203, 192)
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
"#closeMessageBtn:hover{\n"
"background-color:rgb(104, 102, 122);\n"
"border-radius:10px;\n"
"}\n"
"\n"
"#okBtn:hover{\n"
"background-color:rgb(104, 102, 122);\n"
"border-bottom-right-radius:20px;\n"
"}\n"
"\n"
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
        self.closeMessageBtn = QtWidgets.QPushButton(parent=self.frame)
        self.closeMessageBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/x-circle.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.closeMessageBtn.setIcon(icon)
        self.closeMessageBtn.setIconSize(QtCore.QSize(24, 24))
        self.closeMessageBtn.setObjectName("closeMessageBtn")
        self.horizontalLayout.addWidget(self.closeMessageBtn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_2.addWidget(self.frame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_2 = QtWidgets.QFrame(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.changeImageBtn = QtWidgets.QPushButton(parent=self.frame_2)
        self.changeImageBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.changeImageBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/addImage_white.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.changeImageBtn.setIcon(icon1)
        self.changeImageBtn.setIconSize(QtCore.QSize(100, 100))
        self.changeImageBtn.setObjectName("changeImageBtn")
        self.verticalLayout_3.addWidget(self.changeImageBtn)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(parent=self.widget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
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

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.okBtn.setText(_translate("Dialog", "Ok"))
