import telebot
from telebot import types
import pandas as pd
import json
import requests

bot = telebot.TeleBot('6502285968:AAEFgcbUoxHYT8H7z-X-G2g72TellFRwQMo')


def help():
    print("Добавить новую категорию - /new_cat")
    print("Добавить нового специалиста - /new_spec")
    print("Добавить нового пользователя - /new_user")
    print("Добавить новую рекомендацию - /new_rec")
    print("Вывести список пользователей - /user_list")
    print("Вывести список категорий - /cat_list")
    print("Вывести список специалистов - /spec_list")


def count_elements(my_dict):
    c = 0
    for v in my_dict.values():
        if isinstance(v, dict):
            c += count_elements(v)
        elif isinstance(v, list):
            c += len(v)
        elif isinstance(v, str):
            c += 1
    return c


def get_friends_list(user_id):
    access_token = '1f14b34d1f14b34d1f14b34d151c0751b111f141f14b34d7b4e42f7fbf098222890c6b7'  # Здесь нужно заменить на свой access token VK API
    api_version = '5.154'
    url = f'https://api.vk.com/method/friends.get?user_id={user_id}&access_token={access_token}&v={api_version}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        friends_data = response.json()['response']  # Получаем данные о списке друзей
        friends_list = friends_data['items']  # Получаем список id друзей пользователя
        return friends_list
    except requests.exceptions.HTTPError as error:
        print(f'HTTP error occurred: {error}')
    except requests.exceptions.RequestException as error:
        print(f'Request exception occurred: {error}')
    except KeyError:
        print('Error: Unable to retrieve friends list.')


def search(poisk, user_id):
    with open("users_list.json", "r") as my_file:
        users_list_json = my_file.read()
    users_list = json.loads(users_list_json)

    with open("rec_list.json", "r") as my_file:
        rec_list_json = my_file.read()
    rec_list = json.loads(rec_list_json)

    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)

    u_id = users_list[str(user_id)][2]
    friends_list = get_friends_list(u_id)
    print(f'Список id друзей пользователя {u_id}: {friends_list}')
    for i in friends_list:
        if str(i) in str(rec_list):
            print('нашлась рекомендация!!', i)
            for j in rec_list[str(i)]:
                print(j)
                if str(j) in str(specs_list[str(poisk.text)]):
                    print('опана! нашли теbе спеца. Его id', j)
                    for k in specs_list[str(poisk.text)]:
                        if k[0] == j:
                            print(k)



@bot.message_handler(commands=['new_spec'])
def new_spec(message):
    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)

    print("Вы перешли в режим добавления специалиста")
    print("Чтобы выйти введите 0", end='\n')
    for i in specs_list:
        print(i)
    n_cat = str(input("Введите категорию:"))

    if n_cat == '0':
        print('ок выхожу')
    elif n_cat in specs_list:
        n_name = str(input("Введите имя и фамилию специалиста:"))
        n_num = input("Введите номер телефона специалиста:")

        n_id = count_elements(specs_list)
        print('выдан айди', n_id)

        temp_d = specs_list[n_cat]

        temp_d.append([n_id, n_name, n_num])
        specs_list[n_cat] = temp_d

        out = 'Добавлен специалист!' + '\n\n' + 'Категория: ' + str(n_cat) + '\n' + 'Имя: ' + str(n_name) + '\n' + \
              'Телефон: +' + str(n_num) + '\n' + 'ID: ' + str(n_id)
        bot.send_message(message.from_user.id, out)

        specs_list_json = json.dumps(specs_list)
        with open("spec_list.json", "w") as my_file:
            my_file.write(specs_list_json)
    else:
        print('Такой категории нет!', '\n\n')


@bot.message_handler(commands=['new_rec'])
def new_rec(message):
    with open("rec_list.json", "r") as my_file:
        rec_list_json = my_file.read()
    rec_list = json.loads(rec_list_json)

    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)
    t = []
    rec = input("Введите Фамилию, Имя и номер мастера через пробел").split()
    name = rec[0] + ' ' + rec[1]
    num = rec[2]
    print(rec)
    rrr = 'получилась хуйня'
    for i in specs_list:
        for j in specs_list[i]:
            if str(name.lower()) == str(j[1]).lower() and str(num) == str(j[2]):
                #print('Нужный спец найден')
                rrr = j[0]

    user_id = str(message.from_user.id)
    if str(user_id) not in rec_list:
        rec_list[user_id] = [rrr]
    else:
        temp_d = [rec_list[user_id]]
        temp_d.append(rrr)
        rec_list[user_id] = temp_d

    rec_list_json = json.dumps(rec_list)
    with open("rec_list.json", "w") as my_file:
        my_file.write(rec_list_json)


