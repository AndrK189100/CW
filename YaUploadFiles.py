import requests


class YaUploadFiles:

    def __init__(self, token: str):
        self.__token = token

    def create_folder(self, path: str):

        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': path}
        headers = {'Authorization': self.__token}
        resp = requests.put(url=url, params=params, headers=headers)
        if (resp.status_code == 409) or (resp.status_code == 201):
            return {'ok': resp.status_code}
        else:
            return {'error': resp.status_code}

    def upload_files(self, file_url, file_name, path: str):

        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': path + '/' + file_name, 'url': file_url}
        headers = {'Authorization': self.__token}
        resp = requests.post(url, params = params, headers = headers)

        if resp.status_code != 202:
            return {'error': resp.status_code}
        else:
            return {'ok': resp.status_code}
