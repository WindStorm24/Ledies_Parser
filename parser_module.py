import requests
from bs4 import BeautifulSoup as BS
import threading
import datetime

from config import *

from upload_to_s3_module import upload_to_s3
from data_base_module import upload_to_db
from log_module import upload_log


# Створюємо екземпляр сесії
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'


domen = 'https://www.ladies.de'


# Отримуєму максимальну кількість сторінок

r = s.get('https://www.ladies.de/sex-anzeigen?page=1')
# r = s.get('https://www.ladies.de/sex-anzeigen?page=1', proxies=proxies, verify=False)
bs = BS(r.text, 'html.parser')
last_page = bs.find_all('a', class_='page-link')
last_page = last_page[-2].text

error= ''

class Parser(threading.Thread):
    def __init__(self, start_page, finish_page, error):
        threading.Thread.__init__(self)
        self.start_page =start_page
        self.finish_page =finish_page
        self.error = error

    def run(self):

        # Проходимся циклом по всім сторінкам
        for i in range(self.start_page, self.finish_page+1):
            print(f'page:{i}')
            # r = s.get(f'https://www.ladies.de/sex-anzeigen?page={i}', proxies=proxies,verify=False)
            r = s.get(f'https://www.ladies.de/sex-anzeigen?page={str(i)}')

            bs = BS(r.text, 'html.parser')

            all_models = bs.find_all('div', class_='anzeige anzeige-premium gallery-anzeige col-lg-3 col-md-4 col-xs-4')

            mn = 1
            for model in all_models:

                link = model.find('a').get('href')

                # тут мала стояти перевірка на дублікати
                if link != '#' and 'anzp' not in link:

                    r = s.get(domen+link)
                    if r.status_code == 200:
                        pass
                    else:
                        self.error += f'WARRNING:error to get model page\n status_code: {r.status_code}\n'
                        r = s.get(domen + link)
                    # r = s.get(domen+link, proxies=proxies,verify=False)
                    bs = BS(r.text, 'html.parser')

                    # Отримуєм данні які присутні завжди і мають окремий маркер для пошуку
                    try:
                        name = bs.find('h2', class_='page-heading kuenstlername').get_text().strip()
                    except Exception as e:
                        name = ''


                    try:
                        phone = bs.find('strong', itemprop="telephone").get_text().strip()
                    except Exception as e:
                        phone = ''



                    try:
                        adress = bs.find('p', itemprop="addressLocality").get_text().strip()
                    except Exception as e:
                        try:
                            adress = bs.find('p', itemprop="address").get_text().strip()
                        except:
                            try:
                                adress = bs.find('div', class_='col-xs-12 address-details').get_text().strip()
                            except:
                                adress = ''



                    try:
                        about = bs.find('div', id='description').get_text().strip()
                    except Exception as e:
                        try:
                            about = bs.find('div', class_='text-overflow row einzelansicht-text').get_text().strip()
                        except:
                            about = bs.find('div', class_='row einzelansicht-text').get_text().strip()


                    try:
                        service = bs.find('div', class_='column-list').get_text().strip()
                    except Exception as e:
                        service = ''


                    schedule = bs.find('a', class_='name einzelansicht-zeiten').get_text().strip()


                    # Заздалегіть створюємо змінні для заповнення
                    object_type = 0
                    age = ''
                    gender_id = ''
                    height = ''
                    siski = ''
                    intimicy_id = ''
                    haircolor_id = ''
                    lang = ''
                    smoking_id = ''
                    nationality=''
                    body_type=''

                    interior = ''
                    exterior = ''

                    other_data={}


                    # Отримуэм всі інші параметри про модель
                    other_params = bs.find_all('div', class_='attribute-column')

                    # Перебираємо всі параметри
                    try:
                        for param in other_params:

                            # Отримуэм назву ы значення параметру
                            param_name = param.find('div', class_='col-xs-5 hidden-md').get_text().strip()
                            param_value = param.find('div', class_='col-xs-7').get_text().strip()

                            # Перевірямо назву параметра на відповідне значення і записуєм в змінну
                            if param_name == 'Alter':
                                age = param_value
                            elif param_name == 'Geschlecht':
                                gender_id = param_value
                            elif param_name == 'Größe':
                                height = param_value
                            elif param_name == 'Oberweite':
                                siski = param_value
                            elif param_name == 'Intimbereich':
                                intimicy_id = param_value
                            elif param_name == 'Haare':
                                haircolor_id = param_value
                            elif param_name == 'Sprachen':
                                lang = param_value
                            elif param_name == 'Sonstiges':
                                smoking_id = param_value
                            elif param_name == 'Typ':
                                nationality = param_value
                            elif param_name == 'Konfektionsgröße':
                                body_type = param_value
                            else:
                                other_data[param_name]=param_value

                        object_type = 2
                    except Exception as e:
                        for param in other_params:
                            param_name = param.find('p', class_='attribute-heading').get_text().strip()
                            param_value = param.text.replace(param_name, '', 1).strip().replace('\n\n\n', '\n')

                            if param_name == 'Lage & Parken':
                                exterior = param_value
                            elif param_name == 'Ambiente & Größe':
                                interior += param_value + '\n'
                            elif param_name == 'Essen & Trinken':
                                interior += param_value + '\n'
                            else:
                                other_data[param_name] = param_value


                        object_type = 3

                    mn+=1

                    # Отримуэм всі фото з сторінки
                    all_photos = bs.find_all('div', class_='fotothumb lds-10-col-lg-2 lds-10-col-md-2 col-sm-4 col-xs-4 relative')


                    # перебираємо кожне фото
                    n = 1
                    id_list = []
                    url_list=[]
                    for photo in all_photos:
                        # Отримуєм посилання на фото
                        photo_link = photo.find('a', class_='gallery_item').get('href')
                        url_list.append(photo_link)

                        # Запускаэму функцыю модуля завантаження фото
                        upload_to_s3(photo_link, name + str(n) + '.jpg', id_list, self.error)
                    n += 1


                    #Запускаэмо модуль завантаження до БД
                    upload_to_db(domen+link,age,about,adress,body_type,phone,gender_id,haircolor_id,height,lang,nationality,
                                 name,service,siski,schedule,intimicy_id,smoking_id,other_data,object_type,interior, exterior,
                                 id_list,url_list, self.error)




# Визначаэмо рівну кількість сторінок на кожен поток
pages_per_thread = int(last_page)/int(threads_count)
pages_per_thread = int(pages_per_thread)

start_page = 1

# фіксуємо час початку роботи
start_date = str(datetime.datetime.now()).split('.')[0]

threads = []

# Відповідно до кількості потоків задаєм за який проміжок сторінок відповідальний кожен потом
for i in range(1,threads_count+1):
    if threads_count == 1:
        thread = Parser(1, int(last_page)+1, error)
    elif i == threads_count:
        thread=Parser(int(last_page)-pages_per_thread,int(last_page)+1, error)
    else:
        thread=Parser(start_page,pages_per_thread*i, error)
    threads.append(thread)
    thread.start()

    start_page=pages_per_thread*i+1

# Перевіряємо що всі потоки завершили працювати
for thread in threads:
    thread.join()

# фіксуємо час закінчення роботи
finish_date = str(datetime.datetime.now()).split('.')[0]

upload_log(error, start_date, finish_date)