def new_user(id, name, surname, username, v_link):
    with open("users_list.json", "r") as my_file:
        users_list_json = my_file.read()
    users_list = json.loads(users_list_json)

    access_token = '1f14b34d1f14b34d1f14b34d151c0751b111f141f14b34d7b4e42f7fbf098222890c6b7'
    api_version = '5.154'
    url = f'https://api.vk.com/method/users.get?user_ids={v_link}&access_token={access_token}&v={api_version}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        user_data = response.json()['response']
        print(user_data)
        true_id = user_data[0]['id']
        vk_name = user_data[0]['first_name']
        vk_surname = user_data[0]['last_name']
        print(true_id)
    except requests.exceptions.HTTPError as error:
        print(f'HTTP error occurred: {error}')
    except requests.exceptions.RequestException as error:
        print(f'Request exception occurred: {error}')
    except KeyError:
        print('Error: Unable to retrieve friends list.')

    if str(id) not in users_list:
        users_list[id] = [vk_name, vk_surname, true_id, name, surname, username]
        bot.send_message(id, str('Добро пожаловать! Вы ' + str(len(users_list)) + ' пользователь'))
    else:
        bot.send_message(id, 'Рады видеть вас снова')
    users_list_json = json.dumps(users_list)
    with open("users_list.json", "w") as my_file:
        my_file.write(users_list_json)


rec_list = {'id1': [1, 2, 3], 'id2': [1, 237, 4]}

print("Sarafine v.1.0")


@bot.message_handler(commands=['cat_list'])
def cat_list(message):
    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)

    out = "Категории на платформе: " + "\n\n"
    for i in specs_list:
        out += i + '  —  ' + str(len(specs_list[i])) + "\n"
    bot.send_message(message.from_user.id, out)


@bot.message_handler(commands=['user_list'])
def show_users_list(message):
    with open("users_list.json", "r") as my_file:
        users_list_json = my_file.read()
    users_list = json.loads(users_list_json)

    out = ''
    for i in users_list:
        out += '@' + str(users_list[i][-1]) + '\n'
    bot.send_message(message.from_user.id, out)


@bot.message_handler(commands=['new_cat'])
def new_cat(message):
    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)
    cat = str(input('Введите название новой категории:'))

    specs_list[cat] = []

    out = 'Добавлена категория ' + cat
    bot.send_message(message.from_user.id, out)

    specs_list_json = json.dumps(specs_list)
    with open("spec_list.json", "w") as my_file:
        my_file.write(specs_list_json)


@bot.message_handler(commands=['spec_list'])
def sp_list(message):
    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)
    markup = types.ReplyKeyboardMarkup()
    for i in specs_list:
        btn = types.KeyboardButton(str(i))
        markup.add(btn)
    bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=markup)
    print(message.text)
    bot.register_next_step_handler(message, form1)
    types.ReplyKeyboardRemove()


def form1(message):
    with open("spec_list.json", "r") as my_file:
        specs_list_json = my_file.read()
    specs_list = json.loads(specs_list_json)

    if message.text in specs_list:
        out = 'Специалисты в категории ' + message.text + '\n' + 'Количество: ' + str(len(specs_list[message.text])) + '\n\n'
        for i in specs_list[message.text]:
            out += str(str(i) + '\n')
    else:
        out = 'Упс, не нашлась такая категория'
    bot.send_message(message.from_user.id, out)


@bot.message_handler(commands=['start'])
def url(message):
    bot.send_message(message.from_user.id, 'Платформа Sarafine v1.0')
    bot.send_message(message.from_user.id, 'Для использования напишите ссылку на ваш профиль VK')
    bot.register_next_step_handler(message, vk_link)


def vk_link(message):
    ms = message.from_user
    new_user(ms.id, ms.first_name, ms.last_name, ms.username, message.text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'help':
        help()
    else:
        search(message, message.from_user.id)


#specs_list = new_category(specs_list)

#new_spec()
bot.polling()







    #
    #elif message.text == 'cat_list':
     #   cat_list(specs_list)
    #elif message.text == 'spec_list':
     #   sp_list(specs_list)


