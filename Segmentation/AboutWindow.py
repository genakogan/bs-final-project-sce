from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys 
# window class 
class AboutW(QWidget):
     def __init__(self):
        super().__init__()

        self.initUI()
        self.label_1 = QLabel('Left', self)
        self.label_1.setFont(QFont('Times', 10)) 
        self.label_1.move(10,10)
        self.label_1.setStyleSheet("border: 3px solid black;") 
     def initUI(self):

        # Cancel button 
        cancelButton = QPushButton("Cancel")
        # Clossing AboutWindow action
        cancelButton.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}")
        cancelButton.clicked.connect(lambda:self.close())
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('About')
       



# create pyqt5 app 
App = QApplication(sys.argv) 

# create the instance of our Window 
#window = AboutW() 

# showing the wwindow 
#window.show() 

# start the app 
#sys.exit(App.exec()) 
 
