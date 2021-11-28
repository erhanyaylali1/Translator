import sys, os
from PyQt5 import QtWidgets,QtGui,QtCore
import sys, os
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from ibm_watson import LanguageTranslatorV3,SpeechToTextV1,TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import speech_recognition as sr
import wave
from playsound import playsound
import validators
import textract
import unicodedata
import PyPDF2
from docx import Document
from fpdf import FPDF 
from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r"C:\Users\erhan\AppData\Local\Tesseract-OCR\tesseract.exe"

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):






        super().__init__()
        self.ui()
        self.pencere = Window()
        self.setCentralWidget(self.pencere)

        self.pencere.setStyleSheet("""
            QPushButton {
                color: #fff;
                width: 80px;
                height: 25px;
                border: 2px solid #942BFE;
                border-radius: 3px;
                background-color: #942BFE;
                margin: 5px 5px;
            }
            QPushButton:hover {
                border: 2px solid #FF9678;
                background-color: #FF9678;
            }
            QPushButton:pressed {
                border: 2px solid #fff;
                background-color: #fff;
            }
            QTextEdit {
                color: #fff;
                font-size: 15px;
                border: 3px trasnparent;
                border-radius: 3px;
                background-color: #18BC9C;
            }
            QLabel{
                color: #fff;
                font-size: 13px;
                margin-right: 4px;
                margin-bottom: 1px;
                place-holer
            }
            QComboBox {
                color: #fff;
                border: 1px solid #ad575f;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                background-color: #ad575f;
            }
            QComboBox QListView{
                background-color: #ad575f;
            }
        """)
        self.setStyleSheet("""
            background-color: #41436A;            
            """)


    def ui(self):

        self.show()
        self.setGeometry(300,300,800,500)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle("Translator")

        menuBar = self.menuBar()
        menu = menuBar.addMenu("More")
        menuBar.setStyleSheet("QMenuBar{color: #fff;}QMenuBar:pressed{color: #000;}QMenu{color: #fff;font: 10pt;background-color: #41436A;border: 1px solid #fff;}QMenu::item:selected{color: #fff;background-color: green;}")
        open = QtWidgets.QAction("Open File",self)
        open.triggered.connect(self.open)
        about = QtWidgets.QAction("About",self)
        about.triggered.connect(self.about)
        contact = QtWidgets.QAction("Contact",self)
        contact.triggered.connect(self.contact)
        TranslateHistory = QtWidgets.QAction("Translate History",self)
        TranslateHistory.triggered.connect(self.history)
        fromUrl = QtWidgets.QAction("Go to URL",self)
        fromUrl.triggered.connect(self.fromUrl)
        menu.addAction(open)
        menu.addAction(fromUrl)
        menu.addAction(TranslateHistory)
        menu.addAction(about)
        menu.addAction(contact)


    def about(self):

        reply = QtWidgets.QMessageBox.information(self,"About","This application is designed by Erhan Yaylalı.",QtWidgets.QMessageBox.Ok)


    def contact(self):

        buttonReply2 = QtWidgets.QMessageBox.information(self, "Contact", "You can contact us for your informations or problems\nby using xxxxxxxxxx@gmail.com or +90 xxxxxxxx", QtWidgets.QMessageBox.Ok)

    def history(self):

        if self.pencere.historyNum == 0:

            QtWidgets.QMessageBox.warning(self,"Warning","There is no translation history",QtWidgets.QMessageBox.Ok)

        else:
            self.newscreen = History(self.pencere.historyNum,self.pencere.history)

    def fromUrl(self):

        self.browser = Temp()


    def open(self):

        fileName = QtWidgets.QFileDialog.getOpenFileName(self,"Open",os.getenv("Home"),"Text (*.txt *.pdf *.docx *.srt)")
        if(fileName[0].endswith(".txt") or fileName[0].endswith(".docx")):
            text = textract.process(fileName[0])
            self.pencere.text.setText(str(text, 'utf-8'))
            self.pencere.translate()

        elif(fileName[0].endswith(".srt")):

            with open(fileName[0],"r") as file:
                self.pencere.text.setText(file.read())
            self.pencere.translate()

        elif(fileName[0].endswith(".pdf")):

            pdfReader = PyPDF2.PdfFileReader(open(fileName[0],"rb"))
            tx = ""
            for i in range(pdfReader.numPages):
                pgObj = pdfReader.getPage(i)
                tx = tx + pgObj.extractText() + "\n\n" 
            self.pencere.text.setText(tx)
            self.pencere.translate()

        


