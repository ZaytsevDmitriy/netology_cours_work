import requests
from pprint import pprint

with open('vktoken.txt', 'r') as file_objekt:
    TOKEN = file_objekt.read().strip()

user_id = int(input('Введите ID'))


class vkontakte_profile_photo:
    def __init__(self, token: str):
        self.token = token
        self.user = user_id
    def photo_load(self, user_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
        'user_id': user_id,
        'access_token': TOKEN,
        'v': '5.131',
        'album_id': 'profile',
        'extended': '1'
        }
        res = requests.get(url=url, params=params)

        return res.json()

vk = vkontakte_profile_photo(TOKEN)
pprint(vk.photo_load(user_id))


