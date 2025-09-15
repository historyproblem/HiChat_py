from typing import Optional
from sqlalchemy import select, or_, and_
from sqlalchemy.exc import IntegrityError
from core.DataBases import session_scope, engine, Base
from core.DatabaseModels import UsersOrm, MessagesOrm, ChatsOrm
import bcrypt
from datetime import datetime, timezone

class AsyncORM:
    @staticmethod
    async def create_all():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), password_hash.encode())
        except Exception:
            return False

    @staticmethod
    async def insert_user(login: str, name: str, surname: str, password: str):
        password_hash = AsyncORM._hash_password(password)
        async with session_scope() as session:
            user = UsersOrm(login=login, name=name, surname=surname, password_hash=password_hash)
            session.add(user)

    @staticmethod
    async def does_exist(login: str) -> bool:
        async with session_scope() as session:
            res = await session.execute(select(UsersOrm.id).where(UsersOrm.login == login))
            return res.scalar_one_or_none() is not None

    @staticmethod
    async def get_user_by_login(login: str) -> Optional[UsersOrm]:
        async with session_scope() as session:
            res = await session.execute(select(UsersOrm).where(UsersOrm.login == login))
            return res.scalar_one_or_none()

    @staticmethod
    async def check_password(login: str, password: str) -> bool:
        async with session_scope() as session:
            res = await session.execute(select(UsersOrm).where(UsersOrm.login == login))
            user = res.scalar_one_or_none()
            if not user:
                return False
            return AsyncORM._verify_password(password, user.password_hash)

    @staticmethod
    async def __get_id__(name: str, surname: str) -> int:
        async with session_scope() as session:
            res = await session.execute(
                select(UsersOrm.id).where(and_(UsersOrm.name == name, UsersOrm.surname == surname))
            )
            uid = res.scalar_one_or_none()
            return uid if uid is not None else -1

    @staticmethod
    async def get_name(id: int) -> list[str]:
        async with session_scope() as session:
            res = await session.execute(select(UsersOrm.name, UsersOrm.surname).where(UsersOrm.id == id))
            row = res.first()
            if not row:
                return ["", ""]
            return [row.name, row.surname]

    @staticmethod
    async def does_exist_chat(first_id: int, second_id: int) -> int:
        if first_id == second_id:
            pass

        a, b = sorted((first_id, second_id))
        async with session_scope() as session:
            res = await session.execute(
                select(ChatsOrm.id).where(
                    and_(ChatsOrm.first_user_id == a, ChatsOrm.second_user_id == b)
                )
            )
            cid = res.scalar_one_or_none()
            if cid is not None:
                return cid
            chat = ChatsOrm(title="Direct", first_user_id=a, second_user_id=b)
            session.add(chat)

        async with session_scope() as session:
            res = await session.execute(
                select(ChatsOrm.id).where(and_(ChatsOrm.first_user_id == a, ChatsOrm.second_user_id == b))
            )
            cid = res.scalar_one_or_none()
            return cid if cid is not None else -1

    @staticmethod
    async def insert_chat(first_user_id: int, second_user_id: int, title: str):
        a, b = sorted((first_user_id, second_user_id))
        async with session_scope() as session:
            res = await session.execute(
                select(ChatsOrm.id).where(and_(ChatsOrm.first_user_id == a, ChatsOrm.second_user_id == b))
            )
            if res.scalar_one_or_none() is None:
                chat = ChatsOrm(title=title, first_user_id=a, second_user_id=b)
                session.add(chat)

    @staticmethod
    async def send_message(sender_id: int, chat_id: int, message: str):
        async with session_scope() as session:
            msg = MessagesOrm(
                chat_id=chat_id,
                author_id=sender_id,
                sender_id=sender_id,
                text=message,
            )
            session.add(msg)

    @staticmethod
    async def get_chat_list(user_id: int):
        async with session_scope() as session:
            res = await session.execute(
                select(ChatsOrm).where(
                    or_(ChatsOrm.first_user_id == user_id, ChatsOrm.second_user_id == user_id)
                )
            )
            return res.scalars().all()

    @staticmethod
    async def get_messages_list(chat_id: int):
        async with session_scope() as session:
            res = await session.execute(
                select(MessagesOrm).where(MessagesOrm.chat_id == chat_id).order_by(MessagesOrm.created_at.asc())
            )
            return res.scalars().all()

    @staticmethod
    async def found(id: int):
        async with session_scope() as session:
            res = await session.execute(select(UsersOrm).where(UsersOrm.id == id))
            u = res.scalar_one_or_none()
            if not u:
                return []
            return [(u.id, u.name, u.surname, u.login)]
    
    @staticmethod
    async def return_last_msg(cnt: int, chat_id: int):
        async with session_scope() as session:
            res = await session.execute(
                select(MessagesOrm).where(MessagesOrm.chat_id == chat_id).order_by(MessagesOrm.created_at.desc()).limit(cnt)
            )
            arr = res.scalars().all()

        result = []
        for m in reversed(arr):
            name, surname = await AsyncORM.get_name(m.sender_id)
            result.append([f"{name} {surname}".strip(), m.text])
        return result
