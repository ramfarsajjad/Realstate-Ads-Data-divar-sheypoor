import json
import os
import csv
import time
import logging
import psycopg2
from psycopg2 import sql
import requests
import json
import csv
import codecs
import os
import time
import logging
from setup_log import setup_logger
   

def radar_parser3():

    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'div_parser_lev3.log')

    if 'logger_div_pars3' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_div_pars3')
    else:
        logger = setup_logger(log_file, 'logger_div_pars3')

    try:

        directory_path = os.path.join(dir_main, 'archieved_files/scraped_ads/radar_scraped_ads')
        all_files_and_dirs = os.listdir(directory_path)
        all_files = [f for f in all_files_and_dirs if os.path.isfile(os.path.join(directory_path, f))]
        # چاپ نام فایل‌ها
        for token in all_files:
            dir_token = os.path.join(directory_path, f'{token}')
            with open(dir_token, 'r', encoding='utf-8') as file:
                data = json.load(file)

            real_state = {
                "source" : 'radar',
                "token" : data["Id"],
                "sc_time" : data['sc_time'],
                "title" : data["seo"]["web_info"]["title"],
                "rent_sell" : data["category"]["cat2"],
                "apartment_house" : data["category"]["cat3"],
                "category" : data["details"]["category"],
                "register_data" : data["seo"]["register_date"],
                "description" : data["seo"]["description"],
                "province" : '',
                "city" : data["details"]["city"],
                "district" : data["details"]["district"],
                "price" : data["details"]["price"],
                "credit": data["details"]["credit"],
                "rent" : data["details"]["rent"],
                "business_type" : data["details"]["business_type"],
                "image" : '',
                "build_date" :'' ,
                "room" : '' ,
                "meterage" : '' ,
                "location" : '',
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


            if not real_state["rent_sell"] == None:
                # word = real_state["rent_sell"].split('-')
                if real_state["rent_sell"] == 'residential-rent':
                    real_state["rent_sell"] = 'rent'
                elif real_state["rent_sell"] == 'residential-sell':
                    real_state["rent_sell"] = 'sell'


            logger.info('JSON IS READY!')
            
            return real_state

    except:
            logger.exception(f'CAN NOT  PREPARE {real_state["token"]}!\nERORR:')
            
            return None



radar_parser3()