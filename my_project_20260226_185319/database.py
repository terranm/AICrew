# database.py

# 간단한 dictionary 기반 데이터베이스 (실제 데이터베이스 연결은 추후 구현)

database = {
    "users": {},
    "cards": {},
    "characters": {},
    "stages": {}
}

def get_user(username):
    return database["users"].get(username)

def save_user(user):
    database["users"][user.name] = user


