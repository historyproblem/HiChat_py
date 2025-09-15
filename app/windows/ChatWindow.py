from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea, QLabel, QFrame
from PyQt6.QtCore import Qt
from core.ORM import AsyncORM
from core.DatabaseModels import MessagesOrm
from qasync import asyncSlot

class MessageBubble(QFrame):
    def __init__(self, text: str, is_own: bool):
        super().__init__()
        self.setObjectName("bubble")
        self.setStyleSheet(
        "#bubble {border-radius: 12px; padding: 8px 12px; background: %s;}" % ("#DCF8C6" if is_own else "#FFFFFF")
        )
        lay = QVBoxLayout(self)
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lay.addWidget(lbl)
        lay.setContentsMargins(10, 6, 10, 6)

class ChatWindow(QWidget):
    def __init__(self, user_id: int, chat_id: int):
        super().__init__()
        self.user_id = user_id
        self.chat_id = chat_id


        self.setWindowTitle("HiChat — Chat")


        self.root = QVBoxLayout(self)


        # scroll area for messages
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_lay = QVBoxLayout(self.scroll_widget)
        self.scroll_lay.addStretch(1)
        self.scroll.setWidget(self.scroll_widget)


        # input area
        in_lay = QHBoxLayout()
        self.inp = QLineEdit()
        self.btn = QPushButton("Send")
        self.btn.clicked.connect(self.on_send_clicked)
        in_lay.addWidget(self.inp)
        in_lay.addWidget(self.btn)


        self.root.addWidget(self.scroll)
        self.root.addLayout(in_lay)

    async def load_history(self):
        msgs = await AsyncORM.list_messages(self.chat_id, limit=100)
        for m in msgs:
            self._add_bubble(m)
        self._scroll_to_bottom()
    
    def _add_bubble(self, msg: MessagesOrm):
        is_own = (msg.author_id == self.user_id)
        bubble = MessageBubble(msg.text, is_own)
        self.scroll_lay.insertWidget(self.scroll_lay.count() - 1, bubble, 0, Qt.AlignmentFlag.AlignLeft if not is_own else Qt.AlignmentFlag.AlignRight)

    def _scroll_to_bottom(self):
        sb = self.scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    @asyncSlot()
    async def on_send_clicked(self):
        txt = self.inp.text().strip()
        if not txt:
            return
        msg = await AsyncORM.add_message(self.chat_id, self.user_id, txt)
        self._add_bubble(msg)
        self.inp.clear()
        self._scroll_to_bottom()