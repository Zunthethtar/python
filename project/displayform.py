from   PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QPushButton,QWidget,QLabel,QLineEdit,QVBoxLayout,QMessageBox,QTableWidget,QTableWidgetItem,QHeaderView,QMenu,QAction
import sys
from PyQt5.QtCore import Qt
import mysql.connector

class UserTableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('User Table')
        self.setGeometry(200,200,800,400)
        
        self.table_widget=QTableWidget()
        self.setCentralWidget(self.table_widget)
        
        #Create menu and submenu
        menu_bar=self.menuBar()
        go_menu=menu_bar.addMenu("Go to....")
        edit_submenu=QMenu("Edit form ",self)
        go_menu.addMenu(edit_submenu)
        
        #Create action for Edit form
        edit_form_action=QAction("Edit form",self)
        edit_form_action.triggered.connect(self.show_edit_form)
        edit_submenu.addAction(edit_form_action)
        
        #Create window on screen
        
        screen_geometry =QDesktopWidget().screenGeometry()
        window_geometry =self.geometry()
        x=int((screen_geometry.width()-window_geometry.width())/2)
        y=int((screen_geometry.height()-window_geometry.width())/2)
        self.move(x,y)
        
        self.load_data()
    def show_edit_form(self):
        from editform import UserSearchApp
        self.close()
        self.edit=UserSearchApp()
        self.edit.show()
        
    def load_data(self):
         
        try:
             
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Welcome$10000',
                database='project'
            )
        except mysql.connector.Error as e:
            print(f"Failed to connect to database:{e}")
            return
        
        cursor=conn.cursor()
        query="SELECT * FROM users"
        cursor.execute(query)
        
        rows=cursor.fetchall()
        num_rows =len(rows)
        num_columns=len(rows[0])if num_rows > 0 else 0
        
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_columns)
        self.table_widget.setHorizontalHeaderLabels(["ID","Email","Password","Description"])
        
        for row,data in enumerate(rows):
            for col,value in enumerate(data):
                self.table_widget.setItem(row,col,QTableWidgetItem(str(value)))
                
        cursor.close()
        conn.close()
        
        
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setFocusPolicy(Qt.NoFocus)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setStyleSheet("QtableView{selection-background-color: #cce6ff:}")
        
        
if __name__=='__main__':
                app=QApplication(sys.argv)
                user_table_window= UserTableWindow()
                user_table_window.show()
                sys.exit(app.exec_())
 
        
        