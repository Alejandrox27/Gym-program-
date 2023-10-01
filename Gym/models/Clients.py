import datetime

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QItemDelegate, QLineEdit

class Clients():
    def __init__(self):
        self.clients = []
        self.image_cache = {}

    def addClient(self, client):
        """
        This function adds a client from the class 'Client'
        and adds it into a list 'self.clients' where there will
        be all the clients.
        
        Parameters:
        client(Client): the object 'Client' that will be add into
                the list self.clients.
        """
        self.clients.append(client)
        self.clients = sorted(self.clients, key=lambda x: x.id)
        
    def clearClients(self):
        """
        This function clears the list self.clients
        """
        self.clients.clear()
    
    def deleteClient(self, client):
        """
        this functions removes a clients from the list
        self.clients.
        
        Parameters:
        client(Client): object 'Clients' that will be removed
        """
        self.clients.remove(client)

    def entryConfirmation(self):
        """
        this function searches for all expiration dates for the customer
        and if the date is equal to or less than the current date then
        the entry permit will be False
        """
        for client in self.clients:
            if datetime.datetime.now() >= client.expiration_date:
                client.entry = False
                 
    def entryConfirmationDate(self, expiration_date):
        """
        this function receives an expiration_date and compares it
        whit the actual date
        
        Parameters:
        expiration_date(datetime): client expiration date
        
        Returns:
        True: if the expiration_date is higher that the actual date.
        False: if the expiration_date is equal to or less than than the actual date.
        """
        if datetime.datetime.now() >= expiration_date:
            return False
        else:
            return True

    def convert_binary_to_image(self, binary_data):
        """
        This function convert a binary image to a QIcon object

        Parameters:
        binary_data (bytes): binary data from the image
        width (int): desired QIcon width
        height (int): desired QIcon height

        Returns:
        pixmap: The pixmap loaded from the binary data
        None: if there was an error during the convertion.
        """
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(binary_data)
            
            return pixmap
        except:
            return None
                
    def convert_to_binary(self,photo):
        """
        this function converts a image into a binary data
        
        Parameters:
        photo = image root to the image
        
        Returns:
        blob = binary image.
        None = If there was an error during the convertion.
        """
        try:
            with open(photo, 'rb') as f:
                blob = f.read()
                
            return blob
        except:
            return None
        
    def binary_search(self, list, id):
        """
        this function search throught the list 'self.clients' 
        with a binary search to make it faster.
        
        Parameters:
        list: the list to be searched for
        id: the id of a client to search for
        
        Returns:
        list[middle]: client found
        None: Mo client found
        """
        left = 0
        right = len(list) - 1
        
        while left <= right:
            middle = (left + right) // 2
            
            if int(list[middle].id) == int(id):
                return list[middle]
            elif int(list[middle].id) < int(id):
                left = middle + 1
            else:
                right = middle -1
        
        return None 
    
    def calculateExpirationDate(self, enrollment):
        """
        this function calculates que expiration date of a client,
        if enrollment is Monthly then it adds 30 days to the current date
        if enrollment is Diary then it adds 1 days to the current date
        if enrollment is Yearly then it adds 365 days to the current date
        
        Returns:
        final_date: the calculated date
        """
        if enrollment == 'Monthly':
            actual_date = datetime.datetime.now()

            final_date = actual_date + datetime.timedelta(days=30)
        
        elif enrollment == "Yearly":
            actual_date = datetime.datetime.now()

            final_date = actual_date + datetime.timedelta(days=365)
            
        elif enrollment == 'Diary':
            actual_date = datetime.datetime.now()

            final_date = actual_date + datetime.timedelta(days=1)
            
        return final_date
    
class MyDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        """
        locks the columns 0,3,4,5 and 6 of a tableWidget
        """
        column = index.column()
        
        if column == 0 or column == 3 or column == 4 or column == 5 or column == 6:
            return None
        else:
            return QLineEdit(parent)