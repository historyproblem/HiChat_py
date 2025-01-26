from ORM import AsyncORM
import os
import sys
import asyncio

from ORM import AsyncORM

import pdb


ID_now = 0
Name_Surname = "Name of User"
Opened_Chat_ID = 0
Opened_Chat_With = "Chat with User"



async def open_chat(name, surname):
    pdb.set_trace()
    if ID_now == '-1':
        print("You are not logged in\n")
        return '-1', '-1'
    print("first_flag")
    # trash_id = await SyncORM.__get_id__(name, surname)
    pdb.set_trace()
    trash_id = await AsyncORM.__get_id__(name, surname)
    if trash_id == -1:
        print("This user does not exist\n")
        return '-2', '-2'

    print("second_flag")
    opened_chat_id = await AsyncORM.does_exist_chat(ID_now, trash_id)
    chat_with = name + ' ' + surname

    print("third_flag")
    print('successful\n')
    return opened_chat_id, chat_with

async def create_chat(name, surname, title):
    if MainWindow.ID_now == -1:  # функция вызывается "на всякий случай"
        print("You are not logged in\n")
        return
    second_id = await AsyncORM.__get_id__(name, surname)
    await AsyncORM.insert_chat(ID_now, second_id, title)
    print("successful\n")
    return 


async def login(login, password):
    # name, surname = Functions.convert_to_normal(name, surname)
    if await AsyncORM.does_exist(login):
        if await AsyncORM.chek_password(login, password):
            id_now = await AsyncORM.__get_id__(login)
            name_now = name + ' ' + surname
            return id_now, name_now
        else:
            print("Wrong password\n")
            return '-1', '-1'

    else:
        print("User with that name does not exist\n")
        return '-1', '-2'

def convert_to_normal(name, surname):
    trash = name.lower()
    temp = name[0]
    ans_name = temp.upper() + trash[1:].lower()
    trash = surname.lower()
    temp = surname[0]
    ans_surname = temp.upper() + trash[1:].lower()
    return ans_name, ans_surname

async def Process():
    id_now = -1
    name_now = ''
    chat_with = ''
    opened_chat_id = -1
    is_cleared = False
    print("Hi! You can:\n - add *input_name* *input_surname* *password* - add new user"
              "(combinations of name and surname must be unique)\n",
              "- clear all - delete all tables\n",
              "- exit - close this app(tables will remain saved)\n",
              "- login *input_name* *input_surname* *password* - login in user account\n",
              "- logout - logout from user account\n",
              "If You are logged in, You can:\n",
              "- create chat *input_name* *input_surname* *title* - create new chat with anyone, who is in the system\n",
              "- get info - print name, surname and id of your account\n",
              "- open *input_name* *input_surname* - open chat with...\n",
              "- close - close opened chat\n",
              "- send\n",
              "*text*\n send a message into opened chat\n",
              "- show last *count* - show last chat\n",
              )
    while(True):
        if id_now != -1:
            print(f"Now your account name is: {name_now}")
        if opened_chat_id != -1:
            print(f"Now your opened chat with: {chat_with}")
        command_str = input("Command: ")
        array = command_str.split()
        if is_cleared:
            await AsyncORM.create_tables()
            is_cleared = False
        if len(array) == 0:
            continue

        if len(array) == 1:

            if array[0] == 'exit':
                id_now = -1
                print('Good Bye\n')
                break

            if array[0] == 'logout':
                id_now = -1
                print("successful\n")
                continue

            if array[0] == 'close':
                opened_chat_id = -1
                print("successful\n")
                continue

        if len(array) == 2:

            if array[0] == 'clear' and array[1] == 'all':
                confirm_str = input("Are You sure You want to delete all the tables?(Y/n) ")
                if confirm_str.upper() == 'Y':
                    await AsyncORM.create_tables()
                    print('successful\n')
                    is_cleared = True
                    continue
                else:
                    print('tables was not deleted\n')
                    continue

            if array[0] == 'get' and array[1] == 'info':
                if id_now == -1:
                    print("You are not logged in\n")
                    continue
                res = await AsyncORM.found(id_now)
                print(f"name = {res[0][1]}, surname = {res[0][2]}, id = {id_now}")
                continue

        if len(array) == 3:

            if array[0] == 'open':
                if id_now == -1:
                    print("You are not logged in\n")
                    continue
                name_a, surname_a = convert_to_normal(array[1], array[2])
                trash_id = await AsyncORM.__get_id__(name_a, surname_a)
                if trash_id == -1:
                    print("This user does not exist\n")
                    continue
                opened_chat_id = await AsyncORM.does_exist_chat(id_now, trash_id)
                chat_with = name_a + ' ' + surname_a
                print('successful\n')
                continue

            if array[0] == 'show' and array[1] == 'last':
                if id_now == -1:
                    print("You are not logged in\n")
                    continue
                if opened_chat_id == -1:
                    print("No chat is open\n")
                    continue
                counter = int(array[2])
                arr = await AsyncORM.return_last_msg(counter, opened_chat_id)
                for i in range(len(arr)):
                    print(arr[i][0], ": ", arr[i][1], '\n')
                continue

        if len(array) == 4:

            if array[0] == 'add':
                name = array[1]
                surname = array[2]
                name, surname = convert_to_normal(name, surname)
                flag = await AsyncORM.does_exist(name, surname)
                if flag:
                    print("account with this name already exists\n")
                    continue
                await AsyncORM.insert_user_FAKE(name, surname, array[3])
                # await AsyncORM.insert_user(name, surname, array[3])
                print("successful\n")
                continue

            if array[0] == 'login':
                name_a, surname_a = convert_to_normal(array[1], array[2])
                if await AsyncORM.does_exist(name_a, surname_a):
                    if await AsyncORM.chek_password(name_a, surname_a, array[3]):
                        print("You are logged in\n")
                        id_now = await AsyncORM.__get_id__(name_a, surname_a)
                        name_now = name_a + ' ' + surname_a
                        continue
                    else:
                        print("Wrong password\n")
                        continue
                else:
                    print("User with that name does not exist\n")
                    continue

        if len(array) == 5:

            if array[0] == 'create' and array[1] == 'chat':
                if id_now == -1:
                    print("You are not logged in\n")
                    continue
                name, surname = convert_to_normal(array[2], array[3])
                second_id = await AsyncORM.__get_id__(name, surname)
                await AsyncORM.insert_chat(id_now, second_id, array[4])
                print("successful\n")
                continue

        if array[0] == 'send':
            if id_now == -1:
                print("You are not logged in\n")
                continue
            if opened_chat_id == -1:
                print("No chat is open\n")
                continue
            text = input()
            await AsyncORM.send_message(id_now, opened_chat_id, text)
            print("successful\n")
            continue

        print("Your command was incorrect\n")
        continue