class Window(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()
        self.history = []
        self.historyNum = 0

    def init_ui(self):

        self.languages = ["English","French","German","Spanish","Turkish","Italian","Russian",]
        self.codes = ["en","fr","de","es","tr","it","ru"]
        self.codes2 = ["-US","-FR","-DE","-ES","","-IT",""]
        self.voices = ["_AllisonVoice","_ReneeVoice","_DieterVoice","_LauraVoice","","FrancescaVoice",""]
        self.models = ["en-US_BroadbandModel","fr-FR_BroadbandModel","de-DE_BroadbandModel","es-ES_BroadbandModel","","it-IT_BroadbandModel",""]
        self.images = ["eng","fra","deu","spa","tur","ita","rus"]
        self.textFrom = QtWidgets.QLabel("From")
        self.textTo= QtWidgets.QLabel("To")

        self.buttonTranslate = QtWidgets.QPushButton("Translate")
        self.buttonTranslate.clicked.connect(self.translate)
        self.buttonClear = QtWidgets.QPushButton("Clear")
        self.buttonClear.clicked.connect(self.clear)
        self.buttonS2T = QtWidgets.QPushButton("Speech to Text")
        self.buttonS2T.clicked.connect(self.speech2text)
        self.buttonI2T = QtWidgets.QPushButton("Image to Text")
        self.buttonI2T.clicked.connect(self.image2text)
        self.buttonI2T.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonT2S = QtWidgets.QPushButton("Text to Speech")
        self.buttonT2S.clicked.connect(self.text2speech)
        self.buttonSwap = QtWidgets.QPushButton("Swap")
        self.buttonSwap.clicked.connect(self.swap)
        self.save = QtWidgets.QPushButton("Save")
        self.save.clicked.connect(self.saveFunc)
        self.text = QtWidgets.QTextEdit()
        self.text2 = QtWidgets.QTextEdit()

        self.lang1 = QtWidgets.QComboBox()
        self.lang2 = QtWidgets.QComboBox()

        self.lang1.addItems(self.languages)
        self.lang1.setCurrentIndex(0)
        self.lang2.addItems(self.languages)
        self.lang2.setCurrentIndex(4)

        h_boxTop = QtWidgets.QHBoxLayout()  
        h_boxTop.addStretch()
        h_boxTop.addWidget(self.textFrom)
        h_boxTop.addWidget(self.lang1)
        h_boxTop.addStretch()
        h_boxTop.addStretch()
        h_boxTop.addStretch()
        h_boxTop.addWidget(self.textTo)
        h_boxTop.addWidget(self.lang2)
        h_boxTop.addStretch()

        v_boxButtons = QtWidgets.QVBoxLayout()
        v_boxButtonTranslate = QtWidgets.QVBoxLayout()
        v_boxButtonClear = QtWidgets.QVBoxLayout()
        v_boxButtonSwap = QtWidgets.QVBoxLayout()
        v_boxButtonTranslate.addStretch()
        v_boxButtonTranslate.addWidget(self.buttonTranslate)
        v_boxButtonSwap.addWidget(self.buttonSwap)
        v_boxButtonClear.addWidget(self.buttonClear)
        v_boxButtonClear.addStretch()
        v_boxButtons.addLayout(v_boxButtonTranslate)
        v_boxButtons.addLayout(v_boxButtonSwap)
        v_boxButtons.addLayout(v_boxButtonClear)

        v_boxBottom = QtWidgets.QHBoxLayout()
        v_boxButtonS2T = QtWidgets.QHBoxLayout()
        v_boxButtonT2S = QtWidgets.QHBoxLayout()
        v_boxButtonS2T.addWidget(self.buttonS2T)
        v_boxButtonS2T.addWidget(self.buttonI2T)
        v_boxButtonT2S.addWidget(self.save)
        v_boxButtonT2S.addWidget(self.buttonT2S)
        v_boxBottom.addLayout(v_boxButtonS2T)
        v_boxBottom.addStretch()
        v_boxBottom.addLayout(v_boxButtonT2S)


        h_boxBody = QtWidgets.QHBoxLayout()    
        h_boxBody.addWidget(self.text)
        h_boxBody.addLayout(v_boxButtons)
        h_boxBody.addWidget(self.text2)

        v_boxMain = QtWidgets.QVBoxLayout()
        v_boxMain.addLayout(h_boxTop)
        v_boxMain.addLayout(h_boxBody)
        v_boxMain.addLayout(v_boxBottom)

        self.setLayout(v_boxMain)
        self.show()


    def translate(self):

        txt = self.text.toPlainText()

        if not txt:
            reply2 = QtWidgets.QMessageBox.warning(self,"Empty","First Type Something",QtWidgets.QMessageBox.Ok)

        else:
            lng = self.lang1.currentText()
            lng2 = self.lang2.currentText()

            index1 = self.languages.index(lng)
            index2 = self.languages.index(lng2)

            if(self.codes[index1] == "fr" and (self.codes[index2] == "es" or self.codes[index2] == "tr" or self.codes[index2] == "it" or self.codes[index2] == "ru")):
                repl = "You can't translate " + self.languages[index1] + " to " + self.languages[index2]
                buttonReply = QtWidgets.QMessageBox.warning(self, "Error", repl, QtWidgets.QMessageBox.Ok)

            elif(self.codes[index1] == "de" and (self.codes[index2] == "es" or self.codes[index2] == "tr" or self.codes[index2] == "ru")):
                repl = "You can't translate " + self.languages[index1] + " to " + self.languages[index2]
                buttonReply = QtWidgets.QMessageBox.warning(self, "Error", repl, QtWidgets.QMessageBox.Ok)

            elif(self.codes[index1] == "it" and (self.codes[index2] == "fr" or self.codes[index2] == "es" or self.codes[index2] == "tr" or self.codes[index2] == "ru")):
                repl = "You can't translate " + self.languages[index1] + " to " + self.languages[index2]
                buttonReply = QtWidgets.QMessageBox.warning(self, "Error", repl, QtWidgets.QMessageBox.Ok)

            elif(self.codes[index1] == "tr" and (self.codes[index2] == "fr" or self.codes[index2] == "de" or self.codes[index2] == "es" or self.codes[index2] == "it" or self.codes[index2] == "ru")):
                repl = "You can't translate " + self.languages[index1] + " to " + self.languages[index2]
                buttonReply = QtWidgets.QMessageBox.warning(self, "Error", repl, QtWidgets.QMessageBox.Ok)

            elif(self.codes[index1] == "ru" and (self.codes[index2] == "fr" or self.codes[index2] == "de" or self.codes[index2] == "es" or self.codes[index2] == "it" or self.codes[index2] == "tr")):
                repl = "You can't translate " + self.languages[index1] + " to " + self.languages[index2]
                buttonReply = QtWidgets.QMessageBox.warning(self, "Error", repl, QtWidgets.QMessageBox.Ok)

            else:
                code = self.codes[index1] + "-" + self.codes[index2]
                authenticator = IAMAuthenticator("Xe3IeU29IzGioIw3xq18UTbhugHeXo3TUfmRr-jgDfHR")
                translator = LanguageTranslatorV3(authenticator = authenticator,version = "2018-05-01",)
                translator.set_service_url("https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/e12288b7-995d-4405-bafc-aa5d0ca1a116")

                respond = translator.translate(text=txt,model_id = code)
                result = respond.get_result()

                hist = lng + " : " + txt
                hist2 = lng2 + " : " + result["translations"][0]["translation"]
                
                self.history.append([hist,hist2])
                self.historyNum += 1
                self.text2.setText(result["translations"][0]["translation"])


    def speech2text(self):

        r = sr.Recognizer()
        lng = self.lang1.currentText()
        index1 = self.languages.index(lng)
        langCode = self.codes[index1] + self.codes2[index1]

        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source, duration=0.5) 
            audio = r.listen(source)
        
         
        self.text.setText(r.recognize_google(audio, language=langCode))
        self.text2.clear()
        


       
    
    def text2speech(self):

        authenticator = IAMAuthenticator("FvZIDhcS9_vGthEp3UrsZ-0Ca5KnNsuXKIRmfqf6O3vU")
        tx2sp = TextToSpeechV1(authenticator=authenticator)
        tx2sp.set_service_url("https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/16fafc3c-ecc6-4aee-aec4-9c148c2ac7c6")

        lng2 = self.lang2.currentText()
        index2 = self.languages.index(lng2)
        voice2 = self.codes[index2] + self.codes2[index2] + self.voices[index2]

        if (self.codes[index2] == "tr" or self.codes[index2] == "ru"):
            repl = "You can't use Text-to-Speech feauture in " + self.languages[index2]
            buttonReply = QtWidgets.QMessageBox.warning(self, "Error", repl, QtWidgets.QMessageBox.Ok)

        else:
            with open("temp.mp3","wb") as audio:
                audio.write(tx2sp.synthesize(self.text2.toPlainText(),voice=voice2,accept="audio/mp3").get_result().content)

            playsound("temp.mp3")
            os.remove("temp.mp3")


    def image2text(self):

        lng2 = self.lang1.currentText()
        index2 = self.languages.index(lng2)
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,"Open",os.getenv("Home"),"Image (*.png *.jpeg *.jpg)")


        if fileName[0] != "":

            img = Image.open(fileName[0])
            text = tess.image_to_string(img, lang = self.images[index2])
            self.text.setText(text)
        

    def swap(self):

        temp = self.lang1.currentText()
        self.lang1.setCurrentText(self.lang2.currentText())
        self.lang2.setCurrentText(temp)
        temp = self.text.toPlainText()
        self.text.setText(self.text2.toPlainText())
        self.text2.setText(temp)

        
    def clear(self):

        self.text.clear()
        self.text2.clear()
    

    def saveFunc(self):

        if not self.text2.toPlainText():
            buttonReply2 = QtWidgets.QMessageBox.warning(self, "Empyt Content", "You can't save empty file.\n Please first use translator", QtWidgets.QMessageBox.Ok)

        else:
            fileName = QtWidgets.QFileDialog.getSaveFileName(self,"Save File",os.getenv("Home"),"Text (*.txt *.docx *.srt)")
            print(fileName[0])

            if fileName[0].endswith(".txt") or fileName[0].endswith(".srt"):
                with open(fileName[0],"w") as file:
                    file.write(self.text2.toPlainText())

            elif fileName[0].endswith(".docx"):

                mydoc = Document()
                mydoc.add_paragraph(self.text2.toPlainText())
                print(mydoc)
                mydoc.save(fileName[0])
        


