import requests
import json
from pprint import pprint
import csv
import os
import time
import logging
import sys
from setup_log import setup_logger



def syp_sc():

    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'syp_sc.log')
    
    if 'logger_syp_sc' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_syp_sc')
    else:
        logger = setup_logger(log_file, 'logger_syp_sc')
    

    try:
        # URL API
        url = 'https://www.sheypoor.com/api/v10.0.0/search/iran/real-estate'

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)


        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            # تبدیل داده‌های دریافتی به فرمت JSON
            data = response.json()
            
            api_directoir = os.path.join(dir_main, 'archieved_files/api_firstpage/syp_api_firstpage')
            all_api_files_and_dirs = os.listdir(api_directoir)
            all_api_files = [f for f in all_api_files_and_dirs if os.path.isfile(os.path.join(api_directoir, f))]

            myapi_f = os.path.join(api_directoir, f"apisheyp{len(all_api_files)}.json")
            with open(myapi_f, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            dir_tokfile = os.path.join(dir_main, 'scraper')
            mytok_f = os.path.join(dir_tokfile, "syp_tokbase.json")
            if os.path.isfile(mytok_f):
                print(f"{mytok_f} exists.")
                with open(mytok_f, 'r') as file:
                    tokcell = json.load(file)
                    bdata = set(tokcell)
            else:
                print(f"{mytok_f} is not exists. created a new one")
                bdata = set()

            for item in data["data"]:
                if item["type"] == "normal":
                    newtok = item['id']
                    bdata.add(newtok)

            setdata_list = list(bdata)

            
            f = open(mytok_f  , "w")
            f.write(json.dumps(setdata_list))
            f.close()

            logger.info('sheyp tokens downloaded successfully')
        
            
            
        else:
            logger.exception(f'Error fetching data: {response.status_code}\nERORR:')

    except:
        logger.exception('CAN NOT  DOWNLOAD SHEYP TOKENS!\nERORR:')

    

