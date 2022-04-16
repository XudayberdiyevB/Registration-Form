import sqlite3
import sys

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        uic.loadUi("ui/welcome.ui", self)
        self.login.clicked.connect(self.go_to_login)
        self.create.clicked.connect(self.go_to_create)

    @staticmethod
    def go_to_login():
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def go_to_create(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi("ui/login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)

    def login_function(self):
        email = self.emailfield.text()
        password = self.passwordfield.text()

        if len(email) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")

        else:
            conn = sqlite3.connect("data.db")
            cur = conn.cursor()
            query = 'SELECT password FROM user WHERE email =\'' + email + "\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Successfully logged in.")
                self.error.setText("")
            else:
                self.error.setText("Invalid username or password")


user_email = None


class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        uic.loadUi("ui/register.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.sign_up_function)

    def sign_up_function(self):
        email = self.emailfield.text()
        password = self.passwordfield.text()
        confirm_password = self.confirmpasswordfield.text()

        global user_email
        user_email = email

        if len(email) == 0 or len(password) == 0 or len(confirm_password) == 0:
            self.error.setText("Please fill in all inputs.")

        elif password != confirm_password:
            self.error.setText("Passwords do not match.")
        else:
            conn = sqlite3.connect("data.db")
            cur = conn.cursor()

            user_info = [email, password]
            cur.execute('INSERT INTO user (email, password) VALUES (?,?)', user_info)

            conn.commit()
            conn.close()

            fill_profile = FillProfileScreen()
            widget.addWidget(fill_profile)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class FillProfileScreen(QDialog):
    def __init__(self):
        super(FillProfileScreen, self).__init__()
        uic.loadUi("ui/fillprofile.ui", self)
        self.image.setPixmap(QPixmap('ui/placeholder.png'))

        username = self.username.text()
        firstname = self.firstname.text()
        lastname = self.lastname.text()

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute(f'UPDATE user '
                    f'username={username} first_name={firstname} last_name={lastname}'
                    f'WHERE id='
                    )

        conn.commit()
        conn.close()


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:  # noqa E722
    print("Exiting")

if __name__ == "__main__":
    print("Running")
