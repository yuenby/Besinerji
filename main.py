from re import search
import sys
import sqlite3
import time
from turtle import delay
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel, QPushButton, QComboBox

class MainScreen(QMainWindow):
    searchButtons = []
    hastaInfo = []

    returnDanisanIdFunc = lambda button: button.text()

    def __init__(self):
        super(MainScreen, self).__init__()
        self.initUI()
        self.setWindowTitle("Besinerji")
        
    def initUI(self):
        loadUi("mainWindow.ui", self)

        self.showMaximized()
        self.stackedWidget.setCurrentIndex(0)

        self.butonAnasayfa.clicked.connect(self.anasayfaFunc)
        self.logoButton.clicked.connect(self.anasayfaFunc)
        self.lineEdit.textChanged.connect(self.getNames)
        self.danisanEkle.clicked.connect(self.danisanEkleFunc)

    def getNames(self):
        for result in self.searchButtons:
            #print(self.searchButtons)
            result.deleteLater()
        
        self.searchButtons = []
        query = self.lineEdit.text()
        #print(query)

        conn = sqlite3.connect('Danışanlar.db')

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
        

        for i in range(len(info)):
            tempbutton = QPushButton(self)
            tempbutton.setGeometry(550, 440 + i*65, 1111, 65)
            tempbutton.setText( "(" + str(info[i][0]) + ") " + info[i][1] + " " + info[i][2]) 
            #print(info[i][1] + " " + info[i][2])
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
            # tempbutton.clicked.connect(self.infoPage)
            tempbutton.clicked.connect(lambda state, _info=info[i]: self.infoPage(_info))

            self.searchButtons.append(tempbutton)
            self.searchButtons[i].show()

        conn.commit()
        conn.close()
        # print(info)
        
    def infoPage(self, info):
        #print(info)

        for result in self.searchButtons:
            result.deleteLater()
            
        self.stackedWidget.setCurrentIndex(1)
        self.lineEdit.setText("")
        

        self.hastaAdi.setText(info[1] + " " + info[2])

    list = []
    pageIndex = 0
    
    def anasayfaFunc(self):
        for result in self.searchButtons:
            result.deleteLater()

        self.stackedWidget.setCurrentIndex(0)
        self.searchButtons = []
        self.lineEdit.setText("")

    def danisanEkleFunc(self):
        form = QDialog(self)
        loadUi("Danışan Ekleme Formu.ui", form)
        form.showNormal()

        # if isim & soyisim & telefon & yas:
        #     print ("ad soyad telefon ve yas kutucukları boş bırakılamaz")

        def sendFormData():
            conn = sqlite3.connect('Danışanlar2.db')
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


