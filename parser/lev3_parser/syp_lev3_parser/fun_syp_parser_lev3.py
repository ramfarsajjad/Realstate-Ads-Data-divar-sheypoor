import json
import os
import csv
from syp_secfind import dicfdr
from syp_decnum_pass import decnum
import time
import logging
import psycopg2
from psycopg2 import sql
import datetime
from setup_log import setup_logger



def syp_parser3(data):

    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'syp_parser_lev3.log')

    if 'logger_syp_pars3' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_syp_pars3')
    else:
        logger = setup_logger(log_file, 'logger_syp_pars3')
    

    try:
        data = json.loads(data)                
        real_state = {
            "source" : 'sheypoor',
            "token" : data["main"]["id"],
            "sc_time" : data['sc_time'],
            "title" : data["seo"]["title"],
            "rent_sell" :'',
            "apartment_house" : '',
            "category" : '',
            "register_data" : '-',
            "description" : data["seo"]["description"],
            "province" : data['main']['category'][decnum(data['main']['category'], 'region')]['region'],
            "city" : data['main']['category'][decnum(data['main']['category'], 'city')]['city'],
            "district" : '',
            "price" : '',
            "credit": '',
            "rent" : '',
            "business_type" : '',
            "image" : data['main']['IMAGE'],
            "build_date" :'' ,
            "room" : '' ,
            "meterage" : '' ,
            "location" : data['main']['location'],
            "elevator" : '',
            "parking" : '',
            "storage" : '',
            "unitpf" : '',
            "tabaghe" : '',
            "sanad" : '',
            "jahat" : '',
            "vaziat": '',
            "balkon" : '',
            "wc" : '',
            "jenskaff" : '',
            "cooler" : '',
            "heater" : '',
            "tamin_hot_water" : '',
            "expired_date" : ''                        
        }
        
        if not decnum(data['main']['category'], 'category_2') == None:
            real_state['category'] = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2']
            word = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2'].split()
            if word[-1] == 'ویلا':
                real_state["apartment_house"] = 'house'
            elif word[-1] == 'آپارتمان':
                real_state["apartment_house"] = 'apartment'
            else:
                real_state['apartment_house'] = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2']
            if word[0] == 'رهن':
                real_state["rent_sell"] = 'rent'
            elif word[0] == 'خرید':
                real_state["rent_sell"] = 'sell'
            else:
                real_state["rent_sell"] = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2']

        if not decnum(data['main']['category'], 'neighbourhood') == None:
            real_state["district"] = data['main']['category'][decnum(data['main']['category'], 'neighbourhood')]['neighbourhood']   

        if real_state['rent_sell'] == 'sell':
            real_state['price'] = data['main']['price'][0]['amount']
        elif real_state['rent_sell'] == 'rent':
            if not decnum(data['main']['property'], 'رهن') == None:
                word = data['main']['property'][decnum(data['main']['property'], 'رهن')]['رهن'].split()
                real_state['credit'] = word[0]
            if not decnum(data['main']['property'], 'اجاره') == None:
                word = data['main']['property'][decnum(data['main']['property'], 'اجاره')]['اجاره'].split()
                real_state['rent'] = word[0]

        if not decnum(data['main']['property'], 'سن بنا') == None:
                word = data['main']['property'][decnum(data['main']['property'], 'سن بنا')]['سن بنا'].split()            
                if word[0] == 'نوساز':
                    word[0] = 0
                elif word[0] == 'بیشتر':
                    word[0] = 33
                b_date = 1403 - int(word[0])
                real_state['build_date'] = b_date

        if not decnum(data['main']['property'], 'تعداد اتاق') == None:
            real_state['room'] = int(data['main']['property'][decnum(data['main']['property'], 'تعداد اتاق')]['تعداد اتاق'])

        if not decnum(data['main']['property'], 'متراژ') == None:
            real_state['meterage'] = data['main']['property'][decnum(data['main']['property'], 'متراژ')]['متراژ']

        if not decnum(data['main']['property'], 'آسانسور') == None:
            real_state['elevator'] = data['main']['property'][decnum(data['main']['property'], 'آسانسور')]['آسانسور']

        if not decnum(data['main']['property'], 'پارکینگ') == None:
            real_state['parking'] = data['main']['property'][decnum(data['main']['property'], 'پارکینگ')]['پارکینگ']    

        if not decnum(data['main']['property'], 'انباری') == None:
            real_state['storage'] = data['main']['property'][decnum(data['main']['property'], 'انباری')]['انباری']

        if "timePassedLabel" in data['main']:
                word = data['main']['timePassedLabel'].split()
                if len(word) == 2:
                    current_date = datetime.date.today()
                elif len(word) == 3:
                    if word[1] == "روز":
                        current_date = datetime.date.today() - datetime.timedelta(days=int(word[0]))
                    elif word [1] == "هفته":
                        current_date = datetime.date.today() - datetime.timedelta(days=int(word[0]) * 7)
                
                real_state['register_data'] = f"{current_date.day}-{current_date.month}-{current_date.year}"

        real_state['image'] = str(real_state['image'])
        real_state['location'] = str(real_state['location'])

        logger.info('JSON IS READY!')

        return real_state

    except:
        logger.exception(f'CAN NOT  PREPARE {real_state["token"]}!\nERORR:')

        return None
    

