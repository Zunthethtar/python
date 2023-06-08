#pip install mtsql-connector or pip3 install mysql-connector
from   PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QPushButton,QWidget,QLabel,QLineEdit,QVBoxLayout,QMessageBox
import mysql.connector
import bcrypt

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('login')
        self.setFixedSize(300,200)#x,y,w,h
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        
        #create labels and line edits for username and password
        self.email_label=QLabel('Email')
        self.email_label.setStyleSheet('color:blue;')
        self.email_edit=QLineEdit()
        self.password_label=QLabel('Password')
        self.password_edit=QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        #create login button
        self.login_button=QPushButton('Login')
        self.login_button.clicked.connect(self.check_login)

        back_button=QPushButton("Go to Welcome Form")
        back_button.clicked.connect(self.show_welcome_form)
        
        #create layout and add widgets
        layout=QVBoxLayout()
        layout.addWidget(self.email_label.setStyleSheet('color:blue;'))
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(back_button)

        
        self.central_widget.setLayout(layout)
        
        #Create window on screen
        
        screen_geometry =QDesktopWidget().screenGeometry()
        window_geometry =self.geometry()
        x=int((screen_geometry.width()-window_geometry.width())/2)
        y=int((screen_geometry.height()-window_geometry.width())/2)
        self.move(x,y)
        
    def show_welcome_form(self):
            from welcomeform import WelcomeScreen
            self.close()
            self.welcome=WelcomeScreen()
            self.welcome.show()  
                 
    def check_login(self):
            email =self.email_edit.text()
            password= self.password_edit.text()
            
            #connect to MySQL database
            db = mysql.connector.connect(
               host='localhost',
               user='root',
               password='Welcome$10000',
               database='project'
            )
            
            cursor =db.cursor()
            
            #execut SQL qurey to check if email and password are correct
            query ="SELECT password FROM users WHERE email = %s"
            values=(email,)
            cursor.execute(query,values)
            result =cursor.fetchone()
            
            if result:
                hashed_password=result[0].encode()
                if bcrypt.checkpw(password.encode(), hashed_password):
                   QMessageBox.information(self,'project','login successful')
                   from displayform import UserTableWindow
                   self.close
                   self.display=UserTableWindow()
                   self.display.show()
                else:
                   QMessageBox.warning(self,'project','incorrect email or password.')
            else:
                print("Email not found")

if __name__=='__main__':
                 app=QApplication([])
                 login=Login()
                 login.show()
                 app.exec_()



        