class History(QtWidgets.QWidget):

    def __init__(self,number,hist):

        super().__init__()
        self.ui(number,hist)

    def ui(self,number,hist):

        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setGeometry(1130,330,640, 400)
        self.setWindowTitle("History")
        self.show()
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(number)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0,300)
        self.tableWidget.setColumnWidth(1,300)
        
        
        for i in range(0,number):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(hist[i][0]))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(hist[i][1]))

        v_boxTable = QtWidgets.QVBoxLayout()
        v_boxTable.addWidget(self.tableWidget)
        self.setLayout(v_boxTable)


class Browser(QtWidgets.QWidget):

    def __init__(self,url):

        super().__init__()
        self.ui(url)
        


    def ui(self,url):

        self.url = url
        self.browser = QWebEngineView()
        self.browser.setWindowTitle("Web Browser")
        self.browser.load(QtCore.QUrl(self.url))
        self.browser.show()
        self.browser.setWindowIcon(QtGui.QIcon('logo.png'))
        self.browser.setGeometry(830,200,1000,800)


class Temp(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.ui()


    def ui(self):

        self.pencere = Window()
        self.pencere.hide()
        self.show()
        self.setWindowTitle("Web Browser")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setGeometry(1130,330,500,100)
        v_box = QtWidgets.QHBoxLayout()
        v_boxButton = QtWidgets.QHBoxLayout()
        v_boxMain = QtWidgets.QVBoxLayout()
        self.text = QtWidgets.QLabel("Enter URL")
        self.line = QtWidgets.QLineEdit(self)
        self.button = QtWidgets.QPushButton("Go")
        self.button.clicked.connect(self.go)
        v_boxButton.addStretch()
        v_boxButton.addWidget(self.button)
        v_box.addWidget(self.text)
        v_box.addWidget(self.line)
        v_boxMain.addLayout(v_box)
        v_boxMain.addLayout(v_boxButton)
        self.setLayout(v_boxMain)

    def go(self):

        valid = validators.url(self.line.text())
        
        if valid == True:

            self.brows = Browser(self.line.text())
            response = requests.get(self.line.text())
            self.hide()

        else:
            reply = QtWidgets.QMessageBox.warning(self,"Not Valid URL","Please Enter a Valid URL",QtWidgets.QMessageBox.Yes)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())




