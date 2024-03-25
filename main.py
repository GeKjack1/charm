import os
import sys
import platform
import hashlib
from time import sleep
from datetime import datetime
import pickle
from keyauth import api

def clear():
    if platform.system() == 'Windows':
        os.system('cls & title Python Example')
    elif platform.system() == 'Linux':
        os.system('clear')
        sys.stdout.write("\x1b]0;Python Example\x07")
    elif platform.system() == 'Darwin':
        os.system("clear && printf '\e[3J'")
        os.system('''echo -n -e "\033]0;Python Example\007"''')

def get_checksum(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()

def initialize_keyauthapp():
    keyauthapp = load_session()
    if keyauthapp is None:
        keyauthapp = api(
            name="InvaiterTG",
            ownerid="MgDGDkWT2a",
            secret="78299da61348e78567518b7a68cd18a7a8608bf16434313e02ba6231baf0fd04",
            version="1.0",
            hash_to_check=get_checksum(''.join(sys.argv))
        )
    return keyauthapp

def login(keyauthapp):
    user = input('Введите имя пользователя: ')
    password = input('Введите пароль: ')
    keyauthapp.login(user, password)
    save_session(keyauthapp)
    os.system('cls')
    
def load_session():
    if os.path.exists('session.pkl'):
        with open('session.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return None
        
def save_session(keyauthapp):
    with open('session.pkl', 'wb') as f:
        pickle.dump(keyauthapp, f)

def register(keyauthapp):
    user = input('Введите имя пользователя: ')
    password = input('Введите пароль: ')
    license = input('Введите лицензию: ')
    keyauthapp.register(user, password, license)

def upgrade(keyauthapp):
    user = input('Введите имя пользователя: ')
    license = input('Введите лицензию: ')
    keyauthapp.upgrade(user, license)

def check_license(keyauthapp):
    key = input('Введите ваш лицензионный ключ: ')
    keyauthapp.license(key)
    save_session(keyauthapp)

def display_user_data(keyauthapp):
    print("\nUser data: ")
    print("Username: " + keyauthapp.user_data.username)
    print("IP address: " + keyauthapp.user_data.ip)
    print("Hardware-Id: " + keyauthapp.user_data.hwid)

    subs = keyauthapp.user_data.subscriptions
    for i in range(len(subs)):
        sub = subs[i]["subscription"]
        expiry = datetime.utcfromtimestamp(int(subs[i]["expiry"])).strftime('%Y-%m-%d %H:%M:%S')
        timeleft = subs[i]["timeleft"]
        print(f"[{i + 1} / {len(subs)}] | Subscription: {sub} - Expiry: {expiry} - Timeleft: {timeleft}")

    os.system('cls')
    print("Created at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.createdate)).strftime('%Y-%m-%d %H:%M:%S'))
    print("Last login at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.lastlogin)).strftime('%Y-%m-%d %H:%M:%S'))
    print("Expires at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S'))
    print() 

def qwik():
    print('Hello')

def main():
    keyauthapp = initialize_keyauthapp()
    
    try:
        print("""1. Вход
2. Регистрация
3. Обновление
4. Только лицензионный ключ
        """)
        ans = input("Выберите опцию: ")
        if ans == "1":
            login(keyauthapp)
        elif ans == "2":
            register(keyauthapp)
        elif ans == "3":
            upgrade(keyauthapp)
        elif ans == "4":
            check_license(keyauthapp)
        else:
            print("\nНеверная опция")
            sleep(1)
            clear()
            main()
    except KeyboardInterrupt:
        pass  

    display_user_data(keyauthapp)
    qwik()

if __name__ == "__main__":
    main()
