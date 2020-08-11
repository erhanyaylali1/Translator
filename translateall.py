import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from ibm_watson import LanguageTranslatorV3,SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import speech_recognition as sr
import wave


class Window(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.languages = ["English","French","German","Spanish","Turkish","Italian","Russian",]
        self.codes = ["en","fr","de","es","tr","it","ru"]
        self.textArea = QtWidgets.QLabel("From")
        self.textArea2= QtWidgets.QLabel("To")

        self.button = QtWidgets.QPushButton("Translate")
        self.button.clicked.connect(self.translate)
        self.button2 = QtWidgets.QPushButton("Clear")
        self.button2.clicked.connect(self.clear)
        self.button3 = QtWidgets.QPushButton("Speech to Text")
        self.button3.clicked.connect(self.speech2text)
        self.button4 = QtWidgets.QPushButton("Text to Speech")
        self.button4.clicked.connect(self.text2speech)
        self.text = QtWidgets.QTextEdit()
        self.text2 = QtWidgets.QTextEdit()
        self.rec = QtWidgets.QLabel("Recording")
        self.rec.hide()

        self.lang1 = QtWidgets.QComboBox()
        self.lang2 = QtWidgets.QComboBox()

        self.lang1.addItems(self.languages)

        self.lang2.addItems(self.languages)
        self.lang2.setCurrentIndex(4)

        h_box2 = QtWidgets.QHBoxLayout()  
        h_box2.addStretch()
        h_box2.addWidget(self.textArea)
        h_box2.addWidget(self.lang1)
        h_box2.addStretch()
        h_box2.addStretch()
        h_box2.addStretch()
        h_box2.addWidget(self.textArea2)
        h_box2.addWidget(self.lang2)
        h_box2.addStretch()

        v_box2 = QtWidgets.QVBoxLayout()
        v_box3 = QtWidgets.QVBoxLayout()
        v_box4 = QtWidgets.QVBoxLayout()
        v_box3.addStretch()
        v_box3.addWidget(self.button)
        v_box4.addWidget(self.button2)
        v_box4.addStretch()
        v_box2.addLayout(v_box3)
        v_box2.addLayout(v_box4)

        v_box5 = QtWidgets.QHBoxLayout()
        v_box6 = QtWidgets.QHBoxLayout()
        v_box7 = QtWidgets.QVBoxLayout()
        v_box6.addWidget(self.button3)
        v_box6.addWidget(self.rec)
        v_box7.addWidget(self.button4)
        v_box5.addLayout(v_box6)
        v_box5.addStretch()
        v_box5.addLayout(v_box7)


        h_box = QtWidgets.QHBoxLayout()    
        h_box.addWidget(self.text)
        h_box.addLayout(v_box2)
        h_box.addWidget(self.text2)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box)
        v_box.addLayout(v_box5)

        self.setLayout(v_box)
        self.setWindowTitle("Translator")

        self.setGeometry(500,300,800,500)
        self.show()
    

    def translate(self):

        txt = self.text.toPlainText()
        lng = self.lang1.currentText()
        lng2 = self.lang2.currentText()

        index1 = self.languages.index(lng)
        index2 = self.languages.index(lng2)

        code = self.codes[index1] + "-" + self.codes[index2]
        authenticator = IAMAuthenticator("Xe3IeU29IzGioIw3xq18UTbhugHeXo3TUfmRr-jgDfHR")
        translator = LanguageTranslatorV3(authenticator = authenticator,version = "2018-05-01",)
        translator.set_service_url("https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/e12288b7-995d-4405-bafc-aa5d0ca1a116")

        respond = translator.translate(text=txt,model_id = code)
        result = respond.get_result()
        self.text2.setText(result["translations"][0]["translation"])


    def speech2text(self):

        r = sr.Recognizer()
        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source, duration=0.5) 
            audio = r.listen(source)
        
        self.text.setText(r.recognize_google(audio))
        self.translate()
        


       
    
    def text2speech(self):

        pass
        

        


    def clear(self):

        self.text.clear()



app = QtWidgets.QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())




