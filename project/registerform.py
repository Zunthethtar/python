from   PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QPushButton,QWidget,QLabel,QLineEdit,QVBoxLayout,QMessageBox
import bcrypt,re


import mysql.connector
class RegistrationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registration Page')
        self.setGeometry(200,200,400,300)
        
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        
        layout =QVBoxLayout()
        
        email_label=QLabel("Email:")
        self.email_input=QLineEdit()
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        
        
        password_label=QLabel("Password:")
        self.password_input=QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        
        confirm_password_label=QLabel("Confirm Password:")
        self.confirm_password_input=QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        
        desc_label=QLabel("Description:")
        self.desc_input=QLineEdit()
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)
        
        signup_button=QPushButton("Sign Up")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)
        
        back_button=QPushButton("Go to Welcome Form")
        back_button.clicked.connect(self.show_welcome_form)
        layout.addWidget(back_button)
        
        central_widget.setLayout(layout)
        
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
        
    def signup(self): 
        email =self.email_input.text()
        password=self.password_input.text()
        confirm=self.confirm_password_input.text()
        description=self.desc_input.text()
        hashed_password =bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        
        if not email or not password or not confirm or not description:
            self.show_error("All fields are required.")
            return 
        if password!=confirm:
            self.show_error("Passwords do not match")
            return
        if not self.is_valid_email(email):
            self.show_error("Invalid email address")
            return
        
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Welcome$10000',
                database='project'
            )
        except mysql.connector.Error as e:
            self.show_error(f"Fail to connect to database :{e}")
            return
                        
        cursor =conn.cursor()
        query ="SELECT * FROM users WHERE email =%s"
        cursor.execute(query,(email,))
        result =cursor.fetchone()
        if result:
            self.show_error("email already exists")
            return 
            
        query="INSERT INTO users (email,password,description) VALUE (%s,%s,%s)"
        values=(email,hashed_password,description)
        cursor.execute(query,values)
        conn.commit()
            
        cursor.close()
        conn.close
            
        self.show_success("Registration successful")
        from loginform import Login
        self.close()  
        self.login_form=Login()
        self.login_form.show()  
        #self.email_input.clear()
        #self.password_input.clear()
        #self.confirm_password_input.clear()
        #self.desc_input.clear()
            
    def show_error(self,message):
                QMessageBox.warning(self,"Error",message)
                
    def show_success(self,message):
                QMessageBox.information(self,"Success",message)
                
    def is_valid_email(self,email):
                pattern =r'^[\w\.-]+@[\w\.-]+\.\w+$'
                return re.match(pattern,email)is not None
            
if __name__=='__main__':
                 app=QApplication([])
                 registration_page=RegistrationPage()
                 registration_page.show()
                 app.exec_()
            
            