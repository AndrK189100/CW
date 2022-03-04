import requests


class GetVkPhotos:
    __url = 'https://api.vk.com/method/photos.get'

    def __init__(self, token: str, api_v='5.131'):
        self.token = token
        self.api_v = api_v

    def get(self, user_id: str, album_id = 'profile'):

        max_sizes_photos = []
        params = {'owner_id': user_id, 'album_id': album_id, 'count': '1000', 'access_token': self.token,
                  'v': self.api_v, 'extended': '1'}
        resp = requests.get(url=self.__url, params=params)

        if resp.status_code != 200:
            return {'error': resp.status_code}

        resp = resp.json()
        if 'error' in resp:
            return {'error': resp["error"]["error_code"]}

        for item in resp['response']['items']:
            item['sizes'].sort(key=lambda val: int(val['width']) * int(val['height']), reverse=True)
            max_sizes_photos.append({'size': item['sizes'][0]['height'] * item['sizes'][0]['width'],
                                     'name': str(item['likes']['count']), 'url': item['sizes'][0]['url']})

        return max_sizes_photos
