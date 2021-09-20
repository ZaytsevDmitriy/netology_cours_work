import requests
import time
from progress.bar import IncrementalBar
from datetime import date

with open('vktoken.txt', 'r') as file_objekt:
    TOKEN = file_objekt.read().strip()
with open('yandex_token.txt', 'r') as file_objekt:
    YA_TOKEN = file_objekt.read().strip()

user_id = input('Введите ID')


class VkontakteProfilePhoto:
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
            'extended': '1'}
        res = requests.get(url=url, params=params)
        result = res.json()
        vk_photo_list = []
        for i in result['response']['items']:

            vk_photo_dict = {}
            for key in i['likes']:
                if key in vk_photo_dict:
                    vk_photo_dict['file_name'] = date.today()
                else:
                    vk_photo_dict['file_name'] = i['likes']['count']

            for key in i['sizes'][-1]['url']:
                vk_photo_dict['url'] = i['sizes'][-1]['url']
            vk_photo_list.append(vk_photo_dict)
        return vk_photo_list
        # with open('file information.json', 'w', encoding='utf-8') as file_objekt:
        #     file_objekt.write(result)


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):  # Запрос URL для загрузки
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, user_id):
        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.get_headers()
        params = {"path": user_id}
        request = requests.get(url=url, params=params, headers=headers)
        if request.status_code == 200:
            pass
        else:
            response = requests.put(url=url, params=params, headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                print(f"Added new folder \"{user_id}\"")

    def upload_by_url(self, picture_list):
        bar = IncrementalBar('Uploaded files', max=len(picture_list))
        for i in picture_list:
            file_name = i['file_name']
            picture_url = i['url']
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            headers = self.get_headers()
            params = {
                'path': f'{user_id}/{file_name}.jpg',
                'url': f'{picture_url}'
            }
            response = requests.post(url=url, params=params, headers=headers)
            res = response.json()
            bar.next()
            time.sleep(1)
        bar.finish()


def main_logic(token_vk, token_yandex):
    vk = VkontakteProfilePhoto(token_vk)
    picture_list = vk.photo_load(user_id)
    with open('file information.json', 'w', encoding='utf-8') as file_objekt:
        file_objekt.write(f'{picture_list}')
    uploader = YaUploader(token_yandex)
    uploader.create_folder(user_id)
    uploader.upload_by_url(picture_list)
    return


main_logic(TOKEN, YA_TOKEN)
