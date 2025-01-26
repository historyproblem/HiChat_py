import sys
import Functions
from symtable import Function
from PyQt6.QtCore import QThread, pyqtSignal, QEventLoop
from PyQt6.QtWidgets import QMessageBox
# import Main
import pdb
from PyQt6.QtWidgets import QWidget, QDialog, QDialogButtonBox, QApplication, QLineEdit, QVBoxLayout, QPushButton, QLabel, QCheckBox, QMessageBox
from ORM import AsyncORM
import PyQt6
import asyncio
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
import qasync
from AppWindows import HiChatWindow
# from asyncqt import QEventLoop
# from qasync import asyncSlot

########################################################################################################################
########################################################################################################################
########################################################################################################################
class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        loop = qasync.QEventLoop(self)
        asyncio.set_event_loop(loop)
        self.reg_window = RegistrationWindow()
        self.reg_window.show()
        with loop:
            loop.run_forever()
        self.lastWindowClosed.connect(self.byebye)

    def byebye(self):
        loop.close()
        self.exit(0)

########################################################################################################################
class CustomDialog(QDialog):
    def __init__(self, title, text):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout(self)
        self.message = QLabel(text)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)


########################################################################################################################
class LoginWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, login, password):
        super().__init__()
        self.login = login
        self.password = password

    def run(self):
        try:
            does_user_exist = loop.run_until_complete(AsyncORM.does_exist(self.login))
            if not does_user_exist:
                self.finished.emit(False, "User does not exist")
                return

            is_password_correct = loop.run_until_complete(AsyncORM.check_password(self.login, self.password))
            if not is_password_correct:
                self.finished.emit(False, "Wrong password")
                return

            user = loop.run_until_complete(AsyncORM.get_user_by_login(self.login))
            if user:
                ID_of_user = user.id
                self.finished.emit(True, f"Welcome, {user.name} {user.surname}!")
            else:
                self.finished.emit(False, "User details not found")
            # self.finished.emit(True, "")  # Successful login
        except Exception as e:
            self.finished.emit(False, str(e))
        finally:
            self.quit()
# class LoginThread:
#     finished = pyqtSignal(bool, str)  # Сигнал для передачи результата
#
#     def __init__(self, login, password):
#         self.login = login
#         self.password = password
#
#     async def run(self):
#         does_user_exist = await AsyncORM.does_exist(self.login)
#         if not does_user_exist:
#             self.finished.emit(False, "User does not exist")
#             return
#
#         is_password_correct = await AsyncORM.check_password(self.login, self.password)
#         if not is_password_correct:
#             self.finished.emit(False, "Wrong password")
#             return
#
#         self.finished.emit(True, "")  # Успешный вход
#

#
# class CustomDialog(QDialog):
#     def __init__(self, title, text):
#         super().__init__()
#
#         self.setWindowTitle(title)
#
#         QBtn = (
#             QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
#         )
#
#         self.buttonBox = QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)
#
#         self.layout = QVBoxLayout(self)
#         self.setLayout(self.layout)
#         self.message = QLabel(text)
#         self.layout.addWidget(self.message)
#         self.layout.addWidget(self.buttonBox)

########################################################################################################################
class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 200)

        # Центрируем окно
        self.center()

        # Создаем центральный виджет и устанавливаем компоновку
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Добавляем метки и поля для ввода
        self.username_label = QLabel("Enter Login:")
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("""
            QLineEdit {
                border-radius: 10px; /* Закругление углов */
                background-color: #FFFFFF; /* Цвет фона */
                color: black; /* Цвет текста */
                padding: 10px; /* Отступы */
                border: 1px solid #388E3C;
            }
            QLineEdit:hover {
                background-color: #C5E1A5; /* Цвет при наведении */
            }
        """)

        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("""
            QLineEdit {
                border-radius: 10px; /* Закругление углов */
                background-color: #FFFFFF; /* Цвет фона */
                color: black; /* Цвет текста */
                padding: 10px; /* Отступы */
                border: 1px solid #388E3C;
            }
            QLineEdit:hover {
                background-color: #C5E1A5; /* Цвет при наведении */
            }
        """)

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)



        # Создаем кнопку "Log In"
        self.login_button = QPushButton("Log In")
        self.login_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px; /* Закругление углов */
                background-color: #4CAF50; /* Цвет фона */
                color: white; /* Цвет текста */
                padding: 10px; /* Отступы */
            }
            QPushButton:hover {
                background-color: #45a049; /* Цвет при наведении */
            }
        """)
        self.login_button.clicked.connect(self.try_login)

        self.forgot_password_checkbox = QCheckBox("Забыл пароль")
        self.forgot_password_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px; /* Размер шрифта */
                color: #333; /* Цвет текста */
            }
            QCheckBox::indicator {
                width: 20px; /* Ширина индикатора */
                height: 20px; /* Высота индикатора */
                border: 2px solid #388E3C; /* Обводка индикатора */
                border-radius: 4px; /* Закругление углов индикатора */
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50; /* Цвет фона при отмеченном состоянии */
                border: 2px solid #66bb6a; /* Цвет обводки при отмеченном состоянии */
            }
            QCheckBox::indicator:unchecked {
                background-color: white; /* Цвет фона при неотмеченном состоянии */
            }
        """)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.forgot_password_checkbox)
        layout.addWidget(self.login_button)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def center(self):
        # Центрируем окно на экране
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def try_login(self):

        login = self.username_input.text()
        password = self.password_input.text()

        if not login or not password:
            self.show_error("Error", "All fields must be filled.")
            return
        if hasattr(self, 'worker') and self.worker.isRunning():
            QMessageBox.warning(self, "Warning", "A login attempt is already in progress.")
            return

        self.login_button.setEnabled(False)
        self.worker = LoginWorker(login, password)
        self.worker.finished.connect(self.handle_login_result)
        self.worker.start()

    def handle_login_result(self, success, message):
        self.login_button.setEnabled(True)
        if success:
            global main_window
            main_window = HiChatWindow()
            main_window.show()
            self.close()
            # self.show_error(self, "Success", message)
        else:
            self.show_error("Error", message)

    def show_error(self, title, text):
        error_win = QMessageBox()
        error_win.setWindowTitle(title)
        error_win.setText(text)
        error_win.exec()


class FabricOfAsyncFunctions():
    @staticmethod
    def GetChatList(id_of_user):
        char_list = loop.run_until_complete(AsyncORM.get_chat_list(id_of_user))
        return chat_list

########################################################################################################################
########################################################################################################################
########################################################################################################################
def main(args):
    global app
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = App(args)
    app.exec()

# def main():
#     app = QApplication(sys.argv)


if __name__ == "__main__":
    main(sys.argv)
    # main()
