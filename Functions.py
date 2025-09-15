from ORM import AsyncORM

def convert_to_normal(name: str, surname: str):
    name = (name or "").strip()
    surname = (surname or "").strip()
    if not name or not surname:
        return name, surname
    name = name[0].upper() + name[1:].lower()
    surname = surname[0].upper() + surname[1:].lower()
    return name, surname

async def open_chat(current_user_id: int, name: str, surname: str):
    if current_user_id == -1:
        return "-1", "-1"
    name, surname = convert_to_normal(name, surname)
    trash_id = await AsyncORM.__get_id__(name, surname)
    if trash_id == -1:
        return "-2", "-2"
    opened_chat_id = await AsyncORM.does_exist_chat(current_user_id, trash_id)
    chat_with = f"{name} {surname}"
    return opened_chat_id, chat_with

async def create_chat(current_user_id: int, name: str, surname: str, title: str):
    if current_user_id == -1:
        return False
    name, surname = convert_to_normal(name, surname)
    second_id = await AsyncORM.__get_id__(name, surname)
    if second_id == -1:
        return False
    await AsyncORM.insert_chat(current_user_id, second_id, title)
    return True

async def login(login: str, password: str):
    exists = await AsyncORM.does_exist(login)
    if not exists:
        return "-1", "-2"
    ok = await AsyncORM.check_password(login, password)
    if not ok:
        return "-1", "-1"
    user = await AsyncORM.get_user_by_login(login)
    if not user:
        return "-1", "-2"
    name_now = f"{user.name} {user.surname}".strip()
    return user.id, name_now
