from   PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QWidget,QLabel,QVBoxLayout,QDesktopWidget
#from login_db import Login
#from register import RegistrationPage
from PyQt5.QtCore import Qt


class WelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Menu')
        self.setFixedSize(400,300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout =QVBoxLayout()
        
        #Create title label
        title_label=QLabel("Welcome to my application",self)
        title_label.setStyleSheet('color:red;font-size:14pt;')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(100,50,400,60)
        layout.addWidget(title_label)
        
        login_button=QPushButton('Login',self)
        login_button.clicked.connect(self.show_login_form)
        layout.addWidget(login_button)
        login_button.setStyleSheet('font-weight:bold;')
        
        
        signup_button=QPushButton('Signup',self)
        signup_button.clicked.connect(self.show_signup_form)
        layout.addWidget(signup_button)
        signup_button.setStyleSheet('font-weight:bold;')
        
        self.central_widget.setLayout(layout)
        
        #Create window on screen
        screen_geometry =QDesktopWidget().screenGeometry()
        window_geometry =self.geometry()
        x=int((screen_geometry.width()-window_geometry.width())/2)
        y=int((screen_geometry.height()-window_geometry.width())/2)
        self.move(x,y)
        
    def show_login_form(self):
            from loginform import Login
            self.close()
            self.login_form = Login()
            self.login_form.show()
            #pass
            
    def show_signup_form(self):
            from registerform import RegistrationPage
            self.close()
            self.register_form = RegistrationPage()
            self.register_form.show()
            #pass

if __name__=='__main__':
                 app=QApplication([])
                 welcome_screen=WelcomeScreen()
                 welcome_screen.show()
                 app.exec_()
        