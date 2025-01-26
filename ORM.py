import pdb

import asyncio
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from DatabaseModels import ChatsOrm, UsersOrm, MessagesOrm
from DataBases import str_50, async_engine, Base, async_session_factory

import datetime
from sqlalchemy import or_
def gettime():
    s = str(datetime.datetime.now())
    temp = []
    temp.append(s[:10].split('-'))
    temp.append(s[11:19].split(':'))
    temp.append(s[20:])
    arr = []
    for i in range(3):
        arr.append(temp[0][i])
    for i in range(3):
        arr.append(temp[1][i])
    arr.append(temp[2])
    string = ''
    for i in range(len(arr)):
        string += arr[i]
    return string

import bcrypt
# делаю статическое значение соли, чтобы после рестарта приложения возможно было попасть в аккаунт
constant_salt = ('$2b$12$m0TK1fUGcrl8CW5fVzGWDO').encode('utf8')
opened_chat_id = 0
# from asyn_lru
class AsyncORM:
    @staticmethod
    async def clear_all():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(login, name, surname, password):
        async with async_session_factory() as session:
            psw = bcrypt.hashpw(password.encode('utf-8'), constant_salt).decode('utf-8')
            new_user = UsersOrm(name=name, surname=surname, login=login, password_hash=psw)
            session.add(new_user)
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def insert_chat(first_user_id, second_user_id, title):
        async with async_session_factory() as session:
            new_chat = ChatsOrm(first_user_id=first_user_id, second_user_id=second_user_id, title=title)
            session.add(new_chat)
            await session.flush()
            await session.commit()

    @staticmethod
    async def send_message(sender_id, chat_id, message):
        async with async_session_factory() as session:
            res = str(gettime())
            new_msg = MessagesOrm(chat_id=chat_id, sender_id=sender_id, text=message, created_when=res)
            session.add(new_msg)
            await session.flush()
            await session.commit()

    @staticmethod
    async def does_exist(login):
        async with async_session_factory() as session:
            stmt = select(UsersOrm).where(UsersOrm.login == login)
            res = await session.execute(stmt)
            data = res.scalars().all()
            return len(data) > 0

    @staticmethod
    async def get_user_by_login(login):
        async with async_session_factory() as session:
            stmt = select(UsersOrm).where(UsersOrm.login == login)
            res = await session.execute(stmt)
            user = res.scalars().first()
            return user

    @staticmethod
    async def does_exist_chat(first_id, second_id):
        async with async_session_factory() as session:
            stmt = select(ChatsOrm).where((ChatsOrm.first_user_id == first_id) & (ChatsOrm.second_user_id == second_id)
                                        | (ChatsOrm.second_user_id == first_id) & (ChatsOrm.first_user_id == second_id))
            res = await session.execute(stmt)
            data = res.scalars().all()
        if len(data) == 0:
            return -1
        return data[0][0]

    async def found(id):
        async with async_session_factory() as session:
            stmt = select(UsersOrm).where((UsersOrm.id == id))
            res = await session.execute(stmt)
            data = res.scalars().all()
        return data

    @staticmethod
    async def __get_id__(name, surname):
        async with async_session_factory() as session:
            pdb.set_trace()
            if session is None:
                print("Session is None")
                return -1
            stmt = select(UsersOrm).where((UsersOrm.name == name) & (UsersOrm.surname == surname))
            print(f"Executing query: {stmt}")
            res = await session.execute(stmt)

            if res is None:
                print("Query result is None")
                return -1

            data = res.scalars().all()

            print(f"Data fetched: {data}")

            if len(data) == 0:
                return -1
            return data[0].id

    @staticmethod
    async def check_password(login, string):
        async with async_session_factory() as session:
            stmt = select(UsersOrm).where(UsersOrm.login == login)
            res = await session.execute(stmt)
            user = res.scalars().all()
            if len(user) == 0:
                return False
            psw = bcrypt.hashpw(string.encode('utf-8'), constant_salt).decode('utf-8')
            if psw == user[0][3]:
                return True
            return False

    @staticmethod
    async def get_chat_list(user_id):
        async with async_session_factory() as session:
            stmt = select(ChatsOrm).where(or_(ChatsOrm.first_user_id == user_id, ChatsOrm.second_user_id == user_id))
            res = await session.execute(stmt)
            data = res.scalars().all()
            return data

    @staticmethod
    async def get_messages_list(chat_id):
        async with async_session_factory() as session:
            stmt = select(MessagesOrm).where(MessagesOrm.chat_id == chat_id)
            res = await session.execute(stmt)
            data = res.scalars().all()
            return data
    
    @staticmethod
    async def select_chat(first_id, second_id):
         async with async_session_factory() as session:
            stmt = select(ChatsOrm).where((ChatsOrm.first_user_id == first_id) & (ChatsOrm.second_user_id == second_id)
            |(ChatsOrm.first_user_id == second_id) & (ChatsOrm.second_user_id == first_id))
            return await session.execute(query)
        # надо понять, что возвращается

    async def get_name(id):
        async with async_session_factory() as session:
            stmt = select(UsersOrm).where((UsersOrm.id == id))
            res = await session.execute(stmt)
            data = res.scalars().all()
            return [data[0][1], data[0][2]]

    async def return_last_msg(cnt, chat_id):
        async with async_session_factory() as session:
            stmt = select(MessagesOrm).where((MessagesOrm.chat_id == chat_id))
            res = await session.execute(stmt)
            arr = res.scalars().all()
            chat = []
            for i in range(len(arr)):
                chat.append([arr[i][0], arr[i][2], arr[i][3]])
            counter = cnt
            chat.sort(reverse=True)
            if len(arr) < counter:
                counter = len(arr)
            res = []
            for i in range(counter):
                res.append([chat[i][1],chat[i][2]])
            for i in range(counter):
                trash = await (AsyncORM.get_name(chat[i][1]))
                res[i][0] = trash[0] + ' ' + trash[1]
            return res

