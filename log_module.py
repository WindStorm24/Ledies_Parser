import requests
from config import *


def upload_log(errors, date_start, date_end):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
    s.headers['Parser-Api-Token'] = 'TtqVkPT32OV8OSJRhLjj3CbuFk1KmLSs'

    data = {
        'errors':errors,
        'site_name':'ladies.de',
        'date_start':date_start,
        'date_end':date_end
    }

    s.post(log_url, data=data)