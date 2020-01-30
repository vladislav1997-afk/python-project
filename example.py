import requests
from sys import argv
import psycopg2

# подключение к бд
try:
    conn = psycopg2.connect(host="localhost", database="test_database", user="test_user", password="qwerty")
except:
    print('ошибка подключения к бд')
    exit(0)

script, username, password, email, server_domain = argv
# занесение данных в словарь
d = dict(username=username, password=password, email=email, server_domain=server_domain)


def request(username, password, email, server_domain):
    r = requests.get(server_domain, auth=(username, password))
    cursor = conn.cursor()
    if 199 < r.status_code < 300:
        try:
            cursor.execute("INSERT INTO users (login, password, email, server_domain) VALUES (%s, %s, %s, %s)",
                           (username, password, email, server_domain))
        except:
            print('у вас ошибка при работе с таблицой в бд')
            cursor.close()
            conn.close()
            exit(0)

    else:
        print('ошибка регистрации')
    conn.commit()  # <- We MUST commit to reflect the inserted data
    cursor.close()
    conn.close()
    #print(email)


# r = requests.get('https://api.github.com', auth=('user', 'pass'))

request(d['username'], d['password'], d['email'], d['server_domain'])
