import random
import requests
import psycopg2


str1 = '123456789'
str2 = 'qwertyuiopasdfghjklzxcvbnm'
str3 = str2.upper()
str4 = str1 + str2 + str3
ls = list(str4)
random.shuffle(ls)
list_username = []
list_password = []
list_email = []


try:
    conn = psycopg2.connect(host="localhost", database="test_database", user="test_user", password="qwerty")
except:
    print('ошибка подключения к бд')
    exit(0)


print('Пожалуйста выберите сайт на котором хотите зарегистрироваться')
d = {1: 'habr.com', 2: 'uber.com', 3: 'www.gosuslugi.ru'}
print(d)
while 1:
    count = input()
    try:
        count = int(count)
        if 0 < count < 4:
            if count == 1:
                server_domain = 'https://account.habr.com/register/?state=1296ffa11b65c75d755dbaec51c80c81&consumer' \
                                '=habr&hl=ru_RU '
            elif count == 2:
                server_domain = 'https://auth.uber.com/login/?uber_client_name=riderSignUp&_ga=2.195166568.532783625' \
                                '.1580412125-1391091225.1580412125 '
            else:
                server_domain = 'https://esia.gosuslugi.ru/registration/'
            break
    except ValueError:
        print('Введите целое число')


print('Пожалуйста укажите сколько аккаунтов хотите сгенерировать для регистрации')
while 1:
    count = input()
    try:
        count = int(count)
        inf = count
        break
    except ValueError:
        print('Введите целое число')


while count > 0:
    list_username.append(''.join([random.choice(ls) for x in range(6)]))
    list_password.append(''.join([random.choice(ls) for x in range(6)]))
    list_email.append(''.join([random.choice(ls) for x in range(6)]))
    count -= 1


cursor = conn.cursor()


def request(username, password, email, server_domain):
    s = requests.session()
    data = {"lastNamed": username, "password": password, "email": email}
    r = s.post(server_domain, data=data)
    if r.status_code == 200:
        try:
            cursor.execute("INSERT INTO users (login, password, email, server_domain) VALUES (%s, %s, %s, %s)",
                           (username, password, email, server_domain))
        except:
            print('у вас ошибка при работе с таблицой в бд')
            cursor.close()
            conn.close()
            exit(0)
    elif r.status_code == 500:
        print('found 500:неисправность конфигурации сервера, либо появление информации о том, что произошел отказ '
              'компонента')
    elif r.status_code == 403:
        print("found 403:ошибка регистрации")
    conn.commit()


for i in range(inf):
    request(list_username[i], list_password[i], list_email[i], server_domain)


cursor.close()
conn.close()

'''
if __name__ == '__main__':
    print('hello man')
'''
