from config import *
import requests



def upload_to_db(url_page, age, about, adress, body_type, phone,gender,hair,height,lang,nationality,name,
                 service,siski,schedule, sexuality, smoking, other_data, object_type, interior, exterior,
                 media_id_list, media_url_list, error):

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
    s.headers['Parser-Api-Token'] = 'TtqVkPT32OV8OSJRhLjj3CbuFk1KmLSs'

    data={

   "comments": [

   ],

   "object": {
       "object_type": object_type,
       "code": 1,
       "about": about,
       "address": adress,
       "age": age,
       "body_type": body_type,
       "breast": siski,
       "categories": "",
       "city": "",
       "contact_phone": phone,
       "country": "",
       "drinks": "",
       "email": "",
       "ethnicity": "",
       "exterior": exterior,
       "eyes_color": "",
       "facilities": "",
       "file_ids": media_id_list,
       "food_drink": "",
       "gender": gender,
       "hair_color": hair,
       "hair_length": "",
       "hash": "",
       "height": height,
       "instagram_url": "",
       "interior": interior,
       "intimate_haircut": "",
       "is_duplicate": 0,
       "is_remove": 0,
       "is_update": 0,
       "languages": lang,
       "lat": 0,
       "likes": 0,
       "lng": 0,
       "location_parking": "",
       "media_urls": media_url_list,
       "models_url": "",
       "name": name,
       "nationality": nationality,
       "nickname": "",
       "onlyfans_url": "",
       "other_data": other_data,
       "other_messengers": "",
       "other_social_networks": "",
       "payment_methods": "",
       "piercing": "",
       "place_type": "",
       "profile_type": "",
       "ratings": 0,
       "region": "",
       "schedule_work": schedule,
       "services": service,
       "sexuality": sexuality,
       "site_name": "",
       "skin_color": "",
       "smoking": smoking,
       "subscribe_price": 0,
       "subscribers_count": 0,
       "tattoo": "",
       "tg": "",
       "tiktok_url": "",
       "travel": "",
       "twitter_url": "",
       "url_page": url_page,
       "viber": "",
       "wa": "",
       "website_url": ""
   }

}


    r = s.post(data_base_url, json=data)
    print(r.status_code)

    if r.status_code == 201:
        pass
    else:
        error+=f'WARRNING:error uploading data to data_base_api\n status_code{r.status_code}\n'
        r = s.post(data_base_url, json=data)