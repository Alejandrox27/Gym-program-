from GUI.ui_interface import *
from GUI.py_messageBox import (MessageBox,MessageBox_confirmation,MessageBox_dialog,
                               MessageBox_enrollment,MessageBox_copy, MessageBox_Image)
from GUI.py_toggle import PyToggle
from GUI.Python_Circular_ProgressBar.ui_splash_screen import Ui_SplashScreen

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import os
import re
import sys
import sqlite3
import threading
from datetime import datetime

from markdown import markdown

from PyQt6 import QtWidgets, QtCore, QtGui
import pyperclip

from models.Clients import Clients, MyDelegate
from models.Client import Client

counter = 0
jumper = 0

class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        
        ## ==> SET INITIIAL PROGRESS BAR TO (0)
        self.progressBarValue(0)
        
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        #APPLY AND DROP SHADOW effect
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0,0,0,120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)
        
        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.changeLabelLoadingInfo)
        self.timer.start(400)
        
        self.timer_2 = QtCore.QTimer()
        self.timer_2.timeout.connect(self.progress)
        self.timer_2.start(35)
    
        self.show()

    def changeLabelLoadingInfo(self):
        text = self.ui.labelLoadingInfo.text()
        if text == 'loading...':
            self.ui.labelLoadingInfo.setText('loading')
        elif text == 'loading':
            self.ui.labelLoadingInfo.setText('loading.')
        elif text == 'loading.':
            self.ui.labelLoadingInfo.setText('loading..')
        elif text == 'loading..':
            self.ui.labelLoadingInfo.setText('loading...')
        
    # DEF TO LOANDING 
    def progress(self):
        global counter
        global jumper
        value = counter
        
        htmlText = """<p><span style=" font-size:68pt;">{VALUE}</span><span style=" font-size:58pt; vertical-align:super;">%</span></p>"""
        
        newHtml = htmlText.replace("{VALUE}", str(jumper)) # OR INT(VALUE)
        
        #APPLY NEW PERCENTAGE TEXT
        if (value > jumper):
            self.ui.labelPercentage.setText(newHtml)
            jumper += 3
        
        # SET VALUE TO PROGRESS BAR
        # fix max value error if > than 100
        if value >= 100: value = 1.000
        self.progressBarValue(value)
        
        if counter > 100:
            self.timer.stop()
            self.timer_2.stop()
            
            #SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()
            
            self.close()
        
        counter += 1
        
    #def progressbar value   
    def progressBarValue(self, value):
        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
            border-radius:150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(123, 189, 255, 255));
            }
        """
        
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        #stoop workss of 1.000 to 0.000
        progress = (100 - value) / 100.0
        
        #GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)
        
        # SET values to new stylesheet
        
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
        
        #APPLY STYLESHEET WITH NEW VALUES
        self.ui.circularProgress.setStyleSheet(newStylesheet)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        with open("styles/styles.css", 'r') as file:
            style = file.read()
        
        self.setStyleSheet(style)
        self.setWindowTitle('Gym')
        self.setWindowIcon(QtGui.QIcon('icons/dumbbell.png'))
        
        self.clients = Clients()
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.autosave)
        self.timer.start(420000)
        
        self.timer_2 = QtCore.QTimer(self)
        self.timer_2.timeout.connect(self.clients.entryConfirmation)
        self.timer_2.start(300000)
        
        self.default_icon = self.ui.clientImageBtn.icon()
        self.default_image = self.default_icon.pixmap(100,100)
        
        self.confirmation_ob = False
        
        self.drag_position = None
        
        self.row = None
        self.column = None
        
        self.enrollment = None
        self.file_path = None
        self.file_path_load = None
        self.selectedRoot = None
        
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.inicializateGui()
        
        self.show()
    
    def inicializateGui(self):
        self.ui.closeBtn.clicked.connect(lambda: self.close())
        self.ui.minimizeBtn.clicked.connect(lambda: self.showMinimized())
        self.ui.restoreBtn.clicked.connect(lambda: self.restore_or_maximize_window())
        
        self.ui.menuBtn.clicked.connect(lambda: self.slideLeftMenu())
        
        self.ui.homeBtn.clicked.connect(lambda: self.changePage())
        self.ui.loadDataBtn.clicked.connect(lambda: self.changePage())
        self.ui.saveDataBtn.clicked.connect(lambda: self.changePage())
        
        self.ui.helpBtn.clicked.connect(lambda: self.moreMenu())
        self.ui.settingsBtn.clicked.connect(lambda: self.moreMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.moreMenu())
        
        self.ui.closeMoreMenuBtn.clicked.connect(lambda: self.closeMoreMenu())
        
        self.ui.moreBtn.clicked.connect(lambda: self.rightMenu())
        self.ui.addClientBtn.clicked.connect(lambda: self.rightMenu())
        
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.closeRightMenu())
        
        self.ui.searchClientBtn.clicked.connect(lambda: self.search())
        
        self.ui.deleteClientBtn.clicked.connect(lambda: self.deleteClient())
        self.ui.tableWidget.itemClicked.connect(self.onItemClicked)
        self.ui.refreshBtn.clicked.connect(lambda: self.refresh())
        self.ui.saveDataView.clicked.connect(self.dataView)
        
        self.ui.addClientBtn_2.clicked.connect(lambda: self.addClient())
        
        self.ui.clientImageBtn.clicked.connect(lambda: self.addImage())
        
        self.ui.githubBtn.clicked.connect(lambda: self.goToWebpage())
        self.ui.instagramBtn.clicked.connect(lambda: self.goToWebpage())
        self.ui.facebookBtn.clicked.connect(lambda: self.goToWebpage())
        self.ui.gmailBtn.clicked.connect(lambda: self.goToWebpage())
        
        self.ui.sendBtn.clicked.connect(lambda: self.verifyCredentials())
        
        self.setTableWidgetWidth()
        delegate = MyDelegate(self.ui.tableWidget)
        self.ui.tableWidget.setItemDelegate(delegate)
        self.ui.searchClientTxt.setValidator(QtGui.QIntValidator(1,99999999,self))
        self.ui.insertIdTxt.setValidator(QtGui.QIntValidator(1,99999999,self))
        self.ui.tableWidget.cellChanged.connect(self.onCellChanged)
        self.ui.tableWidget.cellDoubleClicked.connect(self.doubleClickedTable)
        
        self.toggle = PyToggle()
        self.ui.horizontalLayout_18.addWidget(self.toggle)
        
        self.ui.spinBox.valueChanged.connect(lambda: self.changeAutosaveTime())
        
        self.saveDataView()
        self.loadDataView()
    
    def doubleClickedTable(self, row, column):
        self.row = row
        self.column = column
        
        if self.column == 3:
            self.message = MessageBox_enrollment()
            self.message.ui.okBtn.clicked.connect(self.TypeEnrollment)
            self.message.exec()
            
        if self.column == 6:
            self.image = False
            self.message = MessageBox_Image()
            self.message.ui.changeImageBtn.clicked.connect(self.changeImage)
            self.message.ui.okBtn.clicked.connect(self.changeClientImage)
            defaultIcon = self.message.ui.changeImageBtn.icon()
            self.defaultIcon = defaultIcon.pixmap(100,100)
            self.message.exec()
            
        content = self.ui.tableWidget.item(self.row, self.column)
        self.content = content.text()
        
    def changeImage(self):
        """
        This function search for an image file with getOpenFileName,
        if the new image is different to the default image from 
        'self.message.ui.changeImageBtn' then it sets the icon to the button.
        """
        self.archive, ok = QtWidgets.QFileDialog.getOpenFileName(self, 'Seleccionar archivo de imagen...', 'C:\\','Archivos de imágenes (*.jpg *.png)')
        
        if ok:
            icon = QtGui.QIcon(self.archive)
            icon_p = icon.pixmap(100,100)
            if self.defaultIcon.toImage() == icon_p.toImage():
                return
            
            self.message.ui.changeImageBtn.setIcon(icon)
            self.image = True
            
    def changeClientImage(self):
        """
        this function changes the image from the table and adds
        the new image to the object Client.photo
        """
        if self.image == True:
            icon = self.message.ui.changeImageBtn.icon()
            
            id = self.ui.tableWidget.item(self.row, 0)
            id = id.text()
            
            client = self.clients.binary_search(self.clients.clients, id)
            client.photo = self.clients.convert_to_binary(self.archive)
            
            photo_1 = QtWidgets.QTableWidgetItem()
            photo_1.setIcon(icon)
            self.ui.tableWidget.setIconSize(QtCore.QSize(100,100))
            self.ui.tableWidget.setItem(self.row, 6, photo_1)
            self.ui.tableWidget.item(self.row, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            
    def TypeEnrollment(self):
        """
        this function change the type enrollment and calculates
        the expiration date and the entry permit. places it in the tableWidget and 
        in the object Client
        """
        self.enrollment = self.message.ui.enrollmentGroupMessage.checkedButton()
        if self.enrollment:
            self.enrollment = self.enrollment.text()
            
            id = self.ui.tableWidget.item(self.row, 0)
            id = id.text()
            
            client = self.clients.binary_search(self.clients.clients, id)
            client.enrollment = self.enrollment
            
            client.expiration_date = self.clients.calculateExpirationDate(self.enrollment)
            client.entry = True
            
            self.ui.tableWidget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(self.enrollment)))
            self.ui.tableWidget.item(self.row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str(client.expiration_date)))
            self.ui.tableWidget.item(self.row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str(client.entry)))
            self.ui.tableWidget.item(self.row, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
    def onCellChanged(self, row, column):
        """
        this function changes an item from the tableWidget.
        """
        if self.column == 6 and column == 6:
            return
        
        if not self.row is None and not self.column is None and row == self.row and self.column == column:
            item = self.ui.tableWidget.item(row, column)
            if item is not None:
                item = item.text().strip()
                
                if len(item) == 0 or item.isalpha() is False:
                    self.ui.tableWidget.setItem(self.row, self.column, QtWidgets.QTableWidgetItem(str(self.content)))
                    self.ui.tableWidget.item(self.row, self.column).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.message = MessageBox(message = 'invalid value,\nuse only alphabetic characters')
                    self.message.exec()
                    return
                
                id = self.ui.tableWidget.item(self.row, 0)
                id = id.text()
                
                client = self.clients.binary_search(self.clients.clients, id)
                
                if not client is None:
                    if column == 1:
                        name = self.ui.tableWidget.item(self.row, 1)
                        client.name = name.text()
                    elif column == 2:
                        objective = self.ui.tableWidget.item(self.row, 2)
                        client.objective = objective.text()
                    elif column == 3:
                        enrollment = self.ui.tableWidget.item(self.row, 3)
                        client.enrollment = enrollment.text()
                        
    def changePage(self):
        """
        this function changes the page from the principal stackedWidget.
        """
        button = self.sender()
        button = button.text().lower()
        
        if button == 'home':
            self.ui.stackedWidget_3.setCurrentIndex(0)
            self.ui.settingsBtn.setStyleSheet('background-color:  transparent;')
            self.ui.infoBtn.setStyleSheet('background-color:  transparent;')
            self.ui.helpBtn.setStyleSheet('background-color:  transparent;')
            self.ui.homeBtn.setStyleSheet('background-color:  #1f232a;')
            self.ui.loadDataBtn.setStyleSheet('background-color:  transparent;')
            self.ui.saveDataBtn.setStyleSheet('background-color:  transparent;')
        elif button == 'load data':
            self.ui.stackedWidget_3.setCurrentIndex(1)
            self.ui.settingsBtn.setStyleSheet('background-color:  transparent;')
            self.ui.infoBtn.setStyleSheet('background-color:  transparent;')
            self.ui.helpBtn.setStyleSheet('background-color:  transparent;')
            self.ui.homeBtn.setStyleSheet('background-color:  transparent;')
            self.ui.loadDataBtn.setStyleSheet('background-color:  #1f232a;')
            self.ui.saveDataBtn.setStyleSheet('background-color:  transparent;')
        elif button == 'save data':
            self.ui.stackedWidget_3.setCurrentIndex(2)
            self.ui.settingsBtn.setStyleSheet('background-color:  transparent;')
            self.ui.infoBtn.setStyleSheet('background-color:  transparent;')
            self.ui.helpBtn.setStyleSheet('background-color:  transparent;')
            self.ui.homeBtn.setStyleSheet('background-color:  transparent;')
            self.ui.loadDataBtn.setStyleSheet('background-color:  transparent;')
            self.ui.saveDataBtn.setStyleSheet('background-color:  #1f232a;')
        
        
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
        
        
    def restore_or_maximize_window(self):
        """
        This function maximizes or restores the window.
        """
        if self.isMaximized():
            self.showNormal()
            self.ui.restoreBtn.setIcon(QtGui.QIcon(u"icons/square.svg"))
            self.setTableWidgetWidth()
        else:
            self.showMaximized()
            self.ui.restoreBtn.setIcon(QtGui.QIcon(u"icons/copy.svg"))
            self.setTableWidgetWidth()
        
    def slideLeftMenu(self): 
        """
        this function opens the left menu with an animation
        """
        width = self.ui.leftMenuContainer.width()
        
        if width == 50:
            newWidth = 123
            
        else:
            newWidth = 50
            
        self.animation = QtCore.QPropertyAnimation(self.ui.leftMenuContainer, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
    
    def moreMenu(self):
        """
        This function opens the menu 'more' with an animation
        """
        width = self.ui.centerMenuContainer.width()
        button = self.sender()
        
        if width == 0:
            newWidth = 200
            
            self.animation = QtCore.QPropertyAnimation(self.ui.centerMenuContainer, b"maximumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(newWidth)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()
            
        if button.text().lower() == 'settings':
            self.ui.stackedWidget.setCurrentIndex(2)
            self.ui.settingsBtn.setStyleSheet('background-color:  #1f232a;')
            self.ui.infoBtn.setStyleSheet('background-color:  transparent;')
            self.ui.helpBtn.setStyleSheet('background-color:  transparent;')
            self.ui.homeBtn.setStyleSheet('background-color:  transparent;')
            self.ui.loadDataBtn.setStyleSheet('background-color:  transparent;')
            self.ui.saveDataBtn.setStyleSheet('background-color:  transparent;')
        elif button.text().lower() == 'information':
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.settingsBtn.setStyleSheet('background-color:  transparent;')
            self.ui.infoBtn.setStyleSheet('background-color:  #1f232a;')
            self.ui.helpBtn.setStyleSheet('background-color:  transparent;')
            self.ui.homeBtn.setStyleSheet('background-color:  transparent;')
            self.ui.loadDataBtn.setStyleSheet('background-color:  transparent;')
            self.ui.saveDataBtn.setStyleSheet('background-color:  transparent;')
        elif button.text().lower() == 'help':
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.settingsBtn.setStyleSheet('background-color:  transparent;')
            self.ui.infoBtn.setStyleSheet('background-color:  transparent;')
            self.ui.helpBtn.setStyleSheet('background-color:  #1f232a;')
            self.ui.homeBtn.setStyleSheet('background-color:  transparent;')
            self.ui.loadDataBtn.setStyleSheet('background-color:  transparent;')
            self.ui.saveDataBtn.setStyleSheet('background-color:  transparent;')
        
    def closeMoreMenu(self):
        """This function closes the menu 'more'"""
        
        width = self.ui.centerMenuContainer.width()
        self.animation = QtCore.QPropertyAnimation(self.ui.centerMenuContainer, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
        
    def rightMenu(self):
        """
        this function opens the right menu with an animation
        """
        button = self.sender()
        width = self.ui.rightMenuContainer.width()
        
        if button.objectName() == 'moreBtn':
            self.animation = QtCore.QPropertyAnimation(self.ui.rightMenuContainer, b"maximumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(200)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()
            
            self.animation = QtCore.QPropertyAnimation(self.ui.rightMenuContainer, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(200)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()
        elif button.objectName() == 'addClientBtn':
            self.animation = QtCore.QPropertyAnimation(self.ui.rightMenuContainer, b"maximumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(250)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()
            
            self.animation = QtCore.QPropertyAnimation(self.ui.rightMenuContainer, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(250)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
            self.animation.start()
        
        if button.objectName() == 'moreBtn':
            self.ui.stackedWidget_2.setCurrentIndex(0)
        elif button.objectName() == 'addClientBtn':
            self.ui.stackedWidget_2.setCurrentIndex(1)
        
    def closeRightMenu(self):
        """
        this function closes the right menu
        """
        width = self.ui.rightMenuContainer.width()
        self.animation = QtCore.QPropertyAnimation(self.ui.rightMenuContainer, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
        
        self.ui.rightMenuContainer.setMaximumWidth(0)
        
        self.animation = QtCore.QPropertyAnimation(self.ui.rightMenuContainer, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()
        
    def setTableWidgetWidth(self):
        """
        this fuction adjusts the size of the tableWidget when the 
        window is maximized or not.
        """
        if self.isMaximized():
            self.ui.tableWidget.setColumnWidth(0,150)
            self.ui.tableWidget.setColumnWidth(1,190)
            self.ui.tableWidget.setColumnWidth(2,170)
            self.ui.tableWidget.setColumnWidth(3,150)
            self.ui.tableWidget.setColumnWidth(4,150)
            self.ui.tableWidget.setColumnWidth(5,150)
            self.ui.tableWidget.setColumnWidth(6,180)
        
        else:
            self.ui.tableWidget.setColumnWidth(0,120)
            self.ui.tableWidget.setColumnWidth(1,160)
            self.ui.tableWidget.setColumnWidth(2,150)
            self.ui.tableWidget.setColumnWidth(3,150)
            self.ui.tableWidget.setColumnWidth(4,120)
            self.ui.tableWidget.setColumnWidth(5,70)
            self.ui.tableWidget.setColumnWidth(6,110)
    
    def search(self):
        """
        this function search for a client in the tableWidget and
        shows only that client
        """
        id = self.ui.searchClientTxt.text()
        
        if id != '':
        
            for row in range(self.ui.tableWidget.rowCount()):
                id_item = self.ui.tableWidget.item(row, 0)
                if id_item and int(id_item.text()) == int(id):
                    self.ui.tableWidget.showRow(row)
                else:
                    self.ui.tableWidget.hideRow(row)
        else:
            self.showContentsTable()
    
    def showContentsTable(self):
        """
        this function shows all the items from the QTableWidget,
        this function happens when there is nothing in the 'search' line edit
        """
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.showRow(row)

    def refresh(self):
        """
        this function clears the tableWidget and adds all the clients from the list
        self.clients.clients
        """
        self.clearTable()
        for client in self.clients.clients:
            photo = self.clients.convert_binary_to_image(client.photo)
            self.addClientTable(client.id, client.name, client.objective, client.enrollment, client.expiration_date, client.entry, photo)
            
            
    def deleteDatabase(self):
        """
        this function deletes a database when the user clicks a 
        database and presses the button delete
        """
        if self.file_path != None and len(self.file_path):
            try:
                self.message = MessageBox_confirmation(message = markdown(f'Do you want to delete the database:\n\n**{self.file_path}**?'),
                                                       icon = 'icons/database_white.png')
                self.message.ui.yesBtn.clicked.connect(self.confirmation)
                self.message.ui.noBtn.clicked.connect(self.confirmation)
                self.message.exec()
                
                if self.confirmation_ob is True:
                    os.remove(self.file_path)
            except OSError as e:
                self.message = MessageBox(message = markdown(f'File could not be deleted {self.file_path}\n\nError: **{e}**'))
                self.message.exec()
        
    def dataView(self, index: QtCore.QModelIndex):
        """
        this function get the path of the chosen element from the save view
        """
        file_info = self.model.fileInfo(index)
        self.file_path = file_info.filePath()
        
    def dataViewLoad(self, index: QtCore.QModelIndex):
        """
        this function get the path of the chosen element from the load view
        """
        file_info = self.model_load.fileInfo(index)
        self.file_path_load = file_info.filePath()
    
    def onItemClicked(self, item):
        """
        this function gets the selected row when the user 
        clicks on an item in the tableWidget
        """
        self.selectedRow = item.row()
        
    def deleteClient(self):
        """
        this function asks the user if the user wants to 
        eliminate a client in a selected row
        """
        if hasattr(self, 'selectedRow'):
                item = self.ui.tableWidget.item(self.selectedRow, 0)
                if item:
                    extracted_text = int(item.text())
                    client = self.clients.binary_search(self.clients.clients, extracted_text)
                    
                    pixmap = self.clients.convert_binary_to_image(client.photo)
                    self.message = MessageBox_confirmation(icon = pixmap, 
                                                           message = markdown(f"Eliminate the client **{client.name}**\n"
                                                                              f"\nwith id **{client.id}**?"))
                    self.message.ui.yesBtn.clicked.connect(self.confirmation)
                    self.message.ui.noBtn.clicked.connect(self.confirmation)
                    self.message.exec()
                        
                    if not self.confirmation_ob is True:
                        return
                    
                    self.clients.deleteClient(client)
                        
        
        if hasattr(self, 'selectedRow'):
            self.ui.tableWidget.removeRow(self.selectedRow)
            
    def confirmation(self):
        """
        this function is a confirmation for the 'MessageBox_confirmation'
        it confirms if the buttton selected in the MessageBox is yes (True)
        or no (False)
        """
        button = self.sender()
        if button.text().lower() == 'yes':
            self.confirmation_ob = True
        else:
            self.confirmation_ob = False
            
    def addClient(self):
        """
        this function asks the user for the specifications of a client 
        and saves it in the list self.clients.clients by means of an object 'Client'.
        """
        icon = self.ui.clientImageBtn.icon()
        new_image = icon.pixmap(100,100)
        
        id = self.ui.insertIdTxt.text()
        name = self.ui.insertNameTxt.text()
        objective = self.ui.insertObjectiveTxt.text()
        enrollment = self.ui.enrollmentGroup.checkedButton()
        
        if new_image.toImage() == self.default_image.toImage():
            self.message = MessageBox(message = 'Add an image')
            self.message.exec()
            return
        
        if len(id)==0:
            self.message = MessageBox(message = 'Add an ID')
            self.message.exec()
            return
        
        client = self.clients.binary_search(self.clients.clients , id)
        
        if len(name) == 0:
            self.message = MessageBox(message = 'Add a name')
            self.message.exec()
            return
        
        if len(objective)==0:
            self.message = MessageBox(message = 'Add an objective')
            self.message.exec()
            return
        
        if enrollment is None:
            self.message = MessageBox(message = 'Choose an enrollment')
            self.message.exec()
            return
        
        enrollment = enrollment.text()
        expiration_date = self.clients.calculateExpirationDate(enrollment)
        
        photo = self.clients.convert_to_binary(self.archive)
        
        if client:
            image = self.clients.convert_binary_to_image(client.photo)
            self.message = MessageBox_confirmation(message = 'That clients already exists,\n'
                                               '¿do you want to change the information?',
                                               icon = image)
            self.message.ui.yesBtn.clicked.connect(self.confirmation)
            self.message.ui.noBtn.clicked.connect(self.confirmation)
            self.message.exec()
            
            if not self.confirmation_ob is True:
                return
            else:
                client.id = id
                client.name = name
                client.objective = objective
                client.enrollment = enrollment
                client.expiration_date = expiration_date
                client.entry = True
                client.photo = photo
                
                for row in range(self.ui.tableWidget.rowCount()):
                    id_item = self.ui.tableWidget.item(row, 0)
                    if id_item and int(id_item.text()) == int(id):
                        self.ui.tableWidget.removeRow(row)
                        
                        self.addClientTable(id, name, objective, enrollment, expiration_date, True, new_image)
                return
            
        newClient = Client(int(id), name, objective, enrollment, expiration_date, True, photo)
        self.clients.addClient(newClient)
        
        self.addClientTable(id, name, objective, enrollment, expiration_date, True, new_image)
            
        self.ui.clientImageBtn.setIcon(self.default_icon)
        self.ui.insertIdTxt.setText('')
        self.ui.insertNameTxt.setText('')
        self.ui.insertObjectiveTxt.setText('')
        
    def addClientTable(self, id, name, objective, enrollment, expiration_date, entry, photo):
        """
        this function adds a client in the tableWidget
        """
        rows = int(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.insertRow(rows)
        
        photo_1 = QtWidgets.QTableWidgetItem()
        photo_1.setIcon(QtGui.QIcon(photo))
        self.ui.tableWidget.setIconSize(QtCore.QSize(100,100))
            
        self.ui.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(id)))
        self.ui.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(str(name)))
        self.ui.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(objective)))
        self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(enrollment)))
        self.ui.tableWidget.setItem(rows, 4, QtWidgets.QTableWidgetItem(str(expiration_date)))
        self.ui.tableWidget.setItem(rows, 5, QtWidgets.QTableWidgetItem(str(entry)))
        self.ui.tableWidget.setItem(rows, 6, photo_1)
        
        self.ui.tableWidget.item(rows, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.item(rows, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.item(rows, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.item(rows, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.item(rows, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.item(rows, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.ui.tableWidget.resizeRowsToContents()
        
    def clearTable(self):
        """
        this fuction clears the tableWidget
        """
        self.ui.tableWidget.setRowCount(0)
    
    def addImage(self):
        """
        this function adds an image to the self.ui.clientImageBtn 
        and saves the root of the image in self.archive
        """
        self.archive, ok = QtWidgets.QFileDialog.getOpenFileName(self, 'Seleccionar archivo de imagen...', 'C:\\','Archivos de imágenes (*.jpg *.png)')
        
        if ok:
            icon = QtGui.QIcon(self.archive)
            self.ui.clientImageBtn.setIcon(icon)
            
    def saveDataView(self):
        """
        this function sets the root path to the self.ui.saveDataView
        """
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath('database')
        self.ui.saveDataView.setModel(self.model)
        self.ui.saveDataView.setRootIndex(self.model.index(self.model.rootPath()))
        
        self.ui.saveDataView.setColumnWidth(0,200)
        self.ui.saveDataView.setColumnWidth(1,150)
        self.ui.saveDataView.setColumnWidth(2,300)
        self.ui.saveDataView.setColumnWidth(3,300)
        
        self.ui.saveDataView.doubleClicked.connect(self.selectedDatabase)
        self.ui.newDataBtn.clicked.connect(self.newDatabase)
        self.ui.newDataBtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.ui.deleteDataBtn.clicked.connect(self.deleteDatabase)
        self.ui.deleteDataBtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.ui.saveDataView.clicked.connect(self.dataView)
    
    def loadDataView(self):
        """
        this function sets the root path to the self.ui.loadDataView
        """
        self.model_load = QtGui.QFileSystemModel()
        self.model_load.setRootPath('database')
        self.ui.loadDataView.setModel(self.model)
        self.ui.loadDataView.setRootIndex(self.model.index(self.model.rootPath()))
        
        self.ui.loadDataView.setColumnWidth(0,200)
        self.ui.loadDataView.setColumnWidth(1,150)
        self.ui.loadDataView.setColumnWidth(2,300)
        self.ui.loadDataView.setColumnWidth(3,300)
        
        self.ui.loadDataView.doubleClicked.connect(self.loadDatabase)
        self.ui.loadDatabaseBtn.clicked.connect(self.loadDatabase)
        self.ui.loadDatabaseBtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.ui.loadDataView.clicked.connect(self.dataViewLoad)
    
    def loadDatabase(self, index: QtCore.QModelIndex):
        """
        this function gets all the clients from a database and 
        adds them into the tableWidget and into the list self.clients.clients
        """
        if self.file_path_load is None:
            self.message = MessageBox()
            self.message.ui.messageLbl.setText('Choose a database to load')
            self.message.exec()
            return

        self.message = MessageBox_confirmation(message = markdown("Want to load the data of the database:\n"
                                            f"\n**{self.file_path_load}**?"),
                                               icon = 'icons/load_white.png')
        self.message.ui.yesBtn.clicked.connect(self.confirmation)
        self.message.ui.noBtn.clicked.connect(self.confirmation)
        self.message.exec()
        
        if self.confirmation_ob is True:
            try:
                conection = sqlite3.connect(self.file_path_load)
                cursor = conection.cursor()
                all_clients = "SELECT * FROM clients"
                cursor.execute(all_clients)
                all = cursor.fetchall()
                
                self.clients.clearClients()
                self.clearTable()
                
                format_date = "%Y-%m-%d %H:%M:%S.%f"
                
                for client in all:
                    id = int(client[0])
                    name = str(client[1])
                    objective = str(client[2])
                    enrollment = str(client[3])
                    expiration_date = datetime.strptime(client[4], format_date)
                    photo = client[6]
                    
                    entry = self.clients.entryConfirmationDate(expiration_date)
                    
                    client = Client(id, name, objective, enrollment, expiration_date, entry, photo)
                    self.clients.addClient(client)
                    
                    photo = self.clients.convert_binary_to_image(photo)
                    
                    self.addClientTable(id, name, objective, enrollment, expiration_date, entry, photo)
                     
                cursor.close()
                conection.commit()
                return True
            
            except sqlite3.Error as e:
                message = MessageBox()
                message.setWindowTitle('Error')
                message.ui.messageLbl.setText('Has ocurred an error, try again.\n'
                                                f'error: {e}')
                message.exec()
            
            finally:
                conection.close()
        
    def selectedDatabase(self, index: QtCore.QModelIndex):
        """
        this function gets the Root from the self.model from the saveDataView
        """
        self.selectedRoot = self.model.filePath(index)
        
        self.saveData()
        
    def newDatabase(self):
        """
        This function asks the user if the user wants to create a new database
        """
        self.name = None
        patron = r'[a-zA-Z]+'
        self.regex = re.compile(patron)
        self.message = MessageBox_dialog(message = 'Insert a name for your database')
        self.message.ui.okBtn.clicked.connect(self.insertName)
        self.message.ui.closeMessageBtn.clicked.connect(self.insertName)
        self.message.exec()
    
    def insertName(self):
        """
        this fuction asks the name for the new database to save.
        """
        button = self.sender()
        button = button.text().lower()
        
        if button == 'ok':
            name = self.message.ui.writeTxt.text()
            name = name.strip()
            if len(name) == 0:
                message = MessageBox(message = 'Insert a name for your database')
                message.setWindowTitle('Save')
                message.exec()
                return
            
            if self.regex.match(name):
                self.selectedRoot = f'database/{name}.db'
                
            else:
                message = MessageBox(message = 'Insert a valid name for your database')
                message.setWindowTitle('Save')
                message.exec()
                return
                
            thread = threading.Thread(target=self.saveInDatabase)
            thread.start()
            update_label_timer = QtCore.QTimer(self)
            update_label_timer.singleShot(10000, lambda: self.ui.autosaveLbl.setText(''))

            self.ui.autosaveLbl.setText(f'correct save - {self.selectedRoot}')
            
    def saveData(self):
        """
        this function asks the use if the user wants to 
        save the data in a selected database
        """
        self.message = MessageBox_confirmation(message = markdown("Want to save the data in this database:\n"
                                            f"\n**{self.selectedRoot}**?"),
                                               icon = 'icons/save.png')
        self.message.ui.yesBtn.clicked.connect(self.confirmation)
        self.message.ui.noBtn.clicked.connect(self.confirmation)
        self.message.exec()
        
        if self.confirmation_ob is True:
            thread = threading.Thread(target=self.saveDataInTable)
            thread.start()
            
            update_label_timer = QtCore.QTimer(self)
            update_label_timer.singleShot(10000, lambda: self.ui.autosaveLbl.setText(''))

            self.ui.autosaveLbl.setText(f'correct save - {self.selectedRoot}')
    
    def saveDataInTable(self):
        """
        This function saves the data from the list self.clients.clients into a database
        """
        if self.selectedRoot != None:
            try:
                conection = sqlite3.connect(self.selectedRoot)
                cursor = conection.cursor()
                
                cursor.execute('BEGIN')
                
                save = "INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)"
                client = "SELECT * FROM clients WHERE ID = ?"
                update = """UPDATE clients SET name = ?, objective = ?, enrollment = ?, expirationDate = ?,
                            entry = ?, photo = ? WHERE ID = ?"""
                all = "SELECT * FROM clients"
                delete = """DELETE From clients WHERE ID = ?"""
                
                id_clients = [c.id for c in self.clients.clients]
                
                for e in self.clients.clients:
                    id = int(e.id)
                    name = str(e.name)
                    objective = str(e.objective)
                    enrollment = str(e.enrollment)
                    expiration_date = str(e.expiration_date)
                    entry = str(e.entry)
                    photo = e.photo
                    
                    cursor.execute(client, (id,))
                    
                    person = cursor.fetchall()
                    
                    if len(person):
                        if person[0][1] != name or person[0][2] != objective or person[0][3] != enrollment or person[0][6] != photo:
                            cursor.execute(update, (name, objective, enrollment, expiration_date, entry, photo, id))
                        
                        continue
                    elif len(person) == 0:
                        cursor.execute(save, (id, name, objective, enrollment, expiration_date, entry, photo))
                        continue
                
                cursor.execute(all)
                    
                clients = cursor.fetchall()
                    
                for c in clients:
                    id = int(c[0])
                    if id not in id_clients:
                        cursor.execute(delete, (id,))
                        continue
                        
                conection.commit()
                return True
            
            except sqlite3.Error as e:
                message = MessageBox(message = 'Has ocurred an error, try again.\n'
                                                f'error: {e}')
                message.setWindowTitle('Error')
                message.exec()
            
            finally:
                conection.close()
        
    def saveInDatabase(self):
        """
        This function creates a new database and saves the data from the list
        self.clients.clients in it.
        """
        if not os.path.exists(self.selectedRoot):
            try:
                conection = sqlite3.connect(self.selectedRoot)
                cursor = conection.cursor()
                
                sql_clients = '''CREATE TABLE clients (
                    ID INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    enrollment TEXT,
                    expirationDate TEXT,
                    entry TEXT,
                    photo BLOB NOT NULL
                )'''
                cursor.execute(sql_clients)

                client_data = [(int(e.id), str(e.name), str(e.objective), str(e.enrollment),
                                str(e.expiration_date), str(e.entry), e.photo) for e in self.clients.clients]

                save = "INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)"
                cursor.executemany(save, client_data)

                conection.commit()
                return True
                        
            except sqlite3.Error as e:
                message = MessageBox(message = 'Has ocurred an error, try again.\n'
                                                f'error: {e}')
                message.setWindowTitle('Error')
                message.exec()
            
            finally:
                conection.close()
        else:
            self.saveData()
            
    def goToWebpage(self):
        """
        this function redirect the user to my social media
        """
        button = self.sender()
        
        if button.objectName() == "githubBtn":
            url = QtCore.QUrl('https://github.com/Alejandrox27')
            QtGui.QDesktopServices.openUrl(url)
        elif button.objectName() == "instagramBtn":
            url = QtCore.QUrl('https://www.instagram.com/_alejandro_829/')
            QtGui.QDesktopServices.openUrl(url)
        elif button.objectName() == "facebookBtn":
            url = QtCore.QUrl('https://www.facebook.com/didier.mejia.50746/')
            QtGui.QDesktopServices.openUrl(url)
        elif button.objectName() == "gmailBtn":
            pyperclip.copy(button.text())
            pos = self.ui.gmailBtn.mapToGlobal(self.ui.gmailBtn.rect().topLeft())
            
            self.message = MessageBox_copy()
            self.message.ui.messageLbl.setText("mail copied to clipboard")
            self.message.move(int(pos.x()) - 47, int(pos.y()) + 10)
            self.message.show()
        
    def verifyCredentials(self):
        """
        this function validates the user's credentials
        """
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.email = self.ui.emailTxt.text()
        self.message = self.ui.questionTxt.toPlainText()
        
        if len(self.email) == 0:
            pos = self.ui.emailTxt.mapToGlobal(self.ui.emailTxt.rect().topLeft())
            self.message = MessageBox_copy()
            self.message.ui.messageLbl.setText("Write your email")
            self.message.move(int(pos.x()) - 53, int(pos.y()) + 14)
            self.message.show()
            return
        
        if not re.fullmatch(regex, self.email):
            pos = self.ui.emailTxt.mapToGlobal(self.ui.emailTxt.rect().topLeft())
            self.message = MessageBox_copy()
            self.message.ui.messageLbl.setText("Invalid email")
            self.message.move(int(pos.x()) - 53, int(pos.y()) + 14)
            self.message.show()
            return
        
        if len(self.ui.subjectTxt.text()) == 0:
            pos = self.ui.subjectTxt.mapToGlobal(self.ui.subjectTxt.rect().topLeft())
            self.message = MessageBox_copy()
            self.message.ui.messageLbl.setText("Write a subject")
            self.message.move(int(pos.x()) - 53, int(pos.y()) + 14)
            self.message.show()
            return
        
        if len(self.message) == 0:
            pos = self.ui.questionTxt.mapToGlobal(self.ui.questionTxt.rect().topLeft())
            self.message = MessageBox_copy()
            self.message.ui.messageLbl.setText("Write a message")
            self.message.move(int(pos.x()) - 53, int(pos.y()) + 150)
            self.message.show()
            return
        
        thread = threading.Thread(target=self.sendEmail)
        thread.start()
        
        
        self.ui.questionTxt.setPlainText('')
        self.ui.emailTxt.setText('')
        self.ui.subjectTxt.setText('')
        
        self.message = MessageBox(message = 'message sent successfully', icon = 'icons/letter_white.png')
        self.message.exec()
        
    def sendEmail(self):
        """
        this function sends a mail to my gmail if you want to leave a review or a question
        """
        msg = MIMEMultipart()
        msg['From'] = "alej.mejia89@gmail.com"
        msg['To'] = "alej.mejia89@gmail.com"
        msg['Subject'] = self.ui.subjectTxt.text()
        
        tMessage = f'The user {self.email} has sent the next message:\n\n{self.message}'
        
        email = MIMEText(tMessage,"plain")
        
        msg.attach(email)
        
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login("alej.mejia89@gmail.com", 'aphlqyvuxoxekgkh')
        
        mailServer.sendmail("alej.mejia89@gmail.com", "alej.mejia89@gmail.com",msg.as_string())
        
        mailServer.close()
        
    def autosave(self):
        """
        this function autosaves the data into a selected database 
        if the toggle is checked
        """
        if self.selectedRoot != None and self.toggle.isChecked() == True:
            thread = threading.Thread(target=self.saveDataInTable)
            thread.start()
            update_label_timer = QtCore.QTimer(self)
            update_label_timer.singleShot(10000, lambda: self.ui.autosaveLbl.setText(''))

            self.ui.autosaveLbl.setText(f'correct autosave - {self.selectedRoot}')
            
    def changeAutosaveTime(self):
        """
        this function changes the time between autosaves
        """
        value = self.ui.spinBox.value()
        
        self.timer.stop()
        time = (value * 300000) / 5
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.autosave)
        self.timer.start(int(time))
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())
