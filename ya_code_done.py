import requests
import json
import time
from datetime import datetime as dt
import os

class VK:
    url_vk = 'https://api.vk.com/method/'
    def __init__(self, access_token, user_id, version= 5.199):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.name_likes_list = []
        self.name_date_list = []
        self.name_id_list = []
        self.name_all = []
        self.id = user_id

    def users_info(self):
        params = {'user_ids': self.id}
        response = requests.get(self.url_vk, params={**self.params, **params})
        return response.json()
    
    def get_common_params(self):
        return {'access_token': self.token, 'v': 5.199, 'owner_id': self.id, 'extended': 1}
    
    def get_photos(self):
        response = requests.get(f'{self.url_vk}photos.getAll', params = self.get_common_params())
        return response.json()
    
    def load_foto(self, data):
        for i in data['response']['items']:
            file_url = i['sizes'][-1]['url']
            sizes_file = i['sizes'][-1]['type']
            name_likes = i['likes']['count']
            name_date = dt.fromtimestamp(i['date']).strftime('%Y_%m_%d_%H_%M_%S')
            self.name_date_list.append(dt.fromtimestamp(i['date']).strftime('%Y_%m_%d_%H_%M_%S'))
            self.name_likes_list.append(i['likes']['count'])
            name_id = i['id']
            self.name_id_list.append(i['id'])    
            time.sleep(0.1)
            api = requests.get(file_url)
            count_likes = self.name_likes_list.count(name_likes)
            count_date = self.name_date_list.count(name_date)
            if count_likes <= 1:
                with open('images/%s.jpg' % name_likes, 'wb') as f:
                      f.write(api.content)
                      self.name_all.append(name_likes)
                file_json = [{'name': name_likes, 'sizes': sizes_file}]
                with open('images/%s.json' % name_likes, 'w') as f:
                      json.dump(file_json, f)
            else:
                if count_date <= 1:
                    with open('images/%s.jpg' % name_date, 'wb') as f:
                        f.write(api.content)
                    self.name_all.append(name_date)
                    file_json = [{'name': name_date, 'sizes': sizes_file}]
                    with open('images/%s.json' % name_date, 'w') as f:
                        json.dump(file_json, f)
                else:
                    with open('images/%s.jpg' % name_id, 'wb') as f:
                        f.write(api.content)
                        self.name_all.append(name_id)
                    file_json = [{'name': name_id, 'sizes': sizes_file}]
                    with open('images/%s.json' % name_id, 'w') as f:
                      json.dump(file_json, f)

class Yandex:
    url_yad = 'https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self, token_poligon, vk_name):
        self.token_poligon = token_poligon
        self.vk_name = vk_name

    def load_photo_to_ya_dick(self, headers):
        for i in self.vk_name:
            res_likes = requests.get(f'{self.url_yad}/upload?path=/test/{i}.jpg', headers=headers).json()
            res_likes_json = requests.get(f'{self.url_yad}/upload?path=/test/{i}.json', headers=headers).json()
            with open(f'images/{i}.jpg', 'rb') as f:
                requests.put(res_likes['href'], files={'file':f})
            with open(f'images/{i}.json', 'rb') as f:
                requests.put(res_likes_json['href'], files={'file':f})

file_name = "token.txt"

if os.path.isfile(file_name):
    with open(file_name, "r") as file:
        access_token = str(file.read().strip())
        print(f"Файл token.txt найден. Токен из файла: {access_token}")
else:
    with open(file_name, "w") as file:
        file.write('')
        print("Файл не найден, создан новый файл token.txt. Введите токен и сохраните его в этом файле.")
    with open(file_name, "r") as file:
        access_token = str(file.read().strip())
        print(f"Файл token.txt найден. Токен из файла: {access_token}")

token_poligon = str(input())
user_id = int(input())
vk = VK(access_token, user_id)
vk_name = vk.name_all
data = vk.get_photos()
ya = Yandex(token_poligon, vk_name)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {ya.token_poligon}'}

vk.load_foto(data)
ya.load_photo_to_ya_dick(headers)

