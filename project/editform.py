from re import U
from   PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QWidget,QLabel,QVBoxLayout,QDesktopWidget,QMessageBox,QFrame,QLineEdit
from PyQt5.QtCore import Qt
import mysql.connector

class UserSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('User Search')
        self.setGeometry(200,200,400,300)
        
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        
        layout=QVBoxLayout()
        
        self.search_input=QLineEdit()
        layout.addWidget(self.search_input)
        search_button=QPushButton("Search")
        search_button.clicked.connect(self.search_user)
        layout.addWidget(search_button)
        
        separator=QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        title_label=QLabel("User info",self)
        title_label.setStyleSheet("font-size:11pt;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        self.user_info_label=QLabel()
        layout.addWidget(self.user_info_label)
        
        userid_label=QLabel("User ID:")
        self.userid_input=QLineEdit()
        self.userid_input.setEnabled(False)
        layout.addWidget(userid_label)
        layout.addWidget(self.userid_input)
        
        email_label=QLabel("Email:")
        self.email_input=QLineEdit()
        self.email_input.setEnabled(False)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        
        desc_label=QLabel("Description:")
        self.desc_input=QLineEdit()
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)
        
        edit_button=QPushButton("Edit")
        edit_button.clicked.connect(self.edit_user)
        layout.addWidget(edit_button)
        
        display_button=QPushButton("View all data")
        display_button.clicked.connect(self.show_display_form)
        layout.addWidget(display_button)
        
                #Create window on screen
        screen_geometry =QDesktopWidget().screenGeometry()
        window_geometry =self.geometry()
        x=int((screen_geometry.width()-window_geometry.width())/2)
        y=int((screen_geometry.height()-window_geometry.width())/2)
        self.move(x,y)
        central_widget.setLayout(layout)
    def search_user(self):
        try:  
            self.conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='Welcome$10000',
            database='project'
            )
        except mysql.connector.Error as e:
            self.show_error(f"Failed to connect to database: {e}")
            return
        
        user_id=self.search_input.text()
        
        if not user_id:
            self.show_error("please enter a user ID.")
            return
        cursor =self.conn.cursor()
        
        query ="SELECT * FROM users WHERE id =%s"
        cursor.execute(query,(user_id,))
        result =cursor.fetchone()
        
        if result:
            self.userid_input.setText(f'{result[0]}')
            self.email_input.setText(f'{result[1]}')
            self.desc_input.setText(f'{result[3]}')
            
        else:
            QMessageBox.warning(self.show_error('User ID not found.'))
            
        cursor.close()
        
    def show_error(self,message):
                QMessageBox.warning(self,"Error",message)
                
    def show_display_form(self):
        from displayform import UserTableWindow
        self.close()
        self.display=UserTableWindow()
        self.display.show()
        
    def edit_user(self):
        id=self.userid_input.text()
        description=self.desc_input.text()
        
        if not description:
            QMessageBox.warning(self.show_error("All fields are required"))
            return
        
        try:
            conn= mysql.connector.connect(
            host='localhost',
            user='root',
            password='Welcome$10000',
            database='project'
            )
        except mysql.connector.Error as e:
            self.show_error(f"Failed to connect to database: {e}")
            return
        
        cursor=conn.cursor()
        
        query="UPDATE users SET description=%s WHERE id=%s"
        values=(description,int(id))
        cursor.execute(query,values)
        conn.commit()
        
        
        cursor.close()
        conn.close()
        
        from displayform import UserTableWindow
        self.close()
        self.display_form=UserTableWindow()
        self.display_form.show()
        
if __name__=='__main__':
                app=QApplication([])
                user_search_app= UserSearchApp()
                user_search_app.show()
                app.exec_()
         
        