import json
import GetVkPhotos
import YaUploadFiles
import time


def get_photos_url(user_id: str, token: str, api_v: str, album_id: str):
    photo_extractor = GetVkPhotos.GetVkPhotos(token=token)
    photos = photo_extractor.get(user_id, album_id)
    return photos


def create_folder(token: str, path: str):
    photos_uploader = YaUploadFiles.YaUploadFiles(token)
    return photos_uploader.create_folder(path)


def upload_photo(token: str, path: str, url: str, file_name: str):
    photos_uploader = YaUploadFiles.YaUploadFiles(token)
    return photos_uploader.upload_files(url, file_name, path)


def create_json(photos: list):
    photos_json = []
    for photo in photos:
        photos_json.append({'file_name': photo['name'] + '.jpg', 'size': photo['size']})
    return photos_json


if __name__ == '__main__':

    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    path = 'disk:/andrew_pd-fpy_py-51'
    api_v = '5.131'
    album_id = 'profile'
    #user_id = '552934290'


    user_id = input('Введите ID пользователя Вконтакте: ')
    ya_token = input('Введите токен Яндекс диска: ')
    print('Работаем...)')

    with open('log.txt', 'w', encoding='UTF-8') as f:
        f.write('====Получение фотографий====\n')
        photos = get_photos_url(user_id, token, api_v, album_id)
        if 'error' in photos:
            f.write(f'Ошибка:{photos["error"]}\n')
            f.write('Программа завершилась ошибкой.')
            exit(photos['error'])
        for photo in photos:
            f.write(f'получен url файла: {photo["url"]}\n')
        f.write(f'Всего получено файлов: {len(photos)}\n')
        f.write('\n')

    for i in  range(len(photos) -1):
        j = i + 1
        count = 1
        while j != len(photos):
            if photos[i]['name'] == photos[j]['name']:
                photos[j]['name'] = photos[j]['name'] + '(' + str(count)  + ')'
                count += 1
            j += 1


    with open('log.txt', 'a', encoding='UTF-8') as f:
        res = create_folder(ya_token, path)
        f.write('====Создание каталога====\n')
        if 'ok' in res:
            if int(res['ok']) == 201:
                f.write('Каталог создан:\n')
                f.write('\n')
            else:
                f.write('Каталог уже существует\n')
                f.write('\n')
        else:
            f.write(f'Создание каталога завершилось ошибкой: {res["error"]}\n')
            f.write('Программа завершилась ошибкой\n')
            exit(res['error'])

    with open('log.txt', 'a', encoding='UTF-8') as f:
        f.write('Загрузка файлов на YANDEX диск:\n')
        for photo in photos:
            res = upload_photo(ya_token, path, photo['url'], photo['name'] + '.jpg')
            time.sleep(1)
            if 'error' in res:
                f.write(f'Ошибка загрузки файла {photo["name"]}. Статус: {res["error"]}\n')
            else:
                f.write(f'Файл {photo["name"]} загружен. Статус: {res["ok"]}\n')
        f.write('\n')

    with open('result.json', 'w') as f:
        json.dump(create_json(photos), f, indent=4)

    with open('log.txt', 'a', encoding='UTF-8') as f:
        f.write('Запись в JSON\n')
        f.write('объект сохранен в файл result.json\n')
        f.write('\n')
        f.write('Программа успешно завершена\n')
    print('Готово.\nИнформация по работе программы находится в файлах result.json и log.txt\n'
          'рабочего каталога программы')

    pass
