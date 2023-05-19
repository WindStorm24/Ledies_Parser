import os
import requests

from config import *


def upload_to_s3(url, name, id_list, error):

    name = name.replace('*','')
    name = name.replace('!','')
    name = name.replace('$','')
    name = name.replace('-','')
    name = name.replace('#','')
    name = name.replace('&','')
    name = name.replace('%','')

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
    s.headers['Content-Type'] = 'multipart/form-data'

    # Скачуємо фото і зберігаємо його на локальний комп'ютер
    r = s.get(url, verify=False)
    with open('files/'+name, 'wb') as fd:
        fd.write(r.content)


    # Відкриваємо фото в режимі читання щоб відправити на сервер
    # with open('files/'+name, 'rb') as fu:
    #
    #     data = {
    #         'source':'ladies.de',
    #     }
    #
    #     # Відправляємо фото на API
    #     r = s.post(s3_url, data=data, files=fu)
    #     print(r.status_code)

        files = {'file': (f'files/{name}', 'photo')}

        data = {
            'source': 'ladies.de',
            'file':''
        }

        # Відправляємо фото на API
        r = s.post(s3_url, data=data, files=files)
        print(r.status_code)


        if r.status_code == 200:
            id = r.text
            id_list.append(id)
        else:
            # повторюємо у разі невдачі
            error+=f'WARRNING:error uploading photo on s3\n status_code {r.status_code}\n'
            files = {'file': (f'files/{name}', 'photo')}

            data = {
                'source': 'ladies.de',
                'file': ''
            }

            # Відправляємо фото на API
            r = s.post(s3_url, data=data, files=files)
            print(r.status_code)
            id = r.text
            id_list.append(id)


    # Видаляємо фото з локального комп'ютера
    os.remove('files/'+name)