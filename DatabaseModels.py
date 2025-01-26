import datetime
from typing import Annotated, Optional
from sqlalchemy import Column
from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.testing.schema import mapped_column
from DataBases import Base, str_50
import bcrypt
# int_prinmary_key = Annotated[int, mapped_column(primary_key=True)]

class UsersOrm(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"[{self.id}, '{self.name}', '{self.surname}', '{self.password}']"

    def __getitem__(self, index):
        return [self.id, self.name, self.surname, self.password_hash][index]

    def __len__(self):
        return 4

class ChatsOrm(Base):
    __tablename__ = 'chats'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_50]
    first_user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) # добавить бы ondelete='CSCADE'
    second_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return f"[{self.id}, '{self.title}', '{self.first_user_id}', '{self.second_user_id}']"

    def __getitem__(self, index):
        return [self.id, self.title, self.first_user_id, self.second_user_id][index]

    def __len__(self):
        return 4

class MessagesOrm(Base):
    __tablename__ = 'messages'
    id = Column(BigInteger, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column()
    created_when: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"[{self.created_when}, '{self.chat_id}', '{self.sender_id}', '{self.text}']"

    def __getitem__(self, index):
        return [self.created_when, self.chat_id, self.sender_id, self.text][index]

    def __len__(self):
        return 4

metadata_obj = MetaData()
