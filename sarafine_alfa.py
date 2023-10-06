import requests


def get_friends_list(user_id):
    access_token = '1f14b34d1f14b34d1f14b34d151c0751b111f141f14b34d7b4e42f7fbf098222890c6b7'  # Здесь нужно заменить на свой access token VK API
    api_version = '5.154'

    # Формирование URL-запроса к методу VK API для получения списка друзей
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


# Запрос ссылки на профиль пользователя в VK
user_profile_link = input('Введите ссылку на профиль VK: ')
user_id = user_profile_link.split('/')[-1]  # Получаем id пользователя из ссылки


friends_list = get_friends_list(user_id)
print(f'Список id друзей пользователя {user_id}: {friends_list}')
