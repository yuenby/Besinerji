import sys
import os
import sqlite3
import time
from turtle import delay
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel, QPushButton, QComboBox

general_path = os.path.abspath(os.path.dirname(__file__))    #The path to the main folder


class MainScreen(QMainWindow):                  #MainScreen CLass
    searchButtons = []                          #Search Results List (QPushButton) 

    def __init__(self):                         #Initialization of Main Screen and UI
        super(MainScreen, self).__init__()
        self.setWindowTitle("Besinerji")
        
                                                #UI
        loadUi(os.path.join(general_path,"mainWindow.ui"), self)
        self.showMaximized()
        self.stackedWidget.setCurrentIndex(0)
        self.butonAnasayfa.clicked.connect(self.anasayfaFunc)
        self.logoButton.clicked.connect(self.anasayfaFunc)
        self.lineEdit.textChanged.connect(self.getNames)
        self.danisanEkle.clicked.connect(self.danisanEkleFunc)

    def getNames(self):                         
        #Triggered when search lineEdit is updated
        #Fetchs the data from database for a search result
        #Generates QpushButtons for the search result and places on the screen

        #Deletes old query result and buttons
        for result in self.searchButtons:           
            #print(self.searchButtons)
            result.deleteLater()
        
        self.searchButtons = []

        #Initializes query as the searchbar text
        query = self.lineEdit.text()

        #Fetches the data from the danışanlar.db
        conn = sqlite3.connect(os.path.join(general_path,"Danışanlar.db"))
        c = conn.cursor()
        c.execute("""SELECT 
                        ID, İsim, Soyisim, Hastalıklar 
                    FROM 
                        Danışanlar
                    WHERE 
                        İsim || ' ' || Soyisim LIKE '%' || ? || '%'
                        AND 0 != LENGTH(?)
                    """, (query, query))
        info = c.fetchall()
        
        #For every query result
        #Generates a button and places it on the screen
        #Also connects buttons to the Infopage function with necessary parameters

        for i in range(len(info)):
            tempbutton = QPushButton(self)                                                      
            tempbutton.setGeometry(550, 440 + i*65, 1111, 65)                                   #i*65 is for the vertical displacement of the new button
            tempbutton.setText( "(" + str(info[i][0]) + ") " + info[i][1] + " " + info[i][2])   

            #Template stylesheet
            stylesheetstring = """border-style: solid;                                          
                        border-width: 5px;
                        border-color: orange;
                        font:20px;
                        text-align:left;
                        padding-left:20px;
                        font-family:"Bahnschrift Light";"""
            
            if i != 0 and len(info):
                stylesheetstring += "\nborder-top-width: 2px;"

            if i != len(info) - 1:
                stylesheetstring += "\nborder-bottom-width: 3px;"
                
            if  i % 2 == 0:
                stylesheetstring += "\nbackground-color:rgb(255, 255, 255);" 
            
            else:
                stylesheetstring += "\nbackground-color:rgb(240, 240, 240);" 

            tempbutton.setStyleSheet(stylesheetstring)

            #Passes the selected query row (info) to the infoPage function for the new page to display
            tempbutton.clicked.connect(lambda state, _info=info[i]: self.infoPage(_info))
            
            self.searchButtons.append(tempbutton)
            self.searchButtons[i].show()

        conn.commit()
        conn.close()
        
    def infoPage(self, info):
        #print(info)

        for result in self.searchButtons:
            result.deleteLater()
            
        self.stackedWidget.setCurrentIndex(1)
        self.lineEdit.setText("")
        
        self.hastaAdi.setText(info[1] + " " + info[2])

    
    def anasayfaFunc(self):
        for result in self.searchButtons:
            result.deleteLater()

        self.stackedWidget.setCurrentIndex(0)
        self.searchButtons = []
        self.lineEdit.setText("")

    def danisanEkleFunc(self):
        form = QDialog(self)
        loadUi(os.path.join(general_path,"Danışan Ekleme Formu.ui"), form)
        form.showNormal()

        # if isim & soyisim & telefon & yas:
        #     print ("ad soyad telefon ve yas kutucukları boş bırakılamaz")

        def sendFormData():
            conn = sqlite3.connect(os.path.join(general_path,"Danışanlar2.db"))
            c = conn.cursor() 
            c.execute("SELECT * FROM Danışanlar ORDER BY ID DESC LIMIT 1;")
            max_id = c. fetchall()
            id = int(0 + 1)

            print("Form Kaydedildi")
            isim = form.lineEditAd.text().lower
            soyisim = form.lineEditSoyad.text().lower
            telefon = form.lineEditTelefon.text()
            yas = form.lineEditYas.text()
            ekstra_bilgi = form.lineEditEkstra.text()
            #hastalik = form.hastalikBox.currentText()
            hastalik = "hastalik"
            yas = int(yas)
            print(type(ekstra_bilgi))

            c.execute("INSERT INTO Danışanlar VALUES (?, ?, ?, ?, ?, ?, ?)",
                                                (id, isim, soyisim, hastalik, telefon, yas, ekstra_bilgi))
            conn.commit()
            conn.close()
            

        form.pushButtonKaydet.clicked.connect(sendFormData)

#Main
app = QApplication(sys.argv)

win = MainScreen()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(win)

win.showFullScreen()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")


