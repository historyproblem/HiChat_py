import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from qasync import QEventLoop, asyncSlot
import asyncio
from app.windows.ChatWindow import ChatWindow
from core.ORM import AsyncORM

########################################################################################################################
########################################################################################################################
########################################################################################################################

class HiChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HiChat — Login / Register")


        lay = QVBoxLayout(self)
        self.login = QLineEdit(); self.login.setPlaceholderText("login")
        self.name = QLineEdit(); self.name.setPlaceholderText("name (for register)")
        self.surname = QLineEdit(); self.surname.setPlaceholderText("surname (for register)")
        self.password = QLineEdit(); self.password.setEchoMode(QLineEdit.EchoMode.Password); self.password.setPlaceholderText("password")
        self.info = QLabel("")


        self.btn_login = QPushButton("Login")
        self.btn_reg = QPushButton("Register")


        self.btn_login.clicked.connect(self.on_login_clicked)
        self.btn_reg.clicked.connect(self.on_register_clicked)


        lay.addWidget(self.login)
        lay.addWidget(self.password)
        lay.addWidget(self.name)
        lay.addWidget(self.surname)
        lay.addWidget(self.btn_login)
        lay.addWidget(self.btn_reg)
        lay.addWidget(self.info)


        self.chat = None

    @asyncSlot()
    async def on_register_clicked(self):
        ok, msg = await AsyncORM.register(
            login=self.login.text().strip(),
            name=self.name.text().strip() or "Anon",
            surname=self.surname.text().strip() or "User",
            password=self.password.text(),
        )
        self.info.setText(msg)


    @asyncSlot()
    async def on_login_clicked(self):
        user = await AsyncORM.login(self.login.text().strip(), self.password.text())
        if not user:
            QMessageBox.warning(self, "Login failed", "Invalid credentials")
            return
        # ensure chat exists
        chat = await AsyncORM.get_or_create_chat("General")
        self.chat = ChatWindow(user_id=user.id, chat_id=chat.id)
        self.chat.show()
        await self.chat.load_history()
        self.hide()
    
    async def _bootstrap():
        await AsyncORM.create_all()

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    win = HiChatWindow(); win.show()

    with loop:
        loop.create_task(AsyncORM.create_all())
        loop.run_forever()


if __name__ == "__main__":
    main